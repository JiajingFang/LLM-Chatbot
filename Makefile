.PHONY: test run

test:
	poetry run pytest

run:
	poetry run uvicorn llm_api.main:app --host 0.0.0.0 --port 8000

docker-compose:
	docker-compose up

docker-compose-down:
	docker-compose down

docker-compose-down-rm:
	docker-compose down --rmi all