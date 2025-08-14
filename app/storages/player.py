import logging
from uuid import UUID

from app.models.player import Player

logger = logging.getLogger(__name__)


class PlayerStorage:
	def __init__(self) -> None:
		self._players: dict[UUID, Player] = {}

	def create(self, name: str) -> Player:
		player = Player(name=name)
		self._players[player.id] = player
		logger.info("Player created with id=%s, name=%s", player.id, player.name)
		return player

	def get(self, player_id: UUID) -> Player:
		player = self._players.get(player_id)
		if player is None:
			raise KeyError("Player not found")
		return self._players[player_id]

	def get_all(self) -> list[Player]:
		return list(self._players.values())

	def exists(self, player_id: UUID) -> bool:
		return player_id in self._players

	def clear_player(self, player_id: UUID) -> None:
		if player_id in self._players:
			del self._players[player_id]
			logger.info("Player &s was removed from storage", player_id)
		else:
			logger.info("Tried to remove player %s, but it just doesn't exist", player_id)

	def clear_all_players(self) -> None:
		num_of_players = len(self._players)
		self._players.clear()
		logger.info("Player information has been cleared! %d removed", num_of_players)
