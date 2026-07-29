import pytest

from procuator.features.decision.DecisionRules import DecisionRules


@pytest.mark.parametrize(
    ("policyDecision", "riskLevel", "riskScore", "expected"),
    [
        ("DENY", "LOW", 9.0, "DENY"),
        ("REFER", "LOW", 9.0, "REFER"),
        ("APPROVE", "HIGH", 3.0, "REFER"),
        ("APPROVE", "MEDIUM", 5.5, "REFER"),
        ("APPROVE", "LOW", 8.0, "APPROVE"),
    ],
)
def testDecisionPriorityRemainsStable(
    policyDecision: str,
    riskLevel: str,
    riskScore: float,
    expected: str,
) -> None:
    assert DecisionRules().determine(policyDecision, riskLevel, riskScore) == expected


def testRiskFlagExtractionPreservesCodesAndText() -> None:
    risk = {
        "risk_flags": [
            {"code": "FIN_LOW", "message": "Financial health is low"},
            "manual_review",
        ]
    }

    assert DecisionRules().extractRiskFlags(risk) == ["FIN_LOW", "manual_review"]
