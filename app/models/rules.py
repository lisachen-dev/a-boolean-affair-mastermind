from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self

from app.constants import ALLOW_REPEATS, CODE_LENGTH, MAX_GUESSES, MAX_VALUE, MIN_VALUE


class Rules(BaseModel):
	code_length: int = Field(default=CODE_LENGTH, ge=1)
	max_guesses: int = Field(default=MAX_GUESSES, ge=1)
	min_value: int = Field(default=MIN_VALUE, ge=0)
	max_value: int = Field(default=MAX_VALUE, ge=0)
	allow_repeats: bool = Field(default=ALLOW_REPEATS)

	@model_validator(mode="after")
	def _validate(self) -> Self:
		if self.min_value > self.max_value:
			raise ValueError("[RULE] min_value must be <= than max_value")
		if not self.allow_repeats:
			pool_size = self.max_value - self.min_value + 1
			if self.code_length > pool_size:
				raise ValueError("[RULE] Pool size not large enough to handle unique values")
