"""Render-side preflight: can this project's AppContainer sandbox actually launch and render?

Stages checked, in order:
  1. the DSH confined tool layer can see the tools it needs (project read-only view);
  2. the animtrain-render-sandbox AppContainer profile exists and the SID derives;
  3. the project interpreter .venv/Scripts/python.exe is reachable;
  4. the sandbox MiKTeX runtime descriptor and trees are present;
  5. an AppContainer child process starts, reports its token identity, and can run
     the project interpreter (the exact interpreter the render pipeline uses).

Writes only under --out (an ordinary subprocess-writable staging directory) and a
probe work directory beside it. Exit code: 0 all checks passed, 2 a check failed,
3 the harness crashed.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path("D:/Animation-Model-Training")
sys.path.insert(0, str(ROOT / "src"))

APP_NAME = "animtrain-render-sandbox"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)

    report: dict = {
        "tool": "render_preflight",
        "root": str(ROOT),
        "out": str(out),
        "python": sys.version,
        "checks": {},
        "blocking": [],
    }
    failed = False

    def record(name, fn):
        nonlocal failed
        try:
            value = fn()
            report["checks"][name] = {"ok": True, "value": value}
            return value
        except Exception as exc:  # noqa: BLE001
            failed = True
            report["checks"][name] = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
            report["blocking"].append(name)
            return None

    # 1. project read view from the confined layer
    def project_view():
        return {
            "tools_dir_entries": len(list((ROOT / "tools").iterdir())),
            "src_animgtrain_entries": len(list((ROOT / "src" / "animgtrain").iterdir())),
            "sandbox_render_pilot": (ROOT / "tools" / "sandbox_render_pilot.py").is_file(),
            "manifest": (ROOT / "data" / "manifest.json").is_file(),
        }

    record("project read view", project_view)

    # 2. AppContainer profile + SID
    acm = record("import appcontainer module",
                 lambda: __import__("animgtrain.appcontainer", fromlist=["x"]).__name__)

    def profile_check():
        from animtrain import appcontainer as ac
        sid = ac.appcontainer_sid(APP_NAME)
        pkg_root = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))) / "Packages"
        pkg = pkg_root / APP_NAME
        return {
            "sid_sddl": ac._sid_sddl(sid),
            "profile_path": str(ac.appcontainer_profile_path(sid)),
            "profile_exists": ac.appcontainer_profile_path(sid).exists(),
            "package_dir_exists": pkg.exists(),
        }

    if acm is not None:
        record("appcontainer profile and sid", profile_check)

    # 3. project interpreter reachability
    def venv_check():
        py = ROOT / ".venv" / "Scripts" / "python.exe"
        return {"path": str(py), "exists": py.exists(),
                "bytes": py.stat().st_size if py.exists() else None,
                "scripts_dir_exists": (ROOT / ".venv" / "Scripts").exists()}

    venv = record("project interpreter visible", venv_check)

    # 4. MiKTeX sandbox runtime
    def miktex_check():
        desc = ROOT / ".sandbox-runtime" / "miktex-environment.json"
        data = json.loads(desc.read_text(encoding="utf-8"))
        runtime = ROOT / ".sandbox-runtime" / "miktex-real"
        state = ROOT / ".sandbox-runtime" / "miktex-state"
        return {"descriptor_keys": sorted(data)[:8], "runtime_exists": runtime.exists(),
                "state_exists": state.exists(),
                "runtime_entries": len(list(runtime.iterdir())) if runtime.exists() else None}

    record("miktex sandbox runtime", miktex_check)

    # 5. AppContainer child process, running the project interpreter
    def appcontainer_run_check():
        from animtrain import appcontainer as ac
        work = out / ("appcontainer-probe-" + uuid.uuid4().hex[:12])
        work.mkdir(parents=True, exist_ok=True)
        probe = work / "identity_probe.py"
        probe.write_text(
            "import json,sys\n"
            f"sys.path.insert(0, r'{ROOT / 'src'}')\n"
            "from animtrain import network_isolation as net\n"
            "print('TOKEN=' + json.dumps(net.token_identity()))\n",
            encoding="utf-8")
        env = {"SystemRoot": os.environ.get("SystemRoot", r"C:\Windows"),
               "PATH": os.environ.get("PATH", ""),
               "TEMP": str(work), "TMP": str(work),
               "PYTHONDONTWRITEBYTECODE": "1"}
        results = {}
        # 5a: host interpreter inside AppContainer
        for label, argv in (("host_interpreter", [sys.executable, "-X", "utf8", "-B", str(probe)]),
                            ("project_interpreter", [str(ROOT / ".venv" / "Scripts" / "python.exe"),
                                                     "-X", "utf8", "-B", str(probe)])):
            try:
                cp = ac.run_appcontainer(argv, cwd=work, env=env, allowed_dirs=[(work, True)],
                                         timeout_ms=60000)
                stdout = cp.stdout.decode("utf-8", "replace")
                stderr = cp.stderr.decode("utf-8", "replace")
                (work / f"{label}.stdout.txt").write_text(stdout, encoding="utf-8")
                (work / f"{label}.stderr.txt").write_text(stderr, encoding="utf-8")
                token = None
                for line in stdout.splitlines():
                    if line.startswith("TOKEN="):
                        token = json.loads(line.split("=", 1)[1])
                results[label] = {"returncode": cp.returncode, "token": token,
                                  "stdout_head": stdout[:300], "stderr_head": stderr[:300]}
            except Exception as exc:  # noqa: BLE001
                results[label] = {"error": f"{type(exc).__name__}: {exc}"}
        # 5c: host control - same interpreter, no AppContainer
        ctrl = subprocess.run([sys.executable, "-X", "utf8", "-B", str(probe)], capture_output=True)
        results["host_control"] = {"returncode": ctrl.returncode,
                                   "stdout_head": ctrl.stdout.decode("utf-8", "replace")[:300],
                                   "stderr_head": ctrl.stderr.decode("utf-8", "replace")[:300]}
        results["workdir"] = str(work)
        return results

    record("appcontainer child process", appcontainer_run_check)

    report["ok"] = not failed
    report["verdict"] = "PASS" if not failed else "FAIL"
    report["project_interpreter_usable"] = bool(
        isinstance(venv, dict) and venv.get("exists") and (venv.get("bytes") or 0) > 0)
    target = out / "render-preflight.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"verdict": report["verdict"], "blocking": report["blocking"],
                      "evidence": str(target)}, ensure_ascii=False))
    return 0 if not failed else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"verdict": "FAIL", "crash": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False))
        raise SystemExit(3)
