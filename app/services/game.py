import logging

from app.constants import (
	ALLOW_REPEATS,
	CODE_LENGTH,
	IS_EXTERNAL_CODE,
	MAX_GUESSES,
	MAX_VALUE,
	MIN_VALUE,
)
from app.models.game import GameCreate
from app.repositories.game import GameStorage
from app.services.random import RandomService

logger = logging.getLogger(__name__)


def resolve_rules(game_create: GameCreate) -> dict:
	rules: dict[str, int | bool] = {
		"code_length": game_create.code_length is not None or CODE_LENGTH,
		"max_guesses": game_create.max_guesses is not None or MAX_GUESSES,
		"max_value": game_create.max_value is not None or MAX_VALUE,
		"min_value": game_create.min_value is not None or MIN_VALUE,
		"allow_repeats": game_create.allow_repeats is not None or ALLOW_REPEATS,
	}
	return rules


def start_game(game_create: GameCreate):
	# resolve rules
	rules = resolve_rules(game_create=game_create)

	# generate secret code
	random_service = RandomService(external_code=IS_EXTERNAL_CODE)
	secret_code = random_service.generate_secret_code(
		code_length=game_create.code_length or CODE_LENGTH,
		min_value=MIN_VALUE,
		max_value=MAX_VALUE,
		allow_repeats=ALLOW_REPEATS,
	)

	# generate storage instance
	# create players
	# create game

	# game loop
	# take turn
	# create guess
	# evaluate guess
	# end game MAX_GUESSES reached or player guessed correctly

	pass
