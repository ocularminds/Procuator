from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import Any

from procuator.features.demo.DemoCatalog import DemoCatalog


class ScenarioFactory:
    """Creates curated and random procurement request scenarios."""

    def __init__(
        self,
        now: datetime,
        seed: int | None = 1337,
        catalog: DemoCatalog | None = None,
    ) -> None:
        self._now = now
        self._random = random.Random(seed)
        self._catalog = catalog or DemoCatalog()

    def createLowRisk(self) -> dict[str, Any]:
        return {
            "request_id": f"REQ-{self._now.strftime('%Y%m%d')}-001",
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
            "required_by": (self._now + timedelta(days=30)).date().isoformat(),
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

    def createMediumRisk(self) -> dict[str, Any]:
        return {
            "request_id": f"REQ-{self._now.strftime('%Y%m%d')}-002",
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
            "required_by": (self._now + timedelta(days=45)).date().isoformat(),
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

    def createHighRisk(self) -> dict[str, Any]:
        return {
            "request_id": f"REQ-{self._now.strftime('%Y%m%d')}-003",
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
            "required_by": (self._now + timedelta(days=60)).date().isoformat(),
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

    def createBorderline(self) -> dict[str, Any]:
        return {
            "request_id": f"REQ-{self._now.strftime('%Y%m%d')}-004",
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
            "required_by": (self._now + timedelta(days=7)).date().isoformat(),
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

    def createEmergency(self) -> dict[str, Any]:
        return {
            "request_id": f"REQ-{self._now.strftime('%Y%m%d')}-005",
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
            "required_by": (self._now + timedelta(days=1)).date().isoformat(),
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

    def createRandom(self) -> dict[str, Any]:
        supplierId = self._random.choice(list(self._catalog.suppliers.keys()))
        supplier = self._catalog.suppliers[supplierId]
        amount = self._random.choice([500, 1500, 3000, 7500, 12000, 25000])
        budget = amount * self._random.uniform(1.2, 3.0)
        limit = self._random.choice([2000, 5000, 10000, 20000])

        return {
            "request_id": f"REQ-{self._now.strftime('%Y%m%d')}-{self._random.randint(100, 999)}",
            "requester_name": (
                f"{self._random.choice(['John', 'Jane', 'Robert', 'Lisa', 'Michael', 'Emily'])} "
                f"{self._random.choice(['Smith', 'Brown', 'Lee', 'Garcia', 'Patel'])}"
            ),
            "requester_email": (
                f"{self._random.choice(['user', 'requester', 'buyer'])}{self._random.randint(1, 99)}@company.com"
            ),
            "department": self._random.choice(self._catalog.departments),
            "supplier_id": supplierId,
            "supplier_name": supplier["name"],
            "amount": float(amount),
            "currency": self._random.choice(["USD", "EUR", "GBP"]),
            "category": self._random.choice(self._catalog.categories),
            "description": (
                f"Purchase of {self._random.choice(['annual', 'quarterly', 'one-time'])} "
                f"{self._random.choice(['supplies', 'services', 'equipment', 'software'])}"
            ),
            "urgency": self._random.choice(["low", "standard", "high", "critical"]),
            "required_by": (self._now + timedelta(days=self._random.randint(1, 90))).date().isoformat(),
            "budget_remaining": float(budget),
            "requester_approval_limit": float(limit),
            "supplier_history": {
                "total_transactions": self._random.randint(0, 50),
                "total_amount": float(self._random.randint(1000, 500000)),
                "avg_delivery_time": self._random.uniform(1.0, 15.0),
                "quality_rating": self._random.uniform(2.0, 5.0),
            },
            "policy_flags": self._random.sample(
                ["new_supplier", "budget_near_limit", "high_value", "special_category"],
                k=self._random.randint(0, 2),
            ),
            "attachments": [f"document_{self._random.randint(1, 5)}.pdf"],
            "expected_decision": self._random.choice(["APPROVE", "REFER", "DENY"]),
            "expected_confidence": self._random.choice(["low", "medium", "high"]),
        }
