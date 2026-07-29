from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any

from procuator.core.Skill import Skill
from procuator.features.risk.RiskAdvisor import RiskAdvisor
from procuator.features.risk.RiskDataSource import DefaultRiskDataSource, RiskDataSource
from procuator.features.risk.RiskModels import RiskAssessment, RiskCacheEntry
from procuator.features.risk.RiskScorer import RiskScorer

logger = logging.getLogger(__name__)


class SupplierRiskChecker(Skill):
    """Coordinates supplier data retrieval, scoring, and guidance."""

    name = "supplier_risk_checker"
    version = "1.2.0"
    description = "Comprehensive supplier risk assessment with component scoring"

    weights: dict[str, float] = {
        "financial": 0.40,
        "compliance": 0.25,
        "operational": 0.20,
        "market": 0.15,
    }

    def __init__(
        self,
        *,
        cacheTtl: timedelta = timedelta(hours=1),
        dataSource: RiskDataSource | None = None,
        scorer: RiskScorer | None = None,
        advisor: RiskAdvisor | None = None,
    ) -> None:
        self._cacheTtl = cacheTtl
        self._cache: dict[str, RiskCacheEntry] = {}
        self._dataSource = dataSource or DefaultRiskDataSource()
        self._scorer = scorer or RiskScorer()
        self._advisor = advisor or RiskAdvisor()

    async def execute(
        self,
        inputs: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        _ = context
        supplierId = str(inputs["supplier_id"])
        industry = str(inputs.get("industry", "general"))
        shouldRefresh = bool(inputs.get("refresh_cache", False))
        cacheKey = f"{supplierId}_{industry}"

        if not shouldRefresh:
            cached = self._cache.get(cacheKey)
            if cached and datetime.now() - cached.cachedAt < self._cacheTtl:
                return cached.data

        try:
            financialData, complianceData, marketData = await asyncio.gather(
                self._dataSource.fetchFinancialData(supplierId),
                self._dataSource.fetchComplianceData(supplierId),
                self._dataSource.fetchMarketData(industry),
                return_exceptions=True,
            )
            financial = self._handleFetchError(financialData, "financial")
            compliance = self._handleFetchError(complianceData, "compliance")
            market = self._handleFetchError(marketData, "market")

            scores = {
                "financial": self._scorer.calculateFinancialScore(financial),
                "compliance": self._scorer.calculateComplianceScore(compliance),
                "operational": self._scorer.calculateOperationalScore(supplierId),
                "market": self._scorer.calculateMarketScore(market),
            }
            totalScore = sum(scores[key] * self.weights[key] for key in scores)
            flags = self._advisor.generateFlags(scores, totalScore)
            assessment = RiskAssessment(
                supplierId=supplierId,
                riskScore=totalScore,
                riskLevel=self._advisor.getRiskLevel(totalScore),
                componentScores=scores,
                riskFlags=flags,
                recommendations=self._advisor.generateRecommendations(scores, flags, totalScore),
                confidence=self._scorer.calculateConfidence(scores),
                updatedAt=datetime.now().isoformat(),
                weights=self.weights,
                version=self.version,
            )
            result = assessment.toDict()
            self._cache[cacheKey] = RiskCacheEntry(cachedAt=datetime.now(), data=result)
            return result
        except Exception as exc:  # noqa: BLE001
            logger.exception("Risk assessment failed")
            return self._buildFallback(inputs, str(exc))

    def _handleFetchError(self, data: Any, dataType: str) -> dict[str, Any]:
        if isinstance(data, Exception):
            logger.warning("Failed to fetch %s data: %s", dataType, data)
            return {"error": str(data), "default_used": True}
        return data

    def _buildFallback(self, inputs: dict[str, Any], error: str) -> dict[str, Any]:
        return {
            "risk_score": 5.0,
            "risk_level": "UNKNOWN",
            "component_scores": {
                "financial": 5.0,
                "compliance": 5.0,
                "operational": 5.0,
                "market": 5.0,
            },
            "risk_flags": [
                {
                    "code": "ASSESSMENT_FAILED",
                    "severity": "HIGH",
                    "message": f"Risk assessment failed: {error}",
                    "component": "system",
                    "score": 0,
                }
            ],
            "recommendations": [
                "Manual review required due to system error",
                "Verify supplier information independently",
            ],
            "confidence": 0.0,
            "last_updated": datetime.now().isoformat(),
            "supplier_id": str(inputs.get("supplier_id", "unknown")),
            "metadata": {"error": error, "fallback_mode": True, "calculation_version": self.version},
        }

    async def close(self) -> None:
        await self._dataSource.close()

    async def aclose(self) -> None:
        """Compatibility alias for the previous public lifecycle method."""
        await self.close()


class SupplierRiskCheckerFactory:
    """Creates the default risk skill for plugin-style consumers."""

    def create(self) -> SupplierRiskChecker:
        return SupplierRiskChecker()


def createSkill() -> SupplierRiskChecker:
    return SupplierRiskCheckerFactory().create()
