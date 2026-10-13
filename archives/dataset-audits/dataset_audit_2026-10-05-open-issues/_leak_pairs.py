import sys
import json
from pathlib import Path

ROOT = Path(".").resolve()
sys.path[:0] = [str(ROOT), str(ROOT / "src")]
from animtrain.structural_leakage import compare, VERSION, implementation_sha256  # noqa: E402
from tools.leakage_population import census  # noqa: E402

pop = census(ROOT / "data/manifest.json", ROOT / "data")
print("population pairs:", len(pop["pairs"]), "| keys:", list(pop)[:8])
cands = []
for pair in pop["pairs"]:
    r = compare(pair["query"]["problem"], pair["train"]["problem"])
    if r.get("candidate"):
        cands.append((pair, r))
print("候选对:", len(cands), "| 规则:", VERSION, "| 实现哈希:", implementation_sha256()[:12])
for pair, r in cands:
    print("=" * 90)
    print("score/键:", json.dumps({k: str(v) for k, v in r.items() if k != "candidate"}, ensure_ascii=False)[:300])
    q, tr = pair["query"], pair["train"]
    print("  query:", json.dumps({k: v for k, v in q.items() if k != "problem"}, ensure_ascii=False)[:160])
    print("   train:", json.dumps({k: v for k, v in tr.items() if k != "problem"}, ensure_ascii=False)[:160])
    print("  query problem:", str(q.get("problem"))[:200])
    print("  train problem:", str(tr.get("problem"))[:200])
