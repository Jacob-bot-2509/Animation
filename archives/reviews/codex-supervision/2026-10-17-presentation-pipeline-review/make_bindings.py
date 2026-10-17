"""生成本轮修复的源绑定清单(SHA/行数/场景前后 SHA),写入档案目录。"""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SUB = ROOT / "reviews/data-prep/2026-10-17-submission/asset-evidence"
PIPE = SUB / "presentation-pipeline"

FILES = [
    SUB / "template-fix-candidate/render_templates_v3_candidate.py",
    SUB / "template-fix-candidate/test_template_v3_candidate.py",
    SUB / "presentation-candidates/build_presentation_candidates.py",
    SUB / "presentation-candidates/presentation-bindings.jsonl",
    PIPE / "pipeline.py",
    PIPE / "test_pipeline.py",
    PIPE / "README.md",
    PIPE / "runs/pipeline-receipt.json",
    PIPE / "runs/verdicts.json",
    HERE / "scene-audit-post-fix.json",
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git_show(path: str) -> bytes | None:
    cp = subprocess.run(["git", "-C", str(ROOT), "show", f"HEAD:{path}"],
                        capture_output=True)
    return cp.stdout if cp.returncode == 0 else None


def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


payload = {
    "generated_at": "2026-10-17",
    "git_head": subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                               capture_output=True, text=True).stdout.strip(),
    "files": {},
    "scene_sha_before_after": {},
    "notes": [
        "v2 模板未改动(工作区字节 55b18a1e...,与 HEAD 版本 3bcb6980... 不同,属本轮之前已存在的未提交改动)",
        "审核包 runs/review-packs 已按 v3 场景重建;结论单全部为空表",
    ],
}

for f in FILES:
    payload["files"][rel(f)] = {"bytes": f.stat().st_size, "sha256": sha(f)}

old_bind = git_show("reviews/data-prep/2026-10-17-submission/asset-evidence/"
                    "presentation-candidates/presentation-bindings.jsonl")
if old_bind:
    before = {}
    for line in old_bind.decode("utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            before[row["sample_id"]] = row["scene_sha256"]
    after = {}
    for line in (SUB / "presentation-candidates/presentation-bindings.jsonl").read_text(
            encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            after[row["sample_id"]] = row["scene_sha256"]
    payload["scene_sha_before_after"] = {
        sid: {"before": before.get(sid), "after": after.get(sid)} for sid in after}

receipt = json.loads((PIPE / "runs/pipeline-receipt.json").read_text(encoding="utf-8"))
payload["receipt"] = {"run_id": receipt["run_id"], "status": receipt["status"],
                      "template_version": receipt["template"]["version"],
                      "samples": len(receipt["scenes"])}
verdicts = json.loads((PIPE / "runs/verdicts.json").read_text(encoding="utf-8"))
payload["verdicts"] = {"overall": verdicts["overall"], "packs": len(verdicts["packs"])}

out = HERE / "source-bindings.json"
out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: payload[k] for k in ("git_head", "receipt", "verdicts")},
                 ensure_ascii=False, indent=2))
print("files:", len(payload["files"]), "scenes:", len(payload["scene_sha_before_after"]))
