"""Local transfer failures and read-only replay of the submitted LAN snapshot."""
from pathlib import Path
import contextlib, copy, importlib.util, io, json, os, socket, stat, subprocess
import sys, tempfile, unittest, uuid, zipfile
from unittest import mock
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import witness_transfer_common as c
import witness_pack as pack
import witness_consumer as consume
import witness_registered_adapter as adapter

SOURCE = ROOT / "reviews/codex-supervision/2026-10-06-all43-sandbox-repair/external-tests/remote-3a28dfd9dc96430a8ed0edb1989c3e76"
CAPTURE = SOURCE / "captures/lan-2026-10-13-a-e605e0ee3a8b4388aa72271d56f473cd"

class AutomationTests(unittest.TestCase):
    def setUp(self):
        work = c.mkdir(ROOT / "reviews/witness-automation/test-work")
        self.base = Path(tempfile.mkdtemp(prefix="local-only-", dir=work)).resolve()
        self.assertTrue(self.base.is_relative_to(work.resolve()))
        # Keep generated frozen jobs and all fault fixtures; never recursively delete a frozen tree.
        self.capture = self.base / "capture-source" / CAPTURE.name
        self.capture.mkdir(parents=True)
        for n in c.RAW_NAMES:
            (self.capture / n).write_bytes((CAPTURE / n).read_bytes())
        self.sync = self.base / "sync"
        self.stage = self.base / "staging"
        self.sync.mkdir()
        raw = c.decode((SOURCE / "sender.json").read_bytes())
        paths = [raw["sender_interfaces"]["path"], raw["sender_interfaces"]["stderr_path"]]
        paths += [str(Path(raw["transport"]["work"]) / n) for n in ("scene.py", "stdout.txt", "stderr.txt")]
        proof = c.decode((self.capture / "process-exit.json").read_bytes())
        self.entry = {"round": raw["round"], "receiver_capture_id": proof["capture_id"],
            "expected_receiver_run_id": proof["receiver_run_id"], "sender_run_id": raw["run_id"],
            "sender_path": str(SOURCE / "sender.json"), "sender_sha256": c.sha((SOURCE / "sender.json").read_bytes()),
            "input_bindings": {p: c.sha(Path(p).read_bytes()) for p in paths}}
        self.config = {"consumer": {"sync_root": str(self.sync), "jobs_root": str(self.base / "jobs"),
                          "runtime_root": str(self.base / "runtime")},
            "sender_registry": [self.entry],
            "automation_source_pins": {f"tools/{n}.py": c.sha((ROOT / "tools" / (n + ".py")).read_bytes())
                for n in ("witness_transfer_common", "witness_pack", "witness_consumer", "witness_registered_adapter")}}
        self.originals = {str(SOURCE / "sender.json"): self.entry["sender_sha256"],
                          **{str(CAPTURE / n): c.sha((CAPTURE / n).read_bytes()) for n in c.RAW_NAMES}}
    def tearDown(self):
        for path, expected in self.originals.items():
            self.assertEqual(c.sha(Path(path).read_bytes()), expected)

    def published(self):
        result = pack.publish(self.capture, self.sync, self.stage)
        return Path(result["ready_path"])

    def rewrite_package(self, ready, change):
        r = c.decode(ready.read_bytes())
        with zipfile.ZipFile(self.sync / (r["package_sha256"] + ".zip")) as z:
            items = [(n, z.read(n)) for n in z.namelist()]
        items = change(items)
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for name, raw in items:
                z.writestr(name, raw)
        raw = buf.getvalue()
        digest = c.sha(raw)
        mr = next(b for n, b in items if n == "PACKAGE_MANIFEST.json")
        r.update(package_sha256=digest, package_bytes=len(raw), manifest_sha256=c.sha(mr))
        out = self.sync / (digest + ".ready.json")
        (self.sync / (digest + ".zip")).write_bytes(raw)
        out.write_bytes(c.encoded(r))
        return out

    def guarded(self, ready):
        with mock.patch.object(socket, "socket", side_effect=AssertionError("Network forbidden")), \
             mock.patch.object(subprocess, "Popen", side_effect=AssertionError("Spawn forbidden")), \
             mock.patch.object(subprocess, "run", side_effect=AssertionError("Probe subprocess forbidden")):
            return consume.consume(self.config, ready)

    def test_default_cli_and_import_have_no_execution(self):
        for module in (pack, consume, adapter):
            with mock.patch.object(socket, "socket", side_effect=AssertionError), \
                 mock.patch.object(subprocess, "Popen", side_effect=AssertionError), contextlib.redirect_stdout(io.StringIO()) as stream:
                self.assertEqual(module.main([]), 3)
                self.assertEqual(json.loads(stream.getvalue())["status"], "PLAN")
        self.assertFalse((self.base / "jobs").exists())

    def test_real_submitted_snapshot_replays_without_network_or_spawn(self):
        result = self.guarded(self.published())
        self.assertEqual(result["status"], "REGISTERED_RECONCILIATION_COMPLETE")
        self.assertEqual(result["adapter"]["points"], {"tcp": "D9", "udp": "D9"})
        self.assertFalse(result["full_surface_accepted"])
        self.assertEqual(result["production"], "CLOSED")
        self.assertEqual(consume.verify_frozen(Path(result["job"]))["status"], result["status"])

    def test_duplicate_consume_and_publish_do_not_create_more_jobs(self):
        ready = self.published()
        first = self.guarded(ready)
        self.assertEqual(first["status"], "REGISTERED_RECONCILIATION_COMPLETE")
        before = {p.relative_to(self.base).as_posix(): c.sha(p.read_bytes())
                  for p in (self.base / "jobs").rglob("*") if p.is_file()}
        second = self.guarded(ready)
        self.assertTrue(second["duplicate"])
        self.assertEqual(second["job"], first["job"])
        self.assertTrue(pack.publish(self.capture, self.sync, self.stage)["duplicate"])
        after = {p.relative_to(self.base).as_posix(): c.sha(p.read_bytes())
                 for p in (self.base / "jobs").rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(len(list(self.stage.glob("pack-*"))), 1)

    def test_ready_before_zip_waits_without_job(self):
        ready = self.published()
        r = c.decode(ready.read_bytes())
        (self.sync / (r["package_sha256"] + ".zip")).rename(self.sync / "saved.notready")
        with self.assertRaisesRegex(c.TransferError, "WAITING_SYNC"):
            self.guarded(ready)
        self.assertFalse((self.base / "jobs").exists() and list((self.base / "jobs").iterdir()))

    def test_partial_zip_waits(self):
        ready = self.published()
        r = c.decode(ready.read_bytes())
        path = self.sync / (r["package_sha256"] + ".zip")
        path.write_bytes(path.read_bytes()[:20])
        with self.assertRaisesRegex(c.TransferError, "WAITING_SYNC"):
            self.guarded(ready)

    def test_unknown_and_missing_sender_binding(self):
        ready = self.published()
        self.config["sender_registry"] = []
        with self.assertRaisesRegex(c.TransferError, "WAITING_SENDER_BINDING"):
            self.guarded(ready)
        self.config["sender_registry"] = [self.entry, self.entry]
        with self.assertRaisesRegex(c.TransferError, "AMBIGUOUS"):
            self.guarded(ready)

    def test_registry_sender_and_native_bytes_are_pinned(self):
        ready = self.published()
        self.config["sender_registry"][0]["sender_sha256"] = "0" * 64
        with self.assertRaisesRegex(c.TransferError, "SENDER_VERSION_DRIFT"):
            self.guarded(ready)
        self.config["sender_registry"][0]["sender_sha256"] = self.entry["sender_sha256"] = self.originals[str(SOURCE / "sender.json")]
        name = next(iter(self.entry["input_bindings"]))
        self.entry["input_bindings"][name] = "0" * 64
        with self.assertRaisesRegex(c.TransferError, "NATIVE_INPUT_CHANGED"):
            self.guarded(ready)

    def test_parent_proof_missing_stderr_and_bool_rc_are_rejected(self):
        (self.capture / "stderr.bin").unlink()
        with self.assertRaises(OSError):
            self.published()
        (self.capture / "stderr.bin").write_bytes(b"")
        p = c.decode((self.capture / "process-exit.json").read_bytes())
        p["exit_code"] = False
        (self.capture / "process-exit.json").write_bytes(c.encoded(p))
        with self.assertRaisesRegex(c.TransferError, "PROCESS_RC_MISSING"):
            self.published()

    def test_actual_nonzero_receiver_rc_is_preserved_and_not_accepted(self):
        p = c.decode((self.capture / "process-exit.json").read_bytes())
        p["exit_code"] = 2
        (self.capture / "process-exit.json").write_bytes(c.encoded(p))
        result = self.guarded(self.published())
        self.assertEqual(result["status"], "NEEDS_EVIDENCE")
        self.assertEqual(result["code"], "PRECHECK_REJECTED")
        self.assertFalse(list(Path(result["job"]).glob("reconciled-*.json")))

    def test_fixture_purpose_cannot_register(self):
        ready = self.published()
        r = c.decode(ready.read_bytes())
        r["purpose"] = "DESIGN_FIXTURE_ONLY"
        ready.write_bytes(c.encoded(r))
        with self.assertRaisesRegex(c.TransferError, "READY_PURPOSE"):
            self.guarded(ready)

    def test_extra_and_traversal_zip_members_are_rejected_without_escape(self):
        ready = self.published()
        bad = self.rewrite_package(ready, lambda items: items + [("../escaped.txt", b"not allowed")])
        with self.assertRaisesRegex(c.TransferError, "ZIP_MEMBERS"):
            self.guarded(bad)
        self.assertFalse((self.base / "escaped.txt").exists())

    def test_duplicate_zip_member_is_rejected(self):
        ready = self.published()
        with contextlib.redirect_stderr(io.StringIO()):
            bad = self.rewrite_package(ready, lambda items: items + [items[1]])
        with self.assertRaisesRegex(c.TransferError, "ZIP_MEMBERS"):
            self.guarded(bad)

    def test_manifest_path_length_and_member_sha_are_checked(self):
        ready = self.published()
        def change(items):
            m = c.decode(items[0][1]);m["files"][0]["sha256"] = "0" * 64
            return [("PACKAGE_MANIFEST.json", c.encoded(m)), *items[1:]]
        bad = self.rewrite_package(ready, change)
        with self.assertRaisesRegex(c.TransferError, "MEMBER_SHA"):
            self.guarded(bad)

    def test_same_logical_identity_changed_content_conflicts(self):
        ready = self.published()
        result = self.guarded(ready)
        self.assertEqual(result["status"], "REGISTERED_RECONCILIATION_COMPLETE")
        p = c.decode((self.capture / "process-exit.json").read_bytes());p["exit_code"] = 2
        (self.capture / "process-exit.json").write_bytes(c.encoded(p))
        bad = self.published()
        with self.assertRaisesRegex(c.TransferError, "LOGICAL_IDENTITY_CONFLICT"):
            self.guarded(bad)

    def test_publish_conflict_never_overwrites_existing_object(self):
        ready = self.published()
        r = c.decode(ready.read_bytes());p = self.sync / (r["package_sha256"] + ".zip")
        p.write_bytes(b"existing changed content")
        with self.assertRaisesRegex(c.TransferError, "PUBLISHED_OBJECT_CONFLICT"):
            self.published()
        self.assertEqual(p.read_bytes(), b"existing changed content")

    def test_frozen_directory_write_and_system_write_are_rejected(self):
        target = self.base / "frozen";target.mkdir()
        (target / "delivery-manifest.json").write_bytes(b"{}")
        with self.assertRaisesRegex(c.TransferError, "FROZEN_DIRECTORY"):
            c.fresh(target / "new.json", b"test")
        if os.name == "nt":
            with self.assertRaisesRegex(c.TransferError, "SYSTEM_WRITE_FORBIDDEN"):
                c.checked(Path(os.environ["SystemRoot"]) / "amt-test-not-created", write=True)

    def test_unknown_reparse_tag_rejected_cloud_tag_narrow(self):
        self.assertTrue(c.cloud_tag(0x9000001a))
        self.assertTrue(c.cloud_tag(0x9000f01a))
        for tag in (0xa0000003, 0xa000000c, 0, True):
            self.assertFalse(c.cloud_tag(tag))
        original = Path.lstat
        def fake(path, *a, **kw):
            if path == self.sync:
                return types.SimpleNamespace(st_mode=stat.S_IFDIR, st_file_attributes=0x400,
                                             st_reparse_tag=0xa0000003)
            return original(path, *a, **kw)
        import types
        with mock.patch.object(Path, "lstat", fake):
            with self.assertRaisesRegex(c.TransferError, "REPARSE_NOT_ALLOWED"):
                c.checked(self.sync, cloud=True)

    def test_two_worker_lock_refused(self):
        runtime = self.base / "runtime-lock"
        with c.lock(runtime):
            with self.assertRaisesRegex(c.TransferError, "WORKER_BUSY"):
                with c.lock(runtime):
                    self.fail("Second worker got lock")

    def test_frozen_job_tampering_cannot_be_reused(self):
        ready = self.published()
        result = self.guarded(ready)
        self.assertEqual(result["status"], "REGISTERED_RECONCILIATION_COMPLETE")
        path = Path(result["job"]) / "REPORT.md"
        # Inject a changed read rather than modifying any frozen directory.
        original_read = c.read_bytes
        def tampered(value, **kwargs):
            raw = original_read(value, **kwargs)
            return raw + b"\nTAMPER" if Path(value) == path else raw
        with mock.patch.object(c, "read_bytes", side_effect=tampered), \
             self.assertRaisesRegex(c.TransferError, "FROZEN_JOB_HASH"):
            self.guarded(ready)

    def test_adapter_interrupted_intent_does_not_rerun(self):
        job = self.base / "manual-job";job.mkdir()
        capture = job / "capture" / CAPTURE.name;capture.mkdir(parents=True)
        for n in c.RAW_NAMES:
            (capture / n).write_bytes((CAPTURE / n).read_bytes())
        (job / "ADAPTER_INTENT.json").write_bytes(b"{}")
        with self.assertRaisesRegex(c.TransferError, "RECOVERY_REQUIRED"), \
             mock.patch.object(socket, "socket", side_effect=AssertionError):
            adapter.reconcile(self.entry, capture, job)
        self.assertFalse(list(job.glob("reconciled-*.json")))

    def test_recovery_from_complete_frozen_job_updates_journal_without_replay(self):
        ready = self.published()
        result = self.guarded(ready)
        journal = self.base / "runtime" / "journal.json"
        state = c.decode(journal.read_bytes());state["jobs"][result["logical_key"]]["state"] = "STARTED"
        journal.write_bytes(c.encoded(state))
        with mock.patch.object(adapter, "reconcile", side_effect=AssertionError("Do not rerun")):
            recovered = self.guarded(ready)
        self.assertTrue(recovered["duplicate"])
        self.assertEqual(c.decode(journal.read_bytes())["jobs"][result["logical_key"]]["state"], "COMPLETE")

if __name__ == "__main__":
    unittest.main()
