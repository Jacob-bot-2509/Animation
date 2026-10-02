"""数据 manifest 基础 schema 与读写(纯标准库)。

manifest 是数据资产的登记账本:每个文件一条 entry,含
路径/SHA256/大小/来源/许可证/split/备注。校验器(validate.py)按此 schema 逐项检查。

设计依据(README 硬约束):所有新数据必须带 manifest/来源/许可证/SHA256/
门禁结果/限制说明;评测集与训练集必须零精确重叠(前项目 20/20 污染教训)。
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

MANIFEST_VERSION = 1
ALLOWED_LICENSES = {"apache-2.0", "mit", "internal-generated", "cc-by-sa-4.0",
                    # 用户确认(2026-10-02):仅内部研究使用,不公开分发,后续转正。
                    # 语义见 DATASET_SCHEMA.md §4;不是 Apache/MIT/CC 的替代品。
                    "Internal-Research-Use-Only"}
ALLOWED_SPLITS = {"raw", "train", "eval", "test"}

# 可校验内容的文件类型;其余文件(如 README/配置)只登记不校验
HASHABLE_SUFFIXES = {".jsonl", ".json", ".parquet", ".py", ".txt", ".md", ".zip", ".html", ".js", ".css", ".svg"}


@dataclass
class Entry:
    """manifest 单条记录。"""
    path: str                      # 相对项目根的路径
    sha256: str = ""               # 空 = 大文件未算,校验时跳过(如实记录,不伪造)
    size: int = 0
    source: str = ""               # 来源:数据集名/URL/生成命令
    license: str = ""              # 许可证;空 = 未标注(校验时报 quarantine)
    split: str = "raw"             # raw|train|eval|test
    notes: str = ""
    extra: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"path": self.path, "sha256": self.sha256, "size": self.size,
                "source": self.source, "license": self.license,
                "split": self.split, "notes": self.notes, **self.extra}


@dataclass
class Manifest:
    """manifest 顶层:名称/版本/生成时间/条目/策略。"""
    name: str
    entries: list[Entry] = field(default_factory=list)
    generated_at: str = ""
    version: int = MANIFEST_VERSION
    policy: str = ""

    def to_dict(self) -> dict:
        return {"name": self.name, "version": self.version,
                "generated_at": self.generated_at,
                "policy": self.policy,
                "entries": [e.to_dict() for e in self.entries]}

    @classmethod
    def from_dict(cls, d: dict) -> "Manifest":
        m = cls(name=d["name"], generated_at=d.get("generated_at", ""),
                version=d.get("version", MANIFEST_VERSION),
                policy=d.get("policy", ""))
        for e in d.get("entries", []):
            extra = {k: v for k, v in e.items()
                     if k not in {"path", "sha256", "size", "source", "license", "split", "notes"}}
            m.entries.append(Entry(
                path=e["path"], sha256=e.get("sha256", ""), size=e.get("size", 0),
                source=e.get("source", ""), license=e.get("license", ""),
                split=e.get("split", "raw"), notes=e.get("notes", ""), extra=extra))
        return m

    @classmethod
    def load(cls, path: Path) -> "Manifest":
        return cls.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2),
                        encoding="utf-8")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sample_content_hash(line: str) -> str:
    """样本级内容哈希:整行去首尾空白后哈希,用于训练/评测精确重叠检测。"""
    return sha256_text(line.strip())


def canonical_problem_text(line: str) -> str:
    """A8:防泄漏核心正文规范化——problem 优先(缺则 solution,再缺回退整行);
    仅折叠空白,不改写数学语义。ID/来源/类别/风格等元数据不参与。"""
    import re as _re

    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        return _re.sub(r"\s+", " ", line.strip())
    text = None
    if isinstance(obj, dict):
        for key in ("problem", "solution"):
            v = obj.get(key)
            if isinstance(v, str) and v.strip():
                text = v
                break
    if text is None:
        return _re.sub(r"\s+", " ", line.strip())
    return _re.sub(r"\s+", " ", text.strip())


def canonical_problem_hash(line: str) -> str:
    """A8:防泄漏身份哈希 = canonical_problem_text 的 SHA256。
    同题不同解/不同 id/不同元数据 → 同哈希;不同题不同哈希。"""
    return sha256_text(canonical_problem_text(line))


def schema_issues(m: Manifest) -> list[str]:
    """schema 级检查:manifest 结构本身是否合法。"""
    out: list[str] = []
    if m.version != MANIFEST_VERSION:
        out.append(f"manifest 版本 {m.version} 不受支持(当前 {MANIFEST_VERSION})")
    if not m.name.strip():
        out.append("manifest 缺少 name")
    seen: set[str] = set()
    for i, e in enumerate(m.entries):
        if not e.path.strip():
            out.append(f"entry #{i} 缺少 path")
            continue
        if e.path in seen:
            out.append(f"path 重复登记: {e.path}")
        seen.add(e.path)
        if e.license and e.license not in ALLOWED_LICENSES:
            out.append(f"{e.path}: 许可证 {e.license} 不在白名单 {sorted(ALLOWED_LICENSES)}")
        if e.split not in ALLOWED_SPLITS:
            out.append(f"{e.path}: split {e.split} 非法(允许 {sorted(ALLOWED_SPLITS)})")
        if e.size < 0:
            out.append(f"{e.path}: size 非法 {e.size}")
    return out
