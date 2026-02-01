from __future__ import annotations

import os
from typing import Any

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


def _base_url() -> str:
    return os.environ.get("PROCUATOR_API_BASE_URL", "https://alease-overcapable-teachably.ngrok-free.dev").rstrip("/")


@tool()
def list_referrals() -> dict[str, Any]:
    """List pending human-in-the-loop referrals.

    Returns:
        dict[str, Any]: Pending referrals and counts.
    """

    resp = requests.get(f"{_base_url()}/referrals", timeout=20)
    resp.raise_for_status()
    return resp.json()
