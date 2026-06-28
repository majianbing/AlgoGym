# Worklog

## 2026-06-28

### Repository Context

- Existing repository was minimal: `README.md`, `LICENSE`, `.gitignore`, and an untracked `AGENTS.md`.
- `AGENTS.md` defines AlgoGym as a local-first algorithm training coach using Next.js, FastAPI, SQLite, Chroma, Ollama, and Docker Compose.

### Build Plan

1. Scaffold frontend, backend, Docker Compose, environment files, and docs.
2. Add backend data models and API endpoints.
3. Implement markdown ingestion into Chroma.
4. Add Ollama-compatible RAG services.
5. Build MVP frontend pages and connect them to the backend.
6. Add tests, sample content, and setup documentation.

### Completed

- Created `docs/CHANGELOG.md` and `docs/WORKLOG.md` to keep implementation history visible.
- Created a baseline FastAPI service with health checks, CORS, settings, and SQLite table initialization.
- Added first-pass domain models for documents, training plans, practice sessions, logs, mistakes, pattern mastery, and app settings.
- Added CRUD-style API routers under `/api`.
- Created a baseline Next.js app shell with AlgoGym navigation and dashboard placeholder content.
- Added the first ingestion service: markdown validation, local upload storage, heading-aware chunking, embedding generation, and Chroma persistence.
- Added an Ollama/OpenAI-compatible chat service and coach endpoints for training plans, workouts, and controlled hint levels.
- Wired the Next.js MVP pages to FastAPI with browser-side loading and error states.
- Added focused chunking tests and `docs/samples/binary-search.md` for manual ingestion checks.
- Validation: `python3 -m compileall backend/app` passes; `python3 -m pytest backend/tests` is blocked until backend dependencies are installed locally.
- Docker Compose images built successfully. Startup found host ports `3000` and `3001` already allocated, so the frontend mapping was changed to `3123:3000`.
- The frontend build warned that `next@15.1.4` has a critical advisory. `npm view next version` returned `16.2.9`, so Next-related packages were updated to that version.

### Realignment To Updated AGENTS.md

- Re-read the expanded `AGENTS.md` and shifted implementation toward the specified API contract and acceptance criteria.
- Stopped running containers before restructuring.
- Replaced the backend persistence layer with SQLAlchemy models for problems, sessions, streaks, documents, weak patterns, and settings.
- Added `seeds/curriculum.json` and automatic seed loading for a functional app before RAG is configured.
- Added required endpoints for documents, plan, today, sessions, hints, review, stats, and settings.
- Switched markdown chunking to `##` section boundaries and added review scheduling logic.
- Switched frontend dependencies to Next.js 14 and Tailwind CSS, then added required routes: `/dashboard`, `/knowledge-base`, `/plan`, `/session`, `/review`, and `/settings`.
- First Compose startup after the switch found that Next.js 14 does not support `next.config.ts`; config was converted to `next.config.js`.
- Initial Docker pytest run collected no tests because `backend/tests` was not copied into the image; backend Dockerfile was updated to include tests.
- `npm run lint` initially prompted for interactive ESLint setup; added `frontend/.eslintrc.json` extending `next/core-web-vitals`.

### Validation

- `docker compose build` completed for backend and frontend.
- `docker compose up -d` starts backend, frontend, and ChromaDB.
- `docker compose exec backend python -m pytest` passes 5 tests.
- `docker compose exec frontend npm run typecheck` passes.
- `docker compose exec frontend npm run lint` passes.
- Smoke checks return HTTP 200 for `/health`, `/api/stats`, `/api/today`, `/api/plan`, `/api/review`, `/api/settings`, and frontend `/dashboard`.
