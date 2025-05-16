PROJECT_PATH = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
SRC_PATH = src
TESTS_PATH = tests
LINT_PATHS = \
	$(SRC_PATH) \
	$(TESTS_PATH)

sync-deps:
	uv sync --frozen --active

update-deps:
	uv lock  --active

lint:
	uv run --active black $(LINT_PATHS)
	uv run --active ruff check $(LINT_PATHS) --fix
	uv run --active mypy $(LINT_PATHS)

lint-ci:
	uv run --active black --check $(LINT_PATHS)
	uv run --active ruff check $(LINT_PATHS)
	uv run --active mypy $(LINT_PATHS)

test:
	uv run --active pytest -s
