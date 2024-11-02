all: type-check lint style-check test

type-check:
	mypy src

lint:
	ruff check src

style-check:
	ruff format --check src

test:
	pytest src --cov signer \
		-W ignore::cryptography.utils.CryptographyDeprecationWarning
