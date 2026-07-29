from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class Referral:
    referralId: str
    createdAt: str
    status: str
    request: dict[str, Any]
    proposedDecision: str
    explanation: list[str]

    def toDict(self) -> dict[str, Any]:
        return {
            "referral_id": self.referralId,
            "created_at": self.createdAt,
            "status": self.status,
            "request": self.request,
            "proposed_decision": self.proposedDecision,
            "explanation": self.explanation,
        }


@dataclass
class AuditEvent:
    eventType: str
    requestId: str
    supplierId: str
    decision: str
    explanation: list[str]
    riskScore: float | None = None
    riskLevel: str | None = None
    policyDecision: str | None = None
    policyFlags: list[str] = field(default_factory=list)
    riskFlags: list[str] = field(default_factory=list)
    createdAt: str = field(default_factory=lambda: datetime.now(tz=UTC).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)

    def toDict(self) -> dict[str, Any]:
        return {
            "event_type": self.eventType,
            "request_id": self.requestId,
            "supplier_id": self.supplierId,
            "decision": self.decision,
            "explanation": self.explanation,
            "risk_score": self.riskScore,
            "risk_level": self.riskLevel,
            "policy_decision": self.policyDecision,
            "policy_flags": self.policyFlags,
            "risk_flags": self.riskFlags,
            "created_at": self.createdAt,
            "metadata": self.metadata,
        }
