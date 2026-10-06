"""Finalize the workflow semantic review into a new bound review artifact.

Reads the workflow result JSON (task output file), joins it with the pending
packet (verifies packet sha + subject coverage 1:1), and writes
reviews/2026-10-06-linalg048-admission/v3-receipt-bound/semantic-review-workflow-v1.json
with honest verdicts (DIFFERENT_CORE_TASK / SAME_CORE_TRAIN_VARIANT /
SAME_CORE_CROSS_SPLIT / UNCERTAIN). Does NOT produce
linalg048-manual-acceptance-v2: the train-variant pair cannot be squeezed
into the all-DIFFERENT protocol, which Codex will revise.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = (ROOT / "reviews/codex-supervision/2026-10-06-bound-receipt-semantic-review"
          / "pending-review-packet.json")
PACKET_SHA = "eb37c77a6c2619726f2b297ae92ec12778d908140c542af5893970ab8578b401"
WORKFLOW_RESULT = Path(
    r"C:\Users\Jacap\AppData\Local\Temp\claude\d--code\ee005e1f-71f1-4697-a746-054f6399acd6"
    r"\tasks\wfwly0rpg.output")
OUT = (ROOT / "reviews/2026-10-06-linalg048-admission/v3-receipt-bound"
       / "semantic-review-workflow-v1.json")
VALID = {"DIFFERENT_CORE_TASK", "SAME_CORE_TRAIN_VARIANT",
         "SAME_CORE_CROSS_SPLIT", "UNCERTAIN"}


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--workflow-result", type=Path, default=WORKFLOW_RESULT)
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args(argv)
    try:
        if sha_bytes(PACKET.read_bytes()) != PACKET_SHA:
            raise ValueError("packet sha mismatch")
        packet = json.loads(PACKET.read_text("utf-8"))
        wf = json.loads(args.workflow_result.read_text("utf-8"))
        result = wf.get("result")
        if not isinstance(result, dict):
            raise ValueError("workflow result shape mismatch")
        pairs = {f"{p['split']}|{p['id']}": p for p in result["pairs"]}
        rows = []
        for subject in packet["semantic_pairs"]:
            key = f"{subject['split']}|{subject['id']}"
            p = pairs.get(key)
            if p is None or p["verdict"] not in VALID:
                raise ValueError("missing/invalid workflow verdict for " + key)
            rows.append({
                "split": subject["split"], "id": subject["id"],
                "problem_sha256": subject["problem_sha256"],
                "verdict": p["verdict"], "reason": p["reason"],
                "evidence": p["evidence"],
            })
        if len(rows) != 296:
            raise ValueError("coverage mismatch: " + str(len(rows)))
        artifact = {
            "schema": "linalg048-semantic-review-workflow-v1",
            "status": "HONEST_REVIEW_COMPLETE_PENDING_PROTOCOL_AND_CODEX_REVIEW",
            "reviewer": "claude-code multi-agent workflow (16 reviewers + "
                        "adversarial challengers + completeness critic)",
            "workflow": {"run_id": "wf_b0af1d57-7f1",
                         "agents": wf.get("agentCount"),
                         "subagent_tokens": wf.get("totalTokens"),
                         "journal": (r"C:\Users\Jacap\.claude\projects\d--code"
                                     r"\ee005e1f-71f1-4697-a746-054f6399acd6"
                                     r"\subagents\workflows\wf_b0af1d57-7f1"
                                     r"\journal.jsonl")},
            "bindings": {
                "packet_raw_sha256": PACKET_SHA,
                "rule_sha256": packet.get("labeling_rule_sha256"),
                "candidate_raw_sha256": packet.get("candidate_raw_sha256"),
                "scene_raw_sha256": packet.get("scene_raw_sha256"),
                "media_raw_sha256": packet.get("media_raw_sha256"),
                "render_evidence_raw_sha256": packet.get("render_evidence_raw_sha256"),
            },
            "counts": result.get("counts"),
            "same_core_train_variant": result.get("trainVariants"),
            "same_core_cross_split": result.get("leakage"),
            "uncertain": result.get("uncertain"),
            "note": ("One pair is SAME_CORE_TRAIN_VARIANT (train|linalg-058: axis-swapped "
                     "transpose shear, same core task). Per the user ruling it is retained "
                     "as an in-train variant pending a density check; the current "
                     "all-DIFFERENT manual-acceptance protocol cannot express this. "
                     "Protocol revision is Codex's. No cross-split leakage was found."),
            "pairs": rows,
        }
        if args.out.exists():
            raise ValueError("output exists: use a new path")
        with args.out.open("x", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(artifact, ensure_ascii=False, indent=1) + "\n")
        print(json.dumps({"counts": artifact["counts"],
                          "same_core_train_variant": artifact["same_core_train_variant"],
                          "same_core_cross_split": artifact["same_core_cross_split"],
                          "uncertain": artifact["uncertain"],
                          "out": str(args.out)}, ensure_ascii=False, indent=1))
        return 0
    except Exception as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
