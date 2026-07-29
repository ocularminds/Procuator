from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class RiskCacheEntry:
    cachedAt: datetime
    data: dict[str, Any]


@dataclass(frozen=True)
class RiskAssessment:
    supplierId: str
    riskScore: float
    riskLevel: str
    componentScores: dict[str, float]
    riskFlags: list[dict[str, Any]]
    recommendations: list[str]
    confidence: float
    updatedAt: str
    weights: dict[str, float]
    version: str

    def toDict(self) -> dict[str, Any]:
        return {
            "risk_score": round(self.riskScore, 2),
            "risk_level": self.riskLevel,
            "component_scores": {key: round(value, 2) for key, value in self.componentScores.items()},
            "risk_flags": self.riskFlags,
            "recommendations": self.recommendations,
            "confidence": self.confidence,
            "last_updated": self.updatedAt,
            "supplier_id": self.supplierId,
            "metadata": {
                "weights_applied": self.weights,
                "data_sources": ["financial_api", "compliance_db", "market_index"],
                "calculation_version": self.version,
            },
        }
