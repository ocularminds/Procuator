from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ApiModel(BaseModel):
    """Base model that maps camelCase code to the existing snake_case API."""

    model_config = ConfigDict(populate_by_name=False)

    def toPayload(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True)


class RiskCheckRequest(ApiModel):
    supplierId: str = Field(..., alias="supplier_id", examples=["SUP-001"])
    industry: str = Field(default="general", examples=["technology"])
    refreshCache: bool = Field(default=False, alias="refresh_cache")


class ProcurementDecisionRequest(ApiModel):
    requestId: str | None = Field(
        default=None,
        alias="request_id",
        examples=["REQ-20260131-001"],
    )
    supplierId: str = Field(..., alias="supplier_id", examples=["SUP-001"])
    industry: str = Field(default="general", examples=["technology"])
    amount: float = Field(..., examples=[1250.0])
    currency: str = Field(default="USD")
    budgetRemaining: float = Field(default=0.0, alias="budget_remaining")
    requesterApprovalLimit: float = Field(default=0.0, alias="requester_approval_limit")
    urgency: str = Field(default="standard", examples=["standard", "critical"])
    supplierHistory: dict[str, Any] | None = Field(default=None, alias="supplier_history")
    refreshCache: bool = Field(default=False, alias="refresh_cache")


class PolicyCheckRequest(ApiModel):
    amount: float = Field(..., examples=[1250.0])
    budgetRemaining: float = Field(default=0.0, alias="budget_remaining")
    requesterApprovalLimit: float = Field(default=0.0, alias="requester_approval_limit")
    urgency: str = Field(default="standard", examples=["standard", "critical"])
    supplierHistory: dict[str, Any] | None = Field(default=None, alias="supplier_history")
