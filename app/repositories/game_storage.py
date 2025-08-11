import logging

from app.constants import (
	ALLOW_REPEATS,
	CODE_LENGTH,
	MAX_GUESSES,
	MAX_VALUE,
	MIN_VALUE,
	RANDOM_EXTERNAL,
)
from app.models.game import Game, GameCreate

logger = logging.getLogger(__name__)


class GameStorage:
	def __init__(self):
		self.games: dict[str, Game] = {}

	def create_game(self, game_create: GameCreate, secret: tuple[str, ...]) -> Game:
		game = Game(
			player_id=game_create.player_id,
			secret=secret,
			code_length=(
				game_create.code_length
				if game_create.code_length is not None
				else CODE_LENGTH
			),
			max_guesses=(
				game_create.max_guesses
				if game_create.max_guesses is not None
				else MAX_GUESSES
			),
			max_value=(
				game_create.max_value
				if game_create.max_value is not None
				else MAX_VALUE
			),
			min_value=(
				game_create.min_value
				if game_create.min_value is not None
				else MIN_VALUE
			),
			allow_repeats=(
				game_create.allow_repeats
				if game_create.allow_repeats is not None
				else ALLOW_REPEATS
			),
			random_external=(
				game_create.random_external
				if game_create.random_external is not None
				else RANDOM_EXTERNAL
			),
		)

		logger.info("Game created successfully!")

		self.games[str(game.id)] = game
		return game

	def get_game(self, game_id: str) -> Game:
		if game_id not in self.games.keys():
			raise KeyError("Game is not found")

		logger.info("Found the game!")
		return self.games[game_id]
