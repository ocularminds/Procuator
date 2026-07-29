from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyDecision:
    decision: str
    policyFlags: list[str]
    reasons: list[str]
    requiredApprover: str | None = None

    def toDict(self) -> dict[str, str | list[str] | None]:
        return {
            "policy_decision": self.decision,
            "policy_flags": self.policyFlags,
            "reasons": self.reasons,
            "required_approver": self.requiredApprover,
        }
