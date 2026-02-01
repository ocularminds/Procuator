# Procuator

Procurement decisioning reference implementation for IBM watsonx Orchestrate.

## Demo (2–3 minutes)

1) Start the stack
- `docker compose up --build`
- Open the web UI: http://127.0.0.1:3000

2) Run a full decision
- Open `Decision` and submit the default request.
- Expected outcome: `APPROVE`, `REFER`, or `DENY` plus an explanation.

3) Show human-in-the-loop (HITL)
- If the decision returns `REFER`, open `Referrals` and click `Approve` or `Deny`.
- Expected outcome: referral status updates and the action is recorded.

4) Show measurable outcomes
- Open `Analytics` to show aggregated decision counts and top flags.

Optional (Orchestrate): import the agents/tools and run the same flow end-to-end using:
- Flow: [apps/api/assets/orchestrate/procurement_decision_flow.yml](apps/api/assets/orchestrate/procurement_decision_flow.yml)
- Agent: [apps/api/assets/orchestrate/procuator_agent_spec.yml](apps/api/assets/orchestrate/procuator_agent_spec.yml)

## Screenshots

Add screenshots under [docs/screenshots](docs/screenshots) and link them here:
- Overview: `docs/screenshots/overview.png`
- Decision: `docs/screenshots/decision.png`
- Referrals (HITL): `docs/screenshots/referrals.png`
- Analytics: `docs/screenshots/analytics.png`
- Orchestrate agent/tools: `docs/screenshots/orchestrate.png`

## IBM technology used

- IBM watsonx Orchestrate: native agent specs, tools, and flow assets under [apps/api/assets/orchestrate](apps/api/assets/orchestrate)
- IBM Cloud Code Engine: deployment workflow in [.github/workflows/deploy-code-engine.yml](.github/workflows/deploy-code-engine.yml)

## Judging criteria mapping

- Completeness & feasibility: runnable end-to-end (API + Web + Orchestrate assets) with repeatable demo scenarios, tests, and containerization.
- Creativity & innovation: multi-agent procurement decisioning with tool-backed risk/policy, HITL referrals, and auditable analytics.
- Design & usability: simple web UI for decisioning + referrals + analytics and Orchestrate starter prompts for quick demos.
- Effectiveness & efficiency: targets high-friction procurement approvals; produces measurable outputs (decisions, flags, audit events, analytics) with a scalable deployment path.

This repo is a production-structured Python package (src-layout) that provides:
- A FastAPI service (`/risk-check`, `/decision`, referrals, analytics/dashboard)
- “Skills” you can wire into an Orchestrate flow (risk checker, policy engine, decision auditor)
- Demo scenarios + dataset generator for repeatable demos

## What’s in the repo

Skills (Python)
- Supplier risk checker: [apps/api/src/procuator/skills/supplier_risk_checker.py](apps/api/src/procuator/skills/supplier_risk_checker.py)
- Policy engine (demo rules): [apps/api/src/procuator/skills/policy_engine.py](apps/api/src/procuator/skills/policy_engine.py)
- Decision auditor (JSONL + analytics): [apps/api/src/procuator/skills/decision_auditor.py](apps/api/src/procuator/skills/decision_auditor.py)

API (FastAPI)
- App: [apps/api/src/procuator/api/app.py](apps/api/src/procuator/api/app.py)

Demo data
- 3 core demo scenarios: [apps/api/src/procuator/data/demo_scenarios.py](apps/api/src/procuator/data/demo_scenarios.py)
- Dataset generator: [apps/api/src/procuator/data/generator.py](apps/api/src/procuator/data/generator.py)

watsonx Orchestrate assets
- Flow example: [apps/api/assets/orchestrate/procurement_decision_flow.yml](apps/api/assets/orchestrate/procurement_decision_flow.yml)
- Native agent spec (tools mapped to API endpoints): [apps/api/assets/orchestrate/procuator_agent_spec.yml](apps/api/assets/orchestrate/procuator_agent_spec.yml)
- Multi-agent orchestrator spec: [apps/api/assets/orchestrate/procuator_orchestrator.yml](apps/api/assets/orchestrate/procuator_orchestrator.yml)
- Multi-agent individual specs: [apps/api/assets/orchestrate/agents](apps/api/assets/orchestrate/agents)
- Import helper (imports collaborators first): [apps/api/assets/orchestrate/import_agents.sh](apps/api/assets/orchestrate/import_agents.sh)

The multi-agent setup separates responsibilities across procurement intake (Perception), supplier risk (Analysis), policy/compliance (Policy), final recommendation (Decision), and execution of human-in-the-loop actions (Action). Agents are intended to rely on tool-backed outputs rather than fabricate risk/policy determinations.

Orchestrate tools (Python-based, API callers):
- Tool sources: [apps/api/assets/orchestrate/tools/python](apps/api/assets/orchestrate/tools/python)
- Tool deps: [apps/api/assets/orchestrate/tools/requirements.txt](apps/api/assets/orchestrate/tools/requirements.txt)

Note (Developer Edition networking): tools run in containers, so set `PROCUATOR_API_BASE_URL` to `http://docker.host.internal:8000` (or your host IP) so tools can reach the locally running API.
- Prompt templates:
  - v1: [apps/api/assets/prompts/procurement_decision_v1.yml](apps/api/assets/prompts/procurement_decision_v1.yml)
  - Structured rationale (“step-by-step” format): [apps/api/assets/prompts/procurement_decision_cot.yml](apps/api/assets/prompts/procurement_decision_cot.yml)

## Run locally

### One-command runner (pick one)

- Docker (API + Web): `docker compose up --build`
  - API: http://127.0.0.1:8000
  - Web: http://127.0.0.1:3000
- Local dev script (API + Web): `./scripts/dev.sh`
  - Uses `.venv/` and runs the API in `--reload` mode.

Create and use the project venv:
- `python -m venv .venv`
- `source .venv/bin/activate`
- `pip install -e 'apps/api[dev]'`

Start the API:
- `cd apps/api && uvicorn procuator.api.app:app --host 127.0.0.1 --port 8000`

Start the web UI:
- `cd apps/web && cp .env.example .env.local`
- `cd apps/web && npm install`
- `cd apps/web && npm run dev`

By default the UI expects the API at `http://127.0.0.1:8000` via `API_BASE_URL`.

Smoke-test:
- `curl -s http://127.0.0.1:8000/health`
- `curl -s http://127.0.0.1:8000/demo/scenarios`
- `curl -s http://127.0.0.1:8000/dashboard`

## API endpoints

- `GET /health`
- `POST /risk-check` (supplier-only scoring)
- `POST /policy-check` (policy engine only)
- `POST /decision` (risk + policy + final decision + optional HITL referral)
- `GET /referrals` / `POST /referrals/{id}/approve` / `POST /referrals/{id}/deny`
- `GET /analytics` (JSON decision analytics)
- `GET /dashboard` (simple HTML dashboard)

## CLI

The CLI entrypoint is `procuator`.

- `procuator risk-check SUP-001 --industry technology`
- `procuator demo-scenarios`
- `procuator decide SUP-009 --industry technology --amount 15000 --budget-remaining 50000 --requester-approval-limit 5000 --supplier-transactions 0`
- `procuator generate-data --output data/procurement_test_data.json --count 10`

## Tests & lint

- `pytest -q`
- `ruff check .`
- `ruff format --check .`

## Deployment

This repo includes a container build and GitHub Actions workflows intended for IBM Cloud Code Engine.

- Backend Dockerfile: [apps/api/Dockerfile](apps/api/Dockerfile)
- CI: [.github/workflows/ci.yml](.github/workflows/ci.yml)
- Code Engine deploy workflow: [.github/workflows/deploy-code-engine.yml](.github/workflows/deploy-code-engine.yml)

## Limitations (intentional for POC)

- Referral state is stored in-memory (good for demos; production would use a shared database)
- Audit trail is JSONL (portable; production would move to managed storage/warehouse)

## Next steps

- Persist referrals/audit events to a database and add basic RBAC
- Add policy authoring/versioning and change approval workflow
- Expand risk signals (sanctions, ESG, delivery performance) with clear provenance

## Docs

Higher-level narrative:
- [architecture.md](architecture.md)
- [workflow.md](workflow.md)
- [engineering.md](engineering.md)

Frontend:
- Next.js UI: [apps/web](apps/web)
