from __future__ import annotations

from datetime import datetime
from typing import Any


class RiskScorer:
    """Calculates independent risk component scores."""

    operationalFactors: dict[str, dict[str, float]] = {
        "SUP-001": {"delivery_reliability": 0.95, "quality_score": 0.92, "response_time": 0.88},
        "SUP-002": {"delivery_reliability": 0.85, "quality_score": 0.78, "response_time": 0.72},
        "SUP-003": {"delivery_reliability": 0.98, "quality_score": 0.96, "response_time": 0.94},
        "SUP-004": {"delivery_reliability": 0.70, "quality_score": 0.65, "response_time": 0.60},
        "SUP-005": {"delivery_reliability": 0.90, "quality_score": 0.85, "response_time": 0.82},
    }
    defaultOperationalFactors = {
        "delivery_reliability": 0.80,
        "quality_score": 0.75,
        "response_time": 0.70,
    }

    def calculateFinancialScore(self, data: dict[str, Any]) -> float:
        score = 5.0

        if data.get("revenue_12m", 0) > 10_000_000:
            score += 2.0
        elif data.get("revenue_12m", 0) > 1_000_000:
            score += 1.0
        elif data.get("revenue_12m", 0) == 0:
            score -= 3.0

        profitMargin = float(data.get("profit_margin", 0))
        if profitMargin > 0.2:
            score += 1.5
        elif profitMargin > 0.1:
            score += 0.5
        elif profitMargin < 0:
            score -= 2.0

        debtToEquity = float(data.get("debt_to_equity", 1.0))
        if debtToEquity < 0.3:
            score += 1.0
        elif debtToEquity > 1.0:
            score -= 1.5

        currentRatio = float(data.get("current_ratio", 1.0))
        if currentRatio > 2.0:
            score += 1.0
        elif currentRatio < 1.0:
            score -= 2.0

        creditScores = {
            "AAA": 2.0,
            "AA": 1.5,
            "A": 1.0,
            "BBB": 0.5,
            "BB": -0.5,
            "B": -1.5,
            "CCC": -3.0,
            "D": -5.0,
        }
        score += creditScores.get(str(data.get("credit_rating", "")), -2.0)

        auditOpinion = str(data.get("audit_opinion", "unknown"))
        if auditOpinion == "clean":
            score += 1.0
        elif auditOpinion == "qualified":
            score -= 0.5
        elif auditOpinion == "adverse":
            score -= 3.0

        return self._clamp(score)

    def calculateComplianceScore(self, data: dict[str, Any]) -> float:
        score = 7.0
        violations = int(data.get("violations", 0))
        score -= violations * 1.5

        certifications = data.get("certifications") or []
        score += min(len(certifications) * 0.5, 2.0)

        lastInspection = data.get("last_inspection")
        if lastInspection:
            inspectionDate = datetime.strptime(str(lastInspection), "%Y-%m-%d")
            monthsAgo = (datetime.now() - inspectionDate).days / 30
            if monthsAgo > 12:
                score -= 2.0
            elif monthsAgo > 6:
                score -= 0.5

        return self._clamp(score)

    def calculateOperationalScore(self, supplierId: str) -> float:
        factors = self.operationalFactors.get(supplierId, self.defaultOperationalFactors)
        averagePerformance = sum(factors.values()) / len(factors)
        return self._clamp(averagePerformance * 10)

    def calculateMarketScore(self, data: dict[str, float]) -> float:
        volatilityScore = (1 - float(data["volatility"])) * 5
        growthScore = float(data["growth"]) * 3
        competitionScore = (1 - float(data["competition"])) * 2
        return self._clamp(volatilityScore + growthScore + competitionScore)

    def calculateConfidence(self, scores: dict[str, float]) -> float:
        dataPoints = sum(1 for score in scores.values() if score > 0)
        baseConfidence = min(1.0, dataPoints / 4)
        scoreRange = max(scores.values()) - min(scores.values())
        consistencyFactor = 1.0 - (scoreRange / 10)
        return round(baseConfidence * consistencyFactor, 2)

    def _clamp(self, score: float) -> float:
        return max(0.0, min(10.0, score))
