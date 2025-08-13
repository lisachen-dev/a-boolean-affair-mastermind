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


	# GAME
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

	def get_all_games_by_player(self, player_id: UUID) -> list[Game]:
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
	# GUESS

		# apply the guess
		# evaluate for status
		# save the game
		# return guess? the game?
		pass

	def get_all_guesses(self) -> list[Guess]:
		pass

	# helpers

	def _score_guess(self, secret: tuple[str,...], guess_value: list[str]) -> Guess:
		"""
		game: attempts_made (len(guesses)) attempts_left
		guess: attempt_number, exact_matches, Partial_matches
		evaluate secret compared to guess_value:
			number in position (exact)
			number in secret, but not in right position (partial)

			secret_leftover = []
			guess_leftover = []

			loop through and match
				* if there is an exact match at the corresponding i, increment exact matches and move on
				* if there isn't, store both in corresponding lists and increment partial match

			for remaining lists, if any guesses are in the secret list, then increment partial match

			create a dictionary to hold remaining values in secret on a count
			compare guess_value by looping and decrement the counts for secrets, but increase the partial amount.
		"""
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
