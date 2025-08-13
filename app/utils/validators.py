from app.models.rules import Rules


def validate_code_sequence(
	values: list[str] | tuple[str, ...],
	code_length: int,
	min_value: int,
	max_value: int,
	allow_repeats: bool,
	label: str,
) -> None:
	if len(values) != code_length:
		raise ValueError(f"{label} Length must be equivalent to {code_length}")

	if not allow_repeats and len(set(values)) != code_length:
		raise ValueError(f"{label} Duplicates are found, but allow_repeats is set to False")

	for value in values:
		if not value.isdigit():
			raise ValueError(f"{label} %s is not a valid integer", value)
		if not min_value <= int(value) <= max_value:
			raise ValueError(f"{label} %s is out of range", value)
