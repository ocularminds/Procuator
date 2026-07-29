from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from procuator.core.Skill import Skill
from procuator.features.decision.DecisionAuditor import DecisionAuditor
from procuator.features.decision.DecisionModels import Referral
from procuator.features.decision.DecisionRules import DecisionRules
from procuator.features.decision.ReferralRepository import ReferralRepository


class DecisionService:
    """Orchestrates risk, policy, referrals, and audit recording."""

    def __init__(
        self,
        riskChecker: Skill,
        policyEngine: Skill,
        auditor: DecisionAuditor,
        referrals: ReferralRepository,
        rules: DecisionRules | None = None,
    ) -> None:
        self._riskChecker = riskChecker
        self._policyEngine = policyEngine
        self._auditor = auditor
        self._referrals = referrals
        self._rules = rules or DecisionRules()

    async def decide(self, request: dict[str, Any]) -> dict[str, Any]:
        requestId = request.get("request_id") or (f"REQ-{datetime.now(tz=UTC).strftime('%Y%m%d')}-{uuid4().hex[:6]}")
        request["request_id"] = requestId

        risk = await self._riskChecker.execute(
            {
                "supplier_id": request["supplier_id"],
                "industry": request.get("industry", "general"),
                "refresh_cache": request.get("refresh_cache", False),
            }
        )
        policy = await self._policyEngine.execute(request)

        riskLevel = str(risk.get("risk_level", "UNKNOWN"))
        riskScore = float(risk.get("risk_score", 0.0))
        policyDecision = str(policy.get("policy_decision", "REFER"))
        policyFlags = list(policy.get("policy_flags") or [])
        riskFlags = self._rules.extractRiskFlags(risk)
        finalDecision = self._rules.determine(policyDecision, riskLevel, riskScore)
        explanation = self._rules.explain(policy, riskFlags, riskLevel, policyDecision)
        humanReview = self._createReferralIfNeeded(
            finalDecision,
            request,
            explanation,
        )

        await self._auditor.execute(
            {
                "event_type": "decision",
                "request_id": requestId,
                "supplier_id": request["supplier_id"],
                "decision": finalDecision,
                "explanation": explanation,
                "risk_score": riskScore,
                "risk_level": riskLevel,
                "policy_decision": policyDecision,
                "policy_flags": policyFlags,
                "risk_flags": riskFlags,
            }
        )

        return {
            "request_id": requestId,
            "supplier_id": request["supplier_id"],
            "decision": finalDecision,
            "explanation": explanation,
            "risk": risk,
            "policy": policy,
            "human_in_the_loop": humanReview,
        }

    def _createReferralIfNeeded(
        self,
        decision: str,
        request: dict[str, Any],
        explanation: list[str],
    ) -> dict[str, Any]:
        if decision != "REFER":
            return {"required": False}

        referralId = uuid4().hex
        referral = Referral(
            referralId=referralId,
            createdAt=datetime.now(tz=UTC).isoformat(),
            status="PENDING",
            request=request,
            proposedDecision=decision,
            explanation=explanation,
        )
        self._referrals.save(referral)
        return {
            "required": True,
            "referral_id": referralId,
            "status": referral.status,
            "approve_url": f"/referrals/{referralId}/approve",
            "deny_url": f"/referrals/{referralId}/deny",
        }
