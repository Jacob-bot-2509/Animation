"""组装 bridge_send 参数;内容来自 bridge-message.md,元数据绑定本次审查批次。"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
RUN_ID = "run-77ee6b3379a54ac0b3cb89b9c097bca5"
FIX = ROOT / "archives/reviews/codex-supervision/2026-10-17-presentation-pipeline-review/FIX_REPORT.md"

msg = {
    "from": "codex",
    "to": "claude-code",
    "type": "review_result",
    "content": (HERE / "bridge-message.md").read_text(encoding="utf-8"),
    "metadata": {
        "mail_run_id": RUN_ID,
        "reviewed_messages": "msg_1792236520380_904,msg_1792236695873_905",
        "fix_report": FIX.relative_to(ROOT).as_posix(),
        "report_sha256": hashlib.sha256(FIX.read_bytes()).hexdigest(),
        "scope": "presentation-pipeline-v1-and-scene-candidates",
        "codex_modified": "true",
    },
}
out = HERE / "bridge-message.json"
out.write_text(json.dumps(msg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(out, "content_chars =", len(msg["content"]))
