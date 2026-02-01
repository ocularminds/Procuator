from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)


class Skill:
    """Minimal skill base class.

    Watsonx Orchestrate has its own SDK/runtime; this base class keeps local
    development/test usage consistent.
    """

    name: str
    version: str
    description: str

    async def execute(self, inputs: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
        raise NotImplementedError


@dataclass(frozen=True)
class CacheEntry:
    timestamp: datetime
    data: dict[str, Any]


class SupplierRiskChecker(Skill):
    """Computes a composite supplier risk score (0-10)."""

    name = "supplier_risk_checker"
    version = "1.2.0"
    description = "Comprehensive supplier risk assessment with component scoring"

    WEIGHTS: dict[str, float] = {
        "financial": 0.40,
        "compliance": 0.25,
        "operational": 0.20,
        "market": 0.15,
    }

    THRESHOLDS: dict[str, float] = {
        "low_risk": 7.0,
        "medium_risk": 4.0,
        "high_risk": 0.0,
    }

    def __init__(self, *, cache_ttl: timedelta = timedelta(hours=1)) -> None:
        self._cache_ttl = cache_ttl
        self._cache: dict[str, CacheEntry] = {}
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10))
        return self._session

    async def execute(self, inputs: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
        supplier_id = str(inputs["supplier_id"])
        industry = str(inputs.get("industry", "general"))
        refresh = bool(inputs.get("refresh_cache", False))

        cache_key = f"{supplier_id}_{industry}"
        if not refresh:
            cached = self._cache.get(cache_key)
            if cached and datetime.now() - cached.timestamp < self._cache_ttl:
                return cached.data

        try:
            financial_data, compliance_data, market_data = await asyncio.gather(
                self._fetch_financial_data(supplier_id),
                self._fetch_compliance_data(supplier_id),
                self._fetch_market_data(industry),
                return_exceptions=True,
            )

            financial_data = self._handle_fetch_error(financial_data, "financial")
            compliance_data = self._handle_fetch_error(compliance_data, "compliance")
            market_data = self._handle_fetch_error(market_data, "market")

            component_scores = {
                "financial": self._calculate_financial_score(financial_data),
                "compliance": self._calculate_compliance_score(compliance_data),
                "operational": self._calculate_operational_score(supplier_id),
                "market": self._calculate_market_score(market_data),
            }

            weighted_score = sum(component_scores[k] * self.WEIGHTS[k] for k in component_scores)
            flags = self._generate_risk_flags(component_scores, weighted_score)
            recommendations = self._generate_recommendations(component_scores, flags, weighted_score)

            result: dict[str, Any] = {
                "risk_score": round(weighted_score, 2),
                "risk_level": self._get_risk_level(weighted_score),
                "component_scores": {k: round(v, 2) for k, v in component_scores.items()},
                "risk_flags": flags,
                "recommendations": recommendations,
                "confidence": self._calculate_confidence(component_scores),
                "last_updated": datetime.now().isoformat(),
                "supplier_id": supplier_id,
                "metadata": {
                    "weights_applied": self.WEIGHTS,
                    "data_sources": ["financial_api", "compliance_db", "market_index"],
                    "calculation_version": self.version,
                },
            }

            self._cache[cache_key] = CacheEntry(timestamp=datetime.now(), data=result)
            return result

        except Exception as exc:  # noqa: BLE001
            logger.exception("Risk assessment failed")
            return self._generate_fallback_result(inputs, str(exc))

    async def _fetch_financial_data(self, supplier_id: str) -> dict[str, Any]:
        api_url = os.getenv("FINANCIAL_API_URL", "https://api.example.com/financial")
        api_key = os.getenv("API_KEY")

        session = await self._get_session()
        try:
            headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
            async with session.get(f"{api_url}/{supplier_id}", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "revenue_12m": data.get("revenue", 1_000_000),
                        "profit_margin": data.get("profit_margin", 0.15),
                        "debt_to_equity": data.get("debt_ratio", 0.5),
                        "current_ratio": data.get("current_ratio", 2.0),
                        "credit_rating": data.get("credit_rating", "BBB"),
                        "last_audit_date": data.get("audit_date", "2023-12-01"),
                        "audit_opinion": data.get("audit_opinion", "clean"),
                    }

                raise RuntimeError(f"Financial API error: {response.status}")

        except Exception as exc:  # noqa: BLE001
            logger.warning("Financial data fetch failed: %s", exc)
            return {
                "revenue_12m": 0,
                "profit_margin": 0,
                "debt_to_equity": 1.0,
                "current_ratio": 1.0,
                "credit_rating": "D",
                "last_audit_date": None,
                "audit_opinion": "unknown",
            }

    async def _fetch_compliance_data(self, supplier_id: str) -> dict[str, Any]:
        compliance_db = {
            "SUP-001": {
                "violations": 0,
                "certifications": ["ISO9001", "ISO14001"],
                "last_inspection": "2024-01-15",
            },
            "SUP-002": {"violations": 2, "certifications": ["ISO9001"], "last_inspection": "2023-11-20"},
            "SUP-003": {
                "violations": 0,
                "certifications": ["ISO9001", "ISO45001", "SOC2"],
                "last_inspection": "2024-02-01",
            },
            "SUP-004": {"violations": 1, "certifications": [], "last_inspection": "2023-09-10"},
            "SUP-005": {"violations": 0, "certifications": ["ISO9001"], "last_inspection": "2024-01-30"},
        }

        default = {"violations": 3, "certifications": [], "last_inspection": "2023-06-01"}
        return compliance_db.get(supplier_id, default)

    async def _fetch_market_data(self, industry: str) -> dict[str, float]:
        market_risk_scores: dict[str, dict[str, float]] = {
            "technology": {"volatility": 0.7, "growth": 0.8, "competition": 0.6},
            "manufacturing": {"volatility": 0.4, "growth": 0.5, "competition": 0.7},
            "healthcare": {"volatility": 0.3, "growth": 0.9, "competition": 0.5},
            "retail": {"volatility": 0.8, "growth": 0.4, "competition": 0.9},
            "general": {"volatility": 0.5, "growth": 0.5, "competition": 0.5},
        }
        return market_risk_scores.get(industry, market_risk_scores["general"])

    def _calculate_financial_score(self, data: dict[str, Any]) -> float:
        score = 5.0

        if data.get("revenue_12m", 0) > 10_000_000:
            score += 2.0
        elif data.get("revenue_12m", 0) > 1_000_000:
            score += 1.0
        elif data.get("revenue_12m", 0) == 0:
            score -= 3.0

        profit_margin = float(data.get("profit_margin", 0))
        if profit_margin > 0.2:
            score += 1.5
        elif profit_margin > 0.1:
            score += 0.5
        elif profit_margin < 0:
            score -= 2.0

        debt_to_equity = float(data.get("debt_to_equity", 1.0))
        if debt_to_equity < 0.3:
            score += 1.0
        elif debt_to_equity > 1.0:
            score -= 1.5

        current_ratio = float(data.get("current_ratio", 1.0))
        if current_ratio > 2.0:
            score += 1.0
        elif current_ratio < 1.0:
            score -= 2.0

        credit_scores = {
            "AAA": 2.0,
            "AA": 1.5,
            "A": 1.0,
            "BBB": 0.5,
            "BB": -0.5,
            "B": -1.5,
            "CCC": -3.0,
            "D": -5.0,
        }
        score += credit_scores.get(str(data.get("credit_rating", "")), -2.0)

        audit_opinion = str(data.get("audit_opinion", "unknown"))
        if audit_opinion == "clean":
            score += 1.0
        elif audit_opinion == "qualified":
            score -= 0.5
        elif audit_opinion == "adverse":
            score -= 3.0

        return max(0.0, min(10.0, score))

    def _calculate_compliance_score(self, data: dict[str, Any]) -> float:
        score = 7.0

        violations = int(data.get("violations", 0))
        score -= violations * 1.5

        certifications = data.get("certifications") or []
        certification_bonus = len(certifications) * 0.5
        score += min(certification_bonus, 2.0)

        last_inspection = data.get("last_inspection")
        if last_inspection:
            last_dt = datetime.strptime(str(last_inspection), "%Y-%m-%d")
            months_ago = (datetime.now() - last_dt).days / 30
            if months_ago > 12:
                score -= 2.0
            elif months_ago > 6:
                score -= 0.5

        return max(0.0, min(10.0, score))

    def _calculate_operational_score(self, supplier_id: str) -> float:
        operational_factors: dict[str, dict[str, float]] = {
            "SUP-001": {"delivery_reliability": 0.95, "quality_score": 0.92, "response_time": 0.88},
            "SUP-002": {"delivery_reliability": 0.85, "quality_score": 0.78, "response_time": 0.72},
            "SUP-003": {"delivery_reliability": 0.98, "quality_score": 0.96, "response_time": 0.94},
            "SUP-004": {"delivery_reliability": 0.70, "quality_score": 0.65, "response_time": 0.60},
            "SUP-005": {"delivery_reliability": 0.90, "quality_score": 0.85, "response_time": 0.82},
        }

        factors = operational_factors.get(
            supplier_id,
            {"delivery_reliability": 0.80, "quality_score": 0.75, "response_time": 0.70},
        )

        avg_performance = sum(factors.values()) / len(factors)
        return max(0.0, min(10.0, avg_performance * 10))

    def _calculate_market_score(self, market_data: dict[str, float]) -> float:
        volatility_score = (1 - float(market_data["volatility"])) * 5
        growth_score = float(market_data["growth"]) * 3
        competition_score = (1 - float(market_data["competition"])) * 2
        total = volatility_score + growth_score + competition_score
        return max(0.0, min(10.0, total))

    def _generate_risk_flags(self, scores: dict[str, float], total_score: float) -> list[dict[str, Any]]:
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

        if total_score < self.THRESHOLDS["medium_risk"]:
            flags.append(
                {
                    "code": "OVERALL_HIGH_RISK",
                    "severity": "CRITICAL",
                    "message": f"Overall risk score ({total_score:.2f}) indicates high risk",
                    "component": "overall",
                    "score": total_score,
                }
            )

        return flags

    def _generate_recommendations(self, scores: dict[str, float], flags: list[Any], total_score: float) -> list[str]:
        recommendations: list[str] = []

        if scores["financial"] < 4.0:
            recommendations.append("Request recent financial statements for review")
            recommendations.append("Consider phased payments or escrow arrangement")

        if scores["compliance"] < 5.0:
            recommendations.append("Verify compliance certifications are current")
            recommendations.append("Schedule compliance audit within 90 days")

        if scores["operational"] < 6.0:
            recommendations.append("Implement delivery performance monitoring")
            recommendations.append("Establish quality assurance checkpoints")

        if total_score < 5.0:
            recommendations.append("High risk - require additional collateral or guarantees")
            recommendations.append("Limit contract value and duration")

        if not flags and total_score > 7.0:
            recommendations.append("Low risk supplier - consider preferred vendor status")

        return recommendations

    def _get_risk_level(self, score: float) -> str:
        if score >= self.THRESHOLDS["low_risk"]:
            return "LOW"
        if score >= self.THRESHOLDS["medium_risk"]:
            return "MEDIUM"
        return "HIGH"

    def _calculate_confidence(self, scores: dict[str, float]) -> float:
        data_points = sum(1 for score in scores.values() if score > 0)
        base_confidence = min(1.0, data_points / 4)
        score_range = max(scores.values()) - min(scores.values())
        consistency_factor = 1.0 - (score_range / 10)
        return round(base_confidence * consistency_factor, 2)

    def _handle_fetch_error(self, data: Any, data_type: str) -> dict[str, Any]:
        if isinstance(data, Exception):
            logger.warning("Failed to fetch %s data: %s", data_type, data)
            return {"error": str(data), "default_used": True}
        return data

    def _generate_fallback_result(self, inputs: dict[str, Any], error: str) -> dict[str, Any]:
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

    async def aclose(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()


def create_skill() -> SupplierRiskChecker:
    return SupplierRiskChecker()
