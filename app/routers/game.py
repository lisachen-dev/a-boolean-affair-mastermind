from uuid import UUID

from fastapi import APIRouter

from app.app_context import game_service
from app.models.game import GameCreate, GameRead
from app.models.guess import GuessCreate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/games", tags=["games"])


@router.post("/", response_model=GameRead)
def start_game(new_game: GameCreate):
	game = game_service.start_game(new_game)
	logger.debug("start_game -> %r", game)
	return game_service.to_game_read(game=game)


@router.get("/", response_model=list[GameRead])
def get_all_games():
	return game_service.get_all_games()


@router.get("/{game_id}", response_model=GameRead)
def get_game(game_id: UUID) -> GameRead:
	return game_service.get_game(game_id)


# guess routes
@router.post("/{game_id}/guesses")
def create_guess(game_id: UUID, new_guess: GuessCreate):
	pass


@router.get("/{game_id}/guesses")
def get_guess_list(game_id: UUID):
	pass
