# AI Radar

A hackathon MVP for discovering recent developments in the AI ecosystem.

## Architecture

- Frontend: Next.js + TypeScript
- Backend: FastAPI + Python
- Database: PostgreSQL
- ORM: SQLAlchemy
- Migrations: Alembic
- Local orchestration: Docker Compose

## Setup

### Prerequisites

- Node.js 20+ and npm
- Python 3.12+ and `venv`
- Docker Desktop or Docker Engine

### 1. Start PostgreSQL

Copy the root `.env.example` to `.env` and update values if needed.

```powershell
copy .env.example .env
docker compose up -d
```

### 2. Backend setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### 3. Run Alembic migrations

```powershell
cd backend
.\.venv\Scripts\activate
alembic upgrade head
```

### 4. Start backend

```powershell
cd backend
.\.venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Shortcuts
# Option A — run the same command via the small Python wrapper:
#
#    python run.py
#
# Option B — using `make` (if you have `make` available on your platform):
#
#    make run
#
# Option C — when installed as a package (optional):
#
#    ai-radar-backend
```

### 5. Frontend setup

```powershell
cd ui
npm install
npm run dev
```

### Health check

- Backend root: `http://localhost:8000/health`
- API route: `http://localhost:8000/api/v1/health`

## Project structure

- `backend/` — FastAPI app, SQLAlchemy models, Alembic migrations
- `ui/` — Next.js TypeScript frontend
- `docker-compose.yml` — PostgreSQL service
- `.env.example` — environment variable examples
- `.gitignore` — ignored build and local files

For now create only:

```text
/
```

with a placeholder AI Radar dashboard.

The page should contain:

* Application name: AI Radar
* Short tagline:
  "Discover what's changing in AI."
* Placeholder sections:

  * Trending
  * Emerging
  * Categories

Do not implement the full trend UI yet.

Use a clean dark-first aesthetic, but keep the implementation simple.

Avoid introducing a large UI component library unless already installed.

---

# Docker Compose

Create a minimal docker-compose.yml containing PostgreSQL only.

Example requirements:

* PostgreSQL 16 or another currently stable PostgreSQL version
* persistent named volume
* configurable database/user/password through environment variables
* expose PostgreSQL locally

Do NOT containerize the frontend or backend yet.

I want to run them directly during development.

---

# Developer experience

Add useful scripts/documentation for:

### Frontend

```text
npm/pnpm install
npm/pnpm run dev
```

### Backend

```text
python -m venv .venv
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Database

```text
docker compose up -d
```

Document the complete local setup in README.md.

Include:

1. Prerequisites
2. Clone/setup
3. Start PostgreSQL
4. Configure environment variables
5. Run Alembic migrations
6. Start backend
7. Start frontend
8. Health-check endpoint

---

# Important constraints

This is a hackathon MVP.

DO NOT add:

* Redis
* Celery
* Kafka
* Kubernetes
* Terraform
* authentication
* vector database
* RAG
* background workers
* microservices
* complex state management
* automated web scraping
* agents
* MCP integration
* A2A integration

Keep the code extremely easy to modify.

Use sensible folder structure and naming, but don't over-engineer.

---

# Git hygiene

Create:

```text
.gitignore
.env.example
```

Ensure these are never committed:

```text
.env
.venv
node_modules
.next
__pycache__
*.pyc
```

---

# Final step

After creating the initial structure:

1. Check that the frontend builds.
2. Check that the backend starts.
3. Check that PostgreSQL starts.
4. Check that the database connection works.
5. Check that Alembic can run the migration.
6. Check that `/health` responds successfully.

If something fails, fix it before finishing.

At the end, give me a concise summary of:

* files created
* commands to run
* current architecture
* anything I need to configure manually

Do not proceed into implementing the trend dashboard or LLM chat yet.
