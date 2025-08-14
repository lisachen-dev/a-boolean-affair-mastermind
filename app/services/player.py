import logging
from uuid import UUID

from app.models.player import Player
from app.storages.player import PlayerStorage

logger = logging.getLogger(__name__)


class PlayerService:
	def __init__(self, player_storage: PlayerStorage) -> None:
		self.player_storage = player_storage

	def create(self, name: str) -> Player:
		if name is None or not str(name).strip():
			raise ValueError("Name is required")
		player = self.player_storage.create(name=name)
		logger.info("Player registered: id=%s name=%s", player.id, player.name)
		return player

	def get(self, player_id: UUID) -> Player:
		player = self.player_storage.get(player_id=player_id)
		logger.debug("Found player %s", player.name)
		return player

	def get_all(self) -> list[Player]:
		return self.player_storage.get_all()
