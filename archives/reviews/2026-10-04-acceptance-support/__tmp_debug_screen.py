"""调试防泄漏屏测试失败:复现 test_near_dup_threshold_configurable 场景。"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(r"D:\Animation-Model-Training")
sys.path.insert(0, str(ROOT / "src"))
from animtrain.manifest import Entry, Manifest, sha256_file, canonical_problem_text  # noqa: E402
from animtrain.validate import validate_manifest  # noqa: E402
from animtrain.near_dup import shingles  # noqa: E402
from animtrain.kp_rule import kp_signature  # noqa: E402

tmp = Path(tempfile.mkdtemp(prefix="dbg-screen-"))
train = tmp / "train" / "a.jsonl"
ev = tmp / "eval" / "b.jsonl"
train.parent.mkdir(); ev.parent.mkdir()
t_text = "求极限 $\\displaystyle\\lim_{x\\to 0}\\frac{1-\\cos x}{x^2}$。"
e_text = "求极限 $\\displaystyle\\lim_{x\\to 0}\\frac{\\sin x-\\tan x}{x^3}$。"
train.write_text(json.dumps({"category": "数学分析", "sub_category": "极限",
                             "problem": t_text}, ensure_ascii=False) + "\n",
                 encoding="utf-8")
ev.write_text(json.dumps({"category": "数学分析", "sub_category": "极限",
                          "problem": e_text}, ensure_ascii=False) + "\n",
              encoding="utf-8")
m = Manifest(name="t", entries=[
    Entry(path="train/a.jsonl", sha256=sha256_file(train), size=train.stat().st_size,
          source="x", license="internal-generated", split="train"),
    Entry(path="eval/b.jsonl", sha256=sha256_file(ev), size=ev.stat().st_size,
          source="x", license="internal-generated", split="eval")])
sa, sb = shingles(canonical_problem_text(train.read_text(encoding="utf-8").splitlines()[0])), shingles(canonical_problem_text(ev.read_text(encoding="utf-8").splitlines()[0]))
u = sa | sb
print("J5:", len(sa & sb) / len(u) if u else 0)
print("sig train:", kp_signature(json.loads(train.read_text(encoding="utf-8").splitlines()[0])))
print("sig eval:", kp_signature(json.loads(ev.read_text(encoding="utf-8").splitlines()[0])))
r = validate_manifest(m, tmp, near_dup_threshold=0.4)
print("problems:", r["problems"])
