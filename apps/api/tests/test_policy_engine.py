import pytest

from procuator.skills.policy_engine import PolicyEngine


def test_policy_engine_auto_approve_simple() -> None:
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
    assert result.policy_flags == []


@pytest.mark.parametrize(
    ("amount", "budget_remaining", "limit", "tx", "expected"),
    [
        (6000, 50000, 5000, 10, "REFER"),
        (1000, 50000, 5000, 0, "REFER"),
        (25000, 10000, 10000, 8, "DENY"),
    ],
)
def test_policy_engine_decisions(amount: float, budget_remaining: float, limit: float, tx: int, expected: str) -> None:
    engine = PolicyEngine()
    result = engine.evaluate(
        {
            "amount": amount,
            "budget_remaining": budget_remaining,
            "requester_approval_limit": limit,
            "urgency": "standard",
            "supplier_history": {"total_transactions": tx},
        }
    )
    assert result.decision == expected
