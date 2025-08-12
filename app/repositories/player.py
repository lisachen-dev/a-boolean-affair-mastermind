import logging
from uuid import UUID

from app.models.player import Player, PlayerCreate

logger = logging.getLogger(__name__)


class PlayerStorage:
	def __init__(self) -> None:
		self._players: dict[UUID, Player] = {}

	def create(self, player_create: PlayerCreate) -> Player:
		player = Player(name=player_create.name)
		self._players[player.id] = player
		return player

	def get(self, player_id: UUID) -> Player:
		if player_id not in self._players:
			raise KeyError("Player does not exist")
		return self._players[player_id]

	def get_all(self) -> list[Player]:
		return list(self._players.values())
