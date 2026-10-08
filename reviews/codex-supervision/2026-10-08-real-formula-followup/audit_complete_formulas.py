"""Read-only independent audit of current, complete local MathTex receipts."""
from __future__ import annotations
import argparse, ast, hashlib, importlib.util, json, sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import native_render_pilot as native
core = native.core

def read(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def require(condition, message):
    if not condition:
        raise ValueError(message)

def reviewed_generators(owner):
    paths = [owner/"received/tools/native_render_pilot.py",
             owner/"display-fix-snapshot/tools/native_render_pilot.py",
             ROOT/"tools/native_render_pilot.py"]
    generators = {}
    for index, path in enumerate(paths):
        spec = importlib.util.spec_from_file_location("reviewed_formula_generator_"+str(index), path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        generators[sha(path)] = module
    return generators

def audit_batch(batch, by_id, allowed_generators):
    batch = core.checked_path(batch, ROOT / "reviews")
    receipt_path = batch / "receipt.json"
    if not receipt_path.exists():
        inputs = read(batch / "run-inputs.json")
        require(inputs["core_manifest_sha256"] == core.CORE_MANIFEST_SHA256, "pending version mismatch")
        ids = [b["id"] for b in inputs["bindings"]]
        require(len(ids) == len(set(ids)), "duplicate pending IDs")
        for b in inputs["bindings"]:
            require(b == by_id.get(b["id"]), "pending actual binding mismatch")
        return {"batch": batch.relative_to(ROOT).as_posix(), "status": "IN_PROGRESS_NO_FINAL_RECEIPT",
                "requested_ids": ids, "qualified_ids": [], "rows": []}
    receipt = read(receipt_path)
    inputs_path = batch / "run-inputs.json"
    inputs = read(inputs_path)
    for key in ("core_manifest_sha256", "generator_sha256", "bindings", "scope"):
        require(inputs[key] == receipt[key], "inputs/receipt disagree: " + key)
    require(receipt["core_manifest_sha256"] == core.CORE_MANIFEST_SHA256, "wrong current manifest")
    require(receipt["generator_sha256"] in allowed_generators, "generator not archived and reviewed")
    require(inputs["scope"] == "TRUSTED_LOCAL_MATHTEX_ONLY", "wrong scope")
    require(receipt["production_evidence"] is False and receipt["PASS_CORE_SCOPE_issued"] is False
            and receipt["production"] == "CLOSED" and receipt["semantic_isolation"] == "NOT_ESTABLISHED"
            and receipt["visual_acceptance"] == "NOT_REVIEWED", "qualification overclaim")
    bindings = receipt["bindings"]
    require(isinstance(bindings, list) and bool(bindings), "empty or invalid completed bindings")
    ids = [b["id"] for b in bindings]
    require(len(ids) == len(set(ids)), "duplicate bound IDs")
    results = receipt["results"]
    require([x["id"] for x in results] == ids, "results/bindings coverage mismatch")
    checked = []
    for b, result in zip(bindings, results):
        rid = b["id"]
        require(b == by_id.get(rid), rid + ": current binding mismatch")
        record = core.load_record(by_id, rid)
        formulas, occurrences = native.formula_inventory(record)
        work = core.checked_path(batch / ("render-" + rid), batch)
        scene = work / "scene.py"
        source = scene.read_bytes()
        require(source == allowed_generators[receipt["generator_sha256"]].build_scene(record).encode("utf-8"), rid + ": scene incomplete or altered")
        tree = ast.parse(source)
        calls = [x for x in ast.walk(tree) if isinstance(x, ast.Call)
                 and isinstance(x.func, ast.Name) and x.func.id == "MathTex"]
        require(len(calls) == 1 and len(calls[0].args) == 1
                and isinstance(calls[0].args[0], ast.Name) and calls[0].args[0].id == "formula",
                rid + ": MathTex placeholder or wrong input")
        inv_path = work / "formula-inventory.json"
        require(read(inv_path) == {"unique_formulas": formulas, "source_occurrences": occurrences},
                rid + ": formula inventory does not match complete actual record")
        for key in ("record_sha256", "math_sha256", "source_sha256"):
            require(result[key] == b[key], rid + ": result binding mismatch " + key)
        require(result["core_manifest_sha256"] == core.CORE_MANIFEST_SHA256, rid + ": result core mismatch")
        require(result["unique_formulas"] == len(formulas)
                and result["source_formula_occurrences"] == len(occurrences)
                and result["formulas_sha256"] == core.dense(formulas), rid + ": formula counts/hash mismatch")
        elapsed = result["elapsed_seconds_exact"]
        require(isinstance(elapsed, str) and Fraction(elapsed) >= 0
                and "." not in elapsed, rid + ": elapsed must be exact fraction")
        require(sha(scene) == result["scene_py_sha256"], rid + ": scene hash mismatch")
        for name, key in (("stdout.bin", "stdout_sha256"), ("stderr.bin", "stderr_sha256")):
            require(sha(work / name) == result[key], rid + ": log hash mismatch")
        success_claim = result["status"] == "PASS_LOCAL_COMPLETE_FORMULA_COMPILATION"
        valid = False
        if result["mp4"] is True and result["mp4_path"]:
            video = core.checked_path(work / result["mp4_path"], work)
            require(video.name == "ConceptScene.mp4" and video.is_file() and video.stat().st_size > 0,
                    rid + ": missing/nonempty video")
            require(sha(video) == result["mp4_sha256"], rid + ": video hash mismatch")
            all_videos = list((work / "media").rglob("ConceptScene.mp4"))
            require(len(all_videos) == 1, rid + ": ambiguous videos")
            valid = True
        passed = type(result["rc"]) is int and result["rc"] == 0 and result["timed_out"] is False and valid
        require(success_claim == passed, rid + ": status inconsistent with execution/video")
        require(result["production_evidence"] is False and result["visual_acceptance"] == "NOT_REVIEWED",
                rid + ": row overclaim")
        checked.append({"id": rid, "status": "PASS_LOCAL_COMPLETE_FORMULA_COMPILATION" if passed else "FAIL_LOCAL_FORMULA_RENDER",
                        "record_sha256": b["record_sha256"], "math_sha256": b["math_sha256"],
                        "source_sha256": b["source_sha256"], "source_path": b["path"], "source_line": b["source_line"],
                        "formula_inventory_sha256": sha(inv_path), "unique_formulas": len(formulas),
                        "source_formula_occurrences": len(occurrences), "scene_py_sha256": sha(scene),
                        "mp4_path": video.relative_to(ROOT).as_posix() if valid else None,
                        "mp4_sha256": result["mp4_sha256"] if valid else None,
                        "scope": "TRUSTED_LOCAL_MATHTEX_ONLY"})
    good = [x for x in checked if x["status"] == "PASS_LOCAL_COMPLETE_FORMULA_COMPILATION"]
    require(receipt["summary"] == {"total": len(checked), "rendered": len(good), "failed": len(checked)-len(good)},
            "reported summary mismatch")
    return {"batch": batch.relative_to(ROOT).as_posix(), "status": "PASS_BOUND_COMPLETE_LOCAL_FORMULAS" if len(good)==len(checked) else "FAIL_LOCAL_FORMULA_BATCH",
            "receipt_sha256": sha(receipt_path), "run_inputs_sha256": sha(inputs_path),
            "generator_sha256": receipt["generator_sha256"], "requested_ids": ids,
            "qualified_ids": [x["id"] for x in good], "rows": checked}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--batches", type=Path, nargs="+", required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    owner = Path(__file__).resolve().parent
    allowed = reviewed_generators(owner)
    bindings = core.load_record_bindings()
    by_id = {b["id"]: b for b in bindings}
    batches = [audit_batch(b.absolute(), by_id, allowed) for b in a.batches]
    requirements = read(ROOT/"reviews/codex-supervision/2026-10-07-deep-isolation-followup/native-resubmission-requirements.json")
    required = set(requirements["claude_required_ids"])
    prior = set(requirements["codex_real_sample_ids"])
    all_rows = [x for b in batches for x in b["rows"]]
    good = {x["id"]: x for x in all_rows if x["status"] == "PASS_LOCAL_COMPLETE_FORMULA_COMPILATION"}
    requested = {rid for b in batches for rid in b["requested_ids"]}
    report = {"schema": "independent-current-formula-followup-v1", "core_manifest_sha256": core.CORE_MANIFEST_SHA256,
              "verifier_sha256": sha(Path(__file__)), "batches": batches,
              "summary": {"current_records_verified": len(bindings), "claude_required": len(required),
                          "claude_qualified": len(required & good.keys()),
                          "claude_pending_ids": sorted(required - good.keys()),
                          "required_current_target_count": len(required|prior),
                          "target_qualified": len((required|prior)&good.keys()),
                          "target_pending_ids": sorted((required|prior)-good.keys()),
                          "unique_qualified_total": len(good), "extra_qualified_ids": sorted(good.keys()-required-prior),
                          "unique_formula_items_across_records": sum(x["unique_formulas"] for x in good.values()),
                          "source_formula_occurrences": sum(x["source_formula_occurrences"] for x in good.values()),
                          "required_not_requested_ids": sorted(required-requested)},
              "mathematics": "INHERITED_BOUND_REVIEW_NOT_REPROVED_BY_COMPILATION",
              "visual_acceptance": "NOT_REVIEWED", "native_sandbox": "UNVERIFIED",
              "semantic_isolation": "NOT_ESTABLISHED", "production": "CLOSED", "PASS_CORE_SCOPE_issued": False}
    out = core.checked_path(a.out.absolute(), owner)
    with out.open("xb") as f: f.write(core.encoded(report))
    print(json.dumps({"summary": report["summary"], "audit_sha256": sha(out)}, ensure_ascii=False))
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
