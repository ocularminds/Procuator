from __future__ import annotations

from typing import Any

from procuator.core.Skill import Skill
from procuator.features.policy.PolicyModels import PolicyDecision


class PolicyEngine(Skill):
    """Evaluates procurement requests against the demo policy rules."""

    name = "policy_engine"
    version = "0.1.0"
    description = "Hardcoded procurement policy evaluation"

    def evaluate(self, request: dict[str, Any]) -> PolicyDecision:
        amount = float(request.get("amount", 0))
        budgetRemaining = float(request.get("budget_remaining", 0))
        requesterLimit = float(request.get("requester_approval_limit", 0))
        urgency = str(request.get("urgency", "standard")).lower()
        supplierHistory = request.get("supplier_history") or {}
        totalTransactions = int(supplierHistory.get("total_transactions", 0))

        flags: list[str] = []
        reasons: list[str] = []

        if amount <= 0:
            flags.append("invalid_amount")
            reasons.append("Request amount must be greater than 0")
            return PolicyDecision(decision="DENY", policyFlags=flags, reasons=reasons)

        if amount > budgetRemaining:
            flags.append("budget_exceeded")
            reasons.append("Requested amount exceeds remaining budget")

        if amount > requesterLimit:
            flags.append("amount_exceeds_limit")
            reasons.append("Requested amount exceeds requester approval limit")

        if totalTransactions < 3:
            flags.append("new_supplier")
            reasons.append("Supplier has limited transaction history")

        emergencyOverride = urgency == "critical" and "budget_exceeded" not in flags
        if emergencyOverride:
            flags.append("emergency_override")
            reasons.append("Critical urgency triggers emergency override")

        if "invalid_amount" in flags:
            decision = "DENY"
        elif "budget_exceeded" in flags and not emergencyOverride:
            decision = "DENY"
        elif "amount_exceeds_limit" in flags or "new_supplier" in flags:
            decision = "REFER"
        else:
            decision = "APPROVE"

        requiredApprover = None
        if decision == "REFER":
            requiredApprover = "director" if amount > 20000 else "manager"

        return PolicyDecision(
            decision=decision,
            policyFlags=flags,
            reasons=reasons,
            requiredApprover=requiredApprover,
        )

    async def execute(
        self,
        inputs: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        _ = context
        return self.evaluate(inputs).toDict()
