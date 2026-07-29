from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

from procuator.core.Skill import Skill
from procuator.features.decision.DecisionModels import AuditEvent

logger = logging.getLogger(__name__)


class DecisionAuditor(Skill):
    """Records decision events and calculates in-memory analytics."""

    name = "decision_auditor"
    version = "0.1.0"
    description = "Records procurement decisions for audit and analytics"

    def __init__(self, *, maxEvents: int = 1000) -> None:
        self._events: list[AuditEvent] = []
        self._maxEvents = maxEvents

    def record(self, event: AuditEvent) -> None:
        self._events.append(event)
        if len(self._events) > self._maxEvents:
            self._events = self._events[-self._maxEvents :]

        auditPath = Path(os.getenv("AUDIT_LOG_PATH", "audit.jsonl"))
        try:
            auditPath.parent.mkdir(parents=True, exist_ok=True)
            with auditPath.open("a", encoding="utf-8") as auditFile:
                auditFile.write(json.dumps(event.toDict()) + "\n")
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to write audit log: %s", exc)

        logger.info(
            "AUDIT decision=%s request_id=%s supplier_id=%s risk=%s policy=%s",
            event.decision,
            event.requestId,
            event.supplierId,
            event.riskScore,
            event.policyDecision,
        )

    def events(self) -> list[dict[str, Any]]:
        return [event.toDict() for event in self._events]

    def analytics(self) -> dict[str, Any]:
        decisionCounts: dict[str, int] = {}
        for event in self._events:
            decisionCounts[event.decision] = decisionCounts.get(event.decision, 0) + 1

        riskScores = [event.riskScore for event in self._events if isinstance(event.riskScore, (int, float))]
        averageRisk = None
        if riskScores:
            averageRisk = sum(float(score) for score in riskScores) / len(riskScores)

        flagCounts: dict[str, int] = {}
        for event in self._events:
            for flag in event.policyFlags + event.riskFlags:
                flagCounts[flag] = flagCounts.get(flag, 0) + 1
        topFlags = sorted(flagCounts.items(), key=lambda item: item[1], reverse=True)[:10]

        return {
            "total": len(self._events),
            "counts_by_decision": decisionCounts,
            "avg_risk_score": averageRisk,
            "top_flags": [{"flag": flag, "count": count} for flag, count in topFlags],
        }

    async def execute(
        self,
        inputs: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        _ = context
        event = AuditEvent(
            eventType=str(inputs.get("event_type", "decision")),
            requestId=str(inputs.get("request_id", inputs.get("supplier_id", "unknown"))),
            supplierId=str(inputs.get("supplier_id", "unknown")),
            decision=str(inputs.get("decision", "UNKNOWN")),
            explanation=list(inputs.get("explanation") or []),
            riskScore=float(inputs["risk_score"]) if inputs.get("risk_score") is not None else None,
            riskLevel=str(inputs["risk_level"]) if inputs.get("risk_level") is not None else None,
            policyDecision=(str(inputs["policy_decision"]) if inputs.get("policy_decision") is not None else None),
            policyFlags=list(inputs.get("policy_flags") or []),
            riskFlags=list(inputs.get("risk_flags") or []),
            metadata=dict(inputs.get("metadata") or {}),
        )
        self.record(event)
        return {"recorded": True, "created_at": event.createdAt}
