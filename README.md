# AI Career Operating System for Students

Single-user MVP that helps students discover career paths, receive a personalized roadmap, track progress, and chat with a local mentor engine.

## Stack

- Frontend: React + Vite + JavaScript
- Backend: Flask + SQLite
- Data flow: React calls Flask REST APIs; Flask persists local data in SQLite

## Project Structure

```text
frontend/   React app shell and feature folders
backend/    Flask app factory, routes, services, and SQLite setup
api/        Vercel serverless entrypoint that serves API and frontend build
docs/       API contract notes
```

## Local Setup

### 1. Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Backend runs on `http://localhost:5000`.

### 2. Frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`.

## Available API Routes

- `GET /api/health`
- `POST /api/intake`
- `GET /api/roadmap`
- `POST /api/progress`
- `POST /api/mentor`

## Production Notes

This is intentionally scoped as a single-user MVP. The deployed Vercel version serves the React build and Flask API from one domain. SQLite is kept for local demo simplicity; real multi-user usage should move persistence to Postgres or Turso before collecting student data.

The backend includes request IDs, basic security headers, lightweight rate limiting for write-heavy endpoints, and deterministic mentor responses. The frontend includes request timeouts, retry behavior for safe reads, loading skeletons, and an error boundary.

## Quality Gates

```powershell
cd backend
.venv\Scripts\python.exe -m unittest discover -s tests

cd ..\frontend
npm run build
```

## Engineering Docs

- `docs/project-audit.md`
- `docs/architecture-decisions.md`
- `docs/testing-strategy.md`
- `docs/interview-guide.md`

## Current Status

The complete local MVP is implemented:
- student discovery questionnaire
- career scoring and track recommendation
- six-week roadmap generation
- SQLite persistence for profile, roadmap, progress, and mentor messages
- task status updates with progress notes
- progress dashboard with completion metrics and next task
- local AI mentor placeholder that uses profile, roadmap, and progress context
- frontend error states and backend request validation

The mentor is intentionally local and deterministic. Add a real AI provider behind `POST /api/mentor` when you are ready to connect `OPENAI_API_KEY`.
