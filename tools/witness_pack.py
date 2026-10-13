"""Package completed v3 captures. Default PLAN; no receiver/probe launch."""
from __future__ import annotations
import argparse, io, json, os, time, uuid, zipfile
from pathlib import Path
import witness_transfer_common as c

def _publish_object(root, name, raw):
    final = c.checked(root / name, root, write=True, cloud=True)
    if final.exists():
        c.require(c.read_bytes(final, root=root, cloud=True, limit=1073741824) == raw,
                  "PUBLISHED_OBJECT_CONFLICT", name)
        return
    temp = root / (name + "." + uuid.uuid4().hex + ".partial")
    c.fresh(temp, raw, root=root, cloud=True)
    c.require(c.read_bytes(temp, root=root, cloud=True, limit=1073741824) == raw,
              "PUBLISH_COPY_CHANGED")
    c.checked(final, root, write=True, cloud=True)
    try:
        if os.name == "nt":
            os.rename(temp, final)  # Windows rename does not replace an existing destination.
        else:
            os.link(temp, final)
    except FileExistsError:
        c.require(c.read_bytes(final, root=root, cloud=True, limit=1073741824) == raw,
                  "PUBLISHED_OBJECT_CONFLICT", name)
    c.require(c.read_bytes(final, root=root, cloud=True, limit=1073741824) == raw,
              "PUBLISH_FINAL_CHANGED")
    # Retain partial files after failures. The consumer ignores all partial objects.

def publish(capture, sync_root, staging_root):
    capture = c.checked(capture)
    c.require(capture.is_dir(), "CAPTURE_DIRECTORY_MISSING")
    blobs = {}
    remaining = 268435456
    for name in c.RAW_NAMES:
        raw = c.read_bytes(capture / name, root=capture, limit=remaining)
        remaining -= len(raw)
        blobs[name] = raw
    proof = c.decode(blobs["process-exit.json"])
    c.require(type(proof) is dict, "PROCESS_PROOF_OBJECT")
    manifest = {
        "schema": "witness-transfer-package-v1", "purpose": "EXPERIMENT_TRANSFER",
        "round": proof.get("round"), "capture_id": proof.get("capture_id"),
        "receiver_run_id": proof.get("receiver_run_id"),
        "wrapper_sha256": proof.get("wrapper_sha256"), "exe_sha256": proof.get("exe_before_sha256"),
        "files": [{"path": "capture/" + capture.name + "/" + name,
                   "bytes": len(blobs[name]), "sha256": c.sha(blobs[name])} for name in c.RAW_NAMES],
    }
    c.manifest_check(manifest)
    c.require(capture.name == manifest["round"] + "-" + manifest["capture_id"], "CAPTURE_BASENAME")
    c.proof_check(manifest, blobs)  # A real nonzero exit remains nonzero, never fabricated.
    for name, raw in blobs.items():
        c.require(c.read_bytes(capture / name, root=capture) == raw, "CAPTURE_CHANGED", name)
    staging = c.mkdir(staging_root)
    manifest_raw = c.encoded(manifest)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
        members = [("PACKAGE_MANIFEST.json", manifest_raw)] + [
            (row["path"], blobs[Path(row["path"]).name]) for row in manifest["files"]]
        for name, raw in members:
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100600 << 16
            z.writestr(info, raw)
    raw_zip = buffer.getvalue()
    c.require(len(raw_zip) <= 1073741824, "PACKAGE_TOO_LARGE")
    digest = c.sha(raw_zip)
    context = c.sha(c.encoded({"package": digest, "capture": str(capture),
                                "sync": str(Path(sync_root).absolute())}))
    work = c.mkdir(staging / ("pack-" + context), staging)
    local_zip = work / (digest + ".zip")
    if local_zip.exists():
        c.require(c.read_bytes(local_zip, root=work, limit=1073741824) == raw_zip, "STAGING_CONFLICT")
    else:
        c.fresh(local_zip, raw_zip, root=work)
    ready = {"schema": "witness-transfer-ready-v1", "purpose": "EXPERIMENT_TRANSFER",
             "round": manifest["round"], "capture_id": manifest["capture_id"],
             "package_sha256": digest, "package_bytes": len(raw_zip),
             "manifest_sha256": c.sha(manifest_raw)}
    sync = c.mkdir(sync_root, cloud=True)
    _publish_object(sync, digest + ".zip", raw_zip)
    _publish_object(sync, digest + ".ready.json", c.encoded(ready))
    result = {"status": "LOCAL_PUBLISHED", "package_sha256": digest,
              "ready_path": str(sync / (digest + ".ready.json")), "source_capture": str(capture),
              "source_hashes": {n: c.sha(b) for n, b in blobs.items()},
              "receiver_exit_code": proof["exit_code"], "remote_arrival_verified": False,
              "production": "CLOSED", "probe_emitted": False}
    receipt_path = work / "publish-receipt.json"
    if receipt_path.exists():
        c.require(c.decode(c.read_bytes(receipt_path, root=work)) == result, "PUBLISH_RECEIPT_CHANGED")
        result = {**result, "duplicate": True}
    else:
        c.new_json(receipt_path, result, root=work)
    return result

def scan(config):
    w = config["witness"]
    root = c.checked(w["capture_root"])
    results = []
    for folder in sorted(root.iterdir()):
        if not folder.is_dir() or not (folder / "process-exit.json").is_file():
            continue
        try:
            results.append(publish(folder, Path(w["sync_root"]), Path(w["staging_root"])))
        except (OSError, ValueError) as exc:
            results.append({"status": "NOT_PUBLISHED", "capture": folder.name,
                            "code": getattr(exc, "code", "INCOMPLETE_CAPTURE"), "detail": str(exc)})
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
        config = c.load_config(args.config, execute=True, role="witness")
        staging = Path(config["witness"]["staging_root"])
        with c.lock(staging / "runtime"):
            while True:
                if (staging / "runtime" / "STOP").exists():
                    return 0
                print(json.dumps({"captures": scan(config), "production": "CLOSED"}), flush=True)
                if not args.watch:
                    return 0
                time.sleep(5)
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "NOT_PUBLISHED", "code": getattr(exc, "code", "IO_ERROR"),
                          "detail": str(exc), "production": "CLOSED"}))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
