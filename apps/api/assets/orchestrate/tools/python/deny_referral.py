from __future__ import annotations

import os
from typing import Any

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


def _base_url() -> str:
    return os.environ.get("PROCUATOR_API_BASE_URL", "https://alease-overcapable-teachably.ngrok-free.dev").rstrip("/")


@tool()
def deny_referral(referral_id: str) -> dict[str, Any]:
    """Deny a pending referral.

    Args:
        referral_id (str): Referral identifier.

    Returns:
        dict[str, Any]: Updated referral status.
    """

    resp = requests.post(f"{_base_url()}/referrals/{referral_id}/deny", timeout=20)
    resp.raise_for_status()
    return resp.json()
