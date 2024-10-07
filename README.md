## Setup variables in .env
```python
# Database
POSTGRES_USER=username
POSTGRES_PORT=5432
POSTGRES_PASSWORD=
POSTGRES_HOST=postgres
POSTGRES_DB=stylinon

#JWT keys
PRIVATE_KEY=
PUBLIC_KEY=

# Acquiring
TOCHKA_TOKEN=
ACQUIRING_PUBLIC_KEY=

# SMTP
SMTP_PASSWORD=
SMTP_HOST=
SMTP_PORT=
SMTP_EMAIL=
SMTP_SENDER_NAME=
```

## How to run

### Development
- Run `make dev` or `docker compose up -d --build`

### Production
- Run `make prod` or `docker compose -f docker-compose.production.yml up -d --build`
