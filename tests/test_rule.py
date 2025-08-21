import pytest

from app.models.rules import Rules


def test_valid_rules_creation():
	rules = Rules(code_length=4, min_value=1, max_value=6, max_guesses=10, allow_repeats=False)

	assert rules.code_length == 4
	assert rules.min_value == 1
	assert rules.max_value == 6
	assert rules.max_guesses == 10
	assert rules.allow_repeats is False


def test_invalid_min_greater_than_max():
	with pytest.raises(ValueError, match=r"\[RULE\] min_value must be <= than max_value"):
		Rules(min_value=5, max_value=1)


def test_invalid_pool_size():
	with pytest.raises(
		ValueError, match=r"\[RULE\] Pool size not large enough to handle unique values"
	):
		Rules(min_value=1, max_value=2, code_length=10, allow_repeats=False)
