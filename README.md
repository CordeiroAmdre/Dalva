# DALVA

LangChain + FastAPI service for the DALVA project. Includes the **Dalva** chat assistant with optional **read-only** PostgreSQL queries for store operations data (products, sales, stores).

> **Breaking change (v0.3.0)**: The chat endpoint moved from `POST /demo/chat` to **`POST /dalva/chat`**. The old path returns 404.

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- OpenAI API key
- Docker (optional, for PostgreSQL + seed data)

## Setup

```bash
uv sync --dev
cp .env.example .env
# Edit .env: OPENAI_API_KEY=sk-...
```

## Run PostgreSQL (optional, for database-backed answers)

```bash
docker compose up -d postgres
# After adding 03-readonly-role.sql for the first time:
# docker compose down -v && docker compose up -d postgres
```

Enable the SQL agent in `.env`:

```env
DATABASE_QUERIES_ENABLED=true
DATABASE_URL=postgresql+psycopg://pdv_readonly:pdv_readonly@127.0.0.1:5432/pdv_ai
```

## Run the API

```bash
uv run uvicorn dalva_backend.main:app --reload --host 127.0.0.1 --port 8000
```

Interactive docs: http://127.0.0.1:8000/docs

## Try the Dalva chat endpoint

```bash
# General question (LLM only when DB disabled)
curl -s -X POST http://127.0.0.1:8000/dalva/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Say hello in one short sentence."}' | jq

# Data question (with DATABASE_QUERIES_ENABLED=true and Postgres running)
curl -s -X POST http://127.0.0.1:8000/dalva/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Qual o preço do Leite Integral 1L?"}' | jq
```

Response includes `used_database` and `data_sources` when the assistant queried PDV data.

## Run tests

```bash
uv run pytest
```

Tests mock the language model and SQL agent — no API key or Docker required for the default suite.

Optional live database tests: `uv run pytest -m db`

## Project layout

```text
src/dalva_backend/
├── main.py                 # FastAPI app
├── config.py               # Settings (.env)
├── controllers/            # HTTP layer (routes)
├── models/                 # Request/response DTOs (Pydantic)
├── services/               # Business logic
├── repositories/           # LLM + SQL agent + read-only DB access
└── prompts/                # LangChain prompt templates
```

## Feature documentation

- `specs/001-langchain-fastapi-example/` — LangChain + FastAPI starter
- `specs/002-langchain-db-queries/` — Database query access
- `specs/003-rename-dalva/` — Dalva identity rename (plan, quickstart, contracts)
