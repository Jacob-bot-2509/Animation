"""Verify admission source reconstruction, native scene schema and version bindings."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("admission_builder", ROOT / "tools/build_math_admission_v1.py")
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
v = b.v


def verify_admission(root: Path, directory: Path):
    directory = (root / directory).resolve()
    if not directory.is_relative_to((root / "reviews").resolve()):
        raise v.VerificationError("admission input outside project reviews")
    patches, source_bindings = b.math.load_verified_math(root)
    templates = b.load_updates(root)
    manifest = v.read_json(directory / "admission-manifest.json")
    if manifest.get("schema") != "math-admission-v2-manifest":
        raise v.VerificationError("legacy v1 schema is not the corrected native-scene version")
    items = manifest.get("items")
    if not isinstance(items, list) or len(items) != 9:
        raise v.VerificationError("incomplete admission manifest")
    expected = {directory / "admission-sources" / s["before"]["path"] for s in source_bindings}
    expected |= {directory / name for name in (
        "scene-updates-candidate.jsonl", "record-bindings.jsonl",
        "scene-binding-audit.json", "ADMISSION_RECEIPT.md")}
    actual = set()
    for item in items:
        v.check_binding(root, item)
        path = v.inside(root, item["path"])
        if path in actual or path not in expected:
            raise v.VerificationError("duplicate or unexpected admission artifact")
        actual.add(path)
    if actual != expected:
        raise v.VerificationError("missing admission source or receipt")
    rows = v.read_jsonl(directory / "scene-updates-candidate.jsonl")
    if len(rows) != 17 or len({x["id"] for x in rows}) != 17:
        raise v.VerificationError("17 unique reviewed scene updates required")
    updates = {x["id"]: x for x in rows}
    if set(updates) != set(templates):
        raise v.VerificationError("scene update scope differs from reviewed version")
    records = v.read_jsonl(directory / "record-bindings.jsonl")
    if len(records) != 30 or len({x["id"] for x in records}) != 30:
        raise v.VerificationError("30 unique final record bindings required")
    by_id = {p["id"]: p for p in patches}
    if {x["id"] for x in records} != set(by_id):
        raise v.VerificationError("final record binding scope incomplete")
    record_bindings = {x["id"]: x for x in records}
    final = {}
    for patch in patches:
        rid = patch["id"]; base = patch["corrected_record"]
        rec = dict(base)
        if rid in templates:
            rec.update({k: templates[rid][k] for k in ("scene_spec", "visual_style") if k in templates[rid]})
        b.validate_scene(rec["scene_spec"])
        fields = {k: rec[k] for k in ("problem", "solution", "answer")}
        required = {"id": rid, "source": patch["source"],
            "base_math_record_dense_sha256": patch["after_record_dense_sha256"],
            "math_fields_dense_sha256": v.digest(v.canonical(fields)),
            "final_record_dense_sha256": v.digest(v.canonical(rec)), "scene_updated": rid in templates}
        if record_bindings[rid] != required:
            raise v.VerificationError("final record version binding mismatch: " + rid)
        if fields != patch["after_math_fields"]:
            raise v.VerificationError("admission changed mathematical fields")
        final[rid] = rec
        if rid in templates:
            row = updates[rid]
            for key, value in required.items():
                if row.get(key) != value:
                    raise v.VerificationError("scene/math version binding mismatch: " + rid)
            if (row.get("scene_spec") != rec["scene_spec"]
                    or row.get("visual_style") != rec.get("visual_style")
                    or row.get("scene_sha_encoding") != "json-sortkeys-compact-utf8"
                    or row.get("old_scene_spec_sha256") != b.scene_sha(base["scene_spec"])
                    or row.get("new_scene_spec_sha256") != b.scene_sha(rec["scene_spec"])):
                raise v.VerificationError("scene bytes or old/new scene binding mismatch: " + rid)
    checked = set()
    full_source_records = 0
    patch_lines = {(p["source"]["source_path"], p["source"]["source_line"]): p["id"] for p in patches}
    for source in source_bindings:
        name = source["before"]["path"]
        before = v.inside(root, source["candidate"]["path"]).read_bytes().splitlines(keepends=True)
        admitted = (directory / "admission-sources" / name).read_bytes().splitlines(keepends=True)
        if len(before) != len(admitted):
            raise v.VerificationError("admission source line count changed")
        for line, (old, new) in enumerate(zip(before, admitted), 1):
            rid = patch_lines.get((name, line))
            if rid:
                if json.loads(new.decode("utf-8-sig")) != final[rid]:
                    raise v.VerificationError("admission record differs from bound version")
                checked.add(rid)
            if not rid or rid not in templates:
                if old != new:
                    raise v.VerificationError("unchanged source line bytes drifted")
            if new.strip(): full_source_records += 1
    if checked != set(by_id):
        raise v.VerificationError("admission source rows missing")
    audit = v.read_json(directory / "scene-binding-audit.json")
    if (audit.get("total") != 30 or audit.get("scene_updated") != 17
            or audit.get("scene_retained") != 13 or audit.get("native_render_performed") is not False
            or audit.get("active_admission") != "PENDING"):
        raise v.VerificationError("audit coverage or render/admission claim is incorrect")
    if (len(audit.get("rows", [])) != 30
            or {x["id"] for x in audit["rows"]} != set(by_id)
            or any(x.get("render_verdict") != "UNVERIFIED"
                   or x.get("scene_updated") != (x["id"] in templates) for x in audit["rows"])):
        raise v.VerificationError("audit rows incomplete or improperly accepted")
    return {"result": "PASS_VERSION_SCHEMA_AND_SOURCE_RECONSTRUCTION",
        "mathematical_records": 30, "updated_native_scenes": 17, "retained_native_scenes": 13,
        "source_files": 5, "full_source_records_preserved": full_source_records,
        "verified_artifacts": 9, "unchanged_source_line_bytes": "PRESERVED",
        "new_math_proof_claimed": False, "native_render": "UNVERIFIED",
        "active_admission": "PENDING", "full_761_math_verdict": "NOT_ESTABLISHED",
        "semantic_isolation_verdict": "NOT_ESTABLISHED", "PASS_CORE_SCOPE_issued": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("reviews/2026-10-07-math-admission-v1"))
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    try:
        result = verify_admission(ROOT, args.input)
        if args.out: v.write_output(ROOT, args.out, result)
        rc = 0
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        result = {"result": "FAIL", "error": type(exc).__name__ + ": " + str(exc)}; rc = 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
