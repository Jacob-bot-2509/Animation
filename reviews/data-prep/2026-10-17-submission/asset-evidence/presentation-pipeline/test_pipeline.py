"""管线 v2 回归:fixture 全部在临时目录,不触碰 reviews/ 下的真实产物。"""
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import unittest
import uuid
from pathlib import Path

PIPE_DIR = Path(__file__).resolve().parent
SUBMISSION = PIPE_DIR.parent
REAL_TEMPLATE = SUBMISSION / "template-fix-candidate/render_templates_v4_candidate.py"
TEST_BASE = Path(os.environ.get("PP_TEST_BASE") or (PIPE_DIR.parents[4] / ".pipeline-tests"))

sys.path.insert(0, str(PIPE_DIR))
import pipeline as pp  # noqa: E402

spec = importlib.util.spec_from_file_location("_test_template_v3", REAL_TEMPLATE)
tpl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tpl)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


RECORDS = [
    {"id": "s-001", "problem": "设 $x>0$，求极限。",
     "scene_spec": {"steps": [
         "先画单位圆，标出 $A=(1,0)$，再作切线。",
         "第二步说明很长很长需要断行处理的内容，确保标点优先断开不出现断词。"],
         "objects": ["单位圆", "切线"]},
     "answer": "1"},
    {"id": "s-002", "problem": "计算 $1+1$。",
     "scene_spec": {"steps": ["直接相加。"], "objects": []}, "answer": "2"},
]


class Fixture:
    def __init__(self, base: Path):
        self.base = base
        self.root = base / "root"
        self.root.mkdir()
        self.cand = base / "cand"
        self.records = base / "records.jsonl"
        self.bind = self.cand / "presentation-bindings.jsonl"
        self.out = base / "runs"
        self.paths = pp.Paths(root=self.root, cand=self.cand, bind=self.bind,
                              template=REAL_TEMPLATE, records=self.records, out=self.out)
        lines = []
        for rec in RECORDS:
            line = json.dumps(rec, ensure_ascii=False)
            lines.append(line)
            (self.cand / "scenes").mkdir(parents=True, exist_ok=True)
            sp = rec["scene_spec"]
            sources = [rec["problem"], *sp["steps"], rec["answer"]]
            code, plan = tpl.scene_blocks_v2(sources[0], sources[1:-1], sources[-1])
            self.scene_path(rec["id"]).write_text(code, encoding="utf-8", newline="\n")
        self.records.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        self.template_sha = sha(REAL_TEMPLATE.read_bytes())
        self.rows = [self._row(rec, line) for rec, line in zip(RECORDS, lines)]
        write_jsonl(self.bind, self.rows)

    def scene_path(self, sid: str) -> Path:
        return self.cand / "scenes" / f"{sid}.py"

    def _row(self, rec: dict, line: str) -> dict:
        sp = rec["scene_spec"]
        sources = [rec["problem"], *sp["steps"], rec["answer"]]
        code, plan = tpl.scene_blocks_v2(sources[0], sources[1:-1], sources[-1])
        return {
            "sample_id": rec["id"],
            "corrected_record_sha256": sha(line.encode()),
            "scene_sha256": sha(self.scene_path(rec["id"]).read_bytes()),
            "template_version": tpl.TEMPLATE_VERSION,
            "template_sha256": self.template_sha,
            "plan_sha256": sha(pp.canonical_plan_bytes(plan)),
            "plan_rows": len(plan["rows"]),
            "plan_pages_provisional": len(plan["provisional_pages"]),
            "coverage_ok": True,
            "layout_status": plan["layout"],
            "geometry_objects": sp.get("objects") or [],
            "render_verdict": "PENDING_REVIEW",
            "visual_verdict": "PENDING_REVIEW",
        }

    def refresh_bindings(self) -> None:
        write_jsonl(self.bind, self.rows)

    def pack(self, sid: str) -> Path:
        return self.out / "review-packs" / sid


class PipelineTests(unittest.TestCase):
    def setUp(self):
        TEST_BASE.mkdir(parents=True, exist_ok=True)
        self.tmp = TEST_BASE / ("pp-test-" + uuid.uuid4().hex[:10])
        self.tmp.mkdir()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.fx = Fixture(self.tmp)

    # ---- build

    def test_build_creates_packs_and_receipt(self):
        receipt = pp.build(self.fx.paths)
        self.assertEqual(receipt["status"], "BUILT_PENDING_RENDER")
        self.assertEqual(receipt["stages"]["generate"]["samples"], 2)
        self.assertEqual(receipt["stages"]["render"]["state"], "REFUSED_GATE_UNAVAILABLE")
        self.assertIs(receipt["stages"]["render"]["rendered"], False)
        self.assertRegex(receipt["run_id"], r"^[0-9a-f]{16}$")
        for sid in ("s-001", "s-002"):
            pack = self.fx.pack(sid)
            for name in ("scene.py", "scene_runnable.py", "problem.md", "answer.md",
                         "plan.json", "bindings.json", "conclusion-sheet.md"):
                self.assertTrue((pack / name).is_file(), f"{sid}/{name} missing")
            b = json.loads((pack / "bindings.json").read_text(encoding="utf-8"))
            self.assertEqual(sha((pack / "scene.py").read_bytes()), b["scene_sha256"])
            self.assertEqual(sha((pack / "scene_runnable.py").read_bytes()), b["runnable_sha256"])
            self.assertEqual(sha((pack / "plan.json").read_bytes()), b["plan_sha256"])
            self.assertIn("class Candidate(Scene)", (pack / "scene_runnable.py").read_text(encoding="utf-8"))
            self.assertIn("from manim import *", (pack / "scene_runnable.py").read_text(encoding="utf-8"))

    def test_build_is_idempotent_and_leaves_no_staging(self):
        pp.build(self.fx.paths)
        before = {p.name: sha(p.read_bytes())
                  for p in (self.fx.out / "review-packs" / "s-001").iterdir()}
        pp.build(self.fx.paths)
        after = {p.name: sha(p.read_bytes())
                 for p in (self.fx.out / "review-packs" / "s-001").iterdir()}
        self.assertEqual(before, after)
        leftovers = [p.name for p in self.fx.out.iterdir()
                     if p.name.startswith(".stage-") or p.name.startswith(".trash-")]
        self.assertEqual(leftovers, [])

    def test_tampered_scene_refused_and_previous_receipt_kept(self):
        pp.build(self.fx.paths)
        receipt = self.fx.out / "pipeline-receipt.json"
        old = sha(receipt.read_bytes())
        self.fx.scene_path("s-001").write_text("tampered\n", encoding="utf-8", newline="\n")
        with self.assertRaises(pp.Refusal) as ctx:
            pp.build(self.fx.paths)
        self.assertIn("scene_sha256 mismatch", str(ctx.exception))
        self.assertEqual(sha(receipt.read_bytes()), old)
        failed = json.loads((self.fx.out / "pipeline-receipt.FAILED.json").read_text(encoding="utf-8"))
        self.assertEqual(failed["status"], "FAILED")
        self.assertIn("scene_sha256 mismatch", failed["error"])

    def test_stale_template_sha_refused(self):
        for row in self.fx.rows:
            row["template_sha256"] = "0" * 64
        self.fx.refresh_bindings()
        with self.assertRaises(pp.Refusal) as ctx:
            pp.build(self.fx.paths)
        self.assertIn("template_sha256 mismatch", str(ctx.exception))

    def test_coverage_false_refused(self):
        for row in self.fx.rows:
            row["coverage_ok"] = False
        self.fx.refresh_bindings()
        with self.assertRaises(pp.Refusal) as ctx:
            pp.build(self.fx.paths)
        self.assertIn("coverage_ok is false", str(ctx.exception))

    def test_illegal_sample_id_refused(self):
        for row in self.fx.rows:
            row["sample_id"] = "../evil"
        self.fx.refresh_bindings()
        with self.assertRaises(pp.Refusal) as ctx:
            pp.build(self.fx.paths)
        self.assertIn("illegal sample_id", str(ctx.exception))

    def test_scene_not_reproducible_refused(self):
        scene = self.fx.scene_path("s-002")
        text = scene.read_text(encoding="utf-8") + "# extra\n"
        scene.write_text(text, encoding="utf-8", newline="\n")
        for row in self.fx.rows:
            if row["sample_id"] == "s-002":
                row["scene_sha256"] = sha(scene.read_bytes())
        self.fx.refresh_bindings()
        with self.assertRaises(pp.Refusal) as ctx:
            pp.build(self.fx.paths)
        self.assertIn("not reproducible", str(ctx.exception))

    def test_broken_fragment_wrapper_refused(self):
        scene = self.fx.scene_path("s-001")
        broken = "        def broken(:\n"
        scene.write_text(broken, encoding="utf-8", newline="\n")
        with self.assertRaises(pp.Refusal) as ctx:
            pp.build(self.fx.paths)
        self.assertIn("scene_sha256 mismatch", str(ctx.exception))  # 先被哈希拦下

    def test_gate_callable_contract(self):
        receipt = pp.build(self.fx.paths, gate=lambda: (True, "synthetic"))
        render = receipt["stages"]["render"]
        self.assertEqual(render["state"], "CERTIFICATE_VALID_RENDER_NOT_RUN")
        self.assertIs(render["rendered"], False)
        self.assertEqual(render["message"], "synthetic")

    def test_gate_refusal_state(self):
        receipt = pp.build(self.fx.paths, gate=lambda: (False, "certificate missing"))
        self.assertEqual(receipt["stages"]["render"]["state"], "REFUSED")

    # ---- verify

    def test_verify_incomplete_then_complete(self):
        pp.build(self.fx.paths)
        verdicts = pp.stage_verify(self.fx.paths)
        self.assertEqual(verdicts["overall"], "REVIEW_INCOMPLETE")
        for sid in ("s-001", "s-002"):
            sheet = self.fx.pack(sid) / "conclusion-sheet.md"
            text = sheet.read_text(encoding="utf-8")
            text = text.replace("- [ ] 过", "- [x] 过")
            text = text.replace("- 审核人:\n", "- 审核人: tester\n")
            text = text.replace("- 时间:\n", "- 时间: 2026-10-17 20:00\n")
            write(sheet, text)
        verdicts = pp.stage_verify(self.fx.paths)
        self.assertEqual(verdicts["overall"], "REVIEW_COMPLETE")
        self.assertEqual({p["verdict"] for p in verdicts["packs"]}, {"过"})

    def test_verify_flags_tampered_runnable(self):
        pp.build(self.fx.paths)
        p = self.fx.pack("s-001") / "scene_runnable.py"
        write(p, p.read_text(encoding="utf-8") + "# tamper\n")
        verdicts = pp.stage_verify(self.fx.paths)
        self.assertEqual(verdicts["overall"], "REVIEW_INCOMPLETE")
        issues = {i for pack in verdicts["packs"] for i in pack["issues"]}
        self.assertTrue(any("sha mismatch" in i for i in issues), issues)

    def test_verify_requires_reason_for_yaogai(self):
        pp.build(self.fx.paths)
        sheet = self.fx.pack("s-001") / "conclusion-sheet.md"
        text = sheet.read_text(encoding="utf-8").replace("- [ ] 要改", "- [x] 要改")
        text = text.replace("- 审核人:\n", "- 审核人: tester\n").replace("- 时间:\n", "- 时间: 2026-10-17 20:00\n")
        write(sheet, text)
        verdicts = pp.stage_verify(self.fx.paths)
        s1 = [p for p in verdicts["packs"] if p["sample_id"] == "s-001"][0]
        self.assertIn("要改 without 修改意见", s1["issues"])

    def test_verify_requires_packs(self):
        with self.assertRaises(pp.Refusal):
            pp.stage_verify(self.fx.paths)


if __name__ == "__main__":
    unittest.main(verbosity=2)
