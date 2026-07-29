from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from procuator.features.demo.DemoCatalog import DemoCatalog
from procuator.features.demo.ScenarioFactory import ScenarioFactory


class ProcurementTestDataGenerator:
    """Builds complete procurement demo datasets."""

    scenarioDefinitions = [
        (
            "Low Risk Auto-Approval",
            "Established supplier, low amount, within budget",
            "createLowRisk",
        ),
        (
            "Medium Risk Referral",
            "New supplier, medium amount, requires manager review",
            "createMediumRisk",
        ),
        (
            "High Risk Denial",
            "High-risk supplier, exceeded budget, compliance issues",
            "createHighRisk",
        ),
        (
            "Borderline Case",
            "Mixed signals - good supplier but near budget limit",
            "createBorderline",
        ),
        (
            "Emergency Request",
            "High urgency, established supplier, special approval needed",
            "createEmergency",
        ),
    ]

    def __init__(
        self,
        seed: int | None = 1337,
        now: datetime | None = None,
        catalog: DemoCatalog | None = None,
    ) -> None:
        self.seed = seed
        self.now = now or datetime.now(tz=UTC)
        self.catalog = catalog or DemoCatalog()
        self.scenarios = ScenarioFactory(self.now, seed, self.catalog)

    def generateTestCases(self, count: int = 10) -> list[dict[str, Any]]:
        testCases: list[dict[str, Any]] = []
        for index, (name, description, factoryMethod) in enumerate(self.scenarioDefinitions):
            scenario = getattr(self.scenarios, factoryMethod)()
            scenario["scenario_name"] = name
            scenario["scenario_description"] = description
            scenario["test_id"] = f"TEST-{index + 1:03d}"
            testCases.append(scenario)

        for index in range(max(0, count - len(self.scenarioDefinitions))):
            scenario = self.scenarios.createRandom()
            scenario["scenario_name"] = f"Random Case {index + 1}"
            scenario["scenario_description"] = "Generated random procurement request"
            scenario["test_id"] = f"RAND-{index + 1:03d}"
            testCases.append(scenario)

        return testCases

    def buildDataset(self, *, count: int = 10) -> dict[str, Any]:
        return {
            "test_cases": self.generateTestCases(count),
            "policy_rules": self.catalog.getPolicyRules(),
            "demo_script": self.catalog.getDemoScript(),
            "suppliers": self.catalog.suppliers,
            "metadata": {"generated_at": self.now.isoformat(), "version": "1.0"},
        }


class DatasetFileWriter:
    """Serializes generated datasets to JSON files."""

    def write(
        self,
        outputPath: str | Path,
        *,
        count: int = 10,
        seed: int | None = 1337,
    ) -> Path:
        path = Path(outputPath)
        data = ProcurementTestDataGenerator(seed=seed).buildDataset(count=count)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return path
