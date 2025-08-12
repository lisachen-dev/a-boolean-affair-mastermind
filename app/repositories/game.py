import logging
from uuid import UUID

from app.models.game import Game, GameCreate
from app.models.rules import Rules

logger = logging.getLogger(__name__)


class GameStorage:
	def __init__(self) -> None:
		self._games: dict[UUID, Game] = {}

	def create(self, game_create: GameCreate, rules: Rules) -> Game:
		game = Game(player_id=game_create.player_id, **rules.model_dump())

		self._games[game.id] = game
		logger.info(f"Game created successfully! id={game.id}")
		return game

	def get(self, game_id: UUID) -> Game:
		if game_id not in self._games:
			raise KeyError("Game is not found")

		logger.info("Found the game!")
		return self._games[game_id]

	def get_all(self) -> list[Game]:
		return list(self._games.values())

	def get_all_by_player(self, player_id: UUID | None) -> list[Game]:

		filtered_games_by_player = []
		for game in self._games.values():
			if game.player_id == player_id:
				filtered_games_by_player.append(game)

		return filtered_games_by_player
