from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PolicyDecision:
    decision: str  # APPROVE | REFER | DENY
    policy_flags: list[str]
    reasons: list[str]
    required_approver: str | None = None


class PolicyEngine:
    """Hardcoded policy engine for demo purposes.

    Evaluates basic procurement constraints:
    - Budget remaining
    - Requester approval limit
    - New supplier restrictions
    - Emergency override

    Inputs are expected to be request-like dicts (similar to generator templates).
    """

    name = "policy_engine"
    version = "0.1.0"
    description = "Hardcoded procurement policy evaluation"

    def evaluate(self, request: dict[str, Any]) -> PolicyDecision:
        amount = float(request.get("amount", 0))
        budget_remaining = float(request.get("budget_remaining", 0))
        requester_limit = float(request.get("requester_approval_limit", 0))
        urgency = str(request.get("urgency", "standard")).lower()

        supplier_history = request.get("supplier_history") or {}
        total_transactions = int(supplier_history.get("total_transactions", 0))

        flags: list[str] = []
        reasons: list[str] = []

        if amount <= 0:
            flags.append("invalid_amount")
            reasons.append("Request amount must be greater than 0")
            return PolicyDecision(decision="DENY", policy_flags=flags, reasons=reasons)

        if amount > budget_remaining:
            flags.append("budget_exceeded")
            reasons.append("Requested amount exceeds remaining budget")

        if amount > requester_limit:
            flags.append("amount_exceeds_limit")
            reasons.append("Requested amount exceeds requester approval limit")

        if total_transactions < 3:
            flags.append("new_supplier")
            reasons.append("Supplier has limited transaction history")

        emergency_override = urgency == "critical" and "budget_exceeded" not in flags
        if emergency_override:
            flags.append("emergency_override")
            reasons.append("Critical urgency triggers emergency override")

        if "invalid_amount" in flags:
            decision = "DENY"
        elif "budget_exceeded" in flags and not emergency_override:
            decision = "DENY"
        elif "amount_exceeds_limit" in flags or "new_supplier" in flags:
            decision = "REFER"
        else:
            decision = "APPROVE"

        required_approver = None
        if decision == "REFER":
            required_approver = "manager"
            if amount > 20000:
                required_approver = "director"

        return PolicyDecision(
            decision=decision,
            policy_flags=flags,
            reasons=reasons,
            required_approver=required_approver,
        )

    async def execute(self, inputs: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
        _ = context
        result = self.evaluate(inputs)
        return {
            "policy_decision": result.decision,
            "policy_flags": result.policy_flags,
            "reasons": result.reasons,
            "required_approver": result.required_approver,
        }
