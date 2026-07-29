from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Path
from fastapi.responses import HTMLResponse

from procuator import __version__
from procuator.api.ApiModels import (
    PolicyCheckRequest,
    ProcurementDecisionRequest,
    RiskCheckRequest,
)
from procuator.api.AppServices import AppServices
from procuator.api.DashboardRenderer import DashboardRenderer
from procuator.features.demo.DemoScenarios import DemoScenarioService


class ApiController:
    """Registers HTTP routes and delegates all behavior to feature services."""

    def __init__(
        self,
        services: AppServices,
        scenarios: DemoScenarioService | None = None,
        dashboard: DashboardRenderer | None = None,
    ) -> None:
        self._services = services
        self._scenarios = scenarios or DemoScenarioService()
        self._dashboard = dashboard or DashboardRenderer()

    def createRouter(self) -> APIRouter:
        router = APIRouter()
        router.add_api_route("/health", self.health, methods=["GET"])
        router.add_api_route("/risk-check", self.riskCheck, methods=["POST"])
        router.add_api_route("/policy-check", self.policyCheck, methods=["POST"])
        router.add_api_route("/demo/scenarios", self.demoScenarios, methods=["GET"])
        router.add_api_route("/decision", self.decide, methods=["POST"])
        router.add_api_route("/referrals", self.listReferrals, methods=["GET"])
        router.add_api_route(
            "/referrals/{referral_id}/approve",
            self.approveReferral,
            methods=["POST"],
        )
        router.add_api_route(
            "/referrals/{referral_id}/deny",
            self.denyReferral,
            methods=["POST"],
        )
        router.add_api_route("/analytics", self.analytics, methods=["GET"])
        router.add_api_route(
            "/dashboard",
            self.dashboard,
            methods=["GET"],
            response_class=HTMLResponse,
        )
        return router

    async def health(self) -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    async def riskCheck(self, payload: RiskCheckRequest) -> dict[str, Any]:
        return await self._services.riskChecker.execute(payload.toPayload())

    async def policyCheck(self, payload: PolicyCheckRequest) -> dict[str, Any]:
        return await self._services.policyEngine.execute(payload.toPayload())

    async def demoScenarios(self) -> dict[str, Any]:
        return {"scenarios": self._scenarios.getScenarios()}

    async def decide(self, payload: ProcurementDecisionRequest) -> dict[str, Any]:
        return await self._services.decisionService.decide(payload.toPayload())

    async def listReferrals(self) -> dict[str, Any]:
        return self._services.referralService.listPending()

    async def approveReferral(
        self,
        referralId: Annotated[str, Path(alias="referral_id")],
    ) -> dict[str, Any]:
        return await self._services.referralService.approve(referralId)

    async def denyReferral(
        self,
        referralId: Annotated[str, Path(alias="referral_id")],
    ) -> dict[str, Any]:
        return await self._services.referralService.deny(referralId)

    async def analytics(self) -> dict[str, Any]:
        return self._services.auditor.analytics()

    async def dashboard(self) -> str:
        return self._dashboard.render(self._services.auditor.analytics())
