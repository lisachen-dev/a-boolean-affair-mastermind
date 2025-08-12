from uuid import UUID

from fastapi import APIRouter

from app.models.game import GameCreate, GameRead
from app.models.guess import GuessCreate

router = APIRouter(prefix="/games", tags=["games"])


@router.post("/", response_model=GameRead)
def start_game(new_game: GameCreate):
	# game = game_service.start_game(create)
	# return game  # _secret isn't part of model_dump
	pass


@router.get("/{game_id}")
def get_game(game_id: UUID):
	pass


# guess routes
@router.post("/{game_id}/guesses")
def create_guess(game_id: UUID, new_guess: GuessCreate):
	pass


@router.get("/{game_id}/guesses")
def get_guess_list(game_id: UUID):
	pass
