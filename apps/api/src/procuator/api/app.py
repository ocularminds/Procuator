from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from procuator import __version__
from procuator.data.demo_scenarios import demo_scenarios
from procuator.skills.decision_auditor import DecisionAuditor
from procuator.skills.policy_engine import PolicyEngine
from procuator.skills.supplier_risk_checker import SupplierRiskChecker

logger = logging.getLogger(__name__)

_skill = SupplierRiskChecker()
_policy = PolicyEngine()
_auditor = DecisionAuditor()


@dataclass
class Referral:
    referral_id: str
    created_at: str
    status: str  # PENDING | APPROVED | DENIED
    request: dict[str, Any]
    proposed_decision: str
    explanation: list[str]


_referrals: dict[str, Referral] = {}


@asynccontextmanager
async def _lifespan(_: FastAPI) -> AsyncIterator[None]:
    try:
        yield
    finally:
        await _skill.aclose()


app = FastAPI(title="Procuator", version=__version__, lifespan=_lifespan)


class RiskCheckRequest(BaseModel):
    supplier_id: str = Field(..., examples=["SUP-001"])
    industry: str = Field(default="general", examples=["technology"])
    refresh_cache: bool = False


class ProcurementDecisionRequest(BaseModel):
    request_id: str | None = Field(default=None, examples=["REQ-20260131-001"])
    supplier_id: str = Field(..., examples=["SUP-001"])
    industry: str = Field(default="general", examples=["technology"])
    amount: float = Field(..., examples=[1250.0])
    currency: str = Field(default="USD")
    budget_remaining: float = Field(default=0.0)
    requester_approval_limit: float = Field(default=0.0)
    urgency: str = Field(default="standard", examples=["standard", "critical"])
    supplier_history: dict[str, Any] | None = None
    refresh_cache: bool = False


class PolicyCheckRequest(BaseModel):
    amount: float = Field(..., examples=[1250.0])
    budget_remaining: float = Field(default=0.0)
    requester_approval_limit: float = Field(default=0.0)
    urgency: str = Field(default="standard", examples=["standard", "critical"])
    supplier_history: dict[str, Any] | None = None


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.post("/risk-check")
async def risk_check(payload: RiskCheckRequest) -> dict[str, Any]:
    return await _skill.execute(payload.model_dump())


@app.post("/policy-check")
async def policy_check(payload: PolicyCheckRequest) -> dict[str, Any]:
    return await _policy.execute(payload.model_dump())


@app.get("/demo/scenarios")
async def demo() -> dict[str, Any]:
    return {"scenarios": demo_scenarios()}


@app.post("/decision")
async def decision(payload: ProcurementDecisionRequest) -> dict[str, Any]:
    request_dict = payload.model_dump()
    request_id = request_dict.get("request_id") or f"REQ-{datetime.now(tz=UTC).strftime('%Y%m%d')}-{uuid4().hex[:6]}"
    request_dict["request_id"] = request_id

    risk = await _skill.execute(
        {
            "supplier_id": request_dict["supplier_id"],
            "industry": request_dict.get("industry", "general"),
            "refresh_cache": request_dict.get("refresh_cache", False),
        }
    )
    policy = await _policy.execute(request_dict)

    explanation: list[str] = []

    risk_level = str(risk.get("risk_level", "UNKNOWN"))
    risk_score = float(risk.get("risk_score", 0.0))
    policy_decision = str(policy.get("policy_decision", "REFER"))
    policy_flags = list(policy.get("policy_flags") or [])
    risk_flags_raw = list(risk.get("risk_flags") or [])
    risk_flags = [
        (str(f.get("code") or f.get("message") or f) if isinstance(f, dict) else str(f)) for f in risk_flags_raw
    ]

    if policy_decision == "DENY":
        final_decision = "DENY"
    elif policy_decision == "REFER":
        final_decision = "REFER"
    elif risk_level == "HIGH":
        final_decision = "REFER"
    elif risk_level == "MEDIUM" and risk_score >= 5.5:
        final_decision = "REFER"
    else:
        final_decision = "APPROVE"

    if policy_flags:
        explanation.append(f"Policy flags: {', '.join(policy_flags)}")
    if risk_flags:
        explanation.append(f"Risk flags: {', '.join(risk_flags)}")
    explanation.extend(list(policy.get("reasons") or []))
    explanation.append(f"Composite decision derived from risk={risk_level} and policy={policy_decision}.")

    hitl: dict[str, Any] | None = None
    if final_decision == "REFER":
        referral_id = uuid4().hex
        referral = Referral(
            referral_id=referral_id,
            created_at=datetime.now(tz=UTC).isoformat(),
            status="PENDING",
            request=request_dict,
            proposed_decision=final_decision,
            explanation=explanation,
        )
        _referrals[referral_id] = referral
        hitl = {
            "required": True,
            "referral_id": referral_id,
            "status": referral.status,
            "approve_url": f"/referrals/{referral_id}/approve",
            "deny_url": f"/referrals/{referral_id}/deny",
        }
    else:
        hitl = {"required": False}

    await _auditor.execute(
        {
            "event_type": "decision",
            "request_id": request_id,
            "supplier_id": request_dict["supplier_id"],
            "decision": final_decision,
            "explanation": explanation,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "policy_decision": policy_decision,
            "policy_flags": policy_flags,
            "risk_flags": risk_flags,
        }
    )

    return {
        "request_id": request_id,
        "supplier_id": request_dict["supplier_id"],
        "decision": final_decision,
        "explanation": explanation,
        "risk": risk,
        "policy": policy,
        "human_in_the_loop": hitl,
    }


@app.get("/referrals")
async def list_referrals() -> dict[str, Any]:
    pending = [r.__dict__ for r in _referrals.values() if r.status == "PENDING"]
    return {"pending": pending, "total_pending": len(pending)}


@app.post("/referrals/{referral_id}/approve")
async def approve_referral(referral_id: str) -> dict[str, Any]:
    referral = _referrals.get(referral_id)
    if referral is None:
        return {"error": "not_found", "referral_id": referral_id}
    referral.status = "APPROVED"
    await _auditor.execute(
        {
            "event_type": "human_approval",
            "request_id": str(referral.request.get("request_id", referral_id)),
            "supplier_id": str(referral.request.get("supplier_id", "unknown")),
            "decision": "APPROVE",
            "explanation": ["Human approval granted"],
            "metadata": {"referral_id": referral_id},
        }
    )
    return {"referral_id": referral_id, "status": referral.status}


@app.post("/referrals/{referral_id}/deny")
async def deny_referral(referral_id: str) -> dict[str, Any]:
    referral = _referrals.get(referral_id)
    if referral is None:
        return {"error": "not_found", "referral_id": referral_id}
    referral.status = "DENIED"
    await _auditor.execute(
        {
            "event_type": "human_denial",
            "request_id": str(referral.request.get("request_id", referral_id)),
            "supplier_id": str(referral.request.get("supplier_id", "unknown")),
            "decision": "DENY",
            "explanation": ["Human denial issued"],
            "metadata": {"referral_id": referral_id},
        }
    )
    return {"referral_id": referral_id, "status": referral.status}


@app.get("/analytics")
async def analytics() -> dict[str, Any]:
    return _auditor.analytics()


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard() -> str:
    stats = _auditor.analytics()
    row_template = "<tr><td>{flag}</td><td style='text-align:right'>{count}</td></tr>"
    rows = "\n".join(row_template.format(flag=d["flag"], count=d["count"]) for d in stats.get("top_flags", []))
    counts = stats.get("counts_by_decision", {})
    counts_rows = "\n".join(
        f"<tr><td>{k}</td><td style='text-align:right'>{v}</td></tr>" for k, v in sorted(counts.items())
    )

    return f"""<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8' />
  <meta name='viewport' content='width=device-width, initial-scale=1' />
  <title>Procuator Dashboard</title>
  <style>
    body {{ font-family: -apple-system, system-ui, Segoe UI, Roboto, Arial, sans-serif; margin: 24px; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
    .card {{ border: 1px solid #ddd; border-radius: 10px; padding: 16px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border-bottom: 1px solid #eee; padding: 8px; }}
    th {{ text-align: left; }}
    code {{ background: #f6f6f6; padding: 2px 6px; border-radius: 6px; }}
  </style>
</head>
<body>
  <h1>Procuator Decision Analytics</h1>
  <p>Total audited decisions: <b>{stats.get("total", 0)}</b></p>
  <p>Average risk score: <b>{stats.get("avg_risk_score")}</b></p>

  <div class='grid'>
    <div class='card'>
      <h2>Counts by Decision</h2>
      <table>
        <thead><tr><th>Decision</th><th style='text-align:right'>Count</th></tr></thead>
        <tbody>
          {counts_rows or "<tr><td colspan='2'>No data yet</td></tr>"}
        </tbody>
      </table>
    </div>
    <div class='card'>
      <h2>Top Flags</h2>
      <table>
        <thead><tr><th>Flag</th><th style='text-align:right'>Count</th></tr></thead>
        <tbody>
          {rows or "<tr><td colspan='2'>No flags yet</td></tr>"}
        </tbody>
      </table>
    </div>
  </div>

  <p style='margin-top: 16px'>Tip: call <code>POST /decision</code> to generate events.</p>
</body>
</html>"""
