DC = docker compose
PROD = ./docker-compose.production.yml

lint:
	mypy ./app
	flake8 ./app

.PHONY: lint