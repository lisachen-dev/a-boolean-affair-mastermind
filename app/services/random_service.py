import logging

import requests
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from requests import ConnectionError, HTTPError, RequestException, Timeout

logger = logging.getLogger(__name__)

RANDOM_BASE_URL = "https://www.random.org/integers/"


def generate_secret_code(external_code: bool):
	pass


def generate_internal_code(
	code_length: int, min_digit: int, max_digit: int, allow_repeats: bool
):
	pass


def generate_external_code(
	code_length: int,
	min_digit: int,
	max_digit: int,
	allow_repeats: bool,
):
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

	# TODO build out exceptions and remaining secret code logic
	try:
		response = requests.get(RANDOM_BASE_URL, params=payload)
		response.raise_for_status()
	except (Timeout, ConnectionError, HTTPError, RequestException):
		raise HTTPException(status_code=502, detail="request failed upstream")

	try:
		pass
		# convert to list[int]
	except:
		pass
		# raise fastapi exception
