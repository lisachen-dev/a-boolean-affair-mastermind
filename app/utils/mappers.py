from app.models.game import Game, GameRead
from app.models.guess import Guess, GuessLastResult, GuessRead
from app.services.game import GameService


def to_game_read(game: Game) -> GameRead:
	attempts_made = len(game.guesses)
	attempts_left = max(game.max_guesses - attempts_made, 0)

	last_guess_result = to_guess_last_result(guess=game.guesses[len(game.guesses) - 1])

	return GameRead(
		**game.model_dump(
			include={
				"id",
				"player_id",
				"status",
				"code_length",
				"max_guesses",
				"min_value",
				"max_value",
				"allow_repeats",
				"finished_at",
			}
		),
		attempts_made=attempts_made,
		attempts_left=attempts_left,
		last_result=last_guess_result,
	)


def to_guess_last_result(guess: Guess) -> GuessLastResult:
	return GuessLastResult(
		**guess.model_dump(
			include={
				"guess_value",
				"exact_matches",
				"partial_matches",
				"created_at",
			}
		)
	)


def to_guess_read(guess: Guess) -> GuessRead:
	return GuessRead(
		**guess.model_dump(
			include={
				"id",
				"game_id",
				"guess_value",
				"exact_matches",
				"partial_matches",
				"created_at",
			}
		)
	)
