"""Legacy compatibility shim.

This repo historically stored prototype/demo code in markdown and in this root file.
The production-ready code now lives under the `src/procuator/` package.

This file remains so existing docs/scripts don't break.
"""

from __future__ import annotations


def main() -> int:
    from procuator.cli import main as procuator_main

    return procuator_main()


if __name__ == "__main__":
    raise SystemExit(main())
