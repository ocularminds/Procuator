from __future__ import annotations

import argparse

from procuator.cli.Commands import (
    DecideCommand,
    DemoScenariosCommand,
    GenerateDataCommand,
    RiskCheckCommand,
)


class CliApplication:
    """Configures and dispatches the Procuator command line."""

    def createParser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(prog="procuator")
        commands = parser.add_subparsers(dest="command", required=True)

        risk = commands.add_parser("risk-check", help="Run a supplier risk check")
        risk.add_argument("supplierId", metavar="supplier_id")
        risk.add_argument("--industry", default="general")
        risk.add_argument("--refresh", action="store_true")
        risk.set_defaults(commandHandler=RiskCheckCommand())

        generate = commands.add_parser("generate-data", help="Generate demo dataset JSON")
        generate.add_argument("--output", default="data/procurement_test_data.json")
        generate.add_argument("--count", type=int, default=10)
        generate.add_argument("--seed", type=int, default=1337)
        generate.set_defaults(commandHandler=GenerateDataCommand())

        demo = commands.add_parser("demo-scenarios", help="Print the 3 core demo scenarios")
        demo.set_defaults(commandHandler=DemoScenariosCommand())

        decide = commands.add_parser("decide", help="Run policy + risk and print a final decision")
        decide.add_argument("supplierId", metavar="supplier_id")
        decide.add_argument("--request-id", dest="requestId", default=None)
        decide.add_argument("--industry", default="general")
        decide.add_argument("--amount", type=float, required=True)
        decide.add_argument("--currency", default="USD")
        decide.add_argument("--budget-remaining", dest="budgetRemaining", type=float, default=0.0)
        decide.add_argument(
            "--requester-approval-limit",
            dest="requesterApprovalLimit",
            type=float,
            default=0.0,
        )
        decide.add_argument(
            "--supplier-transactions",
            dest="supplierTransactions",
            type=int,
            default=0,
        )
        decide.add_argument("--urgency", default="standard")
        decide.add_argument("--refresh", action="store_true")
        decide.set_defaults(commandHandler=DecideCommand())
        return parser

    def run(self) -> int:
        args = self.createParser().parse_args()
        return int(args.commandHandler.execute(args))


def main() -> int:
    return CliApplication().run()


if __name__ == "__main__":
    raise SystemExit(main())
