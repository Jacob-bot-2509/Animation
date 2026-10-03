"""多文件发布事务(B6,纯标准库):journal + 原子单文件写入 + 失败可恢复。

GS1 复修后的不变量:
  1. 目标重复、备份路径碰撞、残留 journal → 发布前拒绝;
  2. journal 持久化 existed_before/stage/committed 标记,中断可按阶段恢复;
  3. 写入阶段失败 → 只回滚有备份的原文件;新文件直接删除残留;
  4. **commit 后清理阶段失败 → 绝不回滚**(原文件已无备份),保留 journal
     与备份,抛 PublishCleanupError 交人工恢复;
  5. recover:损坏 journal fail-closed 保留现场;冻结目标一律拒绝改写
     (rollback 也不绕过冻结);前滚仅清理备份;
  6. 写前冻结保护(复用 A7):目标被冻结/可疑锁 fail-closed 整组拒绝。
"""
from __future__ import annotations

import json
from pathlib import Path

from .atomic_write import atomic_write_text
from .dataset_intake import _assert_not_frozen  # noqa: F401 A7 冻结保护复用
from .fs_guard import ensure_not_exists

JOURNAL_SUFFIX = ".publish-journal.json"
BACKUP_SUFFIX = ".pub-bak"


class PublishCleanupError(RuntimeError):
    """commit 后清理失败:原文件已无备份,绝不自动回滚;保留 journal 交人工。"""


def journal_path(group_dir: Path, group_name: str) -> Path:
    return group_dir / f"{group_name}{JOURNAL_SUFFIX}"


def _backup_of(target: Path) -> Path:
    return Path(str(target) + BACKUP_SUFFIX)


def recover_publish(group_dir: Path, group_name: str, rollback: bool = True) -> dict:
    """恢复被中断的发布。journal 存在 = 上次未完成:
    rollback=True(默认)用备份还原(冻结目标拒绝改写);False 前滚清理备份。
    损坏 journal → fail-closed:保留现场、不删除、不声称恢复成功。
    """
    jp = journal_path(group_dir, group_name)
    if not jp.exists():
        return {"recovered": False, "actions": []}
    try:
        j = json.loads(jp.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"recovered": False, "error": f"journal 损坏,保留现场: {exc}",
                "actions": []}
    items = j.get("items", []) if isinstance(j, dict) else None
    if items is None or not all(
            isinstance(it, dict) and "path" in it and "existed_before" in it
            and "backup" in it for it in items):
        return {"recovered": False, "error": "journal 结构非法,保留现场",
                "actions": []}
    committed = set(j.get("committed", [])) if isinstance(j, dict) else set()
    actions: list[str] = []
    errors: list[str] = []
    for it in items:
        target = Path(it["path"])
        backup = Path(it["backup"])
        existed = bool(it["existed_before"])
        if rollback:
            if not existed:
                # 新文件:删除残留(未提交的原子写失败不会留半成品,存在即删)
                if target.exists():
                    target.unlink(missing_ok=True)
                    actions.append(f"删除残留新文件 {target.name}")
            elif backup.exists():
                try:
                    _assert_not_frozen(target)  # 冻结目标绝不改写(rollback 不绕过)
                except ValueError as exc:
                    errors.append(f"{target.name}: {exc}")
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                backup.replace(target)
                actions.append(f"回滚 {target.name}")
            elif str(target.resolve()) in committed:
                errors.append(f"{target.name}: 已写且无备份,无法自动回滚")
            # else: 未提交且无备份 → 原文件未被触碰(备份前的失败),无需动作
        elif backup.exists():
            backup.unlink(missing_ok=True)
            actions.append(f"前滚清理备份 {target.name}")
    if errors:
        return {"recovered": False, "error": "; ".join(errors),
                "actions": actions}  # 保留 journal,交人工
    jp.unlink(missing_ok=True)
    return {"recovered": True, "actions": actions}


def publish_files(group_dir: Path, group_name: str,
                  items: list[tuple[Path, str]],
                  force: bool = False) -> list[Path]:
    """整组发布文件(原子单文件 + 备份 + 分阶段 journal + 失败回滚)。"""
    if not items:
        raise ValueError("publish_files: 发布清单为空")
    targets = [t for t, _ in items]
    seen: set[str] = set()
    for t in targets:
        key = str(t.resolve())
        if key in seen:
            raise ValueError(f"publish_files: 重复目标 {t}(GS1 拒绝)")
        seen.add(key)
    group_dir.mkdir(parents=True, exist_ok=True)
    jp = journal_path(group_dir, group_name)
    ensure_not_exists(jp, force=False)  # 残留 journal 必须先 recover
    for target in targets:
        _assert_not_frozen(target)
        if target.exists() and not force:
            raise ValueError(f"publish_files: 目标已存在且未 --force: {target}")
        if _backup_of(target).exists():
            raise ValueError(f"publish_files: 备份路径已存在 {_backup_of(target)}"
                             "(GS1 碰撞拒绝,不删除既有备份)")
    # 1. journal:持久化 existed_before + stage
    journal = {"group": group_name, "stage": "writing", "committed": [],
               "items": [{"path": str(t.resolve()),
                          "backup": str(_backup_of(t).resolve()),
                          "existed_before": t.exists()} for t in targets]}
    atomic_write_text(jp, json.dumps(journal, ensure_ascii=False, indent=2))
    try:
        # 2. 写入阶段:备份 → 原子写 → 提交标记持久化
        for target, text in items:
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                backup = _backup_of(target)
                backup.write_bytes(target.read_bytes())
                target.unlink()
            atomic_write_text(target, text)
            journal["committed"].append(str(target.resolve()))
            atomic_write_text(jp, json.dumps(journal, ensure_ascii=False, indent=2))
    except BaseException:
        # 3. 写入阶段失败:回滚(只回滚有备份的原文件;新文件删残留);
        #    回滚完成才删 journal;回滚不了 → 保留 journal 交人工
        result = recover_publish(group_dir, group_name, rollback=True)
        if result.get("recovered"):
            raise
        jp.write_text(json.dumps(journal, ensure_ascii=False, indent=2),
                      encoding="utf-8")  # 保留现场
        raise
    # 4. commit 后清理:失败绝不回滚(原文件已无备份),保留 journal+备份
    journal["stage"] = "cleanup"
    atomic_write_text(jp, json.dumps(journal, ensure_ascii=False, indent=2))
    try:
        for it in journal["items"]:
            Path(it["backup"]).unlink(missing_ok=True)
    except OSError as exc:
        raise PublishCleanupError(
            f"清理备份失败,已保留 journal 与备份交人工恢复: {exc}") from exc
    jp.unlink()
    return targets
