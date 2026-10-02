"""Cross-module CLI contracts: synthetic data only, no model execution."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]
from tools import make_manifest

class TestCliContracts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, content):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return p

    def cli(self, tool, *args, cwd=None):
        return subprocess.run(
            [sys.executable, str(ROOT / "tools" / tool), *map(str, args)],
            cwd=cwd or ROOT, capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING":"utf-8", "PYTHONDONTWRITEBYTECODE":"1"})

    def test_make_manifest_main_uses_supplied_argv(self):
        self.write("data/train/a.jsonl",
                   '{"id":"a","problem":"p","solution":"s","answer":"1"}\n')
        out = self.root / "data/manifest.json"
        with patch.object(sys, "argv", ["unrelated-program"]):
            result = make_manifest.main(["--dir",str(out.parent),"--out",str(out),
                "--source","synthetic","--license","internal-generated"])
        self.assertEqual(result, 0)
        self.assertEqual(self.cli("data_check.py","--manifest",out).returncode, 0)

    def test_make_manifest_cli_and_existing_output(self):
        self.write("data/train/a.jsonl", '{"id":"a"}\n')
        out = self.root / "data/manifest.json"
        args=("--dir",out.parent,"--out",out,"--source","synthetic",
              "--license","internal-generated")
        r=self.cli("make_manifest.py",*args)
        self.assertEqual(r.returncode,0,r.stderr+r.stdout)
        before=out.read_bytes()
        r=self.cli("make_manifest.py",*args)
        self.assertNotEqual(r.returncode,0)
        self.assertEqual(out.read_bytes(),before)
        self.assertNotIn("Traceback",r.stderr)

    def test_manifest_output_elsewhere_rejected_before_writes(self):
        self.write("data/train/a.jsonl", '{"id":"a"}\n')
        out=self.root/"elsewhere/manifest.json"
        r=self.cli("make_manifest.py","--dir",self.root/"data","--out",out)
        self.assertNotEqual(r.returncode,0)
        self.assertFalse(out.exists())
        self.assertNotIn("Traceback",r.stderr)

    def test_force_field_report_never_overwrites_input(self):
        p=self.write("pool.jsonl",'{"id":"a","problem":"p","solution":"s","answer":0}\n')
        before=p.read_bytes()
        r=self.cli("check_fields.py","--jsonl",p,"--report",p,"--force")
        self.assertNotEqual(r.returncode,0)
        self.assertEqual(p.read_bytes(),before)

    def test_field_report_is_written_separately(self):
        p=self.write("pool.jsonl",'{"id":"a"}\n')
        out=self.root/"report.json"
        r=self.cli("check_fields.py","--jsonl",p,"--report",out)
        self.assertEqual(r.returncode,1)
        self.assertEqual(json.loads(out.read_text(encoding="utf-8"))["bad"][0]["sample_id"],"a")

    def test_empty_required_option_rejected(self):
        p=self.write("pool.jsonl",'{"id":"a"}\n')
        r=self.cli("check_fields.py","--jsonl",p,"--required"," , ")
        self.assertEqual(r.returncode,2)

    def test_empty_or_missing_code_directory_is_not_pass(self):
        for p in (self.root,self.root/"missing"):
            with self.subTest(path=p):
                self.assertNotEqual(self.cli("check_code.py","--dir",p).returncode,0)

    def test_default_whitelist_independent_of_cwd_and_scope_visible(self):
        p=self.write("scene.py",'x = Text("hello")\n')
        r=self.cli("check_code.py","--code",p,cwd=self.root)
        self.assertEqual(r.returncode,0,r.stderr+r.stdout)
        self.assertIn("UNVERIFIED",r.stdout)

    def test_empty_or_missing_scan_is_not_pass(self):
        for p in (self.root,self.root/"missing"):
            with self.subTest(path=p):
                self.assertNotEqual(self.cli("data_check.py","--scan",p).returncode,0)

    def test_empty_manifest_not_pass(self):
        p=self.write("empty.json",json.dumps({"name":"empty","entries":[]}))
        self.assertNotEqual(self.cli("data_check.py","--manifest",p).returncode,0)

    def test_invalid_threshold_rejected(self):
        for val in ("nan","inf","1.01","-0.01"):
            with self.subTest(value=val):
                r=self.cli("data_check.py","--dry-run","--near-dup-threshold",val)
                self.assertEqual(r.returncode,2)

    def test_conflicting_modes_rejected(self):
        r=self.cli("data_check.py","--dry-run","--manifest","missing.json")
        self.assertEqual(r.returncode,2)

if __name__ == "__main__":
    unittest.main()
