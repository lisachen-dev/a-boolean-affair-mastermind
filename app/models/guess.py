from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


# TODO reminder to write validation in server/ (remaining attempts calculate)
class GuessBase(BaseModel):
	guess_value: str


class GuessCreate(GuessBase):
	# reminder: does not need id you get game_id from router path
	pass


class GuessRead(GuessBase):
	id: UUID
	game_id: UUID
	attempt_number: int
	exact_matches: int
	partial_matches: int
	created_at: datetime


class Guess(GuessBase):
	id: UUID = Field(default_factory=uuid4)
	game_id: UUID

	# server-only fields
	exact_matches: int = Field(default=0)
	partial_matches: int = Field(default=0)
	attempt_number: int
	created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

	# TODO Plug for future multiplayer consideration
	# TODO idempotency key  to handle retries (network, user double-clicks)
