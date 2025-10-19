MONGO_URI ?= mongodb://localhost:27017

.PHONY: test run

test:
	poetry run pytest

run:
	MONGO_URI=$(MONGO_URI) poetry run uvicorn llm_api.main:app --host 0.0.0.0 --port 8000

docker-compose:
	docker-compose up

docker-compose-down:
	docker-compose down

docker-compose-down-rm:
	docker-compose down --rmi all

frontend:
	cd llm-api-frontend && npm start

frontend-build:
	cd llm-api-frontend && npm run build

frontend-install:
	cd llm-api-frontend && npm install

frontend-dev:
	cd llm-api-frontend && npm run dev

run-mongo-local:
	docker run -d -p 27017:27017 --name mongo mongo:latest