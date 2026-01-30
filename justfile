set shell := ["bash", "-eu", "-o", "pipefail", "-c"]
set dotenv-load := true

VENV_DIR := ".venv"
BUILD_DIR := "build"
DIST_DIR := "dist"
CACHE_DIR := ".cache"

default:
    @just --list

venv:
    @uv venv {{ VENV_DIR }}

sync:
    @uv sync --all-groups --all-extras

setup: venv sync

clean:
    @find -type d -name "{{ DIST_DIR }}" -exec rm -rf {} +
    @find -type d -name "{{ BUILD_DIR }}" -exec rm -rf {} +
    @find -type d -name "{{ CACHE_DIR }}" -exec rm -rf {} +
    @find -type d -name "__pycache__" -exec rm -rf {} +
    @find -type d -name "*.egg-info" -exec rm -rf {} +
    @find -type f -name ".coverage" -exec rm -rf {} +
    @find -type f -name "*,cover" -exec rm -rf {} +
    @find -type f -name "*~" -exec rm -rf {} +
    @find -type f -name "*.egg" -exec rm -rf {} +


upgrade:
    @uv lock --upgrade

test:
    @uv run --group="test" pytest

lint:
    @uv run --group="lint" ty check
    @uv run --group="lint" ruff check --show-fixes --preview
    @uv run --group="lint" ruff format --preview --check

fmt:
    @uv run --group="lint" ruff format --preview

check: fmt lint test
