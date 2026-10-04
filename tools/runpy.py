"""固定入口:执行项目内的临时/一次性 Python 代码文件(替代 python -c)。

用法(唯一调用方式,杜绝 shell 转义事故):
  <venv>/Scripts/python.exe -X utf8 tools/runpy.py <code_file.py>

- 代码用 Write 工具落到项目内文件后执行,绝不内联传 Windows 路径/反斜杠;
- 自动注入 sys.path(项目根 / src / tools);
- 执行失败如实回传退出码。
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
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    code = Path(argv[0])
    if not code.is_absolute():
        code = ROOT / code
    if not code.is_file():
        print(f"代码文件不存在: {code}", file=sys.stderr)
        return 2
    try:
        runpy.run_path(str(code), run_name="__main__")
    except SystemExit as e:  # 透传被跑代码的退出码
        return int(e.code or 0)
    except Exception as e:  # noqa: BLE001
        import traceback
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
