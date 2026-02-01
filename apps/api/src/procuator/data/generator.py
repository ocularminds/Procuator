from __future__ import annotations

import json
import random
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any


@dataclass
class ProcurementTestDataGenerator:
    """Generate realistic test data for demo and automated tests."""

    seed: int | None = 1337
    now: datetime | None = None

    def __post_init__(self) -> None:
        if self.seed is not None:
            random.seed(self.seed)
        if self.now is None:
            self.now = datetime.now(tz=UTC)

        self.departments = [
            "Engineering",
            "Marketing",
            "Operations",
            "HR",
            "Finance",
            "IT",
            "R&D",
            "Sales",
            "Facilities",
        ]

        self.categories = [
            "Software Licenses",
            "Hardware",
            "Office Supplies",
            "Consulting Services",
            "Travel",
            "Training",
            "Marketing Materials",
            "Equipment",
            "Cloud Services",
        ]

        self.suppliers = {
            "SUP-001": {"name": "TechCorp Solutions", "industry": "technology", "risk_profile": "low"},
            "SUP-002": {"name": "Global Manufacturing Inc", "industry": "manufacturing", "risk_profile": "medium"},
            "SUP-003": {"name": "MediCare Supplies", "industry": "healthcare", "risk_profile": "low"},
            "SUP-004": {"name": "Retail Dynamics", "industry": "retail", "risk_profile": "high"},
            "SUP-005": {"name": "General Services Co", "industry": "general", "risk_profile": "medium"},
            "SUP-006": {"name": "Cloud Innovators", "industry": "technology", "risk_profile": "low"},
            "SUP-007": {"name": "Office World", "industry": "retail", "risk_profile": "low"},
            "SUP-008": {"name": "Consulting Partners", "industry": "professional", "risk_profile": "medium"},
            "SUP-009": {"name": "New Startup Tech", "industry": "technology", "risk_profile": "high"},
            "SUP-010": {"name": "Budget Supplies Inc", "industry": "manufacturing", "risk_profile": "high"},
        }

    def generate_test_cases(self, count: int = 10) -> list[dict[str, Any]]:
        scenarios = [
            (
                "Low Risk Auto-Approval",
                "Established supplier, low amount, within budget",
                self._low_risk_template(),
            ),
            (
                "Medium Risk Referral",
                "New supplier, medium amount, requires manager review",
                self._medium_risk_template(),
            ),
            (
                "High Risk Denial",
                "High-risk supplier, exceeded budget, compliance issues",
                self._high_risk_template(),
            ),
            (
                "Borderline Case",
                "Mixed signals - good supplier but near budget limit",
                self._borderline_template(),
            ),
            (
                "Emergency Request",
                "High urgency, established supplier, special approval needed",
                self._emergency_template(),
            ),
        ]

        test_cases: list[dict[str, Any]] = []
        for i, (name, desc, template) in enumerate(scenarios):
            template["scenario_name"] = name
            template["scenario_description"] = desc
            template["test_id"] = f"TEST-{i + 1:03d}"
            test_cases.append(template)

        for i in range(max(0, count - len(scenarios))):
            test_case = self._random_template()
            test_case["scenario_name"] = f"Random Case {i + 1}"
            test_case["scenario_description"] = "Generated random procurement request"
            test_case["test_id"] = f"RAND-{i + 1:03d}"
            test_cases.append(test_case)

        return test_cases

    def generate_policy_rules(self) -> dict[str, Any]:
        return {
            "approval_matrix": {
                "Engineering": {
                    "Software Licenses": {"auto_approve_limit": 5000, "max_limit": 50000},
                    "Hardware": {"auto_approve_limit": 10000, "max_limit": 100000},
                    "Cloud Services": {"auto_approve_limit": 3000, "max_limit": 30000},
                },
                "Marketing": {
                    "Marketing Materials": {"auto_approve_limit": 3000, "max_limit": 30000},
                    "Consulting Services": {"auto_approve_limit": 5000, "max_limit": 50000},
                },
                "IT": {
                    "Hardware": {"auto_approve_limit": 10000, "max_limit": 100000},
                    "Software Licenses": {"auto_approve_limit": 5000, "max_limit": 50000},
                    "Cloud Services": {"auto_approve_limit": 5000, "max_limit": 50000},
                },
            },
            "risk_thresholds": {"auto_approve_max_risk": 4.0, "refer_max_risk": 7.0, "deny_min_risk": 7.1},
            "special_rules": [
                {
                    "rule_id": "EMERGENCY_OVERRIDE",
                    "condition": "urgency == 'critical' AND supplier_risk < 5",
                    "action": "AUTO_APPROVE",
                    "limit_multiplier": 2.0,
                },
                {
                    "rule_id": "NEW_SUPPLIER_LIMIT",
                    "condition": "supplier_transactions < 3",
                    "action": "LIMIT_AMOUNT",
                    "max_amount": 5000,
                },
                {
                    "rule_id": "BUDGET_EXCEEDED",
                    "condition": "amount > budget_remaining",
                    "action": "DENY",
                    "exception": "EMERGENCY_OVERRIDE",
                },
            ],
            "compliance_requirements": [
                "ISO9001 for manufacturing suppliers",
                "SOC2 for cloud service providers",
                "GDPR compliance for EU data handlers",
                "Environmental certification for large equipment",
            ],
        }

    def generate_demo_script(self) -> dict[str, Any]:
        return {
            "title": "IBM watsonx Orchestrate: AI-Powered Procurement Decision Agent",
            "duration": "7 minutes",
            "sections": [
                {
                    "title": "Introduction",
                    "duration": "60 seconds",
                    "content": [
                        "Problem: Manual procurement approvals are slow and inconsistent",
                        "Solution: AI agent that evaluates requests against policies, risk, and budgets",
                        "Built with: IBM watsonx Orchestrate for agentic AI workflows",
                    ],
                }
            ],
        }

    def build_dataset(self, *, count: int = 10) -> dict[str, Any]:
        return {
            "test_cases": self.generate_test_cases(count),
            "policy_rules": self.generate_policy_rules(),
            "demo_script": self.generate_demo_script(),
            "suppliers": self.suppliers,
            "metadata": {"generated_at": self.now.isoformat(), "version": "1.0"},
        }

    def save_dataset(self, output_path: Path, *, count: int = 10) -> dict[str, Any]:
        data = self.build_dataset(count=count)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return data

    # Templates

    def _low_risk_template(self) -> dict[str, Any]:
        assert self.now is not None
        return {
            "request_id": f"REQ-{self.now.strftime('%Y%m%d')}-001",
            "requester_name": "Alex Johnson",
            "requester_email": "alex.johnson@company.com",
            "department": "Engineering",
            "supplier_id": "SUP-001",
            "supplier_name": "TechCorp Solutions",
            "amount": 1250.00,
            "currency": "USD",
            "category": "Software Licenses",
            "description": "Annual license renewal for development tools",
            "urgency": "standard",
            "required_by": (self.now + timedelta(days=30)).date().isoformat(),
            "budget_remaining": 50000.00,
            "requester_approval_limit": 5000.00,
            "supplier_history": {
                "total_transactions": 15,
                "total_amount": 85000.00,
                "avg_delivery_time": 2.5,
                "quality_rating": 4.8,
            },
            "policy_flags": [],
            "attachments": ["quote_2024.pdf"],
            "expected_decision": "APPROVE",
            "expected_confidence": "high",
        }

    def _medium_risk_template(self) -> dict[str, Any]:
        assert self.now is not None
        return {
            "request_id": f"REQ-{self.now.strftime('%Y%m%d')}-002",
            "requester_name": "Maria Rodriguez",
            "requester_email": "maria.rodriguez@company.com",
            "department": "Marketing",
            "supplier_id": "SUP-009",
            "supplier_name": "New Startup Tech",
            "amount": 8500.00,
            "currency": "USD",
            "category": "Marketing Materials",
            "description": "New vendor for promotional items - first order",
            "urgency": "standard",
            "required_by": (self.now + timedelta(days=45)).date().isoformat(),
            "budget_remaining": 15000.00,
            "requester_approval_limit": 5000.00,
            "supplier_history": {
                "total_transactions": 1,
                "total_amount": 1500.00,
                "avg_delivery_time": 7.0,
                "quality_rating": 4.2,
            },
            "policy_flags": ["new_supplier", "amount_exceeds_limit"],
            "attachments": ["contract_draft.pdf", "vendor_application.pdf"],
            "expected_decision": "REFER",
            "expected_confidence": "medium",
        }

    def _high_risk_template(self) -> dict[str, Any]:
        assert self.now is not None
        return {
            "request_id": f"REQ-{self.now.strftime('%Y%m%d')}-003",
            "requester_name": "David Chen",
            "requester_email": "david.chen@company.com",
            "department": "Operations",
            "supplier_id": "SUP-004",
            "supplier_name": "Retail Dynamics",
            "amount": 25000.00,
            "currency": "USD",
            "category": "Equipment",
            "description": "Warehouse equipment purchase",
            "urgency": "standard",
            "required_by": (self.now + timedelta(days=60)).date().isoformat(),
            "budget_remaining": 10000.00,
            "requester_approval_limit": 10000.00,
            "supplier_history": {
                "total_transactions": 8,
                "total_amount": 120000.00,
                "avg_delivery_time": 10.5,
                "quality_rating": 3.1,
            },
            "policy_flags": ["budget_exceeded", "high_risk_supplier", "quality_issues"],
            "attachments": ["invoice_004.pdf", "spec_sheet.pdf"],
            "expected_decision": "DENY",
            "expected_confidence": "high",
        }

    def _borderline_template(self) -> dict[str, Any]:
        assert self.now is not None
        return {
            "request_id": f"REQ-{self.now.strftime('%Y%m%d')}-004",
            "requester_name": "Sarah Williams",
            "requester_email": "sarah.williams@company.com",
            "department": "IT",
            "supplier_id": "SUP-006",
            "supplier_name": "Cloud Innovators",
            "amount": 4750.00,
            "currency": "USD",
            "category": "Cloud Services",
            "description": "Additional cloud storage and compute resources",
            "urgency": "high",
            "required_by": (self.now + timedelta(days=7)).date().isoformat(),
            "budget_remaining": 5000.00,
            "requester_approval_limit": 5000.00,
            "supplier_history": {
                "total_transactions": 12,
                "total_amount": 45000.00,
                "avg_delivery_time": 1.0,
                "quality_rating": 4.9,
            },
            "policy_flags": ["budget_near_limit"],
            "attachments": ["cloud_quote.pdf"],
            "expected_decision": "APPROVE",
            "expected_confidence": "medium",
        }

    def _emergency_template(self) -> dict[str, Any]:
        assert self.now is not None
        return {
            "request_id": f"REQ-{self.now.strftime('%Y%m%d')}-005",
            "requester_name": "James Wilson",
            "requester_email": "james.wilson@company.com",
            "department": "Facilities",
            "supplier_id": "SUP-003",
            "supplier_name": "MediCare Supplies",
            "amount": 12000.00,
            "currency": "USD",
            "category": "Equipment",
            "description": "EMERGENCY: Air conditioning repair for server room",
            "urgency": "critical",
            "required_by": (self.now + timedelta(days=1)).date().isoformat(),
            "budget_remaining": 8000.00,
            "requester_approval_limit": 5000.00,
            "supplier_history": {
                "total_transactions": 25,
                "total_amount": 185000.00,
                "avg_delivery_time": 1.5,
                "quality_rating": 4.7,
            },
            "policy_flags": ["emergency", "amount_exceeds_limit", "budget_exceeded"],
            "attachments": ["emergency_quote.pdf", "temperature_logs.pdf"],
            "expected_decision": "APPROVE",
            "expected_confidence": "high",
        }

    def _random_template(self) -> dict[str, Any]:
        assert self.now is not None
        supplier_id = random.choice(list(self.suppliers.keys()))
        supplier = self.suppliers[supplier_id]

        amount = random.choice([500, 1500, 3000, 7500, 12000, 25000])
        budget = amount * random.uniform(1.2, 3.0)
        limit = random.choice([2000, 5000, 10000, 20000])

        return {
            "request_id": f"REQ-{self.now.strftime('%Y%m%d')}-{random.randint(100, 999)}",
            "requester_name": (
                f"{random.choice(['John', 'Jane', 'Robert', 'Lisa', 'Michael', 'Emily'])} "
                f"{random.choice(['Smith', 'Brown', 'Lee', 'Garcia', 'Patel'])}"
            ),
            "requester_email": f"{random.choice(['user', 'requester', 'buyer'])}{random.randint(1, 99)}@company.com",
            "department": random.choice(self.departments),
            "supplier_id": supplier_id,
            "supplier_name": supplier["name"],
            "amount": float(amount),
            "currency": random.choice(["USD", "EUR", "GBP"]),
            "category": random.choice(self.categories),
            "description": (
                f"Purchase of {random.choice(['annual', 'quarterly', 'one-time'])} "
                f"{random.choice(['supplies', 'services', 'equipment', 'software'])}"
            ),
            "urgency": random.choice(["low", "standard", "high", "critical"]),
            "required_by": (self.now + timedelta(days=random.randint(1, 90))).date().isoformat(),
            "budget_remaining": float(budget),
            "requester_approval_limit": float(limit),
            "supplier_history": {
                "total_transactions": random.randint(0, 50),
                "total_amount": float(random.randint(1000, 500000)),
                "avg_delivery_time": random.uniform(1.0, 15.0),
                "quality_rating": random.uniform(2.0, 5.0),
            },
            "policy_flags": random.sample(
                ["new_supplier", "budget_near_limit", "high_value", "special_category"],
                k=random.randint(0, 2),
            ),
            "attachments": [f"document_{random.randint(1, 5)}.pdf"],
            "expected_decision": random.choice(["APPROVE", "REFER", "DENY"]),
            "expected_confidence": random.choice(["low", "medium", "high"]),
        }


def generate_dataset_json(output_path: str | Path, *, count: int = 10, seed: int | None = 1337) -> Path:
    path = Path(output_path)
    generator = ProcurementTestDataGenerator(seed=seed)
    generator.save_dataset(path, count=count)
    return path
