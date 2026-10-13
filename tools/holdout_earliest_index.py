# -*- coding: utf-8 -*-
"""曝光审核最早证据全量索引:
  1) reviews/ 全部 ≤2026-10-05 的审查目录逐文件 SHA
  2) data/v1、data/v2/raw、早期 dataset_audit_* 目录逐文件 SHA
  3) 桥接消息 09-29~10-05 全部(元数据+内容SHA,不落全文本)
  4) 最早 30 个 git 提交
输出 reviews/2026-10-07-gap-materials/earliest-complete-index-v1.json。只读。"""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reviews/2026-10-07-gap-materials/earliest-complete-index-v1.json"
if OUT.exists():
    raise ValueError("preserve previous index")


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dir_index(base: Path, pattern="*", max_files=20000):
    items = []
    n = 0
    for f in sorted(base.rglob(pattern)):
        if not f.is_file() or n >= max_files:
            continue
        items.append({"path": str(f.relative_to(ROOT)), "sha256": sha_file(f)})
        n += 1
    return items


def main() -> int:
    report = {"schema": "earliest-complete-index-v1", "produced_at": "2026-10-07",
              "sections": {}}

    # 1) 审查目录(09-30 ~ 10-05,2026-10-14 起审查档案统一在 archives/reviews/)
    review_dirs = sorted([d for d in (ROOT / "archives" / "reviews").iterdir()
                          if d.is_dir() and d.name <= "2026-10-05"])
    files = []
    for d in review_dirs:
        files.extend(dir_index(d))
    report["sections"]["review_dirs_le_10_05"] = {
        "dirs": [d.name for d in review_dirs], "n_files": len(files), "files": files}

    # 2) 数据与早期审计
    data_files = []
    for base in ["data/v1", "data/v2/raw"]:
        p = ROOT / base
        if p.is_dir():
            data_files.extend(dir_index(p, "*"))
    audit_files = []
    for d in sorted((ROOT / "archives" / "dataset-audits").glob("dataset_audit_2026-10-0[23]*")):
        audit_files.extend(dir_index(d))
    report["sections"]["data_v1_and_v2raw"] = {"n_files": len(data_files), "files": data_files}
    report["sections"]["early_dataset_audits"] = {"n_files": len(audit_files), "files": audit_files}

    # 3) 桥接消息索引(09-29 ~ 10-05,只元数据+内容SHA)
    import io as _io
    state = json.load(_io.open(r"C:/Users/Jacap/.ai-bridge/state.json", encoding="utf-8"))
    msgs = state.get("messages", state)
    if isinstance(msgs, dict):
        msgs = msgs.get("messages", [])
    msg_index = []
    for m in msgs:
        ts = m.get("timestamp", "")
        if not (ts.startswith("2026-09-") or ts.startswith("2026-10-0") and ts <= "2026-10-05T23:59"):
            continue
        content = m.get("content", "")
        msg_index.append({"id": m["id"], "from": m.get("from"), "to": m.get("to"),
                          "type": m.get("type"), "timestamp": ts,
                          "content_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
                          "content_bytes": len(content.encode("utf-8"))})
    report["sections"]["bridge_messages_until_10_05"] = {
        "n": len(msg_index), "messages": msg_index,
        "note": "仅元数据+内容SHA;最早5封全文本另见 msg105-110-earliest-excerpt.json"}

    # 4) 最早 30 个提交
    cp = subprocess.run(["git", "log", "--reverse", "--format=%H %ad %s", "--date=iso"],
                        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    lines = cp.stdout.strip().splitlines()[:30]
    report["sections"]["earliest_30_commits"] = lines

    OUT.write_text(json.dumps(report, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print("review files:", len(files))
    print("data files:", len(data_files), "| audit files:", len(audit_files))
    print("bridge messages:", len(msg_index))
    print("commits:", len(lines))
    print("index:", OUT)
    print("index sha256:", hashlib.sha256(OUT.read_bytes()).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
