import logging
from uuid import UUID

from app.models.game import Game, GameCreate
from app.models.guess import Guess
from app.models.rules import Rules
from app.services.player import PlayerService
from app.services.random import RandomService
from app.storages.game import GameStorage

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

	def delete_game(self, game_id: UUID) -> None:
		return self.game_storage.clear_game(game_id)

	def delete_all_games(self) -> None:
		return self.game_storage.clear()

	# GUESS

	def submit_guess(self, game_id: UUID, guess_value: list[str]) -> Guess:
		"""submit guess and return if valid"""

		game = self.get_game(game_id)
		game.assert_can_accept_guess()

		game.rules().validate_sequence(guess_value, "[GUESS]")

		guess = Guess(game_id=game.id, guess_value=guess_value)
		guess.score_guess(secret=game._secret, guess_value=guess_value)
		game.guesses.append(guess)

		game.update_status_if_completed(last_guess=guess)
		self.game_storage.update(game)

		logger.info(
			"Guess has been recorded: \ngame=%s \nattempts=%s \nguesses left:%s",
			game.id,
			len(game.guesses),
			game.max_guesses,
		)
		return guess

	def get_all_guesses(self, game_id: UUID) -> list[Guess]:
		game_obj = self.get_game(game_id=game_id)
		return game_obj.guesses
