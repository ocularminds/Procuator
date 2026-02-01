# Engineering notes

## Prompting and explainability

This repo keeps prompt templates as first-class assets (rather than embedding them in markdown):
- Decision prompt (JSON output): [apps/api/assets/prompts/procurement_decision_v1.yml](apps/api/assets/prompts/procurement_decision_v1.yml)
- Structured rationale prompt (step-by-step format): [apps/api/assets/prompts/procurement_decision_cot.yml](apps/api/assets/prompts/procurement_decision_cot.yml)

Note: the “structured rationale” prompt is intended to produce an explainable, auditable summary (checks performed, key factors, and a concise rationale). It should not require models to reveal hidden chain-of-thought.

Scope note: the system is designed to be tool-backed. Risk, policy, and decision outcomes should be sourced from the Procuator API/tools and logged for auditability; prompt templates should improve clarity and consistency rather than introduce ungrounded determinations.

## Skills and responsibilities

Skills are implemented as Python modules (callable from the API and CLI):
- Supplier risk scoring: [apps/api/src/procuator/skills/supplier_risk_checker.py](apps/api/src/procuator/skills/supplier_risk_checker.py)
- Policy evaluation (demo rules; policy can drive hard denies): [apps/api/src/procuator/skills/policy_engine.py](apps/api/src/procuator/skills/policy_engine.py)
- Audit logging + analytics aggregation: [apps/api/src/procuator/skills/decision_auditor.py](apps/api/src/procuator/skills/decision_auditor.py)

The API orchestrates these skills and exposes HITL referral handling and analytics endpoints:
- Service app: [apps/api/src/procuator/api/app.py](apps/api/src/procuator/api/app.py)

Multi-agent mapping (Orchestrate): Perception focuses on intake/normalization, Analysis produces supplier risk assessments, Policy evaluates rules/compliance, Decision synthesizes outputs into APPROVE/REFER/DENY, and Action executes human-in-the-loop referral operations. Each stage is intentionally scoped to reduce ambiguity and improve evaluation of “which agent to use” for a given user intent.

## Audit trail

Decisions are logged as JSONL events. You can control the audit log destination via `AUDIT_LOG_PATH`.

## Demo scenarios

The demo is driven by three curated scenarios:
- [apps/api/src/procuator/data/demo_scenarios.py](apps/api/src/procuator/data/demo_scenarios.py)

They are intentionally tuned so:
- The “complex referral” scenario always results in `REFER`.
- The “hard deny” scenario reliably results in `DENY` due to policy (e.g., `budget_exceeded`).

## Local dev workflow

- Install: `pip install -e 'apps/api[dev]'`
- Test: `pytest -q`
- Lint/format: `ruff check .` and `ruff format --check .`
- Run API: `cd apps/api && uvicorn procuator.api.app:app --host 127.0.0.1 --port 8000`
