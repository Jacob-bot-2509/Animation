"""Compile actual complete mathematical formulas from version-bound trusted local records."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from fractions import Fraction

if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
import core_signatures as core

ROOT = core.ROOT
OUT = ROOT / "reviews/2026-10-07-native-render-pilot"
PY = ROOT / ".venv/Scripts/python.exe"
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,100}")

def escaped(text, index):
    n = 0
    while index > 0 and text[index - 1] == "\\":
        n += 1
        index -= 1
    return bool(n % 2)

def extract_formulas(text):
    if not isinstance(text, str):
        raise ValueError("Math source must be text")
    formulas, i = [], 0
    while i < len(text):
        if text[i] == "$" and not escaped(text, i):
            delimiter = "$" * 2 if text.startswith("$" * 2, i) else "$"
            start = i + len(delimiter)
            end = start
            while end < len(text):
                if text.startswith(delimiter, end) and not escaped(text, end):
                    break
                end += 1
            if end == len(text):
                raise ValueError("Unclosed dollar math delimiter")
            formula = text[start:end].strip()
            i = end + len(delimiter)
        elif text.startswith(r"\(", i) or text.startswith(r"\[", i):
            closing = r"\)" if text.startswith(r"\(", i) else r"\]"
            start = i + 2
            end = text.find(closing, start)
            if end < 0:
                raise ValueError("Unclosed bracket math delimiter")
            formula = text[start:end].strip()
            i = end + 2
        else:
            i += 1
            continue
        if not formula:
            raise ValueError("Empty mathematical formula")
        formulas.append(formula)
    return formulas

def formula_inventory(record):
    locations = []
    for field in ("problem", "solution", "answer"):
        for formula in extract_formulas(record[field]):
            locations.append({"field": field, "formula": formula})
    scene = record.get("scene_spec")
    if scene is not None:
        if not isinstance(scene, dict):
            raise ValueError("Scene must be an object")
        for field in ("objects", "steps"):
            values = scene.get(field, [])
            if not isinstance(values, list):
                raise ValueError("Scene text must be a list")
            for i, text in enumerate(values):
                for formula in extract_formulas(text):
                    locations.append({"field": "scene_spec." + field, "index": i, "formula": formula})
    unique = list(dict.fromkeys(x["formula"] for x in locations))
    if not unique:
        raise ValueError("Record has no mathematical formulas to compile")
    return unique, locations

def build_scene(record):
    formulas, _ = formula_inventory(record)
    # Each exact source formula is the argument to MathTex; no filtering by length.
    return (
        "from manim import *\n"
        "FORMULAS = " + repr(formulas) + "\n"
        "class ConceptScene(Scene):\n"
        "    def construct(self):\n"
        "        maths = [MathTex(formula) for formula in FORMULAS]\n"
        "        group = VGroup(*maths).arrange(DOWN, buff=1/4)\n"
        "        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))\n"
        "        self.add(group)\n"
        "        self.wait(1/5)\n"
    )

def as_bytes(value):
    if value is None:
        return b""
    return value if isinstance(value, bytes) else value.encode("utf-8", errors="replace")

def render_one(rid, work, record, binding, timeout=240):
    if not ID_RE.fullmatch(rid):
        raise ValueError("Invalid output record ID")
    work = core.checked_path(work, core.ROOT / "reviews")
    work.mkdir(exist_ok=False)
    formulas, locations = formula_inventory(record)
    scene = work / "scene.py"
    scene.write_text(build_scene(record), encoding="utf-8", newline="\n")
    (work / "formula-inventory.json").write_bytes(core.encoded({"unique_formulas": formulas, "source_occurrences": locations}))
    command = [str(PY), "-m", "manim", "render", str(scene), "ConceptScene", "-ql", "--media_dir", str(work / "media"), "--disable_caching"]
    start = time.monotonic_ns()
    try:
        proc = subprocess.run(command, capture_output=True, timeout=timeout, cwd=str(work))
        rc, stdout, stderr, timed_out = proc.returncode, proc.stdout, proc.stderr, False
    except subprocess.TimeoutExpired as exc:
        rc, stdout, stderr, timed_out = -1, as_bytes(exc.stdout), as_bytes(exc.stderr), True
    elapsed = str(Fraction(time.monotonic_ns() - start, 1000000000))
    (work / "stdout.bin").write_bytes(as_bytes(stdout))
    (work / "stderr.bin").write_bytes(as_bytes(stderr))
    videos = [core.checked_path(p, work) for p in (work / "media").rglob("ConceptScene.mp4") if p.is_file()]
    valid_video = len(videos) == 1 and videos[0].stat().st_size > 0
    success = type(rc) is int and rc == 0 and not timed_out and valid_video
    return {
        "id": rid, "rc": rc, "timed_out": timed_out, "elapsed_seconds_exact": elapsed,
        "status": "PASS_LOCAL_COMPLETE_FORMULA_COMPILATION" if success else "FAIL_LOCAL_FORMULA_RENDER",
        "unique_formulas": len(formulas), "source_formula_occurrences": len(locations),
        "formulas_sha256": core.dense(formulas), "record_sha256": binding["record_sha256"],
        "math_sha256": binding["math_sha256"], "source_sha256": binding["source_sha256"],
        "core_manifest_sha256": core.CORE_MANIFEST_SHA256,
        "scene_py_sha256": core.digest(scene.read_bytes()),
        "stdout_sha256": core.digest(as_bytes(stdout)), "stderr_sha256": core.digest(as_bytes(stderr)),
        "mp4": valid_video, "mp4_path": videos[0].relative_to(work).as_posix() if valid_video else None,
        "mp4_sha256": core.digest(videos[0].read_bytes()) if valid_video else None,
        "production_evidence": False, "visual_acceptance": "NOT_REVIEWED",
    }

def run(ids, out, timeout=240):
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Unique nonempty IDs required")
    if type(timeout) is not int or timeout <= 0:
        raise ValueError("Positive integer timeout required")
    bindings = core.load_record_bindings()
    by_id = {b["id"]: b for b in bindings}
    records = {}
    for rid in ids:
        if not isinstance(rid, str) or not ID_RE.fullmatch(rid):
            raise ValueError("Invalid record ID")
        records[rid] = core.load_record(by_id, rid)
        formula_inventory(records[rid])
    inputs = {"schema": "native-formula-run-inputs-v2", "core_manifest_sha256": core.CORE_MANIFEST_SHA256,
              "generator_sha256": core.digest(Path(__file__).read_bytes()), "bindings": [by_id[rid] for rid in ids],
              "scope": "TRUSTED_LOCAL_MATHTEX_ONLY"}
    core.publish(out, {"run-inputs.json": core.encoded(inputs)})
    results = []
    for rid in ids:
        # Recheck this actual frozen record immediately before using it.
        record = core.load_record(by_id, rid)
        result = render_one(rid, out / ("render-" + rid), record, by_id[rid], timeout)
        results.append(result)
        print(json.dumps({k: result[k] for k in ("id", "status", "unique_formulas", "rc")}), flush=True)
    passed = sum(r["status"] == "PASS_LOCAL_COMPLETE_FORMULA_COMPILATION" for r in results)
    receipt = {"schema": "native-complete-formula-receipt-v2", **inputs,
               "results": results, "summary": {"total": len(results), "rendered": passed, "failed": len(results) - passed},
               "production_evidence": False, "native_sandbox": "UNVERIFIED",
               "visual_acceptance": "NOT_REVIEWED", "mathematics": "SEPARATE_BOUND_PROOF_REQUIRED",
               "semantic_isolation": "NOT_ESTABLISHED", "production": "CLOSED", "PASS_CORE_SCOPE_issued": False}
    # inputs schema and receipt schema are deliberately distinct.
    receipt["schema"] = "native-complete-formula-receipt-v2"
    with (out / "receipt.json").open("xb") as f:
        f.write(core.encoded(receipt))
    print(json.dumps(receipt["summary"]), flush=True)
    return 0 if passed == len(results) else 3

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ids", nargs="+", required=True)
    parser.add_argument("--batch", default="complete-formulas-v2")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--timeout", type=int, default=240)
    args = parser.parse_args(argv)
    try:
        if not re.fullmatch(r"[a-z0-9-]{1,60}", args.batch):
            raise ValueError("Invalid batch name")
        out = (args.out or OUT / args.batch).absolute()
        return run(args.ids, out, args.timeout)
    except (ValueError, KeyError, TypeError, IndexError, OSError) as exc:
        print(json.dumps({"status": "FAIL_LOCAL_BOUND_RENDER_INPUT", "error": str(exc), "production": "CLOSED"}))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
