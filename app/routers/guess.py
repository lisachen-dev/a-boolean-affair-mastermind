from fastapi import HTTPException
from typing import Optional
from uuid import UUID

from fastapi import APIRouter

from app.app_context import game_service
from app.models.guess import GuessCreate, GuessLastResult, GuessRead
from app.utils.mappers import to_guess_last_result, to_guess_read

router = APIRouter(prefix="/games/{game_id}/guesses", tags=["Guesses"])


@router.post("/", response_model=GuessRead)
def submit_guess(game_id: UUID, new_guess: GuessCreate) -> GuessRead:
	guess = game_service.submit_guess(game_id=game_id, new_guess=new_guess.guess_value)
	return to_guess_read(guess)


@router.get("/", response_model=list[GuessRead])
def get_guess_list(game_id: UUID) -> list[GuessRead]:
	guesses = game_service.get_all_guesses(game_id=game_id)
	return [to_guess_read(guess) for guess in guesses]


@router.get("/last", response_model=Optional[GuessLastResult])
def last_guess_result(game_id: UUID) -> Optional[GuessLastResult]:
	game = game_service.get_game(game_id=game_id)
	if not game.guesses:
		raise HTTPException(status_code=404, detail="No guesses have been made!")
	return to_guess_last_result(game.guesses[-1])
