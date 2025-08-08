install:
	uv sync
run:
	uv run uvicorn app.main:app --reload

lint:
	uv run ruff check .

format:
	uv run ruff format .
	uv run ruff check . --select I --fix

