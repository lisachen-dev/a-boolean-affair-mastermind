from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.app_context import game_service
from app.models.guess import Guess, GuessCreate, GuessLastResult

router = APIRouter(prefix="/games/{game_id}/guesses", tags=["Guesses"])


@router.post("/", response_model=Guess)
def submit_guess(game_id: UUID, new_guess: GuessCreate) -> Guess:
	return game_service.submit_guess(game_id=game_id, new_guess=new_guess.guess_value)


@router.get("/", response_model=list[Guess])
def get_guess_list(game_id: UUID) -> list[Guess]:
	return game_service.get_all_guesses(game_id=game_id)


@router.get("/last", response_model=Optional[GuessLastResult])
def last_guess_result(game_id: UUID) -> Optional[GuessLastResult]:
	game = game_service.get_game(game_id=game_id)
	if not game.guesses:
		raise HTTPException(status_code=404, detail="No guesses have been made!")
	last_guess = game.guesses[-1]
	return last_guess.to_last_result()
