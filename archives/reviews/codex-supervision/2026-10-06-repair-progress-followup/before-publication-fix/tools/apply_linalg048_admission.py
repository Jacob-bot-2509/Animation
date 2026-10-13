"""Apply the linalg-048 v3 admission: replace the active record, re-bind
manifest, re-issue freeze locks, refresh asset evidence, re-screen.

All original bytes are archived under reviews/2026-10-06-linalg048-admission/
before/ before anything is written. Every pre-check must pass or nothing is
modified. Run AFTER admit_linalg048_v3.py has produced render evidence.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from animtrain.kp_rule import kp_signature  # noqa: E402
from animtrain.structural_leakage import compare  # noqa: E402

CANDIDATE_PATH = (ROOT / "reviews/codex-supervision/2026-10-06-holdout-strict-fix"
                  / "linalg048-v3/candidate.json")
CANDIDATE_SHA = "8d30d09d5f1dd5b7c72f429ee5670680f2a84a953fbebd57d8372bfbca56e169"
MANIFEST_SHA = "801f7036cf14b9d44e3a84874878ad176b19124fbfe74154cd5e95c8cbcfc448"
TRAIN_FILE = ROOT / "data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl"
MANIFEST = ROOT / "data/manifest.json"
LOCKS = [ROOT / "data/eval-v2.lock.json", ROOT / "data/test-v2.lock.json"]
ASSET_EVIDENCE = ROOT / "data/asset_evidence.json"
OUT_DIR = ROOT / "reviews/2026-10-06-linalg048-admission"
BEFORE = OUT_DIR / "before"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_queries():
    out = []
    for p in [ROOT / "data/v2/eval/dataset_eval.jsonl",
              ROOT / "data/v2/test/dataset_test.jsonl"]:
        for line in p.read_text("utf-8-sig").splitlines():
            if line.strip():
                out.append(json.loads(line))
    return out


def main() -> int:
    try:
        # ---- pre-checks: nothing may be modified unless all of these pass
        if hashlib.sha256(CANDIDATE_PATH.read_bytes()).hexdigest() != CANDIDATE_SHA:
            raise ValueError("candidate hash mismatch")
        cand = json.loads(CANDIDATE_PATH.read_text("utf-8-sig"))
        if sha(MANIFEST) != MANIFEST_SHA:
            raise ValueError("manifest not at the locked revision")
        manifest = json.loads(MANIFEST.read_text("utf-8"))
        entry = next(e for e in manifest["entries"]
                     if e["path"].endswith("dataset_linalg.jsonl"))
        if sha(TRAIN_FILE) != entry["sha256"]:
            raise ValueError("train file hash vs manifest mismatch")
        train_bytes = TRAIN_FILE.read_bytes()
        lines = train_bytes.decode("utf-8").splitlines()
        if not lines or json.loads(lines[0]).get("id") != "linalg-048":
            raise ValueError("unexpected train file layout")
        active = json.loads(lines[0])
        for lock in LOCKS:
            lk = json.loads(lock.read_text("utf-8"))
            if lk["meta"]["manifest_sha256"] != MANIFEST_SHA:
                raise ValueError("lock not at locked manifest: " + lock.name)
            for e in lk["entries"]:
                p = Path(e["path"])
                if not p.exists() or sha(p) != e["sha256"]:
                    raise ValueError("lock entry hash mismatch: " + str(e["path"]))
        ev = json.loads(ASSET_EVIDENCE.read_text("utf-8"))
        if ev["manifest_sha256"] != MANIFEST_SHA:
            raise ValueError("asset evidence not at locked manifest")
        render_ev = json.loads((OUT_DIR / "render-evidence.json").read_text("utf-8"))
        if not render_ev.get("render", {}).get("ok"):
            raise ValueError("render evidence missing/not ok")

        # ---- archive originals (bytes)
        if BEFORE.exists():
            raise ValueError("before/ archive exists")
        BEFORE.mkdir(parents=True)
        for src in [TRAIN_FILE, MANIFEST, ASSET_EVIDENCE] + LOCKS:
            dst = BEFORE / src.name
            dst.write_bytes(src.read_bytes())
        listing = {p.name: sha(p) for p in BEFORE.iterdir()}
        (BEFORE / "listing.json").write_text(
            json.dumps(listing, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8", newline="\r\n")

        # ---- 1. replace the record line (active key order, candidate values)
        order = list(active.keys())
        new_rec = {k: cand[k] for k in order}
        new_line = json.dumps(new_rec, ensure_ascii=False, separators=(", ", ": "))
        assert "\n" not in new_line
        new_lines = [new_line] + lines[1:]
        new_file_bytes = ("\r\n".join(new_lines) + "\r\n").encode("utf-8")
        TRAIN_FILE.write_bytes(new_file_bytes)
        new_input_sha = hashlib.sha256(new_line.encode("utf-8")).hexdigest()

        # ---- 2. manifest entry
        entry["sha256"] = sha(TRAIN_FILE)
        entry["size"] = len(new_file_bytes)
        if entry.get("notes"):
            entry["notes"] += ";2026-10-06 linalg-048 结构泄漏改写准入(水平剪切)"
        else:
            entry["notes"] = "2026-10-06 linalg-048 结构泄漏改写准入(水平剪切)"
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\r\n",
                            encoding="utf-8", newline="\r\n")
        new_manifest_sha = sha(MANIFEST)

        # ---- 3. re-issue freeze locks (entries unchanged, bind new manifest)
        for lock in LOCKS:
            old_bytes = lock.read_bytes()
            lk = json.loads(lock.read_text("utf-8"))
            lk["meta"]["manifest_sha256"] = new_manifest_sha
            lk["meta"]["revision_reason"] = (
                "linalg-048 结构泄漏改写准入(水平剪切 [[1,3],[0,1]]);eval/test 内容不变")
            lk["meta"]["supersedes_sha256"] = hashlib.sha256(old_bytes).hexdigest()
            lock.write_text(json.dumps(lk, ensure_ascii=False, indent=2) + "\r\n",
                            encoding="utf-8", newline="\r\n")

        # ---- 4. asset evidence refresh for the rewritten record
        ev["manifest_sha256"] = new_manifest_sha
        r48 = ev["records"]["linalg-048"]
        r48["input_sha256"] = new_input_sha
        r48["source"]["sha256"] = sha(TRAIN_FILE)
        r48["scene_source"] = {
            "path": str(OUT_DIR / "render-evidence.json"),
            "note": "v3 shear candidate rendered in AppContainer; semantic/math reviewed; "
                    "asset acceptance for this record remains UNVERIFIED until full "
                    "semantic+visual acceptance"}
        ASSET_EVIDENCE.write_text(json.dumps(ev, ensure_ascii=False, indent=2) + "\r\n",
                                  encoding="utf-8", newline="\r\n")

        # ---- 5. re-screen: new problem vs all queries + other train records
        new_prob = new_rec["problem"]
        queries = load_queries()
        others = []
        for p in ROOT.glob("data/v2/train/leakage-isolated-v3-2026-10-05/*.jsonl"):
            for line in p.read_text("utf-8-sig").splitlines():
                if line.strip():
                    r = json.loads(line)
                    if r.get("id") != "linalg-048":
                        others.append(r)
        cands, sig_eqs = [], []
        for r in queries + others:
            if compare(new_prob, r["problem"])["candidate"]:
                cands.append(r.get("id") or r.get("problem_id"))
            try:
                if kp_signature(r) == kp_signature(new_rec):
                    sig_eqs.append(r.get("id") or r.get("problem_id"))
            except ValueError:
                pass
        if cands:
            raise ValueError("structural candidates remain: " + str(cands))

        report = {
            "schema": "linalg048-admission-apply-v1",
            "candidate_raw_sha256": CANDIDATE_SHA,
            "before_manifest_sha256": MANIFEST_SHA,
            "after_manifest_sha256": new_manifest_sha,
            "train_file": {"path": str(TRAIN_FILE.relative_to(ROOT)),
                           "before_sha256": listing["dataset_linalg.jsonl"],
                           "after_sha256": sha(TRAIN_FILE),
                           "new_input_sha256": new_input_sha,
                           "records": len(new_lines)},
            "locks": {l.name: {"before_sha256": listing[l.name],
                               "after_sha256": sha(l)} for l in LOCKS},
            "asset_evidence_updated": True,
            "rescreen": {"compared_pairs": len(queries) + len(others),
                         "structural_candidates": cands,
                         "signature_equal_count": len(sig_eqs),
                         "signature_equal_ids": sig_eqs[:10]},
            "render_evidence": str(OUT_DIR / "render-evidence.json"),
        }
        report_path = OUT_DIR / "apply-report.json"
        if report_path.exists():
            raise ValueError("apply report exists")
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8", newline="\n")
        print(json.dumps({k: v for k, v in report.items() if k != "rescreen"},
                         ensure_ascii=False, indent=1))
        print("rescreen:", json.dumps(report["rescreen"], ensure_ascii=False))
        return 0
    except Exception as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
