from __future__ import annotations

from abc import ABC, abstractmethod

from procuator.features.decision.DecisionModels import Referral


class ReferralRepository(ABC):
    """Persistence contract for human-in-the-loop referrals."""

    @abstractmethod
    def save(self, referral: Referral) -> None:
        """Store a referral."""

    @abstractmethod
    def find(self, referralId: str) -> Referral | None:
        """Find a referral by identifier."""

    @abstractmethod
    def listPending(self) -> list[Referral]:
        """Return pending referrals."""


class InMemoryReferralRepository(ReferralRepository):
    """Process-local referral storage used by the demo application."""

    def __init__(self) -> None:
        self._referrals: dict[str, Referral] = {}

    def save(self, referral: Referral) -> None:
        self._referrals[referral.referralId] = referral

    def find(self, referralId: str) -> Referral | None:
        return self._referrals.get(referralId)

    def listPending(self) -> list[Referral]:
        return [referral for referral in self._referrals.values() if referral.status == "PENDING"]
