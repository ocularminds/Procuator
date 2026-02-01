from fastapi.testclient import TestClient

import procuator.api.app as api_app


def test_health() -> None:
    with TestClient(api_app.app) as client:
        resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_risk_check() -> None:
    with TestClient(api_app.app) as client:
        resp = client.post(
            "/risk-check",
            json={"supplier_id": "SUP-001", "industry": "technology"},
        )

    assert resp.status_code == 200
    body = resp.json()
    assert body["supplier_id"] == "SUP-001"
    assert 0.0 <= float(body["risk_score"]) <= 10.0


def test_risk_check_missing_supplier_id_returns_422() -> None:
    with TestClient(api_app.app) as client:
        resp = client.post("/risk-check", json={"industry": "technology"})
    assert resp.status_code == 422


def test_policy_check() -> None:
    with TestClient(api_app.app) as client:
        resp = client.post(
            "/policy-check",
            json={
                "amount": 1250,
                "budget_remaining": 50000,
                "requester_approval_limit": 5000,
                "urgency": "standard",
                "supplier_history": {"total_transactions": 10},
            },
        )

    assert resp.status_code == 200
    body = resp.json()
    assert body["policy_decision"] in {"APPROVE", "REFER", "DENY"}
    assert "policy_flags" in body


def test_lifespan_closes_skill_on_shutdown() -> None:
    closed = False

    class DummySkill:
        async def execute(self, _: dict) -> dict:
            return {}

        async def aclose(self) -> None:
            nonlocal closed
            closed = True

    original_skill = api_app._skill
    api_app._skill = DummySkill()  # type: ignore[assignment]
    try:
        with TestClient(api_app.app) as client:
            resp = client.get("/health")
            assert resp.status_code == 200
        assert closed is True
    finally:
        api_app._skill = original_skill


def test_demo_scenarios_endpoint_returns_three() -> None:
    with TestClient(api_app.app) as client:
        resp = client.get("/demo/scenarios")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["scenarios"]) == 3


def test_decision_creates_referral_for_refers() -> None:
    with TestClient(api_app.app) as client:
        resp = client.post(
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

        assert resp.status_code == 200
        body = resp.json()
        assert body["decision"] == "REFER"
        assert "human_in_the_loop" in body
        hitl = body["human_in_the_loop"]
        assert hitl["required"] is True
        referral_id = hitl["referral_id"]
        approve = client.post(f"/referrals/{referral_id}/approve")
        assert approve.status_code == 200
        assert approve.json()["status"] == "APPROVED"


def test_dashboard_and_analytics_endpoints() -> None:
    with TestClient(api_app.app) as client:
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


def test_hard_deny_is_policy_driven_budget_exceeded() -> None:
    with TestClient(api_app.app) as client:
        resp = client.post(
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

    assert resp.status_code == 200
    body = resp.json()
    assert body["decision"] == "DENY"
    assert body["policy"]["policy_decision"] == "DENY"
    assert "budget_exceeded" in (body["policy"]["policy_flags"] or [])
    assert body["human_in_the_loop"]["required"] is False
