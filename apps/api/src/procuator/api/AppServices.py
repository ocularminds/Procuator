from __future__ import annotations

from dataclasses import dataclass, field

from procuator.features.decision.DecisionAuditor import DecisionAuditor
from procuator.features.decision.DecisionService import DecisionService
from procuator.features.decision.ReferralRepository import InMemoryReferralRepository
from procuator.features.decision.ReferralService import ReferralService
from procuator.features.policy.PolicyEngine import PolicyEngine
from procuator.features.risk.SupplierRiskChecker import SupplierRiskChecker


@dataclass
class AppServices:
    """Owns application-scoped services and their lifecycle."""

    riskChecker: SupplierRiskChecker = field(default_factory=SupplierRiskChecker)
    policyEngine: PolicyEngine = field(default_factory=PolicyEngine)
    auditor: DecisionAuditor = field(default_factory=DecisionAuditor)
    referrals: InMemoryReferralRepository = field(default_factory=InMemoryReferralRepository)
    decisionService: DecisionService = field(init=False)
    referralService: ReferralService = field(init=False)

    def __post_init__(self) -> None:
        self.decisionService = DecisionService(
            self.riskChecker,
            self.policyEngine,
            self.auditor,
            self.referrals,
        )
        self.referralService = ReferralService(self.referrals, self.auditor)

    async def close(self) -> None:
        await self.riskChecker.close()
