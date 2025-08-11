import logging
import secrets

import requests
from fastapi import HTTPException
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

logger = logging.getLogger(__name__)

RANDOM_BASE_URL = "https://www.random.org/integers/"


def _validate_provided_parameters(
	code_length: int, min_value: int, max_value: int, allow_repeats: bool
) -> None:
	""" Validate that the parameters passed in are valid """
	if code_length <= 0:
		raise ValueError("[RULE]: Code length cannot go below 0")

	if min_value > max_value:
		raise ValueError("[RULE] Code difference cannot go below 0")

	if not allow_repeats:
		pool_size = max_value - min_value + 1
		if code_length > pool_size:
			raise ValueError(
				"[RULE] Pool size not large enough to handle unique values"
			)


def _validate_secret(
	secret: list[str],
	code_length: int,
	min_value: int,
	max_value: int,
	allow_repeats: bool,
) -> None:
	""" Validate that the secret code falls within rule parameters """
	if len(secret) != code_length:
		raise ValueError("[SECRET] Secret length is invalid code length")

	if not all(min_value <= int(value) <= max_value for value in secret):
		raise ValueError("[SECRET] Part or all of the secret values are out of range")

	if not allow_repeats and len(set(secret)) != code_length:
		raise ValueError(
			"[SECRET] Duplicates are found, but allow_repeats is set to False"
		)


def generate_secret_code(
	external_code: bool,
	code_length: int,
	min_value: int,
	max_value: int,
	allow_repeats: bool,
) -> list[str]:
	""" Generate a numeric secret code using either Python's secrets (internal) or random.org (external) """
	_validate_provided_parameters(code_length, min_value, max_value, allow_repeats)

	if external_code:
		return _generate_external_code(
			code_length=code_length,
			min_value=min_value,
			max_value=max_value,
			allow_repeats=allow_repeats,
		)
	else:
		return _generate_internal_code(
			code_length=code_length,
			min_value=min_value,
			max_value=max_value,
			allow_repeats=allow_repeats,
		)


def _generate_internal_code(
	code_length: int, min_value: int, max_value: int, allow_repeats: bool
) -> list[str]:
	""" Generate the secret code using Python's secrets module """
	rand_num_generator = secrets.SystemRandom()
	pool = list(range(min_value, max_value + 1))

	if allow_repeats:
		values = [rand_num_generator.choice(pool) for _ in range(code_length)]
	else:
		if code_length > len(pool):
			raise ValueError(
				"Allow repeats is set to False and code length is greater than pool of allowed values"
			)
		values = rand_num_generator.sample(pool, code_length)

	secret_list = [str(value) for value in values]

	_validate_secret(secret_list, code_length, min_value, max_value, allow_repeats)

	logger.info("The secret code was generated using Python's secrets module!")

	return secret_list


def _generate_external_code(
	code_length: int,
	min_value: int,
	max_value: int,
	allow_repeats: bool,
) -> list[str]:
	""" Generate the secret code using Random.org """
	is_unique = "off" if allow_repeats else "on"
	payload = {
		"num": code_length,
		"min": min_value,
		"max": max_value,
		"col": 1,
		"base": 10,
		"unique": is_unique,
		"format": "plain",
		"rnd": "new",
	}

	try:
		response = requests.get(RANDOM_BASE_URL, params=payload, timeout=10)
		logger.debug(
			f"Random.org response: [status: {response.status_code}] | response: {response.reason} | url: {response.url}"
		)

		# if there's an error, returns HTTPError object
		response.raise_for_status()

	except Timeout:
		raise HTTPException(
			status_code=500, detail="The request to random.org timed out"
		)

	except ConnectionError:
		raise HTTPException(
			status_code=500, detail="Random.org returned a connection error"
		)

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

	_validate_secret(secret_list, code_length, min_value, max_value, allow_repeats)

	logger.info("The secret code was generated using random.org!")

	return secret_list
