all: type-check lint style-check

type-check:
	mypy src

lint:
	ruff check src

style-check:
	ruff format --check src
