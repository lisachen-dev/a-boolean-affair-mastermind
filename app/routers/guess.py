from uuid import UUID

from fastapi import APIRouter

from app.models.guess import GuessCreate

router = APIRouter(prefix="/games", tags=["Guesses"])


@router.post("/{game_id}/guesses")
def create_guess(game_id: UUID, new_guess: GuessCreate):
	pass


@router.get("/{game_id}/guesses")
def get_guess_list(game_id: UUID):
	pass
