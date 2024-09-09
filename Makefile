DC = docker compose
PROD = ./docker-compose.production.yml

lint:
	mypy ./app
	flake8 ./app
tests:
	pytest -v

cock:
	gcc -Wall -Werror -o test ./*.c -lm; ./test; rm test

.PHONY: lint tests
