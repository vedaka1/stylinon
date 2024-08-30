DC = docker compose
PROD = ./docker-compose.production.yml

lint:
	mypy ./app
	flake8 ./app
tests:
	pytets -v
.PHONY: lint