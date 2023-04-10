PROJECT_PATH = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
SRC_PATH = src
TESTS_PATH = tests
LINT_PATHS = \
$(SRC_PATH) \
$(TESTS_PATH)

lint:
	poetry run black $(LINT_PATHS)
	poetry run ruff check $(LINT_PATHS) --fix
	poetry run mypy $(LINT_PATHS)

lint-ci:
	poetry run black --check $(LINT_PATHS)
	poetry run ruff check $(LINT_PATHS)
	poetry run mypy $(LINT_PATHS)

test:
	poetry run pytest