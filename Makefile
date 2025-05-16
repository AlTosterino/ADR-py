PROJECT_PATH = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
SRC_PATH = src
TESTS_PATH = tests
LINT_PATHS = \
	$(SRC_PATH) \
	$(TESTS_PATH)

sync-deps:
	uv sync --active

update-deps:
	uv lock

lint:
	black $(LINT_PATHS)
	ruff check $(LINT_PATHS) --fix
	mypy $(LINT_PATHS)

lint-ci:
	black --check $(LINT_PATHS)
	ruff check $(LINT_PATHS)
	mypy $(LINT_PATHS)

test:
	pytest -s
