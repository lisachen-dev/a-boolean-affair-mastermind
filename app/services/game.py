import logging
from uuid import UUID

from app.models.game import Game, GameCreate, GameRead
from app.models.guess import Guess, GuessCreate, GuessRead
from app.models.rules import Rules
from app.repositories.game import GameStorage
from app.services.player import PlayerService
from app.services.random import RandomService
from app.utils.validators import validate_code_sequence

logger = logging.getLogger(__name__)

"""

TODO:
attempts_made == max_guesses - attempts_made or 0
if status not IN_PROGRESS, finished_at should be set
if status == WON, the last guess should have exact_matches exact_matches == code.length
reject new guesses after the status is not IN_PROGRESS

"""


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

	def start_game(self, game_create: GameCreate) -> Game:
		logger.debug("Starting game: %s", game_create)

		self.player_service.get(game_create.player_id)

		rules = Rules(
			**game_create.model_dump(
				include={"code_length", "max_guesses", "min_value", "max_value", "allow_repeats"},
				exclude_none=True,
			)
		)
		secret = self.random_service.generate_secret_code(rules)

		new_game = Game(player_id=game_create.player_id, **rules.model_dump())
		new_game._secret = secret
		return self.game_storage.create(new_game)

	def get_game(self, game_id: UUID) -> Game:
		return self.game_storage.get(game_id)

	def list_games_by_player(self, player_id: UUID) -> list[Game]:
		if player_id is None:
			raise ValueError("player_id is required")

		self.player_service.get(player_id)
		return self.game_storage.get_all_by_player(player_id)

	def get_all_games(self) -> list[GameRead]:
		games = self.game_storage.get_all()
		read_games = [self.to_game_read(game) for game in games]
		logger.info("Returning %d games", len(read_games))
		return read_games

	def create_guess(self, game_id: UUID, new_guess: GuessCreate):
		# game
		# validate guess
		# guess
		# apply the guess
		# evaluate for status
		# save the game
		# return guess? the game?
		pass

	def get_all_guesses(self) -> list[Guess]:
		pass

	def _evaluate_guess(self, game: Game, guess_value: str) -> Guess:
		# attempt number iterate
		#
		pass

	def _update_status_if_completed(self, game: Game, last_guess: Guess):
		# WIN? LOSE?
		pass

	# mappings
	@staticmethod
	def to_game_read(game: Game) -> GameRead:
		return GameRead(
			**game.model_dump(
				include={
					"id",
					"status",
					"player_id",
					"guesses",
					"finished_at",
					"code_length",
					"max_guesses",
					"min_value",
					"max_value",
					"allow_repeats",
					"created_at",
				}
			)
		)

	@staticmethod
	def to_guess_read(game_id: UUID, guess: Guess) -> GuessRead:
		pass
