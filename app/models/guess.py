from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


# TODO reminder to wrute validation in server/ (guess_value / attempt_num etc)
class GuessBase(BaseModel):
	guess_value: str


class GuessCreate(GuessBase):
	game_id: UUID


class Guess(GuessBase):
	id: UUID = Field(default_factory=uuid4)
	game_id: UUID

	# server-only fields
	attempt_no: int
	exact_matches: int = Field(default=0)
	partial_matches: int = Field(default=0)
	created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

	# TODO Plug for future multiplayer consideration
	# TODO idempotency key  to handle retries (network, user double-clicks)
