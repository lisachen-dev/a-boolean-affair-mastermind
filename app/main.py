import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.responses import RedirectResponse

load_dotenv()
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logger = logging.getLogger(__name__)
logging.basicConfig(
	level=getattr(logging, LOG_LEVEL, logging.INFO),
	format="%(asctime)s [%(levelname)s - %(name)s] --- %(message)s",
)
logger.info("You have now started A Boolean Affair!")

app = FastAPI(title="A Boolean Affair")


# Root Route redirects to Swagger docs
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
	logger.info("Redirecting to Swagger UI")
	return RedirectResponse(url="/docs")
