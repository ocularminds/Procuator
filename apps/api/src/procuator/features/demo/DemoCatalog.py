from __future__ import annotations

from typing import Any


class DemoCatalog:
    """Owns static data used by generated procurement demos."""

    departments = [
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

    categories = [
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

    suppliers: dict[str, dict[str, str]] = {
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

    def getPolicyRules(self) -> dict[str, Any]:
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
            "risk_thresholds": {
                "auto_approve_max_risk": 4.0,
                "refer_max_risk": 7.0,
                "deny_min_risk": 7.1,
            },
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

    def getDemoScript(self) -> dict[str, Any]:
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
