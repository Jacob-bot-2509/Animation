# DSH-side sandbox experiment harness.
#
# Every case runs as a fresh confined subprocess and reports its own exit code plus a
# JSON payload. Two independent dimensions are judged from the data:
#
#   A. confinement   - does the sandbox block what it must block and allow what it must allow?
#   B. readiness     - does the project's own render pipeline have the inputs it needs?
#
# Usage: python run_dsh_experiment.py --out <staging-dir>
# Exit code: 0 when the confinement dimension fully matches, 2 otherwise, 3 on harness error.

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path("D:/Animation-Model-Training")
PY = Path("D:/Python Interpreter 3147/python.exe")
CASE_DIR = ROOT / "reviews" / "codex-supervision" / "2026-10-08-sandbox-dual-end" / "evidence"

CASES = [
    {
        "name": "workspace_write_inside", "dimension": "confinement", "expect": "allowed",
        "desc": "create and delete a file inside the session workspace",
        "code": "from pathlib import Path\n"
                "p = Path(r'{case_work}') / 'case_inside.tmp'\n"
                "p.write_text('inside', encoding='utf-8')\n"
                "n = p.stat().st_size\n"
                "p.unlink()\n"
                "print(json.dumps({{'bytes': n}}))\n",
    },
    {
        "name": "read_outside_workspace", "dimension": "confinement", "expect": "allowed",
        "desc": "read a plain system file outside the workspace (read-only call)",
        "code": "from pathlib import Path\n"
                "d = Path(r'C:/Windows/win.ini').read_bytes()\n"
                "print(json.dumps({{'bytes': len(d)}}))\n",
    },
    {
        "name": "write_outside_workspace", "dimension": "confinement", "expect": "denied",
        "desc": "attempt a write outside the workspace (must be blocked)",
        "code": "from pathlib import Path\n"
                "p = Path(r'C:/Windows/Temp/_dsh_sandbox_escape.tmp')\n"
                "p.write_text('escape', encoding='utf-8')\n"
                "print(json.dumps({{'wrote': str(p)}}))\n",
    },
    {
        "name": "write_git_metadata", "dimension": "confinement", "expect": "denied",
        "desc": "attempt a write into .git metadata (must be blocked)",
        "code": "from pathlib import Path\n"
                "p = Path(r'{root}/.git/_dsh_sandbox_touch.tmp')\n"
                "p.write_text('x', encoding='utf-8')\n"
                "print(json.dumps({{'wrote': str(p)}}))\n",
    },
    {
        "name": "system_program_readonly", "dimension": "confinement", "expect": "allowed",
        "desc": "invoke a system program read-only (cmd /c ver)",
        "code": "import subprocess\n"
                "cp = subprocess.run(['cmd', '/c', 'ver'], capture_output=True)\n"
                "print(json.dumps({{'rc': cp.returncode, 'stdout': cp.stdout.decode('utf-8','replace').strip()}}))\n",
    },
    {
        "name": "path_forward_slash", "dimension": "confinement", "expect": "allowed",
        "desc": "list src/animtrain with forward-slash separators",
        "code": "from pathlib import Path\n"
                "n = len(list(Path('D:/Animation-Model-Training/src/animtrain').iterdir()))\n"
                "print(json.dumps({{'entries': n}}))\n",
    },
    {
        "name": "path_backslash_literal", "dimension": "confinement", "expect": "allowed",
        "desc": "list src/animtrain with literal backslash separators (same path)",
        "code": "from pathlib import Path\n"
                "n = len(list(Path(r'D:\\\\Animation-Model-Training\\\\src\\\\animgtrain').iterdir()))\n"
                "print(json.dumps({{'entries': n}}))\n",
    },
    {
        "name": "reviews_tree_write", "dimension": "readiness", "expect": "allowed",
        "desc": "write a scratch file into reviews/codex-supervision/ (evidence deliverable location)",
        "code": "from pathlib import Path\n"
                "p = Path(r'{case_dir}') / '_dsh_privileged_probe.tmp'\n"
                "p.write_text('probe', encoding='utf-8')\n"
                "p.unlink()\n"
                "print(json.dumps({{'wrote_and_removed': str(p)}}))\n",
    },
    {
        "name": "project_venv_present", "dimension": "readiness", "expect": "allowed",
        "desc": "project interpreter .venv/Scripts/python.exe exists and is measurable",
        "assert_payload": "exists",
        "code": "from pathlib import Path\n"
                "p = Path('D:/Animation-Model-Training/.venv/Scripts/python.exe')\n"
                "exists = p.exists()\n"
                "print(json.dumps({{'exists': exists, 'bytes': p.stat().st_size if exists else None}}))\n",
    },
    {
        "name": "venv_dir_listable", "dimension": "readiness", "expect": "allowed",
        "desc": "the .venv directory itself is listable from the confined layer",
        "code": "from pathlib import Path\n"
                "n = len(list(Path('D:/Animation-Model-Training/.venv').iterdir()))\n"
                "print(json.dumps({{'entries': n}}))\n",
    },
    {
        "name": "miktex_runtime_readable", "dimension": "readiness", "expect": "allowed",
        "desc": "the sandbox MiKTeX runtime tree is readable",
        "code": "from pathlib import Path\n"
                "n = len(list(Path('D:/Animation-Model-Training/.sandbox-runtime/miktex-real').iterdir()))\n"
                "print(json.dumps({{'entries': n}}))\n",
    },
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)

    results = []
    started = time.time()
    for case in CASES:
        work = out / case["name"]
        work.mkdir(parents=True, exist_ok=True)
        formatted = case["code"].format(case_work=work.as_posix(), case_dir=CASE_DIR.as_posix(),
                                        root=ROOT.as_posix())
        body = ("import json, sys\n"
                "def emit(obj):\n"
                "    print('__RESULT__' + json.dumps(obj))\n"
                "try:\n"
                + "".join("    " + line + "\n" for line in formatted.splitlines())
                + "except Exception as exc:\n"
                  "    emit({'ok': False, 'error': f'{type(exc).__name__}: {exc}'})\n"
                  "    sys.exit(7)\n")
        script = work / "case.py"
        script.write_text(body, encoding="utf-8")

        cp = subprocess.run([str(PY), "-X", "utf8", "-B", str(script)], capture_output=True)
        stdout = cp.stdout.decode("utf-8", "replace")
        stderr = cp.stderr.decode("utf-8", "replace")
        payload = None
        for line in stdout.splitlines():
            if line.startswith("__RESULT__"):
                payload = json.loads(line[len("__RESULT__"):])
        raised = bool(payload) and payload.get("ok") is False
        actual = "denied" if raised else "allowed"
        matched = actual == case["expect"]
        assertion = case.get("assert_payload")
        if matched and assertion and not raised:
            if not (payload or {}).get(assertion):
                matched = False
                if payload is not None:
                    payload["assertion_failed"] = assertion
        results.append({
            "case": case["name"], "dimension": case["dimension"], "desc": case["desc"],
            "expect": case["expect"], "actual": actual, "matched": matched,
            "returncode": cp.returncode, "result": payload,
            "stdout_tail": stdout[-400:], "stderr_tail": stderr[-400:],
            "script": script.as_posix(),
        })
        print(json.dumps({"case": case["name"], "dim": case["dimension"], "expect": case["expect"],
                          "actual": actual, "matched": matched, "rc": cp.returncode}, ensure_ascii=False))

    def dim(name):
        rows = [r for r in results if r["dimension"] == name]
        return {"matched": sum(1 for r in rows if r["matched"]), "total": len(rows),
                "violations": [r["case"] for r in rows if not r["matched"]]}

    confinement = dim("confinement")
    readiness = dim("readiness")
    report = {
        "experiment": "dsh-side sandbox confinement",
        "tool": "run_dsh_experiment.py",
        "root": str(ROOT),
        "interpreter": str(PY),
        "started_unix": started,
        "finished_unix": time.time(),
        "confinement": confinement,
        "readiness": readiness,
        "cases": results,
        "verdict": "PASS" if confinement["matched"] == confinement["total"] else "FAIL",
    }
    target = out / "dsh-experiment.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"verdict": report["verdict"], "confinement": confinement,
                      "readiness": readiness, "evidence": str(target)}, ensure_ascii=False))
    return 0 if report["verdict"] == "PASS" else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"verdict": "ERROR", "error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False))
        raise SystemExit(3)
