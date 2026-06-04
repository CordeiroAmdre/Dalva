# DALVA

LangChain + FastAPI service for the DALVA project. Includes the **Dalva** chat assistant with optional **read-only** database queries for store operations data (products, sales, stores), plus a **React chat frontend** for conversational access to your data.

> **Breaking change (v0.3.0)**: The chat endpoint moved from `POST /demo/chat` to **`POST /dalva/chat`**. The old path returns 404.

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- Node.js 20+ and npm (frontend)
- OpenAI API key

## Setup (backend)

```bash
cd backend
uv sync --dev
cp .env.example .env
# Edit .env: OPENAI_API_KEY=sk-...
```

Enable database-backed answers in `backend/.env`:

```env
DATABASE_QUERIES_ENABLED=true
DATABASE_URL=duckdb:///../data/pdv_ai.duckdb
DATABASE_SCHEMA=pdv
```

Initialize DuckDB (schema + seed; uses repo-root `docker/` and `data/`):

```bash
cd backend
uv run python -m dalva_backend.scripts.init_db
```

## Run the API

```bash
cd backend
uv run uvicorn dalva_backend.main:app --reload --host 127.0.0.1 --port 8000
```

Interactive docs: http://127.0.0.1:8000/docs

## Run the chat frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open: http://localhost:5173

See [specs/006-dalva-chat-frontend/quickstart.md](specs/006-dalva-chat-frontend/quickstart.md) for the full walkthrough.

## Try the Dalva chat endpoint (curl)

```bash
curl -s -X POST http://127.0.0.1:8000/dalva/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Qual o preço do Leite Integral 1L?"}' | jq
```

Response includes `reply`, `model`, `used_database`, `data_sources`, and optional `chart` when query results support visualization.

## Run tests

Backend:

```bash
cd backend && uv run pytest
```

Frontend:

```bash
cd frontend && npm test
```

Tests mock the language model, SQL agent, and HTTP API — no API key required for the default suites.

## Project layout

```text
backend/
├── pyproject.toml
├── src/dalva_backend/
│   ├── main.py               # FastAPI app + CORS
│   ├── controllers/          # HTTP layer (routes)
│   ├── models/               # Request/response DTOs
│   ├── services/             # ChatService, ChartBuilder
│   ├── repositories/         # LLM + SQL agent + read-only DB
│   └── prompts/              # LangChain prompt templates
└── tests/

frontend/
├── src/
│   ├── pages/ChatPage.tsx    # Ant Design chat UI + ECharts
│   ├── hooks/useChatSession.ts
│   └── services/dalvaApi.ts

data/                         # DuckDB (repo root, generated)
docker/duckdb/                # Seed SQL + Parquet (repo root)
```

## Feature documentation

- `specs/009-separate-fe-be-modules/` — Backend/frontend module layout
- `specs/006-dalva-chat-frontend/` — React chat frontend (plan, quickstart, contracts)
- `specs/002-langchain-db-queries/` — Database query access
- `specs/003-rename-dalva/` — Dalva identity rename
