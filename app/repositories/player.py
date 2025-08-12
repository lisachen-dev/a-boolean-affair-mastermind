import logging
from uuid import UUID

from app.models.player import Player, PlayerCreate

logger = logging.getLogger(__name__)


class PlayerStorage:
	def __init__(self) -> None:
		self.players: dict[UUID, Player] = {}

	def create(self, player_create: PlayerCreate) -> Player:
		player = Player(name=player_create.name)

		self.players[player.id] = player
		logger.info(
			"The following player has been registered:\n id: %s\n name: %s",
			player.id,
			player.name,
		)
		return player

	def get(self, player_id: UUID) -> Player:
		if player_id not in self.players:
			raise KeyError("Player does not exist")

		logger.info("Found %s!", self.players[player_id].name)
		return self.players[player_id]
