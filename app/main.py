from fastapi import FastAPI
from starlette.responses import RedirectResponse
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()


# Root Route redirects to Swagger docs
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
	logger.debug('this is a debug message')
	return RedirectResponse(url="/docs")
