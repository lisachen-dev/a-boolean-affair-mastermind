import logging
import secrets

import requests
from fastapi import HTTPException
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

from app.models.rules import Rules
from app.utils.validators import validate_code_sequence

logger = logging.getLogger(__name__)


class RandomService:
	RANDOM_BASE_URL = "https://www.random.org/integers/"

	def __init__(self, is_external_code: bool = True):
		if not isinstance(is_external_code, bool):
			raise TypeError("external_code must be a boolean")
		self.is_external_code = is_external_code

	def generate_secret_code(self, rules: Rules) -> tuple[str, ...]:
		"""Generate a numeric secret code using either Python's secrets (internal) or random.org (external)"""

		# decide if secret_code is generated from random.org or Python's internal tools
		secret_code = (
			self._generate_external_code(rules)
			if self.is_external_code
			else self._generate_internal_code(rules)
		)
		validate_code_sequence(
			values=secret_code,
			code_length=rules.code_length,
			min_value=rules.min_value,
			max_value=rules.max_value,
			allow_repeats=rules.allow_repeats,
			label="[SECRET]",
		)

		# logging successful generation of secret code
		logger.info(
			"The secret code was generated using random.org!"
		) if self.is_external_code else logger.info(
			"The secret code was generated using Python's secrets module!"
		)

		return secret_code

	@classmethod
	def _generate_internal_code(cls, rules: Rules) -> tuple[str, ...]:
		"""Generate the secret code using Python's secrets module"""
		rand_num_generator = secrets.SystemRandom()
		pool = list(range(rules.min_value, rules.max_value + 1))

		if rules.allow_repeats:
			values = [rand_num_generator.choice(pool) for _ in range(rules.code_length)]
		else:
			values = rand_num_generator.sample(pool, rules.code_length)

		secret = tuple(str(value) for value in values)
		return secret

	@classmethod
	def _generate_external_code(cls, rules: Rules) -> tuple[str, ...]:
		"""Generate the secret code using Random.org"""
		payload = {
			"num": rules.code_length,
			"min": rules.min_value,
			"max": rules.max_value,
			"col": 1,
			"base": 10,
			"format": "plain",
			"rnd": "new",
		}

		try:
			response = requests.get(cls.RANDOM_BASE_URL, params=payload, timeout=10)
			logger.debug(
				"Random.org response: [status: %s] | response: %s | url: %s",
				response.status_code,
				response.reason,
				response.url,
			)

		except Timeout:
			raise HTTPException(status_code=500, detail="The request to random.org timed out")

		except ConnectionError:
			raise HTTPException(status_code=500, detail="Random.org returned a connection error")

		except HTTPError:
			raise HTTPException(status_code=500, detail="Could not connect to random.org")

		except RequestException:
			raise HTTPException(
				status_code=500,
				detail="An unexpected error occurred while connecting with random.org",
			)

		# convert the response text to a usable list obj
		lines = []
		for line in response.text.splitlines():
			trimmed_line = line.strip()
			if trimmed_line:
				lines.append(trimmed_line)

		# remove duplicates if not allowed and retry until we get enough unique values
		if not rules.allow_repeats:
			tracking_set = set()
			unique_values = []
			for value in lines:
				if value not in tracking_set:
					tracking_set.add(value)
				if len(unique_values) == rules.code_length:
					break

			# if we didn't get enough unique values, fallback to the internal method.
			if len(unique_values) < rules.code_length:
				return cls._generate_internal_code(rules)

			lines = unique_values

		return tuple(lines)
