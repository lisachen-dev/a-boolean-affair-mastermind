# A Boolean Affair 💃✨
True. False. It’s complicated.

> This relationship is strictly conditional.

---

## Table of Contents


---

## What is this?
A FastAPI backend that implements the mastermind-style code‑breaking game with clean, testable logic and REST endpoints.

---

## Quickstart
If you already have `uv` and `make` installed:

```bash
uv sync     # Install dependencies from pyproject.toml
make run    # Start the project

Open docs:
# Swagger UI:   http://127.0.0.1:8000/docs
# ReDoc:        http://127.0.0.1:8000/redoc
```
**No Make? Here's a fallback command to get the application started:**

    uv run uvicorn app.main:app --reload

---

## First Time Setup

### Install `uv`
`uv` handles Python installation, virtual environments and dependency management.

**Windows (Powershell)**

    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"


macOS and Linux

    curl -LsSf https://astral.sh/uv/install.sh | sh

### Install `make`
Task runner for common scripts

**Mac:** 
You may need Xcode Command Line Tools:

    xcode-select --install

**Windows (CMD/Powershell):*** 
1. **Install [Chocolatey](https://chocolatey.org/install#:~:text=Install%20Chocolatey%20for%20Individual%20Use%3A)** (Windows package manager)
2. In PowerShell (as Administrator):
    ```
    choco install make
    ```
3. Verify Installation
    ```
    make --version
    ```

### Config

[//]: # (TODO: env variables?) 

Install dependencies

    uv sync

Run
```bash
make run
# or: uv run uvicorn app.main:app --reload
```

---

## API Reference

---

## How I'd Improve this

---

## Screenshots

---

## Credits

---

## Troubleshooting

### Managing Dependencies
Adding dependencies to the pyproject.toml

    uv add 'requests==2.31.0'

Remove a package

    uv remove requests

For more, visit [Astral's documentation for `uv`](https://docs.astral.sh/uv/guides/projects/#creating-a-new-project)
