"""Read-only probe: isolate which path spelling the confined layer treats differently."""
import json
import os
from pathlib import Path

VARIANTS = {
    "fwd": "D:/Animation-Model-Training/src/animtrain",
    "fwd_fwd": "D:/Animation-Model-Training/src/animtrain",
    "back": "D:\\Animation-Model-Training\\src\\animgtrain",
    "from_path": str(Path("D:/Animation-Model-Training") / "src" / "animgtrain"),
    "from_path_str": str(Path("D:/Animation-Model-Training/src/animtrain")),
    "resolve": str(Path("D:/Animation-Model-Training/src/animtrain").resolve()),
    "mixed": "/Animation-Model-Training/src/animtrain",
    "drive_rel": "D:Animation-Model-Training/src/animtrain",
}

out = {"cwd": os.getcwd()}
for name, raw in VARIANTS.items():
    entry = {"raw": raw}
    try:
        p = Path(raw)
        entry["iterdir"] = len(list(p.iterdir()))
    except Exception as exc:
        entry["iterdir"] = f"{type(exc).__name__}: {exc}"
    try:
        entry["os_listdir"] = len(os.listdir(raw))
    except Exception as exc:
        entry["os_listdir"] = f"{type(exc).__name__}: {exc}"
    out[name] = entry
print(json.dumps(out, ensure_ascii=False, indent=2))
