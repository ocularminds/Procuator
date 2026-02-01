# Procuator Web UI

This Next.js app is a lightweight frontend for the Procuator FastAPI backend.

It provides:
- A decision form (APPROVE / REFER / DENY)
- Demo scenarios runner
- Human-in-the-loop referrals (approve/deny)
- Analytics view (counts and top flags)

## Run locally

From the repo root, the simplest option is:
- `docker compose up --build`

Or run the web app directly:

1) Configure env:
- `cp .env.example .env.local`

2) Install deps:
- `npm install`

3) Start dev server:
- `npm run dev`

Open http://127.0.0.1:3000

## Configuration

The UI calls the API through a Next.js route handler and uses `API_BASE_URL` to reach the backend.

Common values:
- Local API (non-docker): `API_BASE_URL=http://127.0.0.1:8000`
- Docker Compose (web container → api container): `API_BASE_URL=http://api:8080`

## Pages

- `/` Overview
- `/decision` Submit a request to the `/decision` endpoint
- `/scenarios` Load server demo scenarios and run them
- `/referrals` Review and resolve pending HITL referrals
- `/analytics` View aggregated analytics
