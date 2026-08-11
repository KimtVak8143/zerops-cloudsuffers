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
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

### 3. Run Alembic migrations

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
alembic upgrade head
```

### 4. Start backend

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
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

### 5. Seed sample trend data

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python seed.py
```

### 6. Frontend setup

```powershell
cd ui
npm install
npm run dev
```

### One-command local start

If you already created `backend/.venv` and installed dependencies, you can start everything with:

```bash
bash dev.sh
```

That script starts Docker Compose, activates the backend virtual environment with `Activate.ps1`, runs `python run.py`, and launches the UI.

### Health check

- Backend root: `http://localhost:8000/health`
- API route: `http://localhost:8000/api/v1/health`

## Project structure

- `backend/` — FastAPI app, SQLAlchemy models, Alembic migrations
- `ui/` — Next.js TypeScript frontend
- `docker-compose.yml` — local PostgreSQL service for development
- `.env.example` — environment variable examples
- `.gitignore` — ignored build and local files

## Deployment

### Frontend
- Deploy the `ui/` directory to Vercel.
- Use `NEXT_PUBLIC_API_URL` in Vercel to point at the deployed Zerops backend base URL.
- Keep the frontend configuration environment-driven; do not hardcode `localhost:8000`.

### Backend
- Deploy the `backend/` directory to Zerops.
- `zerops.yaml` defines the `api` service for the FastAPI backend.
- The backend starts with `uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}`.
- The backend uses `DATABASE_URL` and `CORS_ORIGINS` from environment variables.
- `initCommands` runs `alembic upgrade head` before the app starts.
- Health check is configured against `/health`.

### Database
- The Zerops database service should be named `db`.
- The backend should use the generated `db_connectionString` for `DATABASE_URL`.
- Local development continues to use Docker Compose PostgreSQL.

## Required environment variables

### Backend
- `DATABASE_URL` — full SQLAlchemy connection URL for PostgreSQL
- `LLM_API_KEY` — model API key (optional for now)
- `LLM_MODEL` — model name, e.g. `gpt-4o-mini`
- `CORS_ORIGINS` — comma-separated allowed origins, e.g. `http://localhost:3000`

### Frontend
- `NEXT_PUBLIC_API_URL` — base URL of the backend API, e.g. `http://localhost:8000` locally or the Zerops backend URL in production

## Local workflow

1. Copy environment files

```powershell
copy .env.example .env
cd backend
copy .env.example .env
```

2. Start local PostgreSQL

```powershell
docker compose up -d
```

3. Install backend dependencies

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

4. Run Alembic migrations

```powershell
cd backend
.\.venv\Scripts\activate
alembic upgrade head
```

5. Start backend locally

```powershell
cd backend
.\.venv\Scripts\activate
python run.py
```

6. Start frontend locally

```powershell
cd ui
npm install
npm run dev
```

## Verify locally

- Backend health: `http://localhost:8000/health`
- API health: `http://localhost:8000/api/v1/health`
- Trend list: `http://localhost:8000/api/v1/trends`
- Trend detail: `http://localhost:8000/api/v1/trends/<slug>`
- Frontend should use `NEXT_PUBLIC_API_URL=http://localhost:8000`

## Zerops deployment notes

1. Create a Zerops service named `api` using the `backend/` directory.
2. Create a Zerops PostgreSQL service named `db`.
3. Set `DATABASE_URL` in the `api` service from the generated `db_connectionString`.
4. Set `CORS_ORIGINS` to the Vercel frontend origin in production.
5. Set `LLM_API_KEY` and `LLM_MODEL` in Zerops if needed.
6. Deploy the frontend from `ui/` on Vercel and set `NEXT_PUBLIC_API_URL` to the backend URL.
7. Verify `GET /health` returns `{"status":"ok"}`.

## Notes

- Local development remains independent of Zerops.
- The backend uses environment variables for production configuration.
- Do not commit `.env` files or real credentials.


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
