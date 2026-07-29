from __future__ import annotations

from typing import Any


class DecisionRules:
    """Combines policy and risk results into a final procurement decision."""

    def determine(self, policyDecision: str, riskLevel: str, riskScore: float) -> str:
        if policyDecision == "DENY":
            return "DENY"
        if policyDecision == "REFER":
            return "REFER"
        if riskLevel == "HIGH":
            return "REFER"
        if riskLevel == "MEDIUM" and riskScore >= 5.5:
            return "REFER"
        return "APPROVE"

    def extractRiskFlags(self, risk: dict[str, Any]) -> list[str]:
        rawFlags = list(risk.get("risk_flags") or [])
        return [
            str(flag.get("code") or flag.get("message") or flag) if isinstance(flag, dict) else str(flag)
            for flag in rawFlags
        ]

    def explain(
        self,
        policy: dict[str, Any],
        riskFlags: list[str],
        riskLevel: str,
        policyDecision: str,
    ) -> list[str]:
        policyFlags = list(policy.get("policy_flags") or [])
        explanation: list[str] = []

        if policyFlags:
            explanation.append(f"Policy flags: {', '.join(policyFlags)}")
        if riskFlags:
            explanation.append(f"Risk flags: {', '.join(riskFlags)}")
        explanation.extend(list(policy.get("reasons") or []))
        explanation.append(f"Composite decision derived from risk={riskLevel} and policy={policyDecision}.")
        return explanation
