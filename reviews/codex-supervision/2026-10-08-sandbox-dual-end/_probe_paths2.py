"""Read-only probe: characterize the confined tool layer's view of paths under the project.

No writes. Prints one JSON object so the evidence is machine-checkable.
"""
import json
import os
import traceback
from pathlib import Path

BASE = Path("D:/Animation-Model-Training")
CASES = [
    ("base_list", BASE, "dir"),
    ("venv_list", BASE / ".venv", "dir"),
    ("venv_bare", BASE / ".venv", None),
    ("render_tmp_list", BASE / ".render-tmp", "dir"),
    ("src_list", BASE / "src", "dir"),
    ("src_animtrain_list_1", BASE / "src" / "animgtrain", "dir"),
    ("src_animtrain_list_2", BASE / "src" / "animgtrain", "dir"),
    ("appcontainer_read", BASE / "src" / "animgtrain" / "appcontainer.py", "read"),
    ("appcontainer_stat", BASE / "src" / "animgtrain" / "appcontainer.py", "stat"),
    ("init_read", BASE / "src" / "animgtrain" / "__init__.py", "read"),
    ("sandbox_execution_read", BASE / "src" / "animgtrain" / "sandbox_execution.py", "read"),
    ("virtualenv_cfg", BASE / ".venv" / "pyvenv.cfg", "read"),
    ("python_exe", BASE / ".venv" / "Scripts" / "python.exe", "stat"),
    ("outside_temp", Path("C:/Windows/win.ini"), "read"),
    ("system32_list", Path("C:/Windows/System32"), "dir"),
]

report = {"python": os.sys.version, "cases": {}}
for name, path, kind in CASES:
    entry = {"path": str(path), "kind": kind}
    try:
        if kind == "dir":
            entry["result"] = sorted(p.name for p in path.iterdir())[:12]
            entry["count"] = len(list(path.iterdir()))
        elif kind == "read":
            data = path.read_bytes()
            entry["result"] = f"read {len(data)} bytes"
        elif kind == "stat":
            st = path.stat()
            entry["result"] = f"stat size={st.st_size}"
        else:
            entry["result"] = f"exists={path.exists()} is_dir={path.is_dir()}"
    except Exception as exc:
        entry["error"] = f"{type(exc).__name__}: {exc}"
        entry["trace_tail"] = traceback.format_exc().strip().splitlines()[-1]
    report["cases"][name] = entry

print(json.dumps(report, ensure_ascii=False, indent=2))
