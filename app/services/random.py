import logging
import secrets

import requests
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

		# decide if secret_code is generated from random.org or Python's internal tools
		try:
			secret_code = (
				self._generate_external_code(rules)
				if self.is_external_code
				else self._generate_internal_code(rules)
			)
			rules.validate_sequence(values=secret_code, label="[SECRET]")

		except ValueError:
			# If rules/sequence validation fails for any reason, fall back to internal generation
			logger.info("external code invalid per rules - falling back to internal generator")
			secret_code = self._generate_internal_code(rules)
			rules.validate_sequence(values=secret_code, label="[SECRET]")

		if self.is_external_code:
			logger.info("Success! The secret code was generated using random.org")
		else:
			logger.info("Success! The secret code was generated using Python's secrets module!")

		return secret_code

	@classmethod
	def reroute_to_internal(cls, rules: Rules) -> tuple[str, ...]:
		logger.info(
			"Not enough unique values were generated from random.org. Beginning to generate internal secret code..."
		)
		return cls._generate_internal_code(rules)

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
			response.raise_for_status()
			logger.debug(
				"Random.org response: [status: %s] | response: %s | url: %s",
				response.status_code,
				response.reason,
				response.url,
			)

		except (Timeout, ConnectionError, HTTPError, RequestException) as e:
			logger.info("The request to random.org timed out")
			return cls._generate_internal_code(rules=rules)

		# parse non empty lines
		lines = []
		for line in response.text.splitlines():
			trimmed_line = line.strip()
			if trimmed_line:
				lines.append(trimmed_line)

		# remove duplicates if not allowed and retry until we get enough values
		if not rules.allow_repeats:
			tracking_set = set()
			final_code_values: list[str] = []
			for value in lines:
				if value not in tracking_set:
					tracking_set.add(value)
					final_code_values.append(value)
				if len(final_code_values) == rules.code_length:
					break

			# if we didn't get enough unique values, fallback to the internal method.
			if len(final_code_values) < rules.code_length:
				return cls.reroute_to_internal(rules)

			lines = final_code_values

		return tuple(lines)
