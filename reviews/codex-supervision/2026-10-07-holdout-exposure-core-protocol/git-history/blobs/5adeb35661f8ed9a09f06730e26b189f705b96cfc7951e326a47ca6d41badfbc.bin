"""整体代码审查修复测试(msg_174-176):
A7 冻结写保护(convert/report 不得绕过锁,坏锁 fail-closed)、
A6 统一入口门禁(格式 allowlist/空输入/缺核心正文/同 split 重复 ID)、
A8 防泄漏规范化哈希(元数据不参与,同题不同解同哈希)、
G4 字段类型契约(非空字符串列表/容器类型)。合成 fixture,不碰真实数据。
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.dataset_intake import (  # noqa: E402
    check_record, convert_array_to_jsonl)
from animtrain.manifest import (  # noqa: E402
    Entry, Manifest, canonical_problem_hash, canonical_problem_text,
    sample_content_hash, sha256_file)
from animtrain.validate import validate_manifest  # noqa: E402


def clean_record(**over) -> dict:
    rec = {
        "id": "fixture-001", "category": "数学分析", "sub_category": "极限",
        "problem": "求极限 $\\lim_{x \\to 0} \\frac{\\sin x}{x}$ 的值。",
        "solution": "由夹逼定理,极限为 1。", "answer": "1",
        "scene_spec": {"objects": ["单位圆"], "steps": ["画单位圆"]},
        "source": "self-authored", "license": "Internal-Research-Use-Only",
    }
    rec.update(over)
    return rec


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records),
                    encoding="utf-8")


def make_manifest(root: Path, entries: list[tuple[str, str]]) -> Manifest:
    es = []
    for rel, split in entries:
        p = root / rel
        es.append(Entry(path=rel, sha256=sha256_file(p),
                        size=p.stat().st_size, source="x",
                        license="Internal-Research-Use-Only", split=split))
    return Manifest(name="t", entries=es)


class TestA7FreezeWriteProtection(unittest.TestCase):
    """G2:convert/report 写入口不得绕过冻结;坏锁 fail-closed。"""

    def _make_lock(self, d: Path, covered: Path) -> None:
        lock = {"freeze_lock_version": 1, "locked": True,
                "entries": [{"path": str(covered.resolve()), "sha256": "x" * 64,
                             "size": 0}], "n_files": 1}
        (d / "frozen.lock.json").write_text(json.dumps(lock, ensure_ascii=False),
                                            encoding="utf-8")

    def test_convert_refuses_frozen_target_even_force(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            src = d / "src.json"
            src.write_text(json.dumps([clean_record()], ensure_ascii=False),
                           encoding="utf-8")
            dst = d / "frozen.jsonl"
            dst.write_text("old\n", encoding="utf-8")
            self._make_lock(d, dst)
            with self.assertRaises(ValueError) as ctx:
                convert_array_to_jsonl(src, dst, force=True)
            self.assertIn("冻结", str(ctx.exception))
            self.assertEqual(dst.read_text(encoding="utf-8"), "old\n")  # 未被覆盖

    def test_convert_failclosed_on_suspicious_lock(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "bad.lock.json").write_text("not json", encoding="utf-8")
            src = d / "src.json"
            src.write_text(json.dumps([clean_record()], ensure_ascii=False),
                           encoding="utf-8")
            with self.assertRaises(ValueError) as ctx:
                convert_array_to_jsonl(src, d / "out.jsonl")
            self.assertIn("fail-closed", str(ctx.exception))

    def test_report_refuses_lock_output(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            write_jsonl(d / "a.jsonl", [clean_record()])
            out = subprocess.run(
                [sys.executable, "-X", "utf8",
                 str(ROOT / "tools" / "dataset_intake.py"), "report",
                 str(d / "a.jsonl"), "--out", str(d / "x.lock.json"), "--force"],
                capture_output=True, encoding="utf-8", errors="replace")
            self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
            self.assertIn("冻结", out.stdout)


class TestA6UnifiedEntryGate(unittest.TestCase):
    """G1:validate_manifest 与 intake 同口径拒绝格式/空输入/缺正文/重复 ID。"""

    def test_txt_data_entry_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.txt").write_text('{"id": "x"}\n', encoding="utf-8")
            r = validate_manifest(make_manifest(root, [("a.txt", "train")]), root)
            self.assertTrue(any("数据格式仅支持 JSONL" in p for p in r["problems"]))

    def test_empty_jsonl_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.jsonl").write_text("", encoding="utf-8")
            r = validate_manifest(make_manifest(root, [("a.jsonl", "train")]), root)
            self.assertTrue(any("数据文件为空" in p for p in r["problems"]), r)

    def test_id_only_sample_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.jsonl").write_text('{"id": "t1"}\n', encoding="utf-8")
            r = validate_manifest(make_manifest(root, [("a.jsonl", "train")]), root)
            self.assertTrue(any("缺核心正文" in p for p in r["problems"]), r)

    def test_same_split_duplicate_id_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write_jsonl(root / "a.jsonl", [clean_record(id="dup"),
                                           clean_record(id="dup", problem="另一题")])
            r = validate_manifest(make_manifest(root, [("a.jsonl", "train")]), root)
            self.assertTrue(any("ID 重复" in p for p in r["problems"]), r)

    def test_problem_wrong_type_rejected(self):
        """A6 残余反例:非空但类型错误的核心正文必须拒绝。"""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.jsonl").write_text(
                '{"id": "a", "problem": ["p"], "solution": "s", "answer": "1"}\n',
                encoding="utf-8")
            r = validate_manifest(make_manifest(root, [("a.jsonl", "train")]), root)
            self.assertTrue(any("类型非法" in p for p in r["problems"]), r)

    def test_answer_missing_quarantined_at_manifest(self):
        """A6 残余反例:answer=null 在 manifest 层与入场检查同口径 → quarantine。"""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.jsonl").write_text(
                '{"id": "a", "problem": "p", "solution": "s"}\n', encoding="utf-8")
            r = validate_manifest(make_manifest(root, [("a.jsonl", "train")]), root)
            self.assertTrue(any("缺 answer" in q for q in r["quarantines"]), r)
            self.assertFalse(r["ok"])
            self.assertEqual(r["exit_code"], 2)

    def test_sample_id_alias_duplicate_rejected(self):
        """A6 残余反例:仅 sample_id(legacy 别名)的重复也必须检出。"""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.jsonl").write_text(
                '{"sample_id": "dup", "problem": "p1", "solution": "s1", "answer": "1"}\n'
                '{"sample_id": "dup", "problem": "p2", "solution": "s2", "answer": "2"}\n',
                encoding="utf-8")
            r = validate_manifest(make_manifest(root, [("a.jsonl", "train")]), root)
            self.assertTrue(any("ID 重复" in p for p in r["problems"]), r)


class TestA8CanonicalHash(unittest.TestCase):
    """G3:防泄漏身份哈希只看核心正文,元数据不参与。"""

    def test_metadata_ignored(self):
        a = json.dumps(clean_record(id="a"), ensure_ascii=False)
        b = json.dumps(clean_record(id="b", function_family="x" * 50,
                                    source="other", visual_style="yyy"),
                       ensure_ascii=False)
        self.assertNotEqual(sample_content_hash(a), sample_content_hash(b))
        self.assertEqual(canonical_problem_hash(a), canonical_problem_hash(b))
        self.assertEqual(canonical_problem_text(a), canonical_problem_text(b))

    def test_same_problem_different_solution_same_hash(self):
        a = json.dumps(clean_record(solution="解法一"), ensure_ascii=False)
        b = json.dumps(clean_record(solution="完全不同的解法二"), ensure_ascii=False)
        self.assertEqual(canonical_problem_hash(a), canonical_problem_hash(b))

    def test_overlap_detected_via_canonical_hash(self):
        """train/eval 换 id/元数据但同题 → 精确重叠必须检出。"""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write_jsonl(root / "train.jsonl", [clean_record(id="t1")])
            write_jsonl(root / "eval.jsonl",
                        [clean_record(id="e1", function_family="zzz")])
            m = make_manifest(root, [("train.jsonl", "train"),
                                     ("eval.jsonl", "eval")])
            r = validate_manifest(m, root)
            self.assertTrue(any("精确重叠" in p for p in r["problems"]), r)


class TestG4TypeContract(unittest.TestCase):
    def test_objects_empty_list_rejected(self):
        rec = clean_record(scene_spec={"objects": [], "steps": ["画图"]})
        problems, _ = check_record(rec, 1)
        self.assertTrue(any("非空字符串列表" in p for p in problems), problems)

    def test_objects_null_item_rejected(self):
        rec = clean_record(scene_spec={"objects": [None], "steps": ["画图"]})
        problems, _ = check_record(rec, 1)
        self.assertTrue(any("非空字符串列表" in p for p in problems), problems)

    def test_category_container_rejected(self):
        rec = clean_record(category=["数学分析"])
        problems, _ = check_record(rec, 1)
        self.assertTrue(any("category 不是字符串" in p for p in problems), problems)

    def test_source_container_rejected(self):
        rec = clean_record(source={"x": 1})
        problems, _ = check_record(rec, 1)
        self.assertTrue(any("source 不是字符串" in p for p in problems), problems)


class TestB7OptionalMetaTypes(unittest.TestCase):
    def test_function_family_container_rejected(self):
        rec = clean_record(function_family=["多项式"])
        problems, _ = check_record(rec, 1)
        self.assertTrue(any("function_family 不是字符串" in p for p in problems),
                        problems)

    def test_visual_style_container_rejected(self):
        rec = clean_record(visual_style={"x": 1})
        problems, _ = check_record(rec, 1)
        self.assertTrue(any("visual_style 不是字符串" in p for p in problems),
                        problems)

    def test_efficiency_tags_bad_item_rejected(self):
        rec = clean_record(efficiency_tags=["ok", None])
        problems, _ = check_record(rec, 1)
        self.assertTrue(any("efficiency_tags" in p for p in problems), problems)

    def test_check_fields_cli_empty_jsonl_fails(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "empty.jsonl").write_text("", encoding="utf-8")
            out = subprocess.run(
                [sys.executable, "-X", "utf8",
                 str(ROOT / "tools" / "check_fields.py"), "--jsonl",
                 str(d / "empty.jsonl")],
                capture_output=True, encoding="utf-8", errors="replace")
            self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
            self.assertIn("空", out.stdout)


if __name__ == "__main__":
    unittest.main()
