Build a local-first open-source web app called AlgoGym.

GOAL:
AlgoGym is an AI algorithm training coach that helps users build a 
daily algorithm practice habit, like Duolingo streaks but for coding interviews.

PROJECT STRUCTURE:
algogym/
  frontend/        # Next.js 14 + TypeScript + Tailwind
  backend/         # FastAPI + Python
  docker-compose.yml
  README.md

CORE FEATURES:
1. Upload markdown documents about algorithmic patterns
2. Ingest documents into ChromaDB (chunk by ## sections, embed with Ollama nomic-embed-text)
3. Use RAG to generate customized training plans and AI hints
4. Daily workout structure: warm-up (Easy), main (Medium), review (retry mistakes), reflection
5. Track streaks, practice logs, time spent, mistakes, and pattern mastery per user
6. AI hints in 3 levels:
   - Level 1: trigger keyword only (e.g. "think sliding window")
   - Level 2: pattern name + high-level approach
   - Level 3: pseudocode only
   Never show working code unless user explicitly clicks "Unlock Solution"

TECH STACK:
- Frontend: Next.js 14, TypeScript, Tailwind CSS
- Backend: FastAPI, Python 3.11
- DB: SQLite (via SQLAlchemy)
- Vector DB: ChromaDB (local)
- LLM: Ollama (default model: llama3.2, OpenAI-compatible interface)
- RAG: LangChain
- Packaging: Docker Compose

DATABASE ENTITIES:
- problems (id, title, leetcode_url, pattern, difficulty, week, day)
- sessions (id, date, problem_id, status, time_spent_mins, notes, hint_level_used)
- streaks (current_streak, longest_streak, last_active_date)
- documents (id, filename, content, chunked, embedded, created_at)

MVP PAGES:
- /dashboard — streak, today's problems, quick stats
- /knowledge-base — upload markdown docs, view ingested documents
- /plan — 6-week curriculum view, progress per week
- /session — active practice session with timer, hint system, status tracking
- /review — mistakes log, pattern weakness analysis
- /settings — Ollama model, API keys, preferences

SEED DATA:
Include a seeds/curriculum.json with a default 6-week plan.
Week 1: Arrays & HashMap
Week 2: Stack, Prefix Sum, Linked List
Week 3: Binary Tree
Week 4: Graphs & Dijkstra
Week 5: Dynamic Programming & Greedy
Week 6: Backtracking, Heap, Trie, Binary Search

DESIGN PRINCIPLES:
- Local-first, single user, no auth required for MVP
- Clean minimal UI (dark mode preferred)
- Open source friendly: MIT license, clear README, .env.example
- Extensible: easy to swap Ollama for OpenAI API via settings

BACKEND API CONTRACT:
- POST /api/documents/upload
- GET /api/documents
- POST /api/documents/{id}/ingest
- GET /api/plan
- POST /api/plan/generate
- GET /api/today
- POST /api/sessions/start
- POST /api/sessions/{id}/finish
- POST /api/hints
- GET /api/review
- GET /api/stats
- GET /api/settings
- PUT /api/settings

RAG BEHAVIOR:
When generating hints, retrieve relevant algorithmic pattern chunks from ChromaDB.
The assistant must follow the 3-level hint policy.
Do not reveal implementation code unless unlock_solution=true.
Use uploaded documents as preferred context before generic LLM knowledge.

REVIEW SCHEDULING:
Use simple spaced repetition:
- failed problem: review tomorrow
- solved with hint level 2/3: review in 3 days
- solved without hint: review in 7 days
- failed twice: mark pattern as weak

ACCEPTANCE CRITERIA:
- docker compose up starts frontend, backend, chromadb, ollama-compatible configuration
- user can upload a markdown file
- backend chunks markdown by ## headings
- chunks are embedded into ChromaDB
- dashboard shows today’s workout
- session page can start timer, request hints, finish session
- review page shows failed problems and weak patterns
- README includes setup steps and screenshots placeholders

NON-GOALS FOR MVP:
- No user auth
- No online judge integration
- No code execution sandbox
- No multi-user support
- No mobile app
- No payment/subscription

IMPORTANT IMPLEMENTATION NOTES:
- Prefer simple working MVP over complex abstraction.
- Do not implement code execution or online judge integration.
- Use mock problem descriptions if LeetCode content is not available.
- Store only leetcode_url and user notes, do not scrape LeetCode.
- Make all pages functional with seed data even before RAG is configured.
- RAG failure should degrade gracefully with a clear UI message.
- Include tests for markdown chunking and review scheduling logic.