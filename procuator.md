# Procuator

## Problem and solution (≤ 500 words)

### The problem
Enterprise procurement teams are asked to make high-stakes decisions quickly: is this purchase request compliant, within budget, and safe from supplier risk? In many organizations, approvals are still handled by manual review and ticket routing. That creates slow cycle times, inconsistent decisions across reviewers, and audit/compliance gaps (missing “why” behind approvals and denials).

Workflow automation alone doesn’t solve the hard part: decisioning. Teams need a consistent way to combine supplier risk signals, policy rules, and contextual factors into a clear recommendation, with an auditable explanation.

### Our solution
Procuator is a procurement decisioning reference implementation built for IBM watsonx Orchestrate.

It provides an orchestrated decision pipeline that:
- Scores supplier risk (risk intelligence)
- Applies procurement policies (policy-aware evaluation)
- Produces an explainable recommendation (APPROVE / REFER / DENY)
- Records an audit event and exposes lightweight decision analytics
- Supports human-in-the-loop review for referrals

In this repo, the solution is delivered as:
- A FastAPI service backend: [apps/api/src/procuator/api/app.py](apps/api/src/procuator/api/app.py)
- Modular “skills” usable by the service/CLI:
  - Risk checker: [apps/api/src/procuator/skills/supplier_risk_checker.py](apps/api/src/procuator/skills/supplier_risk_checker.py)
  - Policy engine: [apps/api/src/procuator/skills/policy_engine.py](apps/api/src/procuator/skills/policy_engine.py)
  - Audit + analytics: [apps/api/src/procuator/skills/decision_auditor.py](apps/api/src/procuator/skills/decision_auditor.py)

Outcome: consistent, repeatable decisions (and explanations) in seconds, with referrals routed to a human when required.

---

## Agentic AI + watsonx Orchestrate usage (≤ 500 words)

### How agentic AI is used
Procuator uses an agent-style pattern: specialized capabilities handle intake, risk, policy, decisioning, and execution, and an orchestrator composes them into a single, auditable outcome.

Concretely, the orchestrated workflow:
1. Gathers context (the procurement request fields and supplier identifiers)
2. Runs risk and policy checks
3. Produces an explainable rationale summary suitable for audit
4. Routes the request into an approve / refer / deny path
5. Logs the final event and updates analytics

### watsonx Orchestrate implementation
watsonx Orchestrate is the orchestration layer:
- It can model the workflow (steps and routing) and connect skills.
- It can run a reasoning step using prompt templates.
- It can include a human-in-the-loop review node for exceptions.

Scope note: the system is designed to be tool-backed (risk, policy, and decision results come from the Procuator API/tools). It is not legal, financial, or compliance advice.

This repo includes Orchestrate-ready artifacts:
- Flow definition: [apps/api/assets/orchestrate/procurement_decision_flow.yml](apps/api/assets/orchestrate/procurement_decision_flow.yml)
- Prompt templates:
  - Decision prompt: [apps/api/assets/prompts/procurement_decision_v1.yml](apps/api/assets/prompts/procurement_decision_v1.yml)
  - Structured rationale prompt: [apps/api/assets/prompts/procurement_decision_cot.yml](apps/api/assets/prompts/procurement_decision_cot.yml)

The structured rationale prompt is designed to produce an auditable explanation (key checks + key factors + a concise rationale). It should not require revealing hidden chain-of-thought.

---

## Demo scenarios

The demo includes three curated scenarios to show end-to-end behavior:
- [apps/api/src/procuator/data/demo_scenarios.py](apps/api/src/procuator/data/demo_scenarios.py)

They demonstrate:
- Auto-approve
- Human-in-the-loop referral
- Policy-driven denial
