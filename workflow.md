# Workflow (watsonx Orchestrate)

The Orchestrate-ready flow definition lives in:
- [apps/api/assets/orchestrate/procurement_decision_flow.yml](apps/api/assets/orchestrate/procurement_decision_flow.yml)

## High-level flow

1. Perception: extract and normalize procurement request fields from unstructured inputs; focused on data quality and clarification, not decisioning.
2. Analysis: produce a supplier risk assessment using available risk tools and signals.
3. Policy: evaluate the request against procurement rules and compliance requirements using policy tools.
4. Decision: synthesize structured inputs with tool-backed risk and policy outputs into APPROVE / REFER / DENY.
5. Action: execute human-in-the-loop referral operations (approve/deny) and surface next steps; does not modify risk or policy logic.

## How this maps to the local demo service

The local FastAPI service implements the same stages and can be used as a backend for Orchestrate:
- Service entrypoints and routing: [apps/api/src/procuator/api/app.py](apps/api/src/procuator/api/app.py)
- Skills used by the API:
  - [apps/api/src/procuator/skills/supplier_risk_checker.py](apps/api/src/procuator/skills/supplier_risk_checker.py)
  - [apps/api/src/procuator/skills/policy_engine.py](apps/api/src/procuator/skills/policy_engine.py)
  - [apps/api/src/procuator/skills/decision_auditor.py](apps/api/src/procuator/skills/decision_auditor.py)

In the API, these map to:
- Risk: `POST /risk-check`
- Policy: `POST /policy-check`
- Full decision: `POST /decision` (also writes audit events)

## Demo script

- Call `GET /demo/scenarios` to show the three prebuilt cases.
- Call `POST /decision` for each case.
- If a case returns `REFER`, show `GET /referrals`, then approve/deny via the referral endpoints.
- Open `GET /dashboard` to show decision analytics.


