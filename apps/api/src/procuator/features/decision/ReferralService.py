from __future__ import annotations

from typing import Any

from procuator.features.decision.DecisionAuditor import DecisionAuditor
from procuator.features.decision.ReferralRepository import ReferralRepository


class ReferralService:
    """Lists and resolves human-in-the-loop referrals."""

    def __init__(self, referrals: ReferralRepository, auditor: DecisionAuditor) -> None:
        self._referrals = referrals
        self._auditor = auditor

    def listPending(self) -> dict[str, Any]:
        pending = [referral.toDict() for referral in self._referrals.listPending()]
        return {"pending": pending, "total_pending": len(pending)}

    async def approve(self, referralId: str) -> dict[str, Any]:
        return await self._resolve(referralId, "APPROVED", "APPROVE", "Human approval granted")

    async def deny(self, referralId: str) -> dict[str, Any]:
        return await self._resolve(referralId, "DENIED", "DENY", "Human denial issued")

    async def _resolve(
        self,
        referralId: str,
        status: str,
        decision: str,
        explanation: str,
    ) -> dict[str, Any]:
        referral = self._referrals.find(referralId)
        if referral is None:
            return {"error": "not_found", "referral_id": referralId}

        referral.status = status
        await self._auditor.execute(
            {
                "event_type": "human_approval" if decision == "APPROVE" else "human_denial",
                "request_id": str(referral.request.get("request_id", referralId)),
                "supplier_id": str(referral.request.get("supplier_id", "unknown")),
                "decision": decision,
                "explanation": [explanation],
                "metadata": {"referral_id": referralId},
            }
        )
        return {"referral_id": referralId, "status": referral.status}
