from __future__ import annotations

import argparse
import asyncio
import json
from abc import ABC, abstractmethod

from procuator.features.decision.DecisionAuditor import DecisionAuditor
from procuator.features.decision.DecisionRules import DecisionRules
from procuator.features.demo.DatasetGenerator import DatasetFileWriter
from procuator.features.demo.DemoScenarios import DemoScenarioService
from procuator.features.policy.PolicyEngine import PolicyEngine
from procuator.features.risk.SupplierRiskChecker import SupplierRiskChecker


class CliCommand(ABC):
    """Contract implemented by command-line actions."""

    @abstractmethod
    def execute(self, args: argparse.Namespace) -> int:
        """Run a command and return its process status."""


class RiskCheckCommand(CliCommand):
    def execute(self, args: argparse.Namespace) -> int:
        checker = SupplierRiskChecker()

        async def runCheck() -> dict:
            try:
                return await checker.execute(
                    {
                        "supplier_id": args.supplierId,
                        "industry": args.industry,
                        "refresh_cache": args.refresh,
                    }
                )
            finally:
                await checker.close()

        print(json.dumps(asyncio.run(runCheck()), indent=2))
        return 0


class GenerateDataCommand(CliCommand):
    def execute(self, args: argparse.Namespace) -> int:
        outputPath = DatasetFileWriter().write(
            args.output,
            count=args.count,
            seed=args.seed,
        )
        print(str(outputPath))
        return 0


class DemoScenariosCommand(CliCommand):
    def execute(self, args: argparse.Namespace) -> int:
        _ = args
        scenarios = DemoScenarioService().getScenarios()
        print(json.dumps({"scenarios": scenarios}, indent=2))
        return 0


class DecideCommand(CliCommand):
    def execute(self, args: argparse.Namespace) -> int:
        checker = SupplierRiskChecker()
        policyEngine = PolicyEngine()
        auditor = DecisionAuditor()
        rules = DecisionRules()
        request = {
            "request_id": args.requestId,
            "supplier_id": args.supplierId,
            "industry": args.industry,
            "amount": args.amount,
            "currency": args.currency,
            "budget_remaining": args.budgetRemaining,
            "requester_approval_limit": args.requesterApprovalLimit,
            "urgency": args.urgency,
            "supplier_history": {"total_transactions": args.supplierTransactions},
            "refresh_cache": args.refresh,
        }

        async def runDecision() -> dict:
            try:
                risk = await checker.execute(request)
                policy = await policyEngine.execute(request)
                riskLevel = str(risk.get("risk_level", "UNKNOWN"))
                riskScore = float(risk.get("risk_score", 0.0))
                policyDecision = str(policy.get("policy_decision", "REFER"))
                finalDecision = rules.determine(policyDecision, riskLevel, riskScore)
                riskFlags = rules.extractRiskFlags(risk)
                explanation = list(policy.get("reasons") or [])
                policyFlags = list(policy.get("policy_flags") or [])
                if policyFlags:
                    explanation.append(f"Policy flags: {', '.join(policyFlags)}")
                if riskFlags:
                    explanation.append(f"Risk flags: {', '.join(riskFlags)}")

                await auditor.execute(
                    {
                        "event_type": "decision",
                        "request_id": str(request.get("request_id") or request.get("supplier_id")),
                        "supplier_id": str(request.get("supplier_id")),
                        "decision": finalDecision,
                        "explanation": explanation,
                        "risk_score": riskScore,
                        "risk_level": riskLevel,
                        "policy_decision": policyDecision,
                        "policy_flags": policyFlags,
                        "risk_flags": riskFlags,
                    }
                )
                return {
                    "decision": finalDecision,
                    "risk": risk,
                    "policy": policy,
                    "explanation": explanation,
                }
            finally:
                await checker.close()

        print(json.dumps(asyncio.run(runDecision()), indent=2))
        return 0
