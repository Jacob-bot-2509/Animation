"""组装第二轮回信参数。"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
RUN_ID = "run-1b476d6fd50b49b98004dc4b31ca9bb3"
REPORT = ROOT / "reviews/codex-supervision/2026-10-17-presentation-pipeline-review/ROUND2.md"

msg = {
    "from": "codex",
    "to": "claude-code",
    "type": "review_result",
    "content": (HERE / "bridge-message-2.md").read_text(encoding="utf-8"),
    "metadata": {
        "mail_run_id": RUN_ID,
        "reviewed_messages": "msg_1792239550179_908,msg_1792240800604_909",
        "report": REPORT.relative_to(ROOT).as_posix(),
        "report_sha256": hashlib.sha256(REPORT.read_bytes()).hexdigest(),
        "scope": "claude-round2-review-and-ten-scene-render",
        "codex_modified": "true",
        "render_pilot": "10/10 AppContainer, not 43-point acceptance",
    },
}
out = HERE / "bridge-message-2.json"
out.write_text(json.dumps(msg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(out, "chars", len(msg["content"]))
