"""CLI integration regressions for current-manifest freeze evidence."""
from pathlib import Path
from unittest import TestCase, mock
import contextlib
import importlib.util
import io
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from animtrain.freeze import freeze_set
from animtrain.manifest import Manifest, Entry, sha256_file
from animtrain.run_record import RunRecord
from animtrain.preflight import run_preflight

class TestFreezeEvidenceCLI(TestCase):
    def test_freeze_gate_checks_coverage_and_mandatory_binding(self):
        for case in ("matching", "missing_binding", "wrong_binding",
                     "unrelated", "partial", "corrupt", "no_lock"):
            with self.subTest(case=case), tempfile.TemporaryDirectory(
                    prefix="codex-evidence-") as tmp:
                root = Path(tmp)
                data = root / "data"
                data.mkdir()
                ev, te = data / "eval.jsonl", data / "test.jsonl"
                ev.write_text('{"id":"e","problem":"synthetic e","solution":"e"}\n', encoding="utf-8")
                te.write_text('{"id":"t","problem":"synthetic t","solution":"t"}\n', encoding="utf-8")
                mp = data / "manifest.json"
                Manifest(name="synthetic-review", entries=[
                    Entry(path=p.name, split=split, sha256=sha256_file(p),
                          size=p.stat().st_size, source="synthetic test",
                          license="internal-generated")
                    for p, split in [(ev, "eval"), (te, "test")]
                ]).save(mp)
                manifest_hash = sha256_file(mp)
                lock = data / "frozen.lock.json"
                meta = {"manifest_sha256": manifest_hash}
                files = [ev, te]
                if case == "missing_binding":
                    meta = {}
                elif case == "wrong_binding":
                    meta = {"manifest_sha256": "0" * 64}
                elif case == "unrelated":
                    other = data / "unrelated.txt"
                    other.write_text("synthetic note", encoding="utf-8")
                    files = [other]
                elif case == "partial":
                    files = [ev]
                if case == "corrupt":
                    lock.write_text("{", encoding="utf-8")
                elif case != "no_lock":
                    freeze_set(files, lock, meta=meta)
                RunRecord(run_id="probe", kind="dry-run", config={"synthetic": True},
                          git_commit="synthetic-review", manifest_hash=manifest_hash,
                          summary={"command": "synthetic", "manifest": str(mp)},
                          env={"python": sys.version}, dirty={"clean": True}
                          ).save(root / "runs/probe/run_record.json")
                spec = importlib.util.spec_from_file_location("review_preflight_cli",
                                                              ROOT / "tools/preflight.py")
                cli = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(cli)
                captured = {}
                def collect(*args, **kwargs):
                    captured.update(run_preflight(*args, **kwargs))
                    return captured
                # Isolate the real CLI freeze/snapshot checks from external gates.
                with mock.patch.object(cli, "ROOT", root), \
                     mock.patch.object(cli, "run_preflight", side_effect=collect), \
                     mock.patch.object(cli, "validate_manifest", return_value={
                         "ok": True, "n_entries": 2, "problems": [], "quarantines": [],
                         "near_dup_calibrated": True}), \
                     mock.patch("animtrain.preflight.check_gpu", return_value=(True, "mock")), \
                     mock.patch("animtrain.preflight.check_model_dir", return_value=(True, "mock")), \
                     mock.patch("animtrain.render_gate.render_check", return_value={
                         "ok": True, "status": "rendered", "detail": "mock smoke", "unverified": []}), \
                     mock.patch("animtrain.render_gate.math_check", return_value={
                         "ok": True, "status": "verified", "detail": "mock smoke", "unverified": []}), \
                     contextlib.redirect_stdout(io.StringIO()):
                    rc = cli.main(["--ready", "--run-id", "probe", "--manifest", str(mp),
                                   "--model", str(root)])
                gate = next(c for c in captured["checks"] if c["check"] == "freeze_gate")
                self.assertEqual(gate["ok"], case == "matching", (case, gate))
                if case != "matching":
                    self.assertEqual(rc, 1, (case, captured))
