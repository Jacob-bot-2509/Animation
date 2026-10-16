"""Consume approved OneDrive folder snapshots. Never start probes or training."""
from __future__ import annotations
import argparse, contextlib, io, json, stat, time, uuid, zipfile
from pathlib import Path
import witness_transfer_common as c
import witness_registered_adapter as adapter

def pair(ready_path, sync_root):
    ready_path = c.checked(ready_path, sync_root, cloud=True)
    ready_raw = c.read_bytes(ready_path, root=sync_root, cloud=True, limit=65536)
    ready = c.decode(ready_raw)
    c.ready_check(ready, ready_path.name)
    source = Path(sync_root) / (ready["package_sha256"] + ".zip")
    if not source.is_file():
        raise c.TransferError("WAITING_SYNC", "ZIP has not arrived")
    raw = c.read_bytes(source, root=sync_root, cloud=True, limit=1073741824)
    c.require(len(raw) == ready["package_bytes"] and c.sha(raw) == ready["package_sha256"],
              "WAITING_SYNC", "ZIP incomplete or does not match READY")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        items = z.infolist()
        c.require(len(items) == 6 and len({v.filename for v in items}) == 6, "ZIP_MEMBERS")
        c.require(sum(v.file_size for v in items) <= 268435456 + 65536, "ZIP_EXPANSION_LIMIT")
        for v in items:
            c.require(v.file_size >= 0 and not v.flag_bits & 1 and
                      v.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED) and
                      stat.S_IFMT(v.external_attr >> 16) in (0, stat.S_IFREG), "ZIP_MEMBER_TYPE")
        info = z.getinfo("PACKAGE_MANIFEST.json")
        c.require(info.file_size <= 65536, "MANIFEST_TOO_LARGE")
        mr = z.read(info)
        c.require(c.sha(mr) == ready["manifest_sha256"], "MANIFEST_SHA")
        manifest = c.decode(mr)
        prefix = c.manifest_check(manifest)
        c.require(manifest["round"] == ready["round"] and
                  manifest["capture_id"] == ready["capture_id"], "READY_MANIFEST_IDENTITY")
        c.require({v.filename for v in items} ==
                  {"PACKAGE_MANIFEST.json", *[v["path"] for v in manifest["files"]]}, "ZIP_FILE_SET")
        blobs = {}
        for row in manifest["files"]:
            member = z.getinfo(row["path"])
            c.require(member.file_size == row["bytes"], "MEMBER_LENGTH")
            blob = z.read(member)
            c.require(len(blob) == row["bytes"] and c.sha(blob) == row["sha256"], "MEMBER_SHA")
            blobs[Path(row["path"]).name] = blob
    c.proof_check(manifest, blobs)
    c.require(c.sha(c.read_bytes(source, root=sync_root, cloud=True, limit=1073741824)) ==
              ready["package_sha256"], "WAITING_SYNC", "ZIP changed between full snapshot samples")
    c.require(c.read_bytes(ready_path, root=sync_root, cloud=True, limit=65536) == ready_raw,
              "WAITING_SYNC", "READY changed during snapshot")
    return ready, manifest, blobs, raw

def _freeze(job):
    files = []
    for path in sorted(job.rglob("*")):
        c.checked(path, job)
        if path.is_file() and path.name != "delivery-manifest.json":
            raw = c.read_bytes(path, root=job, limit=1073741824)
            files.append({"path": path.relative_to(job).as_posix(), "bytes": len(raw), "sha256": c.sha(raw)})
    c.new_json(job / "delivery-manifest.json", {
        "schema": "witness-consumer-frozen-job-v1", "self_manifest_excluded": True,
        "artifacts": files, "production": "CLOSED", "full_surface_accepted": False}, job)

def verify_frozen(job):
    m = c.decode(c.read_bytes(job / "delivery-manifest.json", root=job))
    c.require(m.get("schema") == "witness-consumer-frozen-job-v1" and
              m.get("production") == "CLOSED", "FROZEN_JOB_SCHEMA")
    rows = m["artifacts"]
    expected = {v["path"] for v in rows}
    actual = {p.relative_to(job).as_posix() for p in job.rglob("*")
              if p.is_file() and p.name != "delivery-manifest.json"}
    c.require(len(expected) == len(rows) and actual == expected, "FROZEN_JOB_FILE_SET")
    for row in rows:
        path = c.checked(job / row["path"], job)
        raw = c.read_bytes(path, root=job, limit=1073741824)
        c.require(len(raw) == row["bytes"] and c.sha(raw) == row["sha256"], "FROZEN_JOB_HASH")
    summary = c.decode(c.read_bytes(job / "SUMMARY.json", root=job))
    c.require(summary.get("production") == "CLOSED" and summary.get("full_surface_accepted") is False,
              "SUMMARY_GATE")
    return summary

def _finish(job, result):
    c.new_json(job / "SUMMARY.json", result, job)
    text = ("Witness material job\n\nStatus: " + result["status"] + "\nProduction: CLOSED\n"
            "Full-surface accepted: false\nIPv6 D2/D8: GAP deferred; preparation not blocked.\n"
            "This report does not authorize training or infer UDP interception mechanisms.\n\n"
            + json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    c.fresh(job / "REPORT.md", text.encode("utf-8"), root=job)
    _freeze(job)

def consume(config, ready_path):
    section = config["consumer"]
    namespace = c.ROOT / "reviews/witness-automation"
    jobs = c.mkdir(section["jobs_root"], namespace)
    runtime = c.mkdir(section["runtime_root"], namespace)
    sync = c.checked(section["sync_root"], cloud=True)
    ready, manifest, blobs, zip_raw = pair(ready_path, sync)
    entries = [e for e in config["sender_registry"] if e.get("round") == manifest["round"] and
               e.get("receiver_capture_id") == manifest["capture_id"]]
    c.require(len(entries) == 1, "WAITING_SENDER_BINDING" if not entries else "AMBIGUOUS_SENDER_BINDING")
    entry = entries[0]
    adapter.binding_inputs(entry)
    identity = {k: manifest[k] for k in ("round", "capture_id", "receiver_run_id")}
    identity["sender_sha256"] = entry["sender_sha256"]
    key = c.sha(c.encoded(identity))
    normalized = {**manifest, "files": sorted(manifest["files"], key=lambda x: x["path"])}
    content_sha = c.sha(c.encoded(normalized))
    version = c.sha(c.encoded(config["automation_source_pins"]))
    ledger_path = runtime / "journal.json"
    ledger = c.decode(c.read_bytes(ledger_path, root=runtime)) if ledger_path.exists() else {
        "schema": "witness-consumer-journal-v1", "jobs": {}}
    c.require(ledger.get("schema") == "witness-consumer-journal-v1" and
              type(ledger.get("jobs")) is dict, "JOURNAL_INVALID")
    old = ledger["jobs"].get(key)
    if old is not None:
        c.require(old["content_sha256"] == content_sha, "LOGICAL_IDENTITY_CONFLICT")
        old_job = c.checked(old["job"], jobs)
        if old["version"] == version:
            if (old_job / "delivery-manifest.json").exists():
                result = verify_frozen(old_job)
                c.require(result["logical_key"] == key and result["content_sha256"] == content_sha,
                          "RECOVERY_IDENTITY")
                old["state"] = "COMPLETE"
                c.atomic_json(ledger_path, ledger, runtime)
                return {**result, "duplicate": True}
            job = old_job
        else:
            c.require(old.get("state") == "COMPLETE", "RECOVERY_REQUIRED",
                      "Previous tool version has an unfinished job")
            job = jobs / ("job-" + uuid.uuid4().hex)
    else:
        job = jobs / ("job-" + uuid.uuid4().hex)
    c.mkdir(job, jobs)
    row = {"content_sha256": content_sha, "version": version, "job": str(job), "state": "STARTED"}
    ledger["jobs"][key] = row
    c.atomic_json(ledger_path, ledger, runtime)
    base = {"logical_key": key, "content_sha256": content_sha, "version": version,
            "job": str(job), "package_sha256": ready["package_sha256"], "identity": identity,
            "production": "CLOSED", "full_surface_accepted": False, "probe_emitted": False,
            "training_started": False, "ipv6_D2_D8": "GAP_DEFERRED_NONBLOCKING_PREPARATION"}
    try:
        path = job / "package.zip"
        if path.exists():
            c.require(c.sha(c.read_bytes(path, root=job, limit=1073741824)) == ready["package_sha256"],
                      "JOB_PACKAGE_CHANGED")
        else:
            c.fresh(path, zip_raw, root=job)
        capture = job / "capture" / (manifest["round"] + "-" + manifest["capture_id"])
        c.mkdir(capture, job)
        for name, raw in blobs.items():
            path = capture / name
            if path.exists():
                c.require(c.read_bytes(path, root=job) == raw, "JOB_INPUT_CHANGED", name)
            else:
                c.fresh(path, raw, root=job)
        receipt = adapter.reconcile(entry, capture, job)
        result = {**base, "status": "REGISTERED_RECONCILIATION_COMPLETE", "adapter": receipt}
        if not (job / "SUMMARY.json").exists():
            _finish(job, result)
        else:
            c.require(c.decode(c.read_bytes(job / "SUMMARY.json", root=job)) == result,
                      "RECOVERY_SUMMARY_CHANGED")
            if not (job / "delivery-manifest.json").exists():
                if not (job / "REPORT.md").exists():
                    c.fresh(job / "REPORT.md", c.encoded(result), root=job)
                _freeze(job)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        if (job / "SUMMARY.json").exists():
            raise c.TransferError("RECOVERY_REQUIRED", exc) from exc
        code = getattr(exc, "code", "BOUNDARY_FAILURE" if type(exc).__name__ == "BoundaryFailure" else "INVALID_EVIDENCE")
        result = {**base, "status": "FAILED" if code == "BOUNDARY_FAILURE" else "NEEDS_EVIDENCE",
                  "code": code, "detail": str(exc)}
        _finish(job, result)
    row["state"] = "COMPLETE"
    c.atomic_json(ledger_path, ledger, runtime)
    return result

def scan(config):
    runtime = c.mkdir(config["consumer"]["runtime_root"], c.ROOT / "reviews/witness-automation")
    root = c.checked(config["consumer"]["sync_root"], cloud=True)
    results = []
    with c.lock(runtime):
        for path in sorted(root.glob("*.ready.json")):
            try:
                results.append(consume(config, path))
            except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile, RuntimeError) as exc:
                results.append({"ready": path.name, "status": "WAITING" if
                    getattr(exc, "code", "").startswith("WAITING_") else "NOT_ACCEPTED",
                    "code": getattr(exc, "code", "INVALID_PACKAGE"), "detail": str(exc),
                    "production": "CLOSED"})
        c.atomic_json(runtime / "latest.json", {"results": results, "production": "CLOSED"}, runtime)
    return results

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path)
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--watch", action="store_true")
    args = ap.parse_args(argv)
    if not args.execute:
        print(json.dumps({"status": "PLAN", "probe_emitted": False, "cloud_write": False}))
        return 3
    try:
        c.require(args.config is not None, "CONFIG_REQUIRED")
        retry_index = 0
        watch_runtime = None
        service_lock = contextlib.nullcontext()
        if args.watch:
            config = c.load_config(args.config, execute=True)
            watch_runtime = Path(config["consumer"]["runtime_root"]).absolute()
            if (watch_runtime / "STOP").exists():
                return 0
            # Hold independently of scan's job lock, including all wait intervals.
            service_lock = c.lock(watch_runtime / "consumer-watch")
        with service_lock:
            while True:
                config = c.load_config(args.config, execute=True)
                if args.watch:
                    c.require(Path(config["consumer"]["runtime_root"]).absolute() == watch_runtime,
                              "WATCH_RUNTIME_CHANGED_RESTART_REQUIRED")
                if (Path(config["consumer"]["runtime_root"]) / "STOP").exists():
                    return 0
                results = scan(config)
                print(json.dumps({"results": results, "production": "CLOSED"}), flush=True)
                if not args.watch:
                    return 0 if all(r.get("status") == "REGISTERED_RECONCILIATION_COMPLETE" for r in results) else 2
                delays = config.get("retry_delays_seconds", [5, 15, 45, 120])
                c.require(type(delays) is list and len(delays) == 4 and
                          all(type(x) is int and 1 <= x <= 120 for x in delays), "RETRY_CONFIG")
                waiting = any(r.get("status") == "WAITING" for r in results)
                delay = delays[retry_index] if waiting else 5
                retry_index = min(retry_index + 1, 3) if waiting else 0
                time.sleep(delay)
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "NOT_ACCEPTED", "code": getattr(exc, "code", "IO_ERROR"),
                          "detail": str(exc), "production": "CLOSED"}))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
