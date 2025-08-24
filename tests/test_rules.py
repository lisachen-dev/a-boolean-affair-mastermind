import pytest

from app.models.rules import Rules


def test_valid_rules_creation():
	rules = Rules(code_length=4, max_guesses=10, min_value=1, max_value=6, allow_repeats=False)
	assert rules.code_length == 4
	assert rules.max_guesses == 10
	assert rules.min_value == 1
	assert rules.max_value == 6
	assert rules.max_repeats is False

	def test_invalid_min_greater_than_max():
		with pytest.raises(ValueError, match=r"\[RULE\] min_value must be <= than max_value"):
			Rules(code_length=4, max_guesses=10, min_value=10, max_value=5)
