DC = docker compose
DEV = docker-compose.yml
PROD = docker-compose.prod.yml

dev:
	$(DC) -f $(DEV) up -d --build

prod:
	$(DC) -f $(PROD) up -d --build

down:
	$(DC) -f $(DEV) -f $(PROD) down

logs:
	$(DC) -f $(DEV) -f $(PROD) logs | tail -50
