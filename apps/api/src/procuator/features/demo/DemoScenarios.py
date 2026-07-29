from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from procuator.features.demo.ScenarioFactory import ScenarioFactory


class DemoScenarioService:
    """Provides the three curated scenarios exposed by the API."""

    def __init__(self, seed: int = 1337, now: datetime | None = None) -> None:
        self._seed = seed
        self._now = now

    def getScenarios(self) -> list[dict[str, Any]]:
        factory = ScenarioFactory(self._now or datetime.now(tz=UTC), self._seed)
        definitions = [
            (
                factory.createLowRisk(),
                "Simple auto-approve",
                "Low amount, within budget and limits; established supplier",
            ),
            (
                factory.createMediumRisk(),
                "Complex referral case",
                "New supplier + amount exceeds requester approval limit",
            ),
            (
                factory.createHighRisk(),
                "Hard deny with explanation",
                "Budget exceeded and high-risk supplier signals",
            ),
        ]

        scenarios: list[dict[str, Any]] = []
        for index, (scenario, name, description) in enumerate(definitions, start=1):
            scenario["scenario_name"] = name
            scenario["scenario_description"] = description
            scenario["test_id"] = f"DEMO-{index:03d}"
            scenarios.append(scenario)
        return scenarios
