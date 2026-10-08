# Render-side sandbox experiment.
#
# Runs the project's own sandboxed render path (AppContainer + MiKTeX, the code in
# tools/sandbox_render_pilot.py) against one manifest-backed record, and records:
#   - whether the AppContainer profile can be used,
#   - whether the project interpreter the pipeline hardcodes is usable,
#   - the child process return code, stdout/stderr and decoded media artifact,
#   - a host (non-AppContainer) control run of the same interpreter.
#
# Writes only under --out. Exit code: 0 when at least one record rendered inside the
# AppContainer, 2 when the sandboxed render could not run, 3 on harness error.

import argparse
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

ROOT = Path("D:/Animation-Model-Training")
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

PY = Path("D:/Python Interpreter 3147/python.exe")
PROJECT_PY = ROOT / ".venv" / "Scripts" / "python.exe"


def sha(path: Path) -> str:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--format", default="png", choices=["png", "mp4"])
    ap.add_argument("--timeout-ms", type=int, default=180000)
    args = ap.parse_args()
    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)

    report = {
        "experiment": "render-side AppContainer sandbox",
        "tool": "run_render_experiment.py",
        "format": args.format,
        "root": str(ROOT),
        "stages": {},
        "started_unix": time.time(),
    }

    # Stage 1: sandbox profile usable?
    try:
        from animtrain import appcontainer as ac
        sid = ac.appcontainer_sid()
        report["stages"]["appcontainer_sid"] = {
            "ok": True, "sid_sddl": ac._sid_sddl(sid),
            "profile_path": str(ac.appcontainer_profile_path(sid)),
            "profile_exists": ac.appcontainer_profile_path(sid).exists(),
        }
    except Exception as exc:  # noqa: BLE001
        report["stages"]["appcontainer_sid"] = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
        ac = None

    # Stage 2: project interpreter (hardcoded by the render pipeline)
    try:
        exists = PROJECT_PY.exists()
        report["stages"]["project_interpreter"] = {
            "ok": exists, "path": str(PROJECT_PY), "exists": exists,
            "bytes": PROJECT_PY.stat().st_size if exists else None,
        }
    except Exception as exc:  # noqa: BLE001
        report["stages"]["project_interpreter"] = {"ok": False, "path": str(PROJECT_PY),
                                                   "error": f"{type(exc).__name__}: {exc}"}

    # Stage 3: host control - does the project interpreter run at all here?
    control = {"argv": [str(PROJECT_PY), "-c", "import sys; print(sys.version)"]}
    try:
        cp = subprocess.run(control["argv"], capture_output=True, timeout=60)
        control.update(returncode=cp.returncode,
                       stdout=cp.stdout.decode("utf-8", "replace")[-400:],
                       stderr=cp.stderr.decode("utf-8", "replace")[-400:])
    except Exception as exc:  # noqa: BLE001
        control.update(error=f"{type(exc).__name__}: {exc}")
    report["stages"]["host_control_project_interpreter"] = control

    # Stage 4: sandboxed render of one record, using the project's own render_one()
    smokes = []
    try:
        from tools import sandbox_render_pilot as srp
        from tools import render_templates as rt
        manifest = ROOT / "data" / "manifest.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        entry = data["entries"][0]
        rec_path = (manifest.parent / entry["path"]).resolve()
        first = json.loads(rec_path.read_text(encoding="utf-8").splitlines()[0])
        rec = dict(first)
        rec["_input_sha256"] = sha(rec_path)
        work = out / ("scene-" + uuid.uuid4().hex[:12])
        env = {"SystemRoot": os.environ.get("SystemRoot", r"C:\Windows"),
               "PATH": os.environ.get("PATH", "")}
        result = srp.render_one(rec, work, env, args.format, args.timeout_ms)
        smokes.append({"manifest": str(manifest), "entry": entry, "record_id": rec.get("id"),
                       "workdir": str(work), "result": result})
    except Exception as exc:  # noqa: BLE001
        smokes.append({"error": f"{type(exc).__name__}: {exc}"})
    report["stages"]["sandboxed_render"] = smokes

    rendered = [s for s in smokes if isinstance(s.get("result"), dict) and s["result"].get("ok")]
    report["rendered_records"] = len(rendered)
    report["verdict"] = "PASS" if rendered else "FAIL"
    report["finished_unix"] = time.time()
    report["evidence_sha256"] = None
    target = out / "render-experiment.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps({"verdict": report["verdict"], "rendered_records": len(rendered),
                      "stage_ok": {k: v.get("ok") for k, v in report["stages"].items()
                                   if isinstance(v, dict)},
                      "evidence": str(target)}, ensure_ascii=False))
    return 0 if rendered else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"verdict": "ERROR", "error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False))
        raise SystemExit(3)
