from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class AuditEvent:
    event_type: str
    request_id: str
    supplier_id: str
    decision: str
    explanation: list[str]
    risk_score: float | None = None
    risk_level: str | None = None
    policy_decision: str | None = None
    policy_flags: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(tz=UTC).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)


class DecisionAuditor:
    """Simple audit trail recorder.

    Writes JSONL to disk (best-effort) and keeps an in-memory ring buffer for dashboards.
    """

    name = "decision_auditor"
    version = "0.1.0"
    description = "Records procurement decisions for audit and analytics"

    def __init__(self, *, max_events: int = 1000) -> None:
        self._events: list[AuditEvent] = []
        self._max_events = max_events

    def record(self, event: AuditEvent) -> None:
        self._events.append(event)
        if len(self._events) > self._max_events:
            self._events = self._events[-self._max_events :]

        path = os.getenv("AUDIT_LOG_PATH", "audit.jsonl")
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with Path(path).open("a", encoding="utf-8") as f:
                f.write(json.dumps(event.__dict__) + "\n")
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to write audit log: %s", exc)

        logger.info(
            "AUDIT decision=%s request_id=%s supplier_id=%s risk=%s policy=%s",
            event.decision,
            event.request_id,
            event.supplier_id,
            event.risk_score,
            event.policy_decision,
        )

    def events(self) -> list[dict[str, Any]]:
        return [e.__dict__ for e in self._events]

    def analytics(self) -> dict[str, Any]:
        counts: dict[str, int] = {}
        for e in self._events:
            counts[e.decision] = counts.get(e.decision, 0) + 1

        avg_risk = None
        risk_scores = [e.risk_score for e in self._events if isinstance(e.risk_score, (int, float))]
        if risk_scores:
            avg_risk = sum(float(x) for x in risk_scores) / len(risk_scores)

        top_flags: dict[str, int] = {}
        for e in self._events:
            for flag in (e.policy_flags or []) + (e.risk_flags or []):
                top_flags[flag] = top_flags.get(flag, 0) + 1

        top_flags_sorted = sorted(top_flags.items(), key=lambda kv: kv[1], reverse=True)[:10]

        return {
            "total": len(self._events),
            "counts_by_decision": counts,
            "avg_risk_score": avg_risk,
            "top_flags": [{"flag": k, "count": v} for k, v in top_flags_sorted],
        }

    async def execute(self, inputs: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
        _ = context
        event = AuditEvent(
            event_type=str(inputs.get("event_type", "decision")),
            request_id=str(inputs.get("request_id", inputs.get("supplier_id", "unknown"))),
            supplier_id=str(inputs.get("supplier_id", "unknown")),
            decision=str(inputs.get("decision", "UNKNOWN")),
            explanation=list(inputs.get("explanation") or []),
            risk_score=(float(inputs["risk_score"]) if inputs.get("risk_score") is not None else None),
            risk_level=(str(inputs["risk_level"]) if inputs.get("risk_level") is not None else None),
            policy_decision=(str(inputs["policy_decision"]) if inputs.get("policy_decision") is not None else None),
            policy_flags=list(inputs.get("policy_flags") or []),
            risk_flags=list(inputs.get("risk_flags") or []),
            metadata=dict(inputs.get("metadata") or {}),
        )
        self.record(event)
        return {"recorded": True, "created_at": event.created_at}
