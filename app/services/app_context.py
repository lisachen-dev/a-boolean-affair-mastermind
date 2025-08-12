from app.constants import IS_EXTERNAL_CODE
from app.repositories.game import GameStorage
from app.repositories.player import PlayerStorage
from app.services.game import GameService
from app.services.random import RandomService

game_storage = GameStorage()
player_storage = PlayerStorage()
random_service = RandomService(external_code=IS_EXTERNAL_CODE)

game_service = GameService(
	game_storage=game_storage, random_service=random_service, player_storage=player_storage
)
