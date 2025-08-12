import logging
from uuid import UUID

from app.models.game import Game, GameCreate
from app.models.rules import Rules

logger = logging.getLogger(__name__)


class GameStorage:
	def __init__(self) -> None:
		self.games: dict[UUID, Game] = {}

	def create(self, game_create: GameCreate, rules: Rules) -> Game:
		game = Game(player_id=game_create.player_id, **rules.model_dump())

		self.games[game.id] = game
		logger.info(f"Game created successfully! id={game.id}")
		return game

	def get(self, game_id: str) -> Game:
		game_id = UUID(game_id)

		if game_id not in self.games:
			raise KeyError("Game is not found")

		logger.info("Found the game!")
		return self.games[game_id]
