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
    env: dict = field(default_factory=dict)       # 环境(python/平台/GPU)
    failure_analysis: dict = field(default_factory=dict)  # 失败:原因/修复/回滚点
    seed: int | None = None                        # B1:随机种子(训练类必填)
    dirty: dict = field(default_factory=dict)      # B1:git dirty 状态
                                                   # {"clean": bool, "changed": [...]}
    version: int = 3

    def to_dict(self) -> dict:
        return {"run_record_version": self.version, "run_id": self.run_id,
                "kind": self.kind, "config": self.config,
                "git_commit": self.git_commit, "manifest_hash": self.manifest_hash,
                "summary": self.summary, "metrics": self.metrics,
                "env": self.env, "failure_analysis": self.failure_analysis,
                "seed": self.seed, "dirty": self.dirty}

    @classmethod
    def from_dict(cls, d: dict) -> "RunRecord":
        return cls(run_id=d.get("run_id", ""), kind=d.get("kind", ""),
                   config=d.get("config", {}), git_commit=d.get("git_commit", ""),
                   manifest_hash=d.get("manifest_hash", ""),
                   summary=d.get("summary", {}), metrics=d.get("metrics", {}),
                   env=d.get("env", {}), failure_analysis=d.get("failure_analysis", {}),
                   seed=d.get("seed"), dirty=d.get("dirty", {}),
                   version=d.get("run_record_version", 1))

    def save(self, path: Path) -> None:
        from .atomic_write import atomic_write_text  # noqa: PLC0415
        atomic_write_text(path, json.dumps(self.to_dict(), ensure_ascii=False, indent=2))

    @classmethod
    def load(cls, path: Path) -> "RunRecord":
        return cls.from_dict(json.loads(path.read_text(encoding="utf-8")))


def check_record(r: RunRecord, manifest_path: Path | None = None) -> list[str]:
    """fail-fast 校验:必填缺失/格式错误/ hash 不可复现 → 问题清单。"""
    problems: list[str] = []
    for k in REQUIRED_NONEMPTY:
        if not str(getattr(r, k, "")).strip():
            problems.append(f"缺少必填字段 {k}(fail-fast)")
    from .fs_guard import valid_run_id  # 局部导入避免循环
    if not valid_run_id(r.run_id):
        problems.append(f"run_id 非法: {r.run_id!r}(只允许 [A-Za-z0-9_-] 1-64,"
                        "防路径穿越)")
    if r.kind not in {"dry-run", "baseline", "improvement", "eval"}:
        problems.append(f"kind 非法: {r.kind}")
    if not r.config:
        problems.append("config 为空 —— 若确为默认配置请显式写 {}(fail-fast)")
    if not r.summary.get("command"):
        problems.append("summary.command 缺失(运行命令不可少,否则无法重放)")
    if len(r.manifest_hash) not in (0, 64):
        problems.append(f"manifest_hash 长度非法 {len(r.manifest_hash)}(应为 64 或空)")
    # R8: hash 非空时必须带 manifest 路径;env 快照必填
    if r.manifest_hash and not r.summary.get("manifest"):
        problems.append("manifest_hash 非空但 summary.manifest 路径缺失(fail-fast)")
    if not r.env:
        problems.append("env 快照为空(记录 python/平台/GPU,缺失 fail-fast)")
    # B1: 训练类(baseline/improvement)必须有 seed;dirty 状态必须明确记录
    if r.kind in ("baseline", "improvement") and not isinstance(r.seed, int):
        problems.append(f"kind={r.kind} 必须有整数 seed(fail-fast,复现依据)")
    if "clean" not in r.dirty:
        problems.append("dirty 状态未记录 —— 必须明确 clean 或变更清单(B1)")
    if manifest_path is not None:
        if not manifest_path.exists():
            problems.append(f"manifest_path 指向不存在的文件: {manifest_path}"
                            "(复审 R8:缺实文件即失败)")
        elif r.manifest_hash:
            actual = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
            if actual != r.manifest_hash:
                problems.append(f"manifest hash 不可复现(记录 {r.manifest_hash[:12]}…,"
                                f"实际 {actual[:12]}…)")
    # msg_101-7:失败必须带失败分析(原因/修复/回滚点),不留无因失败
    if not r.metrics and r.kind != "dry-run" and not r.failure_analysis:
        problems.append("无指标且无 failure_analysis —— 失败必须留原因/修复/回滚点"
                        "(msg_101-7,统一格式)")
    if r.failure_analysis and not r.failure_analysis.get("reason"):
        problems.append("failure_analysis 缺 reason(失败原因)")
    return problems


def verify_replay(r: RunRecord, manifest_path: Path | None = None,
                  git_commit_now: str = "", dirty_now: dict | None = None,
                  config_path: Path | None = None) -> list[str]:
    """B1(GS4 复修):完整重放校验 —— 记录 vs 当前实际状态逐项对照。

    git commit、dirty(clean 标志 + 变更清单 + **变更文件内容哈希**)、
    config 文件哈希、manifest 哈希任一不一致即不可重放;
    训练类记录 config 未绑定实际文件 → fail-closed,不得可选略过。
    """
    problems = check_record(r, manifest_path=manifest_path)
    # 1. 代码状态:git commit 必须与记录一致
    if git_commit_now and r.git_commit and git_commit_now != r.git_commit:
        problems.append(f"代码状态与记录不一致(记录 {r.git_commit[:12]}…,"
                        f"当前 {git_commit_now[:12]}…)—— 不可重放(B1)")
    # 2. 工作区状态:clean 标志、变更清单与内容哈希必须一致(GS4)
    if (dirty_now is not None and isinstance(dirty_now, dict)
            and "clean" in r.dirty and dirty_now.get("clean") is not None):
        if bool(dirty_now["clean"]) != bool(r.dirty["clean"]):
            problems.append(f"工作区 dirty 状态与记录不一致(记录 clean="
                            f"{r.dirty['clean']},当前 {dirty_now['clean']})"
                            "—— 不可重放(B1)")
        else:
            rec_hashes = r.dirty.get("hashes", {}) or {}
            now_hashes = dirty_now.get("hashes", {}) or {}
            if set(rec_hashes) != set(now_hashes):
                problems.append("dirty 变更清单与记录不一致(文件集不同)"
                                "—— 不可重放(B1)")
            elif any(rec_hashes[k] != now_hashes[k] for k in rec_hashes):
                problems.append("dirty 文件内容与记录不一致(哈希变化)"
                                "—— 不可重放(B1)")
    # 3. 配置:训练类记录必须绑定实际文件哈希且当前文件一致(GS4 fail-closed)
    if config_path is None:
        if r.kind in ("baseline", "improvement"):
            problems.append("训练类记录 config 未绑定实际文件"
                            "—— 不可重放(B1 fail-closed,不得可选略过)")
    else:
        import hashlib
        actual = (hashlib.sha256(config_path.read_bytes()).hexdigest()
                  if config_path.exists() else "")
        recorded = (r.config or {}).get("sha256", "") \
            if isinstance(r.config, dict) else ""
        if not recorded:
            problems.append("config 未绑定实际文件哈希 —— 不可重放(B1)"
                            "(训练类记录必须来自实际配置文件)")
        elif actual != recorded:
            problems.append(f"config 文件与记录不一致(记录 {recorded[:12]}…,"
                            f"实际 {actual[:12]}…)—— 不可重放(B1)")
    return problems
