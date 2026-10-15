"""Small local fixtures for safe archival-tool entrypoints; no historical scan."""
from pathlib import Path
import contextlib, hashlib, importlib.util, io, json, socket, subprocess, sys, tempfile, unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import witness_transfer_common as common

def load(name):
    spec = importlib.util.spec_from_file_location("_archival_test_" + name, ROOT / "tools" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

pack = load("render_packs_v2")
html = load("render_packs_v2_html")
index = load("holdout_earliest_index")
MODULES = (pack, html, index)

class ArchivalEntrypointTests(unittest.TestCase):
    def setUp(self):
        root = common.mkdir(ROOT / "reviews/witness-automation/test-work")
        self.base = Path(tempfile.mkdtemp(prefix="archival-entrypoints-", dir=root))
        # Keep all fixtures, including frozen directories, after verification.
    def invoke(self, module, args):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            rc = module.main(args)
        return rc, out.getvalue()
    def source(self, pairs=None):
        source = self.base / "source"
        source.mkdir()
        rec = {"id": "exact-fixture", "problem": "$1/2$", "solution": "$1/3+1/6=1/2$", "answer": "$1/2$"}
        raw = (json.dumps(rec) + "\n").encode()
        candidate = source / "candidate.jsonl"
        candidate.write_bytes(raw)
        bindings = [{"source_path": before, "path": str(candidate.relative_to(ROOT)),
                     "raw_sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
                    for before in (pairs or ["fixture.jsonl"])]
        (source / "candidate-source-bindings.json").write_text(json.dumps(bindings), encoding="utf-8")
        return source, candidate, raw

    def test_default_plan_never_executes_output_or_scan(self):
        for module in MODULES:
            with self.subTest(module=module.__name__), mock.patch.object(socket, "socket", side_effect=AssertionError), \
                 mock.patch.object(subprocess, "run", side_effect=AssertionError), \
                 mock.patch.object(module, "_fresh_output", side_effect=AssertionError):
                rc, out = self.invoke(module, [])
                self.assertEqual(rc, 3)
                self.assertEqual(json.loads(out)["status"], "PLAN")
                self.assertFalse(json.loads(out)["writes"])

    def test_execute_requires_explicit_new_output(self):
        for module in MODULES:
            rc, _ = self.invoke(module, ["--execute"])
            self.assertEqual(rc, 2)

    def test_existing_output_bytes_are_preserved(self):
        existing = self.base / "existing"
        existing.mkdir()
        original = b"do not overwrite"
        (existing / "report.json").write_bytes(original)
        for module in MODULES:
            rc, _ = self.invoke(module, ["--execute", "--out", str(existing)])
            self.assertEqual(rc, 2)
            self.assertEqual((existing / "report.json").read_bytes(), original)
            self.assertEqual({p.name for p in existing.iterdir()}, {"report.json"})

    def test_frozen_ancestor_cannot_gain_new_outputs(self):
        frozen = self.base / "frozen"
        frozen.mkdir()
        (frozen / "delivery-manifest.json").write_bytes(b"{}")
        for module in MODULES:
            output = frozen / module.__name__
            rc, _ = self.invoke(module, ["--execute", "--out", str(output)])
            self.assertEqual(rc, 2)
            self.assertFalse(output.exists())
        self.assertEqual((frozen / "delivery-manifest.json").read_bytes(), b"{}")

    def test_output_outside_project_is_rejected_before_creation(self):
        output = ROOT.parent / (self.base.name + "-outside")
        self.assertFalse(output.exists())
        for module in MODULES:
            rc, _ = self.invoke(module, ["--execute", "--out", str(output)])
            self.assertEqual(rc, 2)
        self.assertFalse(output.exists())

    def test_pack_preserves_exact_fraction_and_source_bytes(self):
        source, candidate, raw = self.source()
        output = self.base / "new-pack"
        with mock.patch.object(pack, "SUP", source):
            rc, _ = self.invoke(pack, ["--execute", "--out", str(output)])
        self.assertEqual(rc, 0)
        self.assertEqual(candidate.read_bytes(), raw)
        text = (output / "render-packs-v2/fixture.md").read_text(encoding="utf-8")
        self.assertIn("$1/3+1/6=1/2$", text)
        report = json.loads((output / "render-packs-v2-report.json").read_text())
        self.assertEqual(report["total_records"], 1)
        self.assertEqual(report["native_render_verdict"], "UNVERIFIED")

    def test_changed_candidate_fails_without_certifying_report(self):
        source, candidate, raw = self.source()
        candidate.write_bytes(raw + b" ")
        output = self.base / "bad-source"
        with mock.patch.object(pack, "SUP", source):
            rc, _ = self.invoke(pack, ["--execute", "--out", str(output)])
        self.assertEqual(rc, 2)
        self.assertFalse((output / "render-packs-v2-report.json").exists())
        self.assertEqual(candidate.read_bytes(), raw + b" ")

    def test_sanitized_pack_name_collision_cannot_overwrite(self):
        source, _, _ = self.source(["a/b.jsonl", "a_b.jsonl"])
        output = self.base / "collision"
        with mock.patch.object(pack, "SUP", source):
            rc, _ = self.invoke(pack, ["--execute", "--out", str(output)])
        self.assertEqual(rc, 2)
        self.assertTrue((output / "render-packs-v2/a_b.md").is_file())
        self.assertFalse((output / "render-packs-v2-report.json").exists())

    def test_html_report_stays_inside_fresh_output(self):
        inputs = self.base / "md"
        inputs.mkdir()
        raw = b"# Exact\n\n$2/3$"
        (inputs / "fraction.md").write_bytes(raw)
        output = self.base / "html"
        rc, _ = self.invoke(html, ["--execute", "--packs", str(inputs), "--out", str(output)])
        self.assertEqual(rc, 0)
        self.assertEqual((inputs / "fraction.md").read_bytes(), raw)
        self.assertIn("$2/3$", (output / "fraction.html").read_text(encoding="utf-8"))
        report = json.loads((output / "render-html-v2-report.json").read_text())
        self.assertEqual(set(report["html_files"]), {"fraction"})

    def test_empty_html_input_is_not_success(self):
        inputs = self.base / "empty-md"
        inputs.mkdir()
        output = self.base / "empty-html"
        rc, _ = self.invoke(html, ["--execute", "--packs", str(inputs), "--out", str(output)])
        self.assertEqual(rc, 2)
        self.assertFalse((output / "render-html-v2-report.json").exists())

    def test_index_excludes_other_inboxes_and_out_of_range_dates(self):
        def row(rid, sender, to, date):
            return {"id": rid, "from": sender, "to": to, "timestamp": date + "T10:00:00Z",
                    "type": "review", "content": "2/3"}
        rows = [row("own-in", "claude-code", "codex", "2026-09-29"),
                row("own-sent", "codex", "claude-code", "2026-10-05"),
                row("other", "claude-code", "third-agent", "2026-10-01"),
                row("before", "claude-code", "codex", "2026-09-28"),
                row("after", "claude-code", "codex", "2026-10-06")]
        output = index.own_message_index(rows)
        self.assertEqual({m["id"] for m in output}, {"own-in", "own-sent"})
        self.assertEqual(output[0]["content_sha256"], hashlib.sha256(b"2/3").hexdigest())
        self.assertNotIn("content", output[0])

    def test_index_quota_cannot_silently_claim_complete(self):
        inputs = self.base / "quota"
        inputs.mkdir()
        (inputs / "a.json").write_bytes(b"{}")
        (inputs / "b.json").write_bytes(b"{}")
        with self.assertRaisesRegex(ValueError, "silently truncated"):
            index.dir_index(inputs, "*", max_files=1)

    def test_index_date_boundary_uses_utc_instant(self):
        rows = [{"id": "before", "from": "claude-code", "to": "codex", "content": "1/2",
                 "timestamp": "2026-09-29T01:00:00+14:00"},
                {"id": "inside", "from": "claude-code", "to": "codex", "content": "1/2",
                 "timestamp": "2026-10-06T01:00:00+14:00"}]
        self.assertEqual([m["id"] for m in index.own_message_index(rows)], ["inside"])

    def test_owned_timestamp_without_offset_cannot_be_certified(self):
        row = {"id": "unknown", "from": "claude-code", "to": "codex", "content": "1/2",
               "timestamp": "2026-10-01T00:00:00"}
        with self.assertRaisesRegex(ValueError, "UTC offset"):
            index.own_message_index([row])

if __name__ == "__main__":
    unittest.main()
