"""执行项目内代码文件，并保留目标脚本的参数和退出语义。

用法: <venv>/Scripts/python.exe -X utf8 tools/runpy.py <code_file.py>
"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))


def main(argv: list[str]) -> int:
    if len(argv) < 1:
        print(__doc__, file=sys.stderr)
        return 2
    code = Path(argv[0])
    if not code.is_absolute():
        code = ROOT / code
    if not code.is_file():
        print(f"代码文件不存在: {code}", file=sys.stderr)
        return 2
    previous_argv = sys.argv
    sys.argv = [str(code)] + argv[1:]
    try:
        runpy.run_path(str(code), run_name="__main__")
    except SystemExit as error:
        if error.code is None:
            return 0
        if isinstance(error.code, int):
            return error.code
        print(error.code, file=sys.stderr)
        return 1
    except Exception:
        import traceback
        traceback.print_exc()
        return 1
    finally:
        sys.argv = previous_argv
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
