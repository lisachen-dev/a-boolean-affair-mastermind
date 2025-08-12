import logging

from app.constants import (
	ALLOW_REPEATS,
	CODE_LENGTH,
	IS_EXTERNAL_CODE,
	MAX_GUESSES,
	MAX_VALUE,
	MIN_VALUE,
)
from app.models.game import Game, GameCreate

logger = logging.getLogger(__name__)


class GameStorage:
	def __init__(self) -> None:
		self.games: dict[str, Game] = {}

	def create(
		self, game_create: GameCreate, secret: tuple[str, ...], rules: dict
	) -> Game:
		game = Game(
			player_id=game_create.player_id,
			secret=secret,
			code_length=game_create.code_length,
			max_guesses=game_create.max_guesses,
			max_value=game_create.max_value,
			min_value=game_create.min_value,
			allow_repeats=game_create.allow_repeats,
		)

		self.games[str(game.id)] = game
		logger.info("Game created successfully!")
		return game

	def get(self, game_id: str) -> Game:
		if game_id not in self.games:
			raise KeyError("Game is not found")

		logger.info("Found the game!")
		return self.games[game_id]
