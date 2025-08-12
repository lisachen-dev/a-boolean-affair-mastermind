

install:
	uv sync
run:
	uv run uvicorn app.main:app --reload

lint:
	uv run ruff check .

format:
	uv run ruff format .					# code style auto-format
	uv run ruff check . --select I --fix	# lint imports and auto fixes

debug:
	uv run uvicorn app.main:app --reload --log-level debug
