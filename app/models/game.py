import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

from app.models.guess import Guess, GuessLastResult
from app.models.rules import Rules

logger = logging.getLogger(__name__)


class GameStatus(str, Enum):
	IN_PROGRESS = "in_progress"
	LOST = "lost"
	WON = "won"


# ----
# DOMAIN (state and logic)
# ----
class Game(BaseModel):
	model_config = ConfigDict(extra="forbid")

	# private (not serialized)
	_secret: tuple[str, ...] = PrivateAttr(default=())

	# identity and state
	id: UUID = Field(default_factory=uuid4)
	status: GameStatus = GameStatus.IN_PROGRESS
	player_id: UUID
	guesses: list[Guess] = Field(default_factory=list)
	finished_at: datetime | None = None
	created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

	# rules - defaults are set there
	code_length: int
	max_guesses: int
	min_value: int
	max_value: int
	allow_repeats: bool

	def rules(self) -> Rules:
		return Rules(
			**self.model_dump(
				include={"code_length", "max_guesses", "min_value", "max_value", "allow_repeats"}
			)
		)

	def assert_can_accept_guess(self) -> None:
		if self.status != GameStatus.IN_PROGRESS:
			raise ValueError("This game is closed! Please start a new game.")
		if len(self.guesses) >= self.max_guesses:
			raise PermissionError("No attempts left")

	def update_status_if_completed(self, last_guess: Guess) -> None:
		if last_guess.exact_matches == self.code_length:
			self._finish(GameStatus.WON)
		elif len(self.guesses) >= self.max_guesses:
			self._finish(GameStatus.LOST)

	def _finish(self, status: GameStatus):
		if self.finished_at is None:
			self.status = status
			self.finished_at = self._utc_now()

	@staticmethod
	def _utc_now() -> datetime:
		return datetime.now(timezone.utc)


# ---
# SCHEMA
# ---
class GameCreate(BaseModel):
	model_config = ConfigDict(extra="forbid")

	player_id: UUID
	code_length: Optional[int] = None
	max_guesses: Optional[int] = None
	min_value: Optional[int] = None
	max_value: Optional[int] = None
	allow_repeats: Optional[bool] = None


class GameView(BaseModel):
	model_config = ConfigDict(extra="forbid")

	id: UUID
	player_id: UUID
	status: GameStatus
	code_length: int
	max_guesses: int
	min_value: int
	max_value: int
	allow_repeats: bool
	attempts_made: int
	attempts_left: int
	last_result: GuessLastResult | None
	finished_at: datetime | None
	created_at: datetime

	@classmethod
	def from_game(cls, game: "Game") -> "GameView":
		last_guess = game.guesses[-1] if game.guesses else None
		base = game.model_dump(
			include={
				"id",
				"status",
				"player_id",
				"finished_at",
				"created_at",
				"last_result",
				"code_length",
				"max_guesses",
				"min_value",
				"max_value",
				"allow_repeats",
			}
		)
		base.update(
			{
				"attempts_made": len(game.guesses),
				"attempts_left": max(game.max_guesses - len(game.guesses), 0),
				"last_result": last_guess.to_last_result() if last_guess else None,
			}
		)

		game_view = cls.model_validate(base)
		logger.debug("New Game View created %s", game_view.id)

		# parse the base class to run field validators and return instance
		return game_view
