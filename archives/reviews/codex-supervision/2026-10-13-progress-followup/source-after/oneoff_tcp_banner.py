"""Exact local TCP banner diagnostic. Default PLAN; use --execute explicitly."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from witness_tcp_diagnostics import main as diagnostic_main

def main(argv=None):
    return diagnostic_main(argv,banner=True)

if __name__=="__main__":
    raise SystemExit(main())
