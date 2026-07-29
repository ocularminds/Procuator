from __future__ import annotations

from typing import Any


class RiskAdvisor:
    """Classifies scores and derives risk guidance."""

    thresholds: dict[str, float] = {
        "low_risk": 7.0,
        "medium_risk": 4.0,
        "high_risk": 0.0,
    }

    def getRiskLevel(self, score: float) -> str:
        if score >= self.thresholds["low_risk"]:
            return "LOW"
        if score >= self.thresholds["medium_risk"]:
            return "MEDIUM"
        return "HIGH"

    def generateFlags(self, scores: dict[str, float], totalScore: float) -> list[dict[str, Any]]:
        flags: list[dict[str, Any]] = []

        if scores["financial"] < 3.0:
            flags.append(
                {
                    "code": "FIN_LOW",
                    "severity": "HIGH",
                    "message": "Financial health is critically low",
                    "component": "financial",
                    "score": scores["financial"],
                }
            )
        if scores["compliance"] < 4.0:
            flags.append(
                {
                    "code": "COMP_LOW",
                    "severity": "MEDIUM",
                    "message": "Compliance score below acceptable threshold",
                    "component": "compliance",
                    "score": scores["compliance"],
                }
            )
        if scores["operational"] < 5.0:
            flags.append(
                {
                    "code": "OP_LOW",
                    "severity": "MEDIUM",
                    "message": "Operational performance needs improvement",
                    "component": "operational",
                    "score": scores["operational"],
                }
            )
        if totalScore < self.thresholds["medium_risk"]:
            flags.append(
                {
                    "code": "OVERALL_HIGH_RISK",
                    "severity": "CRITICAL",
                    "message": f"Overall risk score ({totalScore:.2f}) indicates high risk",
                    "component": "overall",
                    "score": totalScore,
                }
            )

        return flags

    def generateRecommendations(
        self,
        scores: dict[str, float],
        flags: list[dict[str, Any]],
        totalScore: float,
    ) -> list[str]:
        recommendations: list[str] = []

        if scores["financial"] < 4.0:
            recommendations.extend(
                [
                    "Request recent financial statements for review",
                    "Consider phased payments or escrow arrangement",
                ]
            )
        if scores["compliance"] < 5.0:
            recommendations.extend(
                [
                    "Verify compliance certifications are current",
                    "Schedule compliance audit within 90 days",
                ]
            )
        if scores["operational"] < 6.0:
            recommendations.extend(
                [
                    "Implement delivery performance monitoring",
                    "Establish quality assurance checkpoints",
                ]
            )
        if totalScore < 5.0:
            recommendations.extend(
                [
                    "High risk - require additional collateral or guarantees",
                    "Limit contract value and duration",
                ]
            )
        if not flags and totalScore > 7.0:
            recommendations.append("Low risk supplier - consider preferred vendor status")

        return recommendations
