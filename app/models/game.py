import enum
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.constants import (
	ALLOW_REPEATS,
	CODE_LENGTH,
	IS_EXTERNAL_CODE,
	MAX_GUESSES,
	MAX_VALUE,
	MIN_VALUE,
)
from app.models.guess import Guess


class GameStatus(str, enum.Enum):
	IN_PROGRESS = "in_progress"
	LOST = "lost"
	WON = "won"


class GameCreate(BaseModel):
	player_id: UUID
	code_length: Optional[int] = None
	max_guesses: Optional[int] = None
	min_value: Optional[int] = None
	max_value: Optional[int] = None
	allow_repeats: Optional[bool] = None
	is_external_code: Optional[bool] = None


class Game(BaseModel):
	_secret: tuple[str, ...] = PrivateAttr(default=())
	id: UUID = Field(default_factory=uuid4)
	status: GameStatus = GameStatus.IN_PROGRESS
	player_id: UUID
	guesses: list[Guess] = Field(default_factory=list)

	secret: tuple[str, ...] = Field(exclude=True)
	finished_at: datetime | None = None

	code_length: int = Field(
		default=CODE_LENGTH, description="sets limit on length of solution"
	)
	max_guesses: int = Field(
		default=MAX_GUESSES, description="sets limit on amount of guesses user has"
	)
	min_value: int = Field(
		default=MIN_VALUE,
		description="sets min value on range of digits allowed",
	)
	max_value: int = Field(
		default=MAX_VALUE, description="sets max value on range of digits allowed"
	)
	allow_repeats: bool = Field(
		default=ALLOW_REPEATS, description="allows non-unique values"
	)
	is_external_code: bool = Field(
		default=IS_EXTERNAL_CODE,
		description="toggle between using internal and external code generation",
	)

	created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
