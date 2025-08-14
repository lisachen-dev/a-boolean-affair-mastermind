import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse, RedirectResponse

from app.routers import game, guess, player

# --- env + logging ---
load_dotenv()
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
	level=getattr(logging, LOG_LEVEL, logging.INFO),
	format="%(asctime)s [%(levelname)s - %(name)s] --- %(message)s",
	force=True,
)
logger = logging.getLogger(__name__)
logger.info("You have now started A Boolean Affair!")

# --- app setup ---

app = FastAPI(
	title="A Boolean Affair",
	version="0.1.0",
	description="""
	
### True. False. It’s complicated.
> #### This relationship is strictly conditional.

### How It Works:
- **Players**: Create a player profile first.
- **Games**: Start a game with your desired rules or defaults.
- **Guesses**: Try to break the secret code within the allowed number of guesses.

Use the sections below to interact with the API directly.
""",
	openapi_tags=[
		{"name": "Players", "description": "Manage player profiles."},
		{"name": "Games", "description": "Start and manage games."},
		{"name": "Guesses", "description": "Submit and view guesses."},
	],
)


# --- Validation Mapping
@app.exception_handler(RequestValidationError)
def request_validation_400(_request: Request, exc: RequestValidationError):
	"""Map Pydantic validation to 400"""
	logger.debug("Request validation failed: %s", exc.errors())
	return JSONResponse(status_code=400, content={"detail": exc.errors()})


@app.exception_handler(ValueError)
def value_error_400(_request: Request, exc: ValueError):
	"""Map domain validation to 400"""
	return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(KeyError)
def key_error_404(_request: Request, exc: KeyError):
	"""Missing resource -> 404"""
	return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(Exception)
def internal_error_500(_request: Request, exc: Exception):
	"""Catch‑all 500"""
	logger.exception("Unhandled server error: %s", exc)
	return JSONResponse(
		status_code=500, content={"detail": "An unexpected error occurred. Please try again later."}
	)


# --- router access ---
app.include_router(game.router)
app.include_router(player.router)
app.include_router(guess.router)


# --- root redirect to Swagger ---
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
	logger.info("Redirecting to Swagger UI")
	return RedirectResponse(url="/docs")
