import ast
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("native_formula_tested", ROOT / "tools/native_render_pilot.py")
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)

class NativeFormulaTests(unittest.TestCase):
    def setUp(self):
        owner = ROOT / "reviews/codex-supervision/2026-10-08-regression-work"
        owner.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="native-formula-", dir=owner)
        self.root = Path(self.temp.name)
        self.owner = owner
        assert self.root.resolve().is_relative_to(self.owner.resolve())
        (self.root / "reviews").mkdir()
        self.patch = mock.patch.object(n.core, "ROOT", self.root)
        self.patch.start()
        self.record = {"id": "sample", "problem": "$x^2$", "solution": "$x+x$", "answer": "$2x$", "scene_spec": {"objects": ["$x^2$"], "steps": ["$2x$"]}}
        self.binding = {"id": "sample", "record_sha256": "a"*64, "math_sha256": "b"*64, "source_sha256": "c"*64}

    def tearDown(self):
        self.patch.stop()
        assert self.root.resolve().is_relative_to(self.owner.resolve())
        self.temp.cleanup()

    def work(self):
        return self.root / "reviews/render-sample"

    def test_mathex_uses_formula_variable_not_empty_constant(self):
        tree = ast.parse(n.build_scene(self.record))
        calls = [x for x in ast.walk(tree) if isinstance(x, ast.Call) and isinstance(x.func, ast.Name) and x.func.id == "MathTex"]
        self.assertEqual(len(calls), 1)
        self.assertIsInstance(calls[0].args[0], ast.Name)
        self.assertEqual(calls[0].args[0].id, "formula")

    def test_long_formula_not_discarded(self):
        long = "+".join(["x"]*150)
        self.record["problem"] = "$"+long+"$"
        formulas, _ = n.formula_inventory(self.record)
        self.assertIn(long, formulas)

    def test_all_supported_delimiters(self):
        self.assertEqual(n.extract_formulas(r"$a$ $b$ \(c\) \[d\]"), ["a","b","c","d"])

    def test_display_dollar_formula_preserved_complete(self):
        dollar = chr(36)
        formula = r"f=2(x+y/2+az/2)^2+(y-az)^2/2+(2-a^2)z^2"
        self.assertEqual(n.extract_formulas(dollar*2+formula+dollar*2), [formula])

    def test_mixed_inline_display_and_brackets_preserve_order(self):
        dollar = chr(36)
        slash = chr(92)
        text = dollar+"a"+dollar+" "+dollar*2+"b"+dollar*2+" "+slash+"(c"+slash+") "+slash+"[d"+slash+"] "+dollar+"e"+dollar
        self.assertEqual(n.extract_formulas(text), ["a", "b", "c", "d", "e"])

    def test_display_empty_unclosed_and_wrong_closer_rejected(self):
        dollar = chr(36)
        for text in (dollar*4, dollar*2+"x", dollar*2+"x"+dollar):
            with self.assertRaises(ValueError):
                n.extract_formulas(text)

    def test_cjk_formula_uses_xelatex_without_rewriting_text(self):
        text = chr(0x5176)+chr(0x4ed6)
        self.record["answer"] = chr(36)+r"f=0,\\text{"+text+"}"+chr(36)
        tree = ast.parse(n.build_scene(self.record))
        formulas = next(ast.literal_eval(x.value) for x in tree.body if isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id=="FORMULAS" for t in x.targets))
        self.assertIn(r"f=0,\\text{"+text+"}", formulas)
        calls = [x for x in ast.walk(tree) if isinstance(x, ast.Call) and isinstance(x.func, ast.Name)]
        template = next(x for x in calls if x.func.id=="TexTemplate")
        self.assertEqual({x.arg:ast.literal_eval(x.value) for x in template.keywords}, {"tex_compiler":"xelatex","output_format":".xdv"})
        math = next(x for x in calls if x.func.id=="MathTex")
        self.assertTrue(any(x.arg=="tex_template" and isinstance(x.value,ast.Name) and x.value.id=="template" for x in math.keywords))

    def test_escaped_dollar_not_formula(self):
        self.assertEqual(n.extract_formulas(r"price \$5; $x$"), ["x"])

    def test_unclosed_and_empty_formula_rejected(self):
        for text in ("$x", r"\[x", "$"):
            with self.assertRaises(ValueError):
                n.extract_formulas(text)

    def test_unique_complete_occurrence_inventory(self):
        formulas, locations = n.formula_inventory(self.record)
        self.assertEqual(formulas, ["x^2","x+x","2x"])
        self.assertEqual(len(locations), 5)

    def test_no_placeholder_when_no_formula(self):
        self.record["problem"] = self.record["solution"] = self.record["answer"] = "no formulas"
        self.record["scene_spec"] = {"objects": [], "steps": []}
        with self.assertRaises(ValueError):
            n.formula_inventory(self.record)

    def fake_process(self, command, **kwargs):
        work = Path(kwargs["cwd"])
        media = work / "media"
        media.mkdir()
        (media/"ConceptScene.mp4").write_bytes(b"verified fake video for control-flow test only")
        return subprocess.CompletedProcess(command, 0, b"ok", b"")

    def test_nonzero_process_not_success_even_video_present(self):
        def failed(command, **kwargs):
            proc = self.fake_process(command, **kwargs)
            proc.returncode = 1
            return proc
        with mock.patch.object(n.subprocess, "run", side_effect=failed):
            row = n.render_one("sample", self.work(), self.record, self.binding)
        self.assertEqual(row["status"], "FAIL_LOCAL_FORMULA_RENDER")

    def test_zero_exit_without_nonempty_video_fails(self):
        with mock.patch.object(n.subprocess, "run", return_value=subprocess.CompletedProcess([],0,b"",b"")):
            row = n.render_one("sample", self.work(), self.record, self.binding)
        self.assertEqual(row["status"], "FAIL_LOCAL_FORMULA_RENDER")

    def test_timeout_bytes_preserved_and_not_success(self):
        with mock.patch.object(n.subprocess, "run", side_effect=subprocess.TimeoutExpired([],1,output=b"partial",stderr=b"timeout")):
            row = n.render_one("sample", self.work(), self.record, self.binding)
        self.assertTrue(row["timed_out"])
        self.assertEqual((self.work()/"stdout.bin").read_bytes(), b"partial")
        self.assertEqual(row["status"], "FAIL_LOCAL_FORMULA_RENDER")

    def test_failed_batch_exit_code_and_receipt(self):
        with mock.patch.object(n.core, "load_record_bindings", return_value=[self.binding]), mock.patch.object(n.core, "load_record", return_value=self.record), mock.patch.object(n.subprocess, "run", return_value=subprocess.CompletedProcess([],1,b"",b"bad")):
            out = self.root / "reviews/batch"
            self.assertEqual(n.run(["sample"], out), 3)
        receipt = json.loads((out/"receipt.json").read_bytes())
        self.assertEqual(receipt["summary"]["failed"], 1)
        self.assertFalse(receipt["production_evidence"])

    def test_existing_batch_refused(self):
        out = self.root / "reviews/existing"
        out.mkdir(parents=True)
        (out/"receipt.json").write_bytes(b"old")
        with mock.patch.object(n.core, "load_record_bindings", return_value=[self.binding]), mock.patch.object(n.core, "load_record", return_value=self.record):
            with self.assertRaises(FileExistsError):
                n.run(["sample"], out)
        self.assertEqual((out/"receipt.json").read_bytes(), b"old")

    def test_source_binding_failure_before_output(self):
        out = self.root / "reviews/stale"
        with mock.patch.object(n.core, "load_record_bindings", side_effect=ValueError("stale actual version")):
            with self.assertRaises(ValueError):
                n.run(["sample"], out)
        self.assertFalse(out.exists())

    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):
            n.run(["sample","sample"], self.root/"reviews/duplicates")

    def test_complete_local_success_has_bound_video_and_no_global_green(self):
        with mock.patch.object(n.core, "load_record_bindings", return_value=[self.binding]), mock.patch.object(n.core, "load_record", return_value=self.record), mock.patch.object(n.subprocess, "run", side_effect=self.fake_process):
            out = self.root / "reviews/complete"
            self.assertEqual(n.run(["sample"],out),0)
        receipt = json.loads((out/"receipt.json").read_bytes())
        row = receipt["results"][0]
        self.assertEqual(row["unique_formulas"],3)
        self.assertEqual(row["record_sha256"],self.binding["record_sha256"])
        self.assertTrue(row["mp4_sha256"])
        self.assertFalse(receipt["PASS_CORE_SCOPE_issued"])
        self.assertEqual(receipt["visual_acceptance"],"NOT_REVIEWED")

if __name__ == "__main__":
    unittest.main()
