import logging

import requests

logger = logging.getLogger(__name__)

RANDOM_BASE_URL = "https://www.random.org/integers/"


def generate_secret_code(
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
	except:
		pass
		# HTTPError
		# ConnectionError
		# Timeout
		# RequestException - catch all

	try:
		pass
		# convert to list[int]
	except:
		pass
		# raise fastapi exception
