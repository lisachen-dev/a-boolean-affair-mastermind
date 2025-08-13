from app.models.game import Game, GameRead
from app.models.guess import Guess, GuessLastResult, GuessRead
from app.models.player import Player, PlayerRead


def to_player_read(player: Player) -> PlayerRead:
	return PlayerRead(**player.model_dump())


def to_game_read(game: Game) -> GameRead:
	attempts_made = len(game.guesses)
	attempts_left = max(game.max_guesses - attempts_made, 0)

	last_guess = game.guesses[-1] if game.guesses else None
	last_guess_result = last_guess.to_last_result() if last_guess else None

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
