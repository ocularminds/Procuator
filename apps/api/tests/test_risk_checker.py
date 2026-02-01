import pytest

from procuator.skills.supplier_risk_checker import SupplierRiskChecker


@pytest.mark.asyncio
async def test_risk_checker_returns_expected_shape() -> None:
    skill = SupplierRiskChecker()
    result = await skill.execute({"supplier_id": "SUP-001", "industry": "technology"})

    assert set(result.keys()) >= {
        "risk_score",
        "risk_level",
        "component_scores",
        "risk_flags",
        "recommendations",
        "confidence",
        "last_updated",
        "supplier_id",
        "metadata",
    }

    assert result["supplier_id"] == "SUP-001"
    assert 0.0 <= float(result["risk_score"]) <= 10.0
    assert result["risk_level"] in {"LOW", "MEDIUM", "HIGH", "UNKNOWN"}

    await skill.aclose()
