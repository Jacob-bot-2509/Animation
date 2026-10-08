"""Compatibility entry for the reviewed bound rendering pipeline.

Requires a fresh --out path. It generates linalg048-bound-render-v2 with the
same source/isolation/video verification as tools/admit_linalg048_v3.py.
Historical shear-scene-v2-rerender-v1 receipts are never overwritten/upgraded.
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'src')]
from admit_linalg048_v3 import main

if __name__ == '__main__':
    sys.exit(main())
