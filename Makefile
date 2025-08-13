

install:
	uv sync
run:
	uv run uvicorn app.main:app --reload

lint:
	uv run ruff check .


# I: sort imports
# F401: remove unused imported
# --fix: auto format per ruff configurations
format:
	uv run ruff format .
	uv run ruff check . --select I,F401 --fix

debug:
	uv run uvicorn app.main:app --reload --log-level debug
