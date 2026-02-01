from __future__ import annotations

import os
from typing import Any

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


def _base_url() -> str:
    return os.environ.get("PROCUATOR_API_BASE_URL", "https://alease-overcapable-teachably.ngrok-free.dev").rstrip("/")


@tool()
def demo_scenarios() -> dict[str, Any]:
    """Fetch built-in demo procurement scenarios from the Procuator API.

    Returns:
        dict[str, Any]: A payload containing the demo scenarios.
    """

    resp = requests.get(f"{_base_url()}/demo/scenarios", timeout=20)
    resp.raise_for_status()
    return resp.json()
