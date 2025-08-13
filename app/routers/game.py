import logging
from uuid import UUID

from fastapi import APIRouter

from app.app_context import game_service
from app.models.game import GameCreate, GameRead
from app.utils.mappers import to_game_read

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/games", tags=["Games"])


@router.post("/", response_model=GameRead)
def start_game(new_game: GameCreate):
	game = game_service.start_game(new_game)

	return to_game_read(game=game)


@router.get("/", response_model=list[GameRead])
def get_all_games():
	games = game_service.get_all_games()
	return [to_game_read(game) for game in games]


@router.get("/{game_id}", response_model=GameRead)
def get_game(game_id: UUID) -> GameRead:
	game = game_service.get_game(game_id)
	return to_game_read(game)
