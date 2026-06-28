# AlgoGym

AlgoGym is a local-first AI algorithm training coach. It helps users build a daily practice habit with uploaded pattern notes, RAG-generated training plans, daily workouts, streak tracking, mistake review, and tiered hints.

## Stack

- Frontend: Next.js 14 + TypeScript + Tailwind CSS
- Backend: FastAPI + Python 3.11
- Database: SQLite via SQLAlchemy
- Vector database: ChromaDB
- RAG: LangChain-ready services using local Chroma context
- Local LLM: Ollama through an OpenAI-compatible API
- Packaging: Docker Compose

## Repository Layout

```text
backend/      FastAPI app and RAG services
frontend/     Next.js TypeScript app
docs/         Changelog and implementation worklog
seeds/        Default 6-week curriculum
data/         Local runtime data, ignored by Git
```

## Local Development

Copy the environment template before running services:

```bash
cp .env.example .env
```

Run the backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run the frontend:

```bash
cd frontend
npm install
npm run dev
```

Or run both with Docker Compose:

```bash
docker compose up --build
```

The backend API is available at `http://localhost:8000`; Docker Compose exposes the frontend at `http://localhost:3123`.

MVP pages:

- `http://localhost:3123/dashboard`
- `http://localhost:3123/knowledge-base`
- `http://localhost:3123/plan`
- `http://localhost:3123/session`
- `http://localhost:3123/review`
- `http://localhost:3123/settings`

## Ollama Setup

AlgoGym expects an OpenAI-compatible Ollama endpoint. Install/pull models locally before using ingestion or coaching:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

The default API base URL is `http://localhost:11434/v1`.

## Useful Commands

```bash
cd backend && python3 -m compileall app
cd backend && pytest
cd frontend && npm run typecheck
cd frontend && npm run lint
```

## Sample Data

Use `docs/samples/binary-search.md` on the Knowledge Base page to test markdown upload and retrieval.

## Screenshot Placeholders

- Dashboard: add screenshot after first stable UI pass.
- Knowledge Base: add upload and ingestion screenshot.
- Session: add timer and hint workflow screenshot.
