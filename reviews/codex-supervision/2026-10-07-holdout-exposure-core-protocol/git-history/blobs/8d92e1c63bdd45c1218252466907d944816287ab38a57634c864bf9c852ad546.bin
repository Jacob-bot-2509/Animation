"""标准 JSONL 字段映射与校验(msg_101-3,纯标准库)。

核心字段(problem/solution/answer/scene_spec 等)必须与真实项目一一对应,
不得丢失;失败保留原始 sample_id 与原因;不重写原始数据。
"""
from __future__ import annotations

import json
from pathlib import Path

# 标准核心字段(按数据类型配置;reasoning 数据 = problem/solution/answer,
# animation 数据 = scene_spec/code)
DEFAULT_REQUIRED = ["problem", "solution", "answer"]


def _is_missing(value) -> bool:
    """R7:None 或空字符串才算缺失;0/False/空列表是合法值。"""
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    return False


def check_fields(rows: list[dict], required: list[str] | None = None,
                 start_line: int = 1) -> list[dict]:
    """逐行校验必填字段。返回 [{sample_id, line, missing, reason}]。

    start_line: 首行的真实源行号(R7:调用方须传真实行号,不得恒为 1)。
    """
    required = required or DEFAULT_REQUIRED
    bad: list[dict] = []
    for i, row in enumerate(rows, start_line):
        missing = [f for f in required if _is_missing(row.get(f))]
        if missing:
            bad.append({"sample_id": row.get("id") or row.get("sample_id") or f"<line-{i}>",
                        "line": i, "missing": missing,
                        "reason": f"缺失必填字段: {', '.join(missing)}"})
    return bad


def check_jsonl(path: Path, required: list[str] | None = None) -> list[dict]:
    """读 JSONL 逐行校验(只读,不重写)。JSON 解析失败也保留行号与原因。"""
    required = required or DEFAULT_REQUIRED
    bad: list[dict] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            bad.append({"sample_id": f"<line-{i}>", "line": i, "missing": [],
                        "reason": f"JSON 解析失败: {exc}"})
            continue
        if not isinstance(row, dict):
            bad.append({"sample_id": f"<line-{i}>", "line": i, "missing": [],
                        "reason": "行不是 JSON 对象"})
            continue
        bad += check_fields([row], required, start_line=i)
    return bad
