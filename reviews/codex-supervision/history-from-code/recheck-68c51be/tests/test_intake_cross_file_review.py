"""End-to-end cross-file intake ID regressions."""
from pathlib import Path
from unittest import TestCase
import contextlib, importlib.util, io, sys, tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from animtrain.dataset_intake import intake_report
from tests.test_dataset_intake import clean_record,write_jsonl
spec=importlib.util.spec_from_file_location("review_cross_intake_cli",ROOT/"tools/dataset_intake.py")
cli=importlib.util.module_from_spec(spec);spec.loader.exec_module(cli)

class TestCrossFileIDReview(TestCase):
    def _files(self,root,same_name=False,unique=False):
        left,right=root/"left",root/"right"
        left.mkdir();right.mkdir()
        a,b=left/"samples.jsonl",right/("samples.jsonl" if same_name else "other.jsonl")
        write_jsonl(a,[clean_record(id="dup")])
        write_jsonl(b,[clean_record(id="unique" if unique else "dup",problem="other problem")])
        return a,b

    def test_same_basename_report_rejects_and_locates_both_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            a,b=self._files(Path(tmp),same_name=True)
            rep=intake_report([a,b])
            self.assertFalse(rep["ok"])
            self.assertEqual(rep["exit_code"],1)
            detail="\n".join(rep["problems"])
            self.assertIn(str(a.resolve()),detail)
            self.assertIn(str(b.resolve()),detail)

    def test_cli_checks_cross_file_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            a,b=self._files(Path(tmp))
            output=io.StringIO()
            with contextlib.redirect_stdout(output):
                rc=cli.main(["check",str(a),str(b)])
            self.assertEqual(rc,1,output.getvalue())

    def test_cli_checks_same_basename_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            a,b=self._files(Path(tmp),same_name=True)
            with contextlib.redirect_stdout(io.StringIO()):
                rc=cli.main(["check",str(a),str(b)])
            self.assertEqual(rc,1)

    def test_cli_accepts_unique_ids_in_same_basename_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            a,b=self._files(Path(tmp),same_name=True,unique=True)
            with contextlib.redirect_stdout(io.StringIO()):
                rc=cli.main(["check",str(a),str(b)])
            self.assertEqual(rc,0)
