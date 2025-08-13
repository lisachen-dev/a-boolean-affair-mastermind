from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

"""
DOMAIN (state and logic)
"""


class Guess(BaseModel):
	id: UUID = Field(default_factory=uuid4)
	game_id: UUID
	guess_value: list[str]
	exact_matches: int = Field(default=0)
	partial_matches: int = Field(default=0)
	created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

	def to_last_result(self) -> "GuessLastResult":
		return GuessLastResult(
			guess_value=self.guess_value,
			exact_matches=self.exact_matches,
			partial_matches=self.partial_matches,
		)


"""
SCHEMAS (request/response)
"""


class GuessLastResult(BaseModel):
	guess_value: list[str]
	exact_matches: int
	partial_matches: int


class GuessCreate(BaseModel):
	guess_value: list[str]
