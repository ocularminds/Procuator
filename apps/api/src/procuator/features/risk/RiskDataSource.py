from __future__ import annotations

import logging
import os
from abc import ABC, abstractmethod
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)


class RiskDataSource(ABC):
    """Data contract required by supplier risk assessment."""

    @abstractmethod
    async def fetchFinancialData(self, supplierId: str) -> dict[str, Any]:
        """Return normalized financial data for a supplier."""

    @abstractmethod
    async def fetchComplianceData(self, supplierId: str) -> dict[str, Any]:
        """Return normalized compliance data for a supplier."""

    @abstractmethod
    async def fetchMarketData(self, industry: str) -> dict[str, float]:
        """Return normalized market data for an industry."""

    @abstractmethod
    async def close(self) -> None:
        """Release resources owned by the data source."""


class DefaultRiskDataSource(RiskDataSource):
    """Fetches remote financial data and serves demo compliance/market data."""

    complianceData: dict[str, dict[str, Any]] = {
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
    defaultComplianceData: dict[str, Any] = {
        "violations": 3,
        "certifications": [],
        "last_inspection": "2023-06-01",
    }
    marketData: dict[str, dict[str, float]] = {
        "technology": {"volatility": 0.7, "growth": 0.8, "competition": 0.6},
        "manufacturing": {"volatility": 0.4, "growth": 0.5, "competition": 0.7},
        "healthcare": {"volatility": 0.3, "growth": 0.9, "competition": 0.5},
        "retail": {"volatility": 0.8, "growth": 0.4, "competition": 0.9},
        "general": {"volatility": 0.5, "growth": 0.5, "competition": 0.5},
    }

    def __init__(self) -> None:
        self._session: aiohttp.ClientSession | None = None

    async def _getSession(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10))
        return self._session

    async def fetchFinancialData(self, supplierId: str) -> dict[str, Any]:
        apiUrl = os.getenv("FINANCIAL_API_URL", "https://api.example.com/financial")
        apiKey = os.getenv("API_KEY")
        session = await self._getSession()

        try:
            headers = {"Authorization": f"Bearer {apiKey}"} if apiKey else {}
            async with session.get(f"{apiUrl}/{supplierId}", headers=headers) as response:
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

    async def fetchComplianceData(self, supplierId: str) -> dict[str, Any]:
        return self.complianceData.get(supplierId, self.defaultComplianceData)

    async def fetchMarketData(self, industry: str) -> dict[str, float]:
        return self.marketData.get(industry, self.marketData["general"])

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()
