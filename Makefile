build:
	docker compose -f .devcontainer/docker-compose.yml up -d --build

down:
	docker compose -f .devcontainer/docker-compose.yml down

initial-migration:
	docker compose -f .devcontainer/docker-compose.yml exec api alembic revision --autogenerate -m "Initial migration"

apply-migrations:
	docker compose -f .devcontainer/docker-compose.yml exec api alembic upgrade head

up:
	docker compose -f .devcontainer/docker-compose.yml up -d

load:
	docker compose -f .devcontainer/docker-compose.yml exec api python3 load.py

run-tests:
	docker compose -f .devcontainer/docker-compose.yml exec api pytest

coverage:
	docker exec -it api pytest --cov=apps tests/


init: init-aerich upgrade
restart: down up
