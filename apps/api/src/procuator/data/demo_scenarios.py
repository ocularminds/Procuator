from __future__ import annotations

from typing import Any

from procuator.data.generator import ProcurementTestDataGenerator


def demo_scenarios(*, seed: int = 1337) -> list[dict[str, Any]]:
    """Return the 3 core scenarios requested for the demo."""

    gen = ProcurementTestDataGenerator(seed=seed)

    auto = gen._low_risk_template()
    auto["scenario_name"] = "Simple auto-approve"
    auto["scenario_description"] = "Low amount, within budget and limits; established supplier"

    referral = gen._medium_risk_template()
    referral["scenario_name"] = "Complex referral case"
    referral["scenario_description"] = "New supplier + amount exceeds requester approval limit"

    deny = gen._high_risk_template()
    deny["scenario_name"] = "Hard deny with explanation"
    deny["scenario_description"] = "Budget exceeded and high-risk supplier signals"

    for i, t in enumerate([auto, referral, deny], start=1):
        t["test_id"] = f"DEMO-{i:03d}"

    return [auto, referral, deny]
