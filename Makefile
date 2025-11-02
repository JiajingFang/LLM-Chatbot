MONGO_URI ?= mongodb://localhost:27017

.PHONY: test run

test:
	poetry run pytest

run-mongo-local:
	docker run -d -p 27017:27017 --name mongo mongo:latest

stop-mongo-local:
	docker stop mongo && docker rm mongo

run-local:
	MONGO_URI=$(MONGO_URI) poetry run uvicorn llm_api.main:app --host 0.0.0.0 --port 8000

docker-compose:
	docker-compose up -d

docker-compose-down:
	docker-compose down

docker-compose-down-clean-all:
	docker-compose down -v --rmi all

docker-logs-backend:
	docker-compose logs -f llm-api

docker-logs-mongo:
	docker-compose logs -f mongodb

docker-logs-frontend:
	docker-compose logs -f frontend


frontend:
	cd llm-api-frontend && npm start

frontend-build:
	cd llm-api-frontend && npm run build

frontend-install:
	cd llm-api-frontend && npm install

frontend-dev:
	cd llm-api-frontend && npm run dev