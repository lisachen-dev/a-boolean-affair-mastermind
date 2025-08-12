from uuid import UUID

from fastapi import APIRouter

from app.models.game import GameCreate, GameRead
from app.models.guess import GuessCreate
from app.services.game import start_game

router = APIRouter(prefix="/games", tags=["games"])


@router.post("/", response_model=GameRead)
def start_game(create: GameCreate):
	# game = game_service.start_game(create)
	# return game  # _secret isn't part of model_dump
	pass


@router.get("/{game_id}")
def get_game(game_id: UUID):
	pass


# guess routes
@router.get("/{game_id}/guesses")
def get_guess_list(game_id: UUID):
	pass


@router.post("/{game_id}/guesses")
def create_guess(game_id: UUID, new_guess: GuessCreate):
	pass
