from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

# TODO Plug for future multiplayer consideration
# TODO reminder to write validation in server/ (remaining attempts calculate)


class GuessCreate(BaseModel):
	guess_value: list[str]


class GuessRead(BaseModel):
	id: UUID
	game_id: UUID
	guess_value: list[str]
	attempt_number: int
	exact_matches: int
	partial_matches: int
	created_at: datetime


class GuessLastResult(BaseModel):
	guess_value: list[str]
	attempt_number: int
	exact_matches: int
	partial_matches: int
	created_at: datetime


class Guess(BaseModel):
	id: UUID = Field(default_factory=uuid4)
	game_id: UUID
	guess_value: list[str]
	attempt_number: int
	exact_matches: int = Field(default=0)
	partial_matches: int = Field(default=0)
	created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
