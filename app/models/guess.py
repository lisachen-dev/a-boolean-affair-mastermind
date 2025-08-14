from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


# ----
# DOMAIN (state and logic)
# ----
class Guess(BaseModel):
	model_config = ConfigDict(extra="forbid")
	id: UUID = Field(default_factory=uuid4)
	game_id: UUID
	guess_value: list[str]
	exact_matches: int = Field(default=0)
	partial_matches: int = Field(default=0)
	created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

	def score_guess(self, secret: tuple[str, ...], guess_value: list[str]) -> None:
		"""
		assumes lengths have been validated
		"""
		secret_remaining = {}
		guess_remaining = []

		for i in range(len(secret)):
			if guess_value[i] == secret[i]:
				self.exact_matches += 1
				continue

			guess_remaining.append(guess_value[i])
			secret_remaining[secret[i]] = secret_remaining.get(secret[i], 0) + 1

		# determine partial matches on remaining values without double counting
		for guess_val in guess_remaining:
			if secret_remaining.get(guess_val, 0) > 0:
				self.partial_matches += 1
				secret_remaining[guess_val] -= 1

	def to_last_result(self) -> "GuessLastResult":
		return GuessLastResult(
			guess_value=self.guess_value,
			exact_matches=self.exact_matches,
			partial_matches=self.partial_matches,
		)


# ----
# SCHEMAS (request/response)
# ----
class GuessLastResult(BaseModel):
	model_config = ConfigDict(extra="forbid")
	guess_value: list[str]
	exact_matches: int
	partial_matches: int


class GuessCreate(BaseModel):
	model_config = ConfigDict(extra="forbid")
	guess_value: list[str]
