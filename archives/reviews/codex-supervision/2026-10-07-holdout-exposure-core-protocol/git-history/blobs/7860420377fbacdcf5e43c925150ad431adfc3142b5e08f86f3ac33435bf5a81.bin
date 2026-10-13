"""运行记录(msg_101-5,纯标准库):统一格式 + fail-fast 校验 + 可重放依据。

每条运行必须记录:config 快照、git commit、manifest hash、运行摘要、指标。
任何缺失 → fail-fast(不静默,便于定位)。dry-run 同样记录,保证可重放。

统一存放: runs/<run_id>/run_record.json
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

REQUIRED_NONEMPTY = {"run_id", "kind", "git_commit", "manifest_hash"}


@dataclass
class RunRecord:
    run_id: str
    kind: str                       # dry-run | baseline | improvement | eval
    config: dict                    # config 快照(可为空 dict = 用默认配置,显式写 {})
    git_commit: str
    manifest_hash: str
    summary: dict = field(default_factory=dict)   # 命令/时间/结论
    metrics: dict = field(default_factory=dict)   # 指标(loss/通过率/…)
    version: int = 1

    def to_dict(self) -> dict:
        return {"run_record_version": self.version, "run_id": self.run_id,
                "kind": self.kind, "config": self.config,
                "git_commit": self.git_commit, "manifest_hash": self.manifest_hash,
                "summary": self.summary, "metrics": self.metrics}

    @classmethod
    def from_dict(cls, d: dict) -> "RunRecord":
        return cls(run_id=d.get("run_id", ""), kind=d.get("kind", ""),
                   config=d.get("config", {}), git_commit=d.get("git_commit", ""),
                   manifest_hash=d.get("manifest_hash", ""),
                   summary=d.get("summary", {}), metrics=d.get("metrics", {}),
                   version=d.get("run_record_version", 1))

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2),
                        encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "RunRecord":
        return cls.from_dict(json.loads(path.read_text(encoding="utf-8")))


def check_record(r: RunRecord, manifest_path: Path | None = None) -> list[str]:
    """fail-fast 校验:必填缺失/格式错误/ hash 不可复现 → 问题清单。"""
    problems: list[str] = []
    for k in REQUIRED_NONEMPTY:
        if not str(getattr(r, k, "")).strip():
            problems.append(f"缺少必填字段 {k}(fail-fast)")
    if r.kind not in {"dry-run", "baseline", "improvement", "eval"}:
        problems.append(f"kind 非法: {r.kind}")
    if not r.config:
        problems.append("config 为空 —— 若确为默认配置请显式写 {}(fail-fast)")
    if not r.summary.get("command"):
        problems.append("summary.command 缺失(运行命令不可少,否则无法重放)")
    if len(r.manifest_hash) not in (0, 64):
        problems.append(f"manifest_hash 长度非法 {len(r.manifest_hash)}(应为 64 或空)")
    if manifest_path is not None and manifest_path.exists() and r.manifest_hash:
        actual = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        if actual != r.manifest_hash:
            problems.append(f"manifest hash 不可复现(记录 {r.manifest_hash[:12]}…,"
                            f"实际 {actual[:12]}…)")
    return problems
