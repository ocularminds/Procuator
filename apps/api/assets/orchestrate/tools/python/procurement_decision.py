from __future__ import annotations

import os
import re
from typing import Any

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


def parse_money(value: Any) -> float:
    """Parse a money-like value into a float.

    Accepts inputs like:
    - 15000
    - 15000.50
    - "15000"
    - "$15,000"
    - "USD 15,000.00"
    - "15k" / "15K"

    Raises:
        ValueError: If the value cannot be parsed.
    """

    if value is None:
        raise ValueError("money value is required")

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()
    if not text:
        raise ValueError("money value is empty")

    text = text.upper()
    for code in ("USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "INR"):
        text = text.replace(code, " ")
    for sym in ("$", "€", "£", "¥"):
        text = text.replace(sym, " ")

    text = re.sub(r"\s+", "", text)

    magnitude = 1.0
    if text.endswith("K"):
        magnitude = 1_000.0
        text = text[:-1]
    elif text.endswith("M"):
        magnitude = 1_000_000.0
        text = text[:-1]

    text = text.replace(",", "")
    if not re.fullmatch(r"-?\d+(\.\d+)?", text):
        raise ValueError(f"unable to parse money value: {value!r}")

    return float(text) * magnitude


def _base_url() -> str:
    return os.environ.get("PROCUATOR_API_BASE_URL", "https://alease-overcapable-teachably.ngrok-free.dev").rstrip("/")


@tool()
def procurement_decision(
    supplier_id: str,
    amount: float | str,
    industry: str = "general",
    currency: str = "USD",
    budget_remaining: float | str = 0.0,
    requester_approval_limit: float | str = 0.0,
    urgency: str = "standard",
    supplier_history: dict[str, Any] | None = None,
    request_id: str | None = None,
    refresh_cache: bool = False,
) -> dict[str, Any]:
    """Compute a full procurement decision using the Procuator API.

    Args:
        supplier_id (str): Supplier identifier.
        amount (float | str): Requested amount. Accepts values like 15000 or "$15,000".
        industry (str): Supplier industry.
        currency (str): Currency code.
        budget_remaining (float | str): Remaining budget. Accepts values like 50000 or "$50,000".
        requester_approval_limit (float | str): Requester approval limit. Accepts values like 5000 or "$5,000".
        urgency (str): Standard or critical.
        supplier_history (dict[str, Any] | None): Optional supplier history metadata.
        request_id (str | None): Optional client request identifier.
        refresh_cache (bool): If true, bypass any cached risk result.

    Returns:
        dict[str, Any]: Decision payload including risk, policy, explanation, and HITL referral info.
    """

    payload: dict[str, Any] = {
        "supplier_id": supplier_id,
        "industry": industry,
        "amount": parse_money(amount),
        "currency": currency,
        "budget_remaining": parse_money(budget_remaining),
        "requester_approval_limit": parse_money(requester_approval_limit),
        "urgency": urgency,
        "supplier_history": supplier_history,
        "refresh_cache": refresh_cache,
    }
    if request_id:
        payload["request_id"] = request_id

    resp = requests.post(f"{_base_url()}/decision", json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()
