from fastapi.testclient import TestClient

from procuator.api.Application import createApp
from procuator.api.AppServices import AppServices


def testHealth() -> None:
    with TestClient(createApp()) as client:
        response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body


def testRiskCheck() -> None:
    with TestClient(createApp()) as client:
        response = client.post(
            "/risk-check",
            json={"supplier_id": "SUP-001", "industry": "technology"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["supplier_id"] == "SUP-001"
    assert 0.0 <= float(body["risk_score"]) <= 10.0


def testRiskCheckMissingSupplierIdReturns422() -> None:
    with TestClient(createApp()) as client:
        response = client.post("/risk-check", json={"industry": "technology"})
    assert response.status_code == 422


def testPolicyCheck() -> None:
    with TestClient(createApp()) as client:
        response = client.post(
            "/policy-check",
            json={
                "amount": 1250,
                "budget_remaining": 50000,
                "requester_approval_limit": 5000,
                "urgency": "standard",
                "supplier_history": {"total_transactions": 10},
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["policy_decision"] in {"APPROVE", "REFER", "DENY"}
    assert "policy_flags" in body


def testLifespanClosesSkillOnShutdown() -> None:
    isClosed = False

    class DummySkill:
        async def execute(self, _: dict, context: dict | None = None) -> dict:
            _ = context
            return {}

        async def close(self) -> None:
            nonlocal isClosed
            isClosed = True

    services = AppServices(riskChecker=DummySkill())  # type: ignore[arg-type]
    with TestClient(createApp(services)) as client:
        response = client.get("/health")
        assert response.status_code == 200
    assert isClosed is True


def testDemoScenariosEndpointReturnsThree() -> None:
    with TestClient(createApp()) as client:
        response = client.get("/demo/scenarios")
    assert response.status_code == 200
    body = response.json()
    assert len(body["scenarios"]) == 3


def testDecisionCreatesReferralForRefers() -> None:
    with TestClient(createApp()) as client:
        response = client.post(
            "/decision",
            json={
                "supplier_id": "SUP-009",
                "industry": "technology",
                "amount": 15000,
                "budget_remaining": 50000,
                "requester_approval_limit": 5000,
                "urgency": "standard",
                "supplier_history": {"total_transactions": 0},
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert body["decision"] == "REFER"
        assert "human_in_the_loop" in body
        humanReview = body["human_in_the_loop"]
        assert humanReview["required"] is True
        referralId = humanReview["referral_id"]
        approve = client.post(f"/referrals/{referralId}/approve")
        assert approve.status_code == 200
        assert approve.json()["status"] == "APPROVED"


def testDashboardAndAnalyticsEndpoints() -> None:
    with TestClient(createApp()) as client:
        client.post(
            "/decision",
            json={
                "supplier_id": "SUP-001",
                "industry": "technology",
                "amount": 1250,
                "budget_remaining": 50000,
                "requester_approval_limit": 5000,
                "urgency": "standard",
                "supplier_history": {"total_transactions": 10},
            },
        )

        analytics = client.get("/analytics")
        assert analytics.status_code == 200
        stats = analytics.json()
        assert "total" in stats

        dash = client.get("/dashboard")
        assert dash.status_code == 200
        assert "Procuator Decision Analytics" in dash.text


def testHardDenyIsPolicyDrivenBudgetExceeded() -> None:
    with TestClient(createApp()) as client:
        response = client.post(
            "/decision",
            json={
                "supplier_id": "SUP-004",
                "industry": "retail",
                "amount": 25000,
                "budget_remaining": 10000,
                "requester_approval_limit": 10000,
                "urgency": "standard",
                "supplier_history": {"total_transactions": 8},
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "DENY"
    assert body["policy"]["policy_decision"] == "DENY"
    assert "budget_exceeded" in (body["policy"]["policy_flags"] or [])
    assert body["human_in_the_loop"]["required"] is False
