import logging
from datetime import datetime, timezone
from uuid import UUID

from app.models.game import Game, GameCreate, GameStatus
from app.models.guess import Guess
from app.models.rules import Rules
from app.repositories.game import GameStorage
from app.services.player import PlayerService
from app.services.random import RandomService
from app.utils.validators import validate_code_sequence

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

	# GAME

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

	def get_all_games(self) -> list[Game]:
		games = self.game_storage.get_all()
		logger.debug("Returning %d games", len(games))
		return games

	# GUESS

	def submit_guess(self, game_id: UUID, guess_value: list[str]) -> Guess:
		"""submit guess and return the read-friendly GuessRead"""

		game = self.get_game(game_id)
		if game.status != GameStatus.IN_PROGRESS:
			raise ValueError("This game is closed! Please start a new game.")
		if len(game.guesses) >= game.max_guesses:
			raise PermissionError("No attempts left")

		# validate guess input against game rules
		validate_code_sequence(
			values=guess_value,
			code_length=game.code_length,
			min_value=game.min_value,
			max_value=game.max_value,
			allow_repeats=game.allow_repeats,
			label="[GUESS]",
		)

		exact_matches, partial_matches = self._score_guess(
			secret=game._secret, guess_value=guess_value
		)

		guess = Guess(
			game_id=game.id,
			guess_value=guess_value,
			exact_matches=exact_matches,
			partial_matches=partial_matches,
			created_at=self._utc_now(),
		)

		game.guesses.append(guess)

		self._update_status_if_completed(game=game, last_guess=guess)
		self.game_storage.update(game)

		logger.info(
			"Guess has been recorded: game=%s attempts=%s %s",
			game.id,
			len(game.guesses),
			game.max_guesses,
		)
		return guess

	def get_all_guesses(self, game_id: UUID) -> list[Guess]:
		game_obj = self.get_game(game_id=game_id)
		return game_obj.guesses

	# HELPERS

	@staticmethod
	def _score_guess(secret: tuple[str, ...], guess_value: list[str]) -> tuple[int, int]:
		"""
		Returns exact_match_count and partial_match_count
		assumes lengths have been validated
		"""
		# determine exact matches and store remaining values for later
		exact_match_count = 0
		secret_remaining = {}
		guess_remaining = []

		for i in range(len(secret)):
			if guess_value[i] == secret[i]:
				exact_match_count += 1
				continue

			guess_remaining.append(guess_value[i])
			secret_remaining[secret[i]] = secret_remaining.get(secret[i], 0) + 1

		# determine partial matches on remaining values without double counting
		partial_match_count = 0
		for guess_val in guess_remaining:
			if secret_remaining.get(guess_val, 0) > 0:
				partial_match_count += 1
				secret_remaining[guess_val] -= 1

		return exact_match_count, partial_match_count

	def _update_status_if_completed(self, game: Game, last_guess: Guess) -> None:
		if last_guess.exact_matches == game.code_length:
			game.status = GameStatus.WON
			game.finished_at = self._utc_now()
		elif len(game.guesses) >= game.max_guesses:
			game.status = GameStatus.LOST
			game.finished_at = self._utc_now()

	@staticmethod
	def _utc_now() -> datetime:
		return datetime.now(timezone.utc)
