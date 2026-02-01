from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Runtime configuration.

    This is intentionally minimal; IBM Cloud Code Engine can inject env vars.
    """

    financial_api_url: str = "https://api.example.com/financial"
    api_key_env: str = "API_KEY"


DEFAULT_SETTINGS = Settings()
