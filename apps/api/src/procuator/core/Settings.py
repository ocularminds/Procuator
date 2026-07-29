from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Runtime configuration injected by the deployment environment."""

    financialApiUrl: str = "https://api.example.com/financial"
    apiKeyEnvironmentName: str = "API_KEY"


defaultSettings = Settings()
