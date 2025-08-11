import logging

import requests
from fastapi import HTTPException
from requests import ConnectionError, HTTPError, RequestException, Timeout

logger = logging.getLogger(__name__)

RANDOM_BASE_URL = "https://www.random.org/integers/"


def _validate_provided_parameters(
		code_length: int,
		min_digit: int,
		max_digit: int,
		allow_repeats: bool
) -> None:

	if code_length <= 0:
		raise ValueError("[RULE]: Code length cannot go below 0")

	if min_digit > max_digit:
		raise ValueError("[RULE] Code difference cannot go below 0")

	if not allow_repeats:
		pool_size = max_digit - min_digit + 1
		if code_length > pool_size:
			raise ValueError("[RULE] Pool size not large enough to handle unique values")

def _validate_secret(
		secret: str,
		code_length: int,
		min_digit: int,
		max_digit: int,
		allow_repeats: bool
) -> None:

	if len(secret) != code_length:
		raise ValueError("[SECRET] Secret length is invalid code length")

	if not all(min_digit <= int(digit) <= max_digit for digit in secret):
		raise ValueError("[SECRET] Part or all of the secret values are out of range")

	if not allow_repeats and len(set(secret)) != code_length:
		raise ValueError("[SECRET] Duplicates are found, but allow_repeats is set to False")

def generate_secret_code(
	external_code: bool,
	code_length: int,
	min_digit: int,
	max_digit: int,
	allow_repeats: bool
) -> str:
	"""
	TODO Create explanative docstring
	Generate secret code based on game rules and indicator for using Random.org or Python's built-in random generator
	"""

	secret_code = (
		generate_external_code(
			code_length=code_length,
			min_digit=min_digit,
			max_digit=max_digit,
			allow_repeats=allow_repeats,
		)
		if external_code
		else generate_internal_code(
			code_length=code_length,
			min_digit=min_digit,
			max_digit=max_digit,
			allow_repeats=allow_repeats,
		)
	)

	return secret_code


def generate_internal_code(
	code_length: int, min_digit: int, max_digit: int, allow_repeats: bool
) -> str:
	pass


def generate_external_code(
	code_length: int,
	min_digit: int,
	max_digit: int,
	allow_repeats: bool,
) -> str:

	_validate_provided_parameters(code_length, min_digit, max_digit, allow_repeats)

	is_unique = "off" if allow_repeats else "on"

	payload = {
		"num": code_length,
		"min": min_digit,
		"max": max_digit,
		"col": 1,
		"base": 10,
		"unique": is_unique,
		"format": "plain",
		"rnd": "new",
	}

	try:
		response = requests.get(RANDOM_BASE_URL, params=payload, timeout=10)
		logger.debug(
			f"random.org response: status: {response.status_code}, response: {response.reason}"
		)

		# if there's an error, returns HTTPError object
		response.raise_for_status()

	except Timeout:
		raise HTTPException(status_code=500, detail="The request to the random number service timed out")

	except ConnectionError:
		raise HTTPException(status_code=500, detail="The random number service returned an error")

	except HTTPError:
		raise HTTPException(status_code=500, detail="Could not connect to random.org")

	except RequestException:
		raise HTTPException(status_code=500, detail="An unexpected error occurred while connecting with random.org")

	format_response = response.text.replace("\n","").strip()
	_validate_secret(format_response,code_length, min_digit, max_digit, allow_repeats)
	return format_response

# TODO: remove this once you're done testing
if __name__ == "__main__":
	code = generate_external_code(
		code_length=4,
		min_digit=0,
		max_digit=9,
		allow_repeats=False
	)
	print(f"Generated code: {code}")
