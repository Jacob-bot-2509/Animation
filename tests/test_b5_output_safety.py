"""B5 output/sampling safety; all writable fixtures stay inside the project."""
import contextlib,copy,importlib.util,io,json,shutil,sys,tempfile,unittest,uuid
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
P=Path(__file__).absolute().parents[1]
sys.path.insert(0,str(P/"src"))
from animtrain.b5_output import new_output_dir
def module(name,file):
    s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
ann=module("b5_sampler_safety","tools/b5_annotation_set.py")
cal=module("b5_report_safety","tools/b5_calibrate.py")
SCRATCH=P/"reviews/codex-supervision/2026-10-17-b5-safety-test-runtime"

class B5SafetyTests(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(exist_ok=True);self.root=Path(tempfile.mkdtemp(dir=SCRATCH,prefix="output-"))
        self.input=self.root/"records.json";self.input.write_text(json.dumps([
            {"id":"a","problem":"text $|x|$ end","category":"synthetic"},
            {"id":"b","problem":"text $|y|$ end","category":"synthetic"}]))
    def tearDown(self):
        assert self.root.resolve().is_relative_to(SCRATCH.resolve()) and self.root!=SCRATCH
        shutil.rmtree(self.root)
    def test_exclusive_directory_no_existing_changes(self):
        target=self.root/"new";self.assertEqual(new_output_dir(target),target)
        (target/"old.txt").write_text("original")
        with self.assertRaises(FileExistsError):new_output_dir(target)
        self.assertEqual((target/"old.txt").read_text(),"original")
    def test_outside_ads_device_dot_and_frozen_rejected(self):
        for target in (Path(r"D:\code/x"),self.root/"x:ads",self.root/"NUL.txt",
                       str(self.root)+"/../outside",P/"archives/reviews/codex-supervision/2026-10-17-template-diversity-review/new"):
            with self.subTest(target=str(target)):
                with self.assertRaises(ValueError):new_output_dir(target)
    def test_reparse_rejected(self):
        with patch.object(Path,"is_symlink",return_value=True):
            with self.assertRaises(ValueError):new_output_dir(self.root/"new")
    def test_exact_boundary_and_no_float_scores(self):
        pairs=ann._build_pairs({"a":{"problem":"abcdef"},"b":{"problem":"abcdeg"}},0,1,0,42)
        self.assertEqual(len(pairs),1);self.assertEqual(pairs[0]["jaccard"],"1/3")
        self.assertEqual(pairs[0]["similarity_counts"],{"intersection":1,"union":3})
        self.assertNotIsInstance(pairs[0]["jaccard"],float)
    def test_invalid_sample_counts_rejected(self):
        for counts in ((-1,1,1),(True,1,1),(0,0,0)):
            with self.assertRaises(ValueError):ann._build_pairs({},*counts,42)
    def test_conflicting_id_text_rejected(self):
        self.input.write_text(json.dumps([{"id":"same","problem":"one"},{"id":"same","problem":"two"}]))
        with self.assertRaises(ValueError):ann._load_problems([self.input])
    def test_missing_id_empty_problem_or_array_rejected(self):
        for data in ({},[],[{"problem":"x"}],[{"id":"a","problem":""}]):
            self.input.write_text(json.dumps(data))
            with self.assertRaises(ValueError):ann._load_problems([self.input])
    def test_annotation_cli_protects_existing_labeled_output(self):
        target=self.root/"labeled";target.mkdir();f=target/"b5-annotation-set.json";f.write_text('{"user_labels":"KEEP"}')
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit) as ex:
            ann.main(["--records",str(self.input),"--top","10","--mid","10","--low","10","--out",str(target)])
        self.assertEqual(ex.exception.code,2);self.assertEqual(f.read_text(),'{"user_labels":"KEEP"}')
    def test_annotation_new_output_fraction_and_math_bars(self):
        target=self.root/"fresh"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ann.main(["--records",str(self.input),"--top","10","--mid","10","--low","10","--out",str(target)]),0)
        data=json.loads((target/"b5-annotation-set.json").read_text())
        self.assertEqual(len(data["pairs"]),1);Fraction(data["pairs"][0]["jaccard"])
        text=(target/"b5-annotation-set.md").read_text(encoding="utf-8")
        self.assertIn("$|x|$",text);self.assertNotIn(r"$\|x\|$",text)
    def fake_report(self):
        return {"calibration":{"calibrated":False,"note":"synthetic"},"mismatches":[]}
    def test_calibration_cli_protects_existing_report(self):
        target=self.root/"old-report";target.mkdir();f=target/"b5-calibration-report.json";f.write_text("KEEP")
        source=self.root/"annotation.json";source.write_text('{"pairs":[]}')
        with patch.object(cal,"build_report",return_value=self.fake_report()),contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit) as ex:
            cal.main(["--annotation",str(source),"--out",str(target)])
        self.assertEqual(ex.exception.code,2);self.assertEqual(f.read_text(),"KEEP")
    def test_calibration_new_output_explicitly_diagnostic(self):
        target=self.root/"report";source=self.root/"annotation.json";source.write_text('{"pairs":[]}')
        with patch.object(cal,"build_report",return_value=self.fake_report()),patch.object(cal,"render_markdown",return_value="synthetic\n"),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cal.main(["--annotation",str(source),"--out",str(target)]),0)
        data=json.loads((target/"b5-calibration-report.json").read_text())
        self.assertEqual(data["qualification"],"DEVELOPMENT_DIAGNOSTIC_NOT_INDEPENDENT_CALIBRATION")
    def test_default_outputs_do_not_target_data(self):
        old=self.root/"data/b5-annotation-set";old.mkdir(parents=True);(old/"b5-annotation-set.json").write_text("KEEP")
        with patch.object(ann,"ROOT",self.root),contextlib.redirect_stdout(io.StringIO()):
            ann.main(["--records",str(self.input),"--top","10","--mid","10","--low","10"])
        self.assertEqual((old/"b5-annotation-set.json").read_text(),"KEEP")
        self.assertEqual(len(list((self.root/"reviews/b5-candidates").glob("annotation-*/b5-annotation-set.json"))),1)
        source=self.root/"annotation.json";source.write_text('{"pairs":[]}')
        old=self.root/"data/b5-calibration-report";old.mkdir();(old/"b5-calibration-report.json").write_text("KEEP")
        with patch.object(cal,"ROOT",self.root),patch.object(cal,"build_report",return_value=self.fake_report()),patch.object(cal,"render_markdown",return_value="synthetic"),contextlib.redirect_stdout(io.StringIO()):
            cal.main(["--annotation",str(source)])
        self.assertEqual((old/"b5-calibration-report.json").read_text(),"KEEP")
        self.assertEqual(len(list((self.root/"reviews/b5-candidates").glob("calibration-*/b5-calibration-report.json"))),1)

if __name__=="__main__":unittest.main(verbosity=2)
