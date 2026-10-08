"""Input preservation regressions for intake conversion/report CLI."""
from pathlib import Path
from unittest import TestCase
import contextlib, importlib.util, io, json, sys, tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from animtrain.dataset_intake import convert_array_to_jsonl
from tests.test_dataset_intake import clean_record,write_jsonl

spec=importlib.util.spec_from_file_location("guard_intake_cli",ROOT/"tools/dataset_intake.py")
cli=importlib.util.module_from_spec(spec);spec.loader.exec_module(cli)

class TestIntakeInputGuards(TestCase):
    def test_convert_force_cannot_replace_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/"source.json"
            src.write_text(json.dumps([clean_record()],ensure_ascii=False),encoding="utf-8")
            before=src.read_bytes()
            with self.assertRaises(ValueError):
                convert_array_to_jsonl(src,src,force=True)
            self.assertEqual(src.read_bytes(),before)

    def test_convert_alias_cli_fails_without_changing_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);src=root/"source.json"
            src.write_text(json.dumps([clean_record()],ensure_ascii=False),encoding="utf-8")
            before=src.read_bytes()
            with contextlib.redirect_stdout(io.StringIO()):
                rc=cli.main(["convert",str(src),str(root/"."/"source.json"),"--force"])
            self.assertNotEqual(rc,0)
            self.assertEqual(src.read_bytes(),before)

    def test_report_force_cannot_replace_any_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);a,b=root/"a.jsonl",root/"b.jsonl"
            write_jsonl(a,[clean_record(id="a")]);write_jsonl(b,[clean_record(id="b")])
            before={p:p.read_bytes() for p in [a,b]}
            with contextlib.redirect_stdout(io.StringIO()):
                rc=cli.main(["report",str(a),str(b),"--out",str(b),"--force"])
            self.assertNotEqual(rc,0)
            for p,content in before.items():self.assertEqual(p.read_bytes(),content)

    def test_new_report_keeps_inputs_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);src=root/"input.jsonl";out=root/"report.md"
            write_jsonl(src,[clean_record()])
            before=src.read_bytes()
            with contextlib.redirect_stdout(io.StringIO()):
                rc=cli.main(["report",str(src),"--out",str(out)])
            self.assertEqual(rc,0)
            self.assertTrue(out.is_file())
            self.assertEqual(src.read_bytes(),before)
