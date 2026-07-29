import pytest

from procuator.features.policy.PolicyEngine import PolicyEngine


def testPolicyEngineAutoApproveSimple() -> None:
    engine = PolicyEngine()
    result = engine.evaluate(
        {
            "amount": 1000,
            "budget_remaining": 50000,
            "requester_approval_limit": 5000,
            "urgency": "standard",
            "supplier_history": {"total_transactions": 10},
        }
    )
    assert result.decision == "APPROVE"
    assert result.policyFlags == []


@pytest.mark.parametrize(
    ("amount", "budgetRemaining", "limit", "transactions", "expected"),
    [
        (6000, 50000, 5000, 10, "REFER"),
        (1000, 50000, 5000, 0, "REFER"),
        (25000, 10000, 10000, 8, "DENY"),
    ],
)
def testPolicyEngineDecisions(
    amount: float,
    budgetRemaining: float,
    limit: float,
    transactions: int,
    expected: str,
) -> None:
    engine = PolicyEngine()
    result = engine.evaluate(
        {
            "amount": amount,
            "budget_remaining": budgetRemaining,
            "requester_approval_limit": limit,
            "urgency": "standard",
            "supplier_history": {"total_transactions": transactions},
        }
    )
    assert result.decision == expected
