"""冻结数据集锁(B3,纯标准库):eval/test 冻结后不可变,哈希变化大声失败。

前项目教训(20/20 评测污染)的根治手段:评测集一旦锁定,任何字节变化
都必须被检出并拒绝,而不是静默漂移。

用法:
  freeze_set(files, lock_path, meta)   → 生成锁(每个文件 sha256+size)
  check_frozen(lock_path)              → 校验锁内文件哈希一致,返回问题清单
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

LOCK_VERSION = 1


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def freeze_set(files: list[Path], lock_path: Path, meta: dict | None = None) -> dict:
    """把一组文件冻结进锁(锁与数据同目录约定;已存在锁拒绝覆盖)。"""
    if not lock_path.name.endswith('.lock.json'):
        raise ValueError(f"冻结锁必须命名为 *.lock.json(统一发现约定),实际: {lock_path.name}")
    if lock_path.exists():
        raise ValueError(f"锁已存在,拒绝覆盖: {lock_path}(冻结后不可重新生成)")
    if not files:
        raise ValueError("待冻结文件列表为空 —— 空锁无效(BR3)")
    entries = []
    for f in files:
        if not f.is_file():
            raise ValueError(f"待冻结文件不存在: {f}")
        entries.append({"path": str(f), "sha256": sha256_file(f),
                        "size": f.stat().st_size})
    lock = {"freeze_lock_version": LOCK_VERSION,
            "locked": True,
            "n_files": len(entries),
            "meta": meta or {},
            "entries": entries,
            "policy": "冻结后文件不可修改;哈希不一致即拒绝使用该数据集"}
    from .atomic_write import atomic_write_text  # noqa: PLC0415 局部导入避免环
    atomic_write_text(lock_path, json.dumps(lock, ensure_ascii=False, indent=2))
    return lock


def frozen_paths(lock_path: Path) -> set[str]:
    """锁内冻结文件路径集合(写入前保护用;锁损坏时返回空集+警告由 check_frozen 负责)。"""
    try:
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    return {str(Path(e["path"]).resolve())
            for e in lock.get("entries", []) if isinstance(e, dict) and "path" in e}


def _is_freeze_lock(p: Path) -> bool:
    """判断文件是否是冻结锁(有 freeze_lock_version 字段且 locked)。"""
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return isinstance(d, dict) and "freeze_lock_version" in d


def discover_locks(roots: list[Path], max_depth: int = 4) -> tuple[list[Path], list[Path]]:
    """自动发现冻结锁:在 roots 各目录及向上 max_depth 层父目录里
    找 *.lock.json。返回 (valid_locks, suspicious_locks):
      valid       带 freeze_lock_version 的合法冻结锁
      suspicious  范围内的 *.lock.json 但无法识别(坏 JSON/无冻结字段)
                  —— fail closed:发现可疑锁标记必须拒绝写入,不得忽略

    BR5 复验(omitted_corrupt / omitted_nonstandard):
    写入保护不得靠调用方记得传参,也不得靠锁恰好可解析。
    """
    found_valid: set[Path] = set()
    found_suspicious: set[Path] = set()
    for root in roots:
        cur = root if root.is_dir() else root.parent
        for _ in range(max_depth):
            if cur is None or not cur.is_dir():
                break
            for p in cur.glob("*.lock.json"):
                if _is_freeze_lock(p):
                    found_valid.add(p.resolve())
                else:
                    found_suspicious.add(p.resolve())
            if cur.parent == cur:
                break
            cur = cur.parent
    return sorted(found_valid), sorted(found_suspicious)


def check_frozen(lock_path: Path) -> list[str]:
    """校验锁内每个文件与锁记录一致。返回问题清单(空 = 冻结完好)。

    BR3 严格:schema 不完整、locked 非 True、entries 为空、n_files 与
    条目数不一致 —— 全部可定位失败,不默认通过。
    """
    try:
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"锁不可读: {exc}"]
    if not isinstance(lock, dict):
        return ["锁不是 JSON 对象"]
    if lock.get("freeze_lock_version") != LOCK_VERSION:
        return [f"锁版本不支持: {lock.get('freeze_lock_version')}"]
    if lock.get("locked") is not True:
        return [f"锁未处于 locked 状态: {lock.get('locked')!r}(BR3)"]
    entries = lock.get("entries")
    if not isinstance(entries, list) or not entries:
        return ["锁 entries 为空或缺失 —— 空锁无效(BR3)"]
    if lock.get("n_files") != len(entries):
        return [f"n_files({lock.get('n_files')}) 与 entries 数({len(entries)})不一致(BR3)"]
    problems: list[str] = []
    for i, e in enumerate(entries):
        if not isinstance(e, dict) or "path" not in e:
            problems.append(f"entry #{i} 缺 path 字段(BR3)")
            continue
        p = Path(e["path"])
        if not p.is_file():
            problems.append(f"{e['path']}: 文件不存在(冻结数据集被删/移动)")
            continue
        actual = sha256_file(p)
        if actual != e["sha256"]:
            problems.append(f"{e['path']}: 哈希变化(冻结后不可修改;"
                            f"登记 {e['sha256'][:12]}…,实际 {actual[:12]}…)")
        if p.stat().st_size != e["size"]:
            problems.append(f"{e['path']}: size 变化(登记 {e['size']},"
                            f"实际 {p.stat().st_size})")
    return problems
