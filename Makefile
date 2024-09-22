type-check:
	mypy src

lint:
	ruff check src

style-check:
	ruff format --check src
