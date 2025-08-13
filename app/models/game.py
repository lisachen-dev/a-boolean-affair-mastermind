import enum
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, PrivateAttr

from app.models.guess import Guess, GuessLastResult


class GameStatus(str, enum.Enum):
	IN_PROGRESS = "in_progress"
	LOST = "lost"
	WON = "won"


class GameRead(BaseModel):
	id: UUID
	player_id: UUID
	status: GameStatus
	attempts_made: int  # calculate this, len(guesses?)
	attempts_left: int  # calculate this, max guesses - attempts made?
	code_length: int
	max_guesses: int
	min_value: int
	max_value: int
	allow_repeats: bool
	finished_at: datetime | None = None
	created_at: datetime
	last_result: GuessLastResult | None = None


class GameCreate(BaseModel):
	player_id: UUID
	code_length: Optional[int] = None
	max_guesses: Optional[int] = None
	min_value: Optional[int] = None
	max_value: Optional[int] = None
	allow_repeats: Optional[bool] = None


class Game(BaseModel):
	_secret: tuple[str, ...] = PrivateAttr(default=())
	id: UUID = Field(default_factory=uuid4)
	status: GameStatus = GameStatus.IN_PROGRESS
	player_id: UUID
	guesses: list[Guess] = Field(default_factory=list)
	finished_at: datetime | None = None
	created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

	# Required for Rules class - defaults are set there
	code_length: int
	max_guesses: int
	min_value: int
	max_value: int
	allow_repeats: bool
