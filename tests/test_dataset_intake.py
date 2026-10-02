"""候选数据集入场检查测试(msg_152:P0 聚焦验收)。

覆盖: JSON 数组拒绝/显式转换、重复与冲突 ID、缺 answer、空元数据、
许可证语义、中文进公式、疑似漏反斜杠(只报不改)、干净样本通过。
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
    check_duplicate_ids, check_intake_file, check_record,
    convert_array_to_jsonl, detect_json_array, intake_report)


def clean_record(**over) -> dict:
    """一条可通过入场检查的干净样本(合成 fixture,不代表真实数据)。"""
    rec = {
        "id": "fixture-001",
        "category": "数学分析",
        "sub_category": "极限",
        "function_family": "夹逼定理",
        "visual_style": "面积比较",
        "efficiency_tags": ["高亮比较"],
        "problem": "求极限 $\\lim_{x \\to 0} \\frac{\\sin x}{x}$ 的值。",
        "solution": "由夹逼定理, $\\cos x < \\frac{\\sin x}{x} < 1$, 故极限为 1。",
        "answer": "1",
        "scene_spec": {"objects": ["单位圆"], "steps": ["画单位圆"]},
        "source": "self-authored",
        "license": "internal-generated",
    }
    rec.update(over)
    return rec


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records),
                    encoding="utf-8")


class TestArrayRejectionAndConvert(unittest.TestCase):
    def test_detect_json_array(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.json"
            p.write_text(json.dumps([{"id": 1}], ensure_ascii=False), encoding="utf-8")
            self.assertTrue(detect_json_array(p))
            q = Path(d) / "y.jsonl"
            write_jsonl(q, [{"id": 1}])
            self.assertFalse(detect_json_array(q))

    def test_array_rejected_as_sample_entry(self):
        """P0#1: JSON 数组不得被误当正式样本通过。"""
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "dataset_x.json"
            p.write_text(json.dumps([clean_record()], ensure_ascii=False),
                         encoding="utf-8")
            rep = check_intake_file(p)
            self.assertEqual(rep["status"], "rejected")
            self.assertEqual(rep["exit_code"], 1)
            self.assertTrue(any("JSON 数组" in x for x in rep["problems"]), rep)

    def test_cli_check_rejects_array(self):
        """CLI 层面同样拒绝,退出码 1。"""
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "dataset_x.json"
            p.write_text(json.dumps([clean_record()], ensure_ascii=False),
                         encoding="utf-8")
            out = subprocess.run(
                [sys.executable, "-X", "utf8",
                 str(ROOT / "tools" / "dataset_intake.py"), "check", str(p)],
                capture_output=True, encoding="utf-8", errors="replace")
            self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
            self.assertIn("JSON 数组", out.stdout)

    def test_convert_roundtrip_and_no_overwrite(self):
        """显式转换:内容一致、原文件不动、默认拒绝覆盖、--force 可覆盖。"""
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "src.json"
            records = [clean_record(id="a"), clean_record(id="b")]
            src.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
            before = src.read_text(encoding="utf-8")
            dst = Path(d) / "dst.jsonl"
            result = convert_array_to_jsonl(src, dst)
            self.assertEqual(result["n_records"], 2)
            self.assertEqual(src.read_text(encoding="utf-8"), before)  # 原文件未动
            lines = dst.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual([json.loads(l)["id"] for l in lines], ["a", "b"])
            # 默认拒绝覆盖
            with self.assertRaises(ValueError):
                convert_array_to_jsonl(src, dst)
            # --force 覆盖
            convert_array_to_jsonl(src, dst, force=True)

    def test_convert_cli(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "src.json"
            src.write_text(json.dumps([clean_record()], ensure_ascii=False),
                           encoding="utf-8")
            dst = Path(d) / "out.jsonl"
            out = subprocess.run(
                [sys.executable, "-X", "utf8",
                 str(ROOT / "tools" / "dataset_intake.py"), "convert",
                 str(src), str(dst)], capture_output=True, encoding="utf-8",
                errors="replace")
            self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
            self.assertTrue(dst.exists())


class TestDuplicateIds(unittest.TestCase):
    def test_same_id_same_content_reported(self):
        recs = [clean_record(id="dup"), clean_record(id="dup")]
        problems = check_duplicate_ids([(1, recs[0]), (2, recs[1])])
        self.assertEqual(len(problems), 1)
        self.assertIn("整条重复", problems[0])
        self.assertIn("1", problems[0]) and self.assertIn("2", problems[0])

    def test_same_id_different_content_conflict(self):
        recs = [clean_record(id="dup"), clean_record(id="dup",
                                                     problem="另一个题目")]
        problems = check_duplicate_ids([(1, recs[0]), (7, recs[1])])
        self.assertEqual(len(problems), 1)
        self.assertIn("冲突", problems[0])
        self.assertIn("7", problems[0])  # 行号可定位

    def test_duplicate_id_fails_intake(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "dup.jsonl"
            write_jsonl(p, [clean_record(id="dup"), clean_record(id="dup")])
            rep = check_intake_file(p)
            self.assertEqual(rep["status"], "rejected")


class TestFieldChecks(unittest.TestCase):
    def test_missing_answer_is_quarantine_not_silent_ok(self):
        """P0#3: 缺 answer 不得 ok=true,按 candidate 语义报告。"""
        rec = clean_record()
        del rec["answer"]
        problems, quarantines = check_record(rec, 1)
        self.assertEqual(problems, [])
        self.assertTrue(any("缺 answer" in q for q in quarantines), quarantines)

    def test_missing_key_field_is_problem(self):
        for key in ("id", "category", "problem", "solution", "scene_spec",
                    "source", "license"):
            rec = clean_record()
            del rec[key]
            problems, _ = check_record(rec, 1)
            self.assertTrue(any(f"缺关键字段" in p and key in p for p in problems),
                            f"{key}: {problems}")

    def test_empty_metadata_reported(self):
        """P0#3: 可选元数据缺/空 → quarantine,不得假绿。"""
        rec = clean_record(function_family="", visual_style="", efficiency_tags=[])
        _, quarantines = check_record(rec, 1)
        self.assertTrue(any("可选元数据缺/空" in q for q in quarantines), quarantines)

    def test_missing_answer_makes_file_candidate(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "noans.jsonl"
            rec = clean_record()
            del rec["answer"]
            write_jsonl(p, [rec])
            rep = check_intake_file(p)
            self.assertEqual(rep["status"], "candidate")
            self.assertEqual(rep["exit_code"], 2)
            self.assertFalse(rep["ok"])

    def test_unknown_top_level_field_reported(self):
        rec = clean_record(custom_field="x")
        _, quarantines = check_record(rec, 1)
        self.assertTrue(any("非正式字段" in q for q in quarantines), quarantines)


class TestLicenseSemantics(unittest.TestCase):
    def test_internal_license_is_quarantine(self):
        """P0#4: Internal-Research-Use-Only 不是公开再分发许可证。"""
        rec = clean_record(license="Internal-Research-Use-Only")
        _, quarantines = check_record(rec, 1)
        self.assertTrue(any("不是公开再分发许可证" in q for q in quarantines),
                        quarantines)

    def test_unknown_license_is_problem(self):
        rec = clean_record(license="whatever-v1")
        problems, _ = check_record(rec, 1)
        self.assertTrue(any("不在白名单" in p for p in problems), problems)

    def test_whitelist_license_passes(self):
        for lic in ("apache-2.0", "mit", "internal-generated", "cc-by-sa-4.0"):
            rec = clean_record(license=lic)
            problems, quarantines = check_record(rec, 1)
            self.assertEqual(problems, [], f"{lic}: {problems}")
            self.assertEqual([q for q in quarantines if "license" in q], [],
                             f"{lic}: {quarantines}")


class TestLatexRules(unittest.TestCase):
    def test_cjk_inside_math_is_problem(self):
        """P0#5: 中文进公式必渲染失败(TeX 无 CJK)。"""
        rec = clean_record(problem="求 $x 加 y$ 的值。")
        problems, _ = check_record(rec, 1)
        self.assertTrue(any("中文" in p for p in problems), problems)

    def test_cjk_in_scene_spec_detected(self):
        rec = clean_record(scene_spec={"objects": ["曲线$y=高$"]})
        problems, _ = check_record(rec, 1)
        self.assertTrue(any("中文" in p for p in problems), problems)

    def test_render_risk_reported_but_not_rewritten(self):
        """疑似漏反斜杠只报 render_risk,不自动改写数学语义。"""
        for bad in ("$\\lim_{b\\to +infty}x$", "$lim_{b\\to 1} x$",
                    "$\\arctan b$ 与 $arctan b$"):
            rec = clean_record(problem=f"讨论 {bad} 的性质。")
            _, quarantines = check_record(rec, 1)
            self.assertTrue(any("疑似漏反斜杠" in q for q in quarantines),
                            f"{bad}: {quarantines}")
            # 内容未被改写
            self.assertIn(bad, rec["problem"])

    def test_clean_latex_ok(self):
        rec = clean_record(problem="求 $\\lim_{x \\to 0} \\frac{\\sin x}{x}$。")
        problems, quarantines = check_record(rec, 1)
        self.assertFalse(any("漏反斜杠" in q or "中文" in p
                             for p in problems for q in quarantines))


class TestIntakeFileAndReport(unittest.TestCase):
    def test_clean_file_passes(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ok.jsonl"
            write_jsonl(p, [clean_record(id="a"), clean_record(id="b")])
            rep = check_intake_file(p)
            self.assertEqual(rep["status"], "clean")
            self.assertTrue(rep["ok"])
            self.assertEqual(rep["exit_code"], 0)

    def test_bad_json_line_and_non_object_reported(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.jsonl"
            p.write_text("not json\n[1,2]\n", encoding="utf-8")
            rep = check_intake_file(p)
            self.assertTrue(any("JSON 解析失败" in x for x in rep["problems"]))
            self.assertTrue(any("不是 JSON 对象" in x for x in rep["problems"]))

    def test_intake_report_aggregates_categories(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            write_jsonl(d / "a.jsonl", [clean_record(id="a"),
                                        clean_record(id="b", category="概率论")])
            write_jsonl(d / "b.jsonl", [clean_record(id="c")])
            rep = intake_report([d / "a.jsonl", d / "b.jsonl"])
            self.assertEqual(rep["n_records"], 3)
            self.assertEqual(rep["categories"], {"数学分析": 2, "概率论": 1})
            self.assertEqual(rep["status"], "clean")


if __name__ == "__main__":
    unittest.main()
