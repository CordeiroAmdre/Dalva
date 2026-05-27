# DALVA

LangChain + FastAPI service for the DALVA project. Includes the **Dalva** chat assistant with optional **read-only** DuckDB queries for store operations data (products, sales, stores).

> **Breaking change (v0.3.0)**: The chat endpoint moved from `POST /demo/chat` to **`POST /dalva/chat`**. The old path returns 404.

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- OpenAI API key

## Setup

```bash
uv sync --dev
cp .env.example .env
# Edit .env: OPENAI_API_KEY=sk-...
```

## Initialize DuckDB (optional, for database-backed answers)

Static PDV data (categories, products, stores, **sales**, etc.) lives in **`docker/duckdb/parquet/`** as Parquet files. `init_db` loads everything into DuckDB via `read_parquet()`.

```bash
# Regenerate Parquet files after editing seed data (optional)
uv run python -m dalva_backend.scripts.build_parquet

# Create the DuckDB database file
uv run python -m dalva_backend.scripts.init_db
```

Enable the SQL agent in `.env`:

```env
DATABASE_QUERIES_ENABLED=true
DATABASE_URL=duckdb:///./data/pdv_ai.duckdb
```

To reset the database:

```bash
rm -f data/pdv_ai.duckdb
uv run python -m dalva_backend.scripts.init_db
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

# Data question (with DATABASE_QUERIES_ENABLED=true and init_db completed)
curl -s -X POST http://127.0.0.1:8000/dalva/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Qual o preço do Leite Integral 1L?"}' | jq
```

Response includes `used_database` and `data_sources` when the assistant queried PDV data.

## Run tests

```bash
uv run pytest
```

Tests mock the language model and SQL agent — no API key or DuckDB file required for the default suite.

Optional live DuckDB tests: `uv run pytest -m db`

## Project layout

```text
src/dalva_backend/
├── main.py                 # FastAPI app
├── config.py               # Settings (.env)
├── scripts/init_db.py      # DuckDB schema + seed loader
├── controllers/            # HTTP layer (routes)
├── models/                 # Request/response DTOs (Pydantic)
├── services/               # Business logic
├── repositories/           # LLM + SQL agent + read-only DB access
└── prompts/                # LangChain prompt templates

docker/duckdb/
├── init/01-schema.sql      # Table definitions
└── parquet/                # Static seed data (Parquet)
    ├── categorias.parquet
    ├── produtos.parquet
    ├── vendas.parquet
    ├── itens_venda.parquet
    └── ...

data/pdv_ai.duckdb          # Created by init_db (gitignored)
```

## Feature documentation

- `specs/001-langchain-fastapi-example/` — LangChain + FastAPI starter
- `specs/002-langchain-db-queries/` — Database query access
- `specs/003-rename-dalva/` — Dalva identity rename
- `specs/005-duckdb-database/` — DuckDB storage migration
