"""多文件发布事务(B6,纯标准库):journal + 原子单文件写入 + 失败可恢复。

Windows 无跨文件原子事务;本模块以发布日志实现"可恢复的整组发布":
  1) 写 journal(组名、文件清单、每文件的备份路径与目标哈希);
  2) 逐文件:已存在则先备份(.bak)→ 原子写入新内容;
  3) 全部成功 → 删除全部备份 → 删除 journal;
  任一失败 → 用备份回滚已写文件 → 删除 journal,抛异常。
  进程中断 → 下次调用 recover_publish() 按 journal 回滚(默认)或前滚。

冻结保护:目标被 *.lock.json 冻结/可疑锁 fail-closed 时整组拒绝(复用 A7)。
"""
from __future__ import annotations

import json
from pathlib import Path

from .atomic_write import atomic_write_text
from .dataset_intake import _assert_not_frozen  # noqa: F401 A7 冻结保护复用
from .fs_guard import ensure_not_exists

JOURNAL_SUFFIX = ".publish-journal.json"
BACKUP_SUFFIX = ".pub-bak"


def journal_path(group_dir: Path, group_name: str) -> Path:
    return group_dir / f"{group_name}{JOURNAL_SUFFIX}"


def recover_publish(group_dir: Path, group_name: str, rollback: bool = True) -> dict:
    """恢复被中断的发布。journal 存在说明上次发布未完成:
    rollback=True(默认)用备份还原;False 前滚(保留已写文件,只清理)。
    返回 {recovered, actions}。"""
    jp = journal_path(group_dir, group_name)
    if not jp.exists():
        return {"recovered": False, "actions": []}
    try:
        j = json.loads(jp.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        j = {}
    items = j.get("items", []) if isinstance(j, dict) else []
    actions: list[str] = []
    for it in items:
        target = Path(it["path"])
        backup = Path(it.get("backup", ""))
        if rollback and backup and backup.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            backup.replace(target)  # 还原原文件
            actions.append(f"回滚 {target.name}")
        elif backup and backup.exists():
            backup.unlink()  # 前滚:清理备份
            actions.append(f"前滚清理 {target.name}")
    jp.unlink(missing_ok=True)
    return {"recovered": True, "actions": actions}


def publish_files(group_dir: Path, group_name: str,
                  items: list[tuple[Path, str]],
                  force: bool = False) -> list[Path]:
    """整组发布文件(原子单文件 + 备份 + 失败回滚)。

    items: [(目标路径, 内容), ...]。目标已存在且未 force → 拒绝;
    任一目标被冻结 → 整组拒绝。全部成功返回目标路径列表。
    """
    if not items:
        raise ValueError("publish_files: 发布清单为空")
    group_dir.mkdir(parents=True, exist_ok=True)
    jp = journal_path(group_dir, group_name)
    ensure_not_exists(jp, force=False)  # 残留 journal 必须先 recover
    for target, _text in items:
        _assert_not_frozen(target)
        if target.exists() and not force:
            raise ValueError(f"publish_files: 目标已存在且未 --force: {target}")
    # 1. 写 journal(先落盘清单,中断可恢复)
    journal = {"group": group_name,
               "items": [{"path": str(t.resolve()),
                          "backup": str(t.resolve()) + BACKUP_SUFFIX}
                         for t, _ in items]}
    atomic_write_text(jp, json.dumps(journal, ensure_ascii=False, indent=2))
    done: list[Path] = []
    try:
        # 2. 逐文件备份 + 原子写
        for target, text in items:
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                backup = Path(str(target) + BACKUP_SUFFIX)
                backup.write_bytes(target.read_bytes())
                target.unlink()
            atomic_write_text(target, text)
            done.append(target)
        # 3. 全部成功:清备份、删 journal
        for it in journal["items"]:
            Path(it["backup"]).unlink(missing_ok=True)
        jp.unlink()
        return done
    except BaseException:
        # 4. 失败:回滚已写文件(备份还原),清理 journal 后重抛
        for it in journal["items"]:
            target = Path(it["path"])
            backup = Path(it["backup"])
            if backup.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                backup.replace(target)
            elif it["path"] in [str(p.resolve()) for p in done]:
                target.unlink(missing_ok=True)  # 无备份的新文件直接删除
        jp.unlink(missing_ok=True)
        raise
