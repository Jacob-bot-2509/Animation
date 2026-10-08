"""多文件发布事务(B6,纯标准库):journal + 原子单文件写入 + 失败可恢复。

msg_216 复修后的不变量:
  1. 整组命名空间互斥:target/backup/journal 路径(含别名)两两不得重叠,
     发布前整体预验,任一冲突整组拒绝;
  2. 备份原子写入(tmp+os.replace),记录 old/new 内容哈希绑定;
  3. journal 严格 schema(group/stage/committed/items{path,backup,
     existed_before,hash_old,hash_new}),损坏/缺字段 fail-closed 保留现场;
  4. 阶段感知恢复:stage=writing 才允许回滚;stage=cleanup 只前滚清理,
     绝不把已提交组回滚;
  5. 回滚幂等:目标哈希==hash_old 即已恢复,跳过;每恢复一步持久化进度;
  6. 冻结保护覆盖全部改写/删除动作(含新文件残留删除),rollback 不绕过;
  7. 清理失败 → PublishCleanupError,保留 journal+备份交人工,绝不回滚。
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .atomic_write import atomic_write_bytes, atomic_write_text
from .dataset_intake import _assert_not_frozen  # noqa: F401 A7 冻结保护复用
from .fs_guard import ensure_not_exists

JOURNAL_SUFFIX = ".publish-journal.json"
BACKUP_SUFFIX = ".pub-bak"
STAGES = ("writing", "cleanup")


class PublishCleanupError(RuntimeError):
    """commit 后清理失败:已提交组绝不回滚;保留 journal 交人工。"""


def journal_path(group_dir: Path, group_name: str) -> Path:
    return group_dir / f"{group_name}{JOURNAL_SUFFIX}"


def _backup_of(target: Path) -> Path:
    return Path(str(target) + BACKUP_SUFFIX)


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def _validate_journal(j: dict, jp: Path) -> str | None:
    """严格 schema 校验;返回错误原因或 None。"""
    if not isinstance(j, dict):
        return "journal 非对象"
    if not isinstance(j.get("group"), str) or not j["group"].strip():
        return "journal 缺 group"
    if j.get("stage") not in STAGES:
        return f"journal stage 非法: {j.get('stage')!r}"
    if not isinstance(j.get("committed"), list):
        return "journal 缺 committed 列表"
    items = j.get("items")
    if not isinstance(items, list) or not items:
        return "journal items 缺失/空"
    for it in items:
        if not isinstance(it, dict):
            return "journal item 非对象"
        for key in ("path", "backup", "existed_before", "hash_old", "hash_new"):
            if key not in it:
                return f"journal item 缺字段 {key}"
        if not isinstance(it["existed_before"], bool):
            return "journal item existed_before 非 bool"
        for hkey in ("hash_old", "hash_new"):
            if not isinstance(it[hkey], str):
                return f"journal item {hkey} 非法"
    return None


def recover_publish(group_dir: Path, group_name: str, rollback: bool = True) -> dict:
    """恢复被中断的发布。stage=cleanup 时只前滚(已提交组绝不回滚);
    stage=writing 且 rollback=True 时幂等回滚;损坏 journal fail-closed。"""
    jp = journal_path(group_dir, group_name)
    if not jp.exists():
        return {"recovered": False, "actions": []}
    try:
        j = json.loads(jp.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"recovered": False, "error": f"journal 损坏,保留现场: {exc}",
                "actions": []}
    err = _validate_journal(j, jp)
    if err:
        return {"recovered": False, "error": f"{err},保留现场", "actions": []}
    forward_only = j["stage"] == "cleanup"
    actions: list[str] = []
    errors: list[str] = []
    committed = set(j["committed"])
    for it in j["items"]:
        target = Path(it["path"])
        backup = Path(it["backup"])
        existed = it["existed_before"]
        if forward_only or not rollback:
            # 已提交组/前滚:只清理备份,绝不回滚
            backup.unlink(missing_ok=True)
            actions.append(f"前滚清理备份 {backup.name}")
            continue
        # 回滚阶段:幂等
        if existed:
            if target.exists() and it["hash_old"] \
                    and _sha256_file(target) == it["hash_old"]:
                continue  # 已恢复,幂等跳过
            if backup.exists():
                try:
                    _assert_not_frozen(target)
                except ValueError as exc:
                    errors.append(f"{target.name}: {exc}")
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                backup.replace(target)
                actions.append(f"回滚 {target.name}")
            elif str(target.resolve()) in committed:
                errors.append(f"{target.name}: 已写且无备份,无法自动回滚")
            # else: 未提交且无备份 → 原文件未被触碰
        else:
            if target.exists():
                try:
                    _assert_not_frozen(target)  # 冻结新文件也不得删除
                except ValueError as exc:
                    errors.append(f"{target.name}: {exc}")
                    continue
                target.unlink(missing_ok=True)
                actions.append(f"删除残留新文件 {target.name}")
        # 幂等:每恢复一步持久化进度(把已恢复项标入 committed 的镜像)
        j["restored"] = j.get("restored", []) + [it["path"]]
        atomic_write_text(jp, json.dumps(j, ensure_ascii=False, indent=2))
    if errors:
        return {"recovered": False, "error": "; ".join(errors),
                "actions": actions}  # 保留 journal
    jp.unlink(missing_ok=True)
    return {"recovered": True, "actions": actions}


def publish_files(group_dir: Path, group_name: str,
                  items: list[tuple[Path, str]],
                  force: bool = False) -> list[Path]:
    """整组发布文件(命名空间互斥 + 原子备份 + 分阶段 journal + 幂等回滚)。"""
    if not items:
        raise ValueError("publish_files: 发布清单为空")
    group_dir.mkdir(parents=True, exist_ok=True)
    jp = journal_path(group_dir, group_name)
    ensure_not_exists(jp, force=False)  # 残留 journal 必须先 recover
    # 1. 命名空间互斥预验:target/backup/journal 两两不得重叠(含别名)
    targets = [t for t, _ in items]
    resolved: dict[str, str] = {}
    for t in targets:
        key = str(t.resolve())
        if key in resolved:
            raise ValueError(f"publish_files: 重复目标 {t}(msg_216)")
        resolved[key] = "target"
    jkey = str(jp.resolve())
    if jkey in resolved:
        raise ValueError("publish_files: 目标与 journal 路径重叠(msg_216)")
    resolved[jkey] = "journal"
    for t in targets:
        b = _backup_of(t)
        bkey = str(b.resolve())
        if bkey in resolved:
            raise ValueError(f"publish_files: 备份路径与 {resolved[bkey]} "
                             f"重叠: {b}(msg_216)")
        resolved[bkey] = "backup"
        if b.exists():
            raise ValueError(f"publish_files: 备份路径已存在 {b}"
                             "(msg_216 碰撞拒绝,不删除既有备份)")
        _assert_not_frozen(t)
        if t.exists() and not force:
            raise ValueError(f"publish_files: 目标已存在且未 --force: {t}")
    # 2. journal:持久化 existed_before + 新旧内容哈希绑定
    journal = {"group": group_name, "stage": "writing", "committed": [],
               "restored": [], "items": []}
    for t, text in items:
        journal["items"].append({
            "path": str(t.resolve()), "backup": str(_backup_of(t).resolve()),
            "existed_before": t.exists(),
            "hash_old": _sha256_file(t) if t.exists() else "",
            "hash_new": hashlib.sha256(text.encode("utf-8")).hexdigest()})
    atomic_write_text(jp, json.dumps(journal, ensure_ascii=False, indent=2))
    try:
        # 3. 写入阶段:原子备份 → 原子写 → 提交标记持久化
        for target, text in items:
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                atomic_write_bytes(_backup_of(target), target.read_bytes())
                target.unlink()
            atomic_write_text(target, text)
            journal["committed"].append(str(target.resolve()))
            atomic_write_text(jp, json.dumps(journal, ensure_ascii=False, indent=2))
    except BaseException:
        result = recover_publish(group_dir, group_name, rollback=True)
        if result.get("recovered"):
            raise
        raise  # 恢复失败时 journal 已在 recover 中保留
    # 4. commit 后清理:失败绝不回滚
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
