import logging
from uuid import UUID

from fastapi import APIRouter

from app.app_context import game_service
from app.models.game import GameCreate, GameView

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/games", tags=["Games"])


@router.post("/", response_model=GameView)
def start_game(new_game: GameCreate) -> GameView:
	game = game_service.start_game(new_game)
	logger.debug("before GameView")
	return GameView.from_game(game)


@router.get("/", response_model=list[GameView])
def get_all_games() -> list[GameView]:
	games = game_service.get_all_games()
	return [GameView.from_game(game) for game in games]


@router.get("/{game_id}", response_model=GameView)
def get_game(game_id: UUID) -> GameView:
	game = game_service.get_game(game_id)
	return GameView.from_game(game)
