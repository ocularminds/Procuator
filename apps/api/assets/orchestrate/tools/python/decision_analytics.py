from __future__ import annotations

import os
from typing import Any

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


def _base_url() -> str:
    return os.environ.get("PROCUATOR_API_BASE_URL", "https://alease-overcapable-teachably.ngrok-free.dev").rstrip("/")


@tool()
def decision_analytics() -> dict[str, Any]:
    """Get decision analytics from the Procuator API.

    Returns:
        dict[str, Any]: Aggregate analytics derived from the audit trail.
    """

    resp = requests.get(f"{_base_url()}/analytics", timeout=20)
    resp.raise_for_status()
    return resp.json()
