from __future__ import annotations

import argparse
import json
from pathlib import Path

from procuator.data.demo_scenarios import demo_scenarios
from procuator.data.generator import generate_dataset_json
from procuator.skills.decision_auditor import DecisionAuditor
from procuator.skills.policy_engine import PolicyEngine
from procuator.skills.supplier_risk_checker import SupplierRiskChecker


def _cmd_risk_check(args: argparse.Namespace) -> int:
    skill = SupplierRiskChecker()
    payload = {"supplier_id": args.supplier_id, "industry": args.industry, "refresh_cache": args.refresh}

    import asyncio

    result = asyncio.run(skill.execute(payload))
    print(json.dumps(result, indent=2))
    return 0


def _cmd_generate_data(args: argparse.Namespace) -> int:
    output = Path(args.output)
    generate_dataset_json(output, count=args.count, seed=args.seed)
    print(str(output))
    return 0


def _cmd_demo_scenarios(_: argparse.Namespace) -> int:
    print(json.dumps({"scenarios": demo_scenarios()}, indent=2))
    return 0


def _cmd_decide(args: argparse.Namespace) -> int:
    risk = SupplierRiskChecker()
    policy = PolicyEngine()
    auditor = DecisionAuditor()

    request = {
        "request_id": args.request_id,
        "supplier_id": args.supplier_id,
        "industry": args.industry,
        "amount": args.amount,
        "currency": args.currency,
        "budget_remaining": args.budget_remaining,
        "requester_approval_limit": args.requester_approval_limit,
        "urgency": args.urgency,
        "supplier_history": {"total_transactions": args.supplier_transactions},
        "refresh_cache": args.refresh,
    }

    import asyncio

    risk_result = asyncio.run(risk.execute(request))
    policy_result = asyncio.run(policy.execute(request))

    risk_level = str(risk_result.get("risk_level", "UNKNOWN"))
    policy_decision = str(policy_result.get("policy_decision", "REFER"))
    risk_score = float(risk_result.get("risk_score", 0.0))

    if policy_decision == "DENY":
        final = "DENY"
    elif policy_decision == "REFER":
        final = "REFER"
    elif risk_level == "HIGH":
        final = "REFER"
    elif risk_level == "MEDIUM" and risk_score >= 5.5:
        final = "REFER"
    else:
        final = "APPROVE"

    explanation = list(policy_result.get("reasons") or [])
    if policy_result.get("policy_flags"):
        explanation.append(f"Policy flags: {', '.join(policy_result['policy_flags'])}")
    risk_flags_raw = list(risk_result.get("risk_flags") or [])
    risk_flags = [
        (str(f.get("code") or f.get("message") or f) if isinstance(f, dict) else str(f)) for f in risk_flags_raw
    ]
    if risk_flags:
        explanation.append(f"Risk flags: {', '.join(risk_flags)}")

    asyncio.run(
        auditor.execute(
            {
                "event_type": "decision",
                "request_id": str(request.get("request_id") or request.get("supplier_id")),
                "supplier_id": str(request.get("supplier_id")),
                "decision": final,
                "explanation": explanation,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "policy_decision": policy_decision,
                "policy_flags": list(policy_result.get("policy_flags") or []),
                "risk_flags": risk_flags,
            }
        )
    )

    print(
        json.dumps(
            {
                "decision": final,
                "risk": risk_result,
                "policy": policy_result,
                "explanation": explanation,
            },
            indent=2,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="procuator")
    sub = parser.add_subparsers(dest="cmd", required=True)

    risk = sub.add_parser("risk-check", help="Run a supplier risk check")
    risk.add_argument("supplier_id")
    risk.add_argument("--industry", default="general")
    risk.add_argument("--refresh", action="store_true")
    risk.set_defaults(func=_cmd_risk_check)

    gen = sub.add_parser("generate-data", help="Generate demo dataset JSON")
    gen.add_argument("--output", default="data/procurement_test_data.json")
    gen.add_argument("--count", type=int, default=10)
    gen.add_argument("--seed", type=int, default=1337)
    gen.set_defaults(func=_cmd_generate_data)

    demo = sub.add_parser("demo-scenarios", help="Print the 3 core demo scenarios")
    demo.set_defaults(func=_cmd_demo_scenarios)

    decide = sub.add_parser("decide", help="Run policy + risk and print a final decision")
    decide.add_argument("supplier_id")
    decide.add_argument("--request-id", default=None)
    decide.add_argument("--industry", default="general")
    decide.add_argument("--amount", type=float, required=True)
    decide.add_argument("--currency", default="USD")
    decide.add_argument("--budget-remaining", type=float, default=0.0)
    decide.add_argument("--requester-approval-limit", type=float, default=0.0)
    decide.add_argument("--supplier-transactions", type=int, default=0)
    decide.add_argument("--urgency", default="standard")
    decide.add_argument("--refresh", action="store_true")
    decide.set_defaults(func=_cmd_decide)

    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
