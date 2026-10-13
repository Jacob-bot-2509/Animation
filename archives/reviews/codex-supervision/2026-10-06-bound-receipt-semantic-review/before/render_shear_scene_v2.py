"""Re-render Codex's revised shear scene v2 (shear-scene-v2.py) via the
reviewed AppContainer transport, and write a fully bound receipt.

This is NOT the admit/apply pipeline (those are owned by Codex now). It only
produces the fresh isolated render + evidence the visual re-verification
needs: scene source sha, video sha, frame count, rc, isolation evidence,
final/mid frame PNGs.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from animtrain.sandbox_execution import render_scene, decode_video  # noqa: E402

SCENE_PATH = (ROOT / "reviews/codex-supervision/2026-10-06-repair-progress-followup"
              / "shear-scene-v2.py")
SCENE_SHA = "e21c9ff372911a46a8538025f6e1f4f4f4cb36371fbef7740fe47fd71c65149e"
OUT_DIR = ROOT / "reviews/2026-10-06-linalg048-admission/v2-rerender"


def main() -> int:
    try:
        src_bytes = SCENE_PATH.read_bytes()
        if hashlib.sha256(src_bytes).hexdigest() != SCENE_SHA:
            raise ValueError("scene sha mismatch")
        source = src_bytes.decode("utf-8")
        if "class ConceptScene" not in source:
            raise ValueError("scene class missing")
        if OUT_DIR.exists():
            raise ValueError("output dir exists: use a fresh one")
        OUT_DIR.mkdir(parents=True)
        print("rendering shear-scene-v2 in AppContainer ...", flush=True)
        result = render_scene(source)
        if not result.get("ok"):
            print("[FAIL]", result.get("detail"))
            return 1
        transport = result["transport"]
        artifact = decode_video(Path(result["output"]["path"]))
        import av
        with av.open(artifact["path"]) as c:
            frames = list(c.decode(video=0))
        final_png = OUT_DIR / "frame-final.png"
        mid_png = OUT_DIR / f"frame-{len(frames)//2}.png"
        frames[-1].to_image().save(final_png)
        frames[len(frames) // 2].to_image().save(mid_png)
        receipt = {
            "schema": "shear-scene-v2-rerender-v1",
            "scene_source": str(SCENE_PATH.relative_to(ROOT)),
            "scene_raw_sha256": SCENE_SHA,
            "scene_source_sha256": transport.get("source_sha256"),
            "video_sha256": artifact["sha256"],
            "video": artifact,
            "returncode": transport.get("rc"),
            "stdout_tail": transport.get("stdout", "")[-400:],
            "stderr_tail": transport.get("stderr", "")[-400:],
            "work_dir": transport.get("work"),
            "command": transport.get("command"),
            "isolation": result.get("isolation"),
            "frames": {"total": len(frames), "final_png": str(final_png),
                       "mid_png": str(mid_png)},
        }
        (OUT_DIR / "receipt.json").write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8", newline="\n")
        print(json.dumps({"rc": receipt["returncode"],
                          "video_sha256": receipt["video_sha256"],
                          "frames": len(frames),
                          "work": transport.get("work"),
                          "receipt": str(OUT_DIR / "receipt.json")},
                         ensure_ascii=False))
        return 0
    except Exception as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
