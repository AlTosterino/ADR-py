PROJECT_PATH = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
SRC_PATH = src
TESTS_PATH = tests
LINT_PATHS = \
$(SRC_PATH) \
$(TESTS_PATH)

lint:
	poetry run autoflake --in-place --recursive --ignore-init-module-imports --remove-duplicate-keys --remove-unused-variables --remove-all-unused-imports $(LINT_PATHS)
	poetry run isort $(LINT_PATHS)
	poetry run black $(LINT_PATHS)
	poetry run mypy $(LINT_PATHS)

lint-ci:
	poetry run autoflake --check --recursive --ignore-init-module-imports --remove-duplicate-keys --remove-unused-variables --remove-all-unused-imports $(LINT_PATHS)
	poetry run isort --check-only $(LINT_PATHS)
	poetry run black --check $(LINT_PATHS)
	poetry run mypy $(LINT_PATHS)

test:
	poetry run pytest