from app.constants import IS_EXTERNAL_CODE
from app.repositories.game import GameStorage
from app.repositories.player import PlayerStorage
from app.services.game import GameService
from app.services.player import PlayerService
from app.services.random import RandomService

# repositories
_game_storage = GameStorage()
_player_storage = PlayerStorage()

# services
random_service = RandomService(external_code=IS_EXTERNAL_CODE)
player_service = PlayerService(player_storage=_player_storage)
game_service = GameService(
	game_storage=_game_storage, random_service=random_service, player_service=player_service
)
