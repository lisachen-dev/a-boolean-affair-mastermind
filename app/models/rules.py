from typing import Sequence

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Self

from app.constants import ALLOW_REPEATS, CODE_LENGTH, MAX_GUESSES, MAX_VALUE, MIN_VALUE


class Rules(BaseModel):
	model_config = ConfigDict(extra="forbid")

	code_length: int = Field(default=CODE_LENGTH, ge=1)
	max_guesses: int = Field(default=MAX_GUESSES, ge=1)
	min_value: int = Field(default=MIN_VALUE, ge=0)
	max_value: int = Field(default=MAX_VALUE, ge=0)
	allow_repeats: bool = Field(default=ALLOW_REPEATS)

	@model_validator(mode="after")
	def _validate_self(self) -> Self:
		if self.min_value > self.max_value:
			raise ValueError("[RULE] min_value must be <= than max_value")
		if not self.allow_repeats:
			pool_size = self.max_value - self.min_value + 1
			if self.code_length > pool_size:
				raise ValueError("[RULE] Pool size not large enough to handle unique values")
		return self

	def validate_sequence(
		self,
		values: Sequence[str],
		label: str = "[CODE]",
	) -> None:
		if len(values) != self.code_length:
			raise ValueError(f"{label} Length must be equivalent to {self.code_length}")

		if not self.allow_repeats and len(set(values)) != len(values):
			raise ValueError(f"{label} Duplicates are found, but allow_repeats is set to False")

		for value in values:
			if not value.isdigit():
				raise ValueError(f"{label} {value} is not a valid integer")
			if not self.min_value <= int(value) <= self.max_value:
				raise ValueError(f"{label} {value} is out of range")
