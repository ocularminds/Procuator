from __future__ import annotations

import re
from typing import Any


_CURRENCY_SYMBOLS = {
    "$": "USD",
    "€": "EUR",
    "£": "GBP",
    "¥": "JPY",
}


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

    # Remove common currency codes and symbols; we only need the numeric amount.
    # Keep digits, '.', ',', '-', and magnitude suffixes.
    # Examples: "$15,000" -> "15,000"; "USD 15k" -> "15k"
    text = text.upper()
    for code in ("USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "INR"):
        text = text.replace(code, " ")
    for sym in _CURRENCY_SYMBOLS.keys():
        text = text.replace(sym, " ")

    text = text.strip().replace("_", " ")
    text = re.sub(r"\s+", "", text)

    magnitude = 1.0
    if text.endswith("K"):
        magnitude = 1_000.0
        text = text[:-1]
    elif text.endswith("M"):
        magnitude = 1_000_000.0
        text = text[:-1]

    # Drop thousands separators.
    text = text.replace(",", "")

    if not re.fullmatch(r"-?\d+(\.\d+)?", text):
        raise ValueError(f"unable to parse money value: {value!r}")

    return float(text) * magnitude
