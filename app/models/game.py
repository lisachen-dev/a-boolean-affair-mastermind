import enum
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.constants import ALLOW_REPEATS, CODE_LENGTH, DIGIT_POOL_SIZE, MAX_GUESSES
from app.models.guess import Guess


class StatusEnum(str, enum.Enum):
	CREATED = "created"
	IN_PROGRESS = "in_progress"
	LOST = "lost"
	WON = "won"


class GameCreate(BaseModel):
	player_id: UUID
	code_length: Optional[int] = None
	max_guesses: Optional[int] = None
	digit_pool_size: Optional[int] = None
	allow_repeats: Optional[bool] = None


class Game(BaseModel):
	id: UUID = Field(default_factory=uuid4)
	status: StatusEnum = StatusEnum.CREATED  # TODO flip to IN_PROGRESS on 1st guess
	player_id: UUID
	guesses: list[Guess] = Field(default_factory=list)

	secret: str = Field(exclude=True)
	finished_at: datetime | None = None

	code_length: int = Field(
		default=CODE_LENGTH, description="sets limit on length of solution"
	)
	max_guesses: int = Field(
		default=MAX_GUESSES, description="sets limit on amount of guesses user has"
	)
	digit_pool_size: int = Field(
		default=DIGIT_POOL_SIZE,
		description="sets limit on variations of digits allowed",
	)
	allow_repeats: bool = Field(
		default=ALLOW_REPEATS, description="allows non-unique values"
	)

	created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
