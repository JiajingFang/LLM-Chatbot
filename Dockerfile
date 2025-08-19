FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev

COPY llm_api ./llm_api

EXPOSE 8000
CMD ["uvicorn", "llm_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
