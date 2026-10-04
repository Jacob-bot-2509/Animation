"""Retired unsafe acceptance entry point; never grants original toolchain ACLs."""
from __future__ import annotations
import json
import sys


def main(argv=None):
    print(json.dumps({
        "verdict": "UNVERIFIED", "retired": True, "production_gate": "CLOSED",
        "reason": "Legacy token-class and original-toolchain ACL probes are disabled.",
        "replacement": "tools/network_acceptance.py --baseline-evidence <reviewed-json> --output <evidence-dir>",
        "scope": "Replacement verifies local loopback only; full isolation remains unverified."
    }))
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
