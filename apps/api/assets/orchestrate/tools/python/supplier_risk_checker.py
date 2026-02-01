from __future__ import annotations

import os
from typing import Any

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


def _base_url() -> str:
    return os.environ.get("PROCUATOR_API_BASE_URL", "https://alease-overcapable-teachably.ngrok-free.dev").rstrip("/")


@tool()
def supplier_risk_checker(supplier_id: str, industry: str = "general", refresh_cache: bool = False) -> dict[str, Any]:
    """Compute supplier risk using the Procuator API.

    Args:
        supplier_id (str): Supplier identifier.
        industry (str): Supplier industry.
        refresh_cache (bool): If true, bypass any cached risk result.

    Returns:
        dict[str, Any]: Risk score, level, and flags.
    """

    resp = requests.post(
        f"{_base_url()}/risk-check",
        json={"supplier_id": supplier_id, "industry": industry, "refresh_cache": refresh_cache},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()
