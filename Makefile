# Makefile for DealMind

.PHONY: build up down logs shell migrate init_db test

build:
	docker compose build

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

shell:
	docker compose run --rm backend /bin/bash

migrate:
	docker compose run --rm backend bash -lc "alembic upgrade head || true"

init_db:
	docker compose run --rm backend bash -lc "python -m app.utils.manage_db init"

test:
	cd backend && python3 -m unittest -v tests/test_extraction_unittest.py
