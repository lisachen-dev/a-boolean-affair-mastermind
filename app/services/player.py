import logging
from uuid import UUID

from app.models.player import Player, PlayerCreate, PlayerRead
from app.repositories.player import PlayerStorage

logger = logging.getLogger(__name__)


class PlayerService:
	def __init__(self, player_storage: PlayerStorage) -> None:
		self.player_storage = player_storage

	def create(self, name: str) -> Player:
		player = self.player_storage.create(PlayerCreate(name=name))
		logger.info("Player registered: id=%s name=%s", player.id, player.name)
		return player

	def get(self, player_id: UUID) -> Player:
		if player_id is None:
			raise ValueError("player_id is required")

		player = self.player_storage.get(player_id=player_id)
		logger.info("Founder player %s", player.name)
		return player

	def get_all(self) -> list[PlayerRead]:
		players = self.player_storage.get_all()
		read_players = [self.to_player_read(player) for player in players]
		logger.info("Returning %d players", len(read_players))
		return read_players

	# validations
	def validate_user_exists(self, player_id: UUID) -> None:
		self.get(player_id)

	# mappings
	@staticmethod
	def to_player_read(player: Player) -> PlayerRead:
		return PlayerRead(**player.model_dump())
