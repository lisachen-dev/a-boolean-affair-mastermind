import logging
from uuid import UUID

from app.models.game import Game

logger = logging.getLogger(__name__)


class GameStorage:
	def __init__(self) -> None:
		self._games: dict[UUID, Game] = {}

	def create(self, game: Game) -> Game:
		self._games[game.id] = game
		logger.info("Game created successfully! id=%s", game.id)
		return game

	def get(self, game_id: UUID) -> Game:
		if game_id not in self._games:
			raise KeyError("Game not found")

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

	def update(self, game: Game) -> Game:
		if game not in self._games:
			raise KeyError("Game not found")
		self._games[game.id] = game
		logger.info("Game updated successfully! id=%s", game.id)
		return game
