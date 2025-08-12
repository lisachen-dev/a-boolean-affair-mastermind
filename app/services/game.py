import logging
from uuid import UUID

from app.constants import (
	ALLOW_REPEATS,
	CODE_LENGTH,
	MAX_GUESSES,
	MAX_VALUE,
	MIN_VALUE,
)
from app.models.game import Game, GameCreate, GameRead
from app.models.guess import Guess, GuessCreate, GuessRead
from app.models.rules import Rules
from app.repositories.game import GameStorage
from app.repositories.player import PlayerStorage
from app.services.player import PlayerService
from app.services.random import RandomService

logger = logging.getLogger(__name__)


class GameService:
	def __init__(
		self,
		game_storage: GameStorage,
		random_service: RandomService,
		player_service: PlayerService,
	):
		self.game_storage = game_storage
		self.random_service = random_service
		self.player_service = player_service

	@staticmethod
	def _decide_default(value, fallback):
		return value if value is not None else fallback

	def _resolve_rules(self, new_game: GameCreate) -> Rules:
		return Rules(
			code_length=self._decide_default(new_game.code_length, CODE_LENGTH),
			max_guesses=self._decide_default(new_game.max_guesses, MAX_GUESSES),
			min_value=self._decide_default(new_game.min_value, MIN_VALUE),
			max_value=self._decide_default(new_game.max_value, MAX_VALUE),
			allow_repeats=self._decide_default(new_game.allow_repeats, ALLOW_REPEATS),
		)

	def start_game(self, game_create: GameCreate) -> Game:
		# verify player exists

		# rules
		# secret
		# game
		# return game
		pass

	def get_game(self, game_id: UUID) -> Game:
		return self.game_storage.get(game_id)

	def list_games_by_player(self, player_id: UUID | None = None) -> list[Game]:
		return self.game_storage.get_all_by_player(player_id)

	def list_all_games(self):
		return self.game_storage.get_all()

	def create_guess(self, game_id: UUID, new_guess: GuessCreate):
		# game
		# validate guess
		# guess
		# apply the guess
		# evaluate for status
		# save the game
		# return guess? the game?
		pass

	# validations

	def _validate_guess_input(self, guess_value: str, rules: Rules) -> None:
		pass

	def _evaluate_guess(self, game: Game, guess_value: str) -> Guess:
		# attempt number iterate
		#
		pass

	def _update_statis_if_completed(selfself, game: Game, last_guess: Guess):
		# WIN? LOSE?
		pass

	# mappings
	@staticmethod
	def to_game_read(game: Game) -> GameRead:
		return GameRead(**game.model_dump())

	@staticmethod
	def to_guess_read(self, game_id: UUID, guess: Guess) -> GuessRead:
		pass
