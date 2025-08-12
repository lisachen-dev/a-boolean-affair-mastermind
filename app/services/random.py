import logging
import secrets

import requests
from fastapi import HTTPException
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

from app.models.rules import Rules

logger = logging.getLogger(__name__)


class RandomService:
	RANDOM_BASE_URL = "https://www.random.org/integers/"

	def __init__(self, is_external_code: bool = True):
		if not isinstance(is_external_code, bool):
			raise TypeError("external_code must be a boolean")
		self.is_external_code = is_external_code

	def generate_secret_code(self, rules: Rules) -> tuple[str, ...]:
		"""Generate a numeric secret code using either Python's secrets (internal) or random.org (external)"""
		return (
			self._generate_external_code(rules)
			if self.is_external_code
			else self._generate_internal_code(rules)
		)

	@staticmethod
	def _validate_secret(secret: tuple[str, ...], rules: Rules) -> None:
		"""Validate that the secret code falls within rule parameters"""
		if len(secret) != rules.code_length:
			raise ValueError("Secret length is invalid code length")

		if not rules.allow_repeats and len(set(secret)) != rules.code_length:
			raise ValueError("Duplicates are found, but allow_repeats is set to False")

		for value in secret:
			if not value.isdigit():
				raise ValueError("[SECRET] %s is not a valid integer", value)
			if not rules.min_value <= int(value) <= rules.max_value:
				raise ValueError("[SECRET] %s is out of range", value)

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
		cls._validate_secret(secret, rules)
		logger.info("The secret code was generated using Python's secrets module!")
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

		secret_list = []
		for line in response.text.splitlines():
			trimmed_line = line.strip()

			if trimmed_line:
				secret_list.append(trimmed_line)

		secret = tuple(secret_list)
		cls._validate_secret(secret, rules)
		logger.info("The secret code was generated using random.org!")
		return secret
