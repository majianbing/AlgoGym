# Changelog

All notable project changes are recorded here as the repository evolves.

## 2026-06-28

- Started the AlgoGym implementation from the local-first MVP brief in `AGENTS.md`.
- Planned a staged build covering project scaffolding, FastAPI backend, SQLite models, Chroma ingestion, Ollama-backed RAG, Next.js UI pages, Docker Compose, and tests.
- Added the initial monorepo scaffold with `backend/`, `frontend/`, `docs/`, Docker Compose, and `.env.example`.
- Added FastAPI SQLite models and API routers for dashboard data, documents, training plans, practice sessions, review items, mastery, and settings.
- Added markdown upload, UTF-8 file storage, markdown chunking, Ollama/OpenAI-compatible embeddings, and Chroma upsert support.
- Added coach services and endpoints for RAG-backed plan generation, workout generation, and tiered hints that avoid full solutions by default.
- Wired frontend pages to backend APIs and added initial chunking tests plus a sample binary-search markdown document.
- Adjusted Docker defaults so the backend container calls Ollama through `host.docker.internal`.
- Changed the Compose frontend host port to `3123` after `3000` and `3001` were already allocated locally.
- Updated Next.js and `eslint-config-next` from `15.1.4` to `16.2.9` after the Docker build reported a critical advisory.
- Realigned the project to the updated `AGENTS.md`: Next.js 14, Tailwind, Python 3.11, SQLAlchemy entities, required `/api` contract, `##` markdown chunking, seed curriculum, and review scheduling tests.
- Verified Docker Compose startup, backend tests, frontend lint/typecheck, and key API/frontend smoke checks.
