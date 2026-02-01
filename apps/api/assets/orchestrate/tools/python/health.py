from __future__ import annotations

import os
from typing import Any

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


def _base_url() -> str:
    return os.environ.get("PROCUATOR_API_BASE_URL", "https://alease-overcapable-teachably.ngrok-free.dev").rstrip("/")


@tool()
def health() -> dict[str, Any]:
    """Check Procuator API health.

    Returns:
        dict[str, Any]: Health payload containing status and version.
    """

    resp = requests.get(f"{_base_url()}/health", timeout=10)
    resp.raise_for_status()
    return resp.json()
