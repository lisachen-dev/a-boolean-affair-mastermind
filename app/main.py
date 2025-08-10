import logging

from fastapi import FastAPI
from starlette.responses import RedirectResponse

logger = logging.getLogger(__name__)
logging.basicConfig(
	level=logging.DEBUG
)  # DEBUG, INFO, WARNING, ERROR, CRITICAL (order of filtered views)
logger.info("-------You have now started A Boolean Affair!")

app = FastAPI(title="A Boolean Affair")


# Root Route redirects to Swagger docs
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
	logger.info("-------Redirecting to Swagger UI")
	return RedirectResponse(url="/docs")
