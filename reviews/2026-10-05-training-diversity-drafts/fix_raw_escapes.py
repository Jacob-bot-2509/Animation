"""定点修复:对 build_draft.py 中 raw string 行(r"...")把双反斜杠命令
(\\mu 等)改为单反斜杠。仅处理 problem/solution/answer 的 r 字符串行;
scene_spec 的非 raw 双引号行不触碰(其 \\ 即单个反斜杠,正确)。
前提:该批 raw 字符串内没有矩阵行分隔符(\\\\ 仅用于命令双重转义)。
目标文件经环境变量 FIX_TARGET 指定(经 runpy 执行时 argv 被占用)。
用法: FIX_TARGET=<build_draft.py> <venv>/Scripts/python.exe -X utf8
      tools/runpy.py reviews/2026-10-05-training-diversity-drafts/fix_raw_escapes.py
"""
from __future__ import annotations
import os
import re
import sys
from pathlib import Path


def main() -> int:
    target = os.environ.get("FIX_TARGET", "")
    p = Path(target)
    if not p.is_absolute():
        p = Path.cwd() / p
    if not p.is_file():
        print(f"FIX_TARGET 无效: {target}")
        return 2
    text = p.read_text(encoding="utf-8")
    out, n = [], 0
    for line in text.splitlines(keepends=True):
        # raw 字符串行:字段后紧跟 r"
        if re.search(r'"(problem|solution|answer)":\s*r"', line):
            fixed = line.replace("\\\\", "\\")
            n += line.count("\\\\")
            out.append(fixed)
        else:
            out.append(line)
    p.write_text("".join(out), encoding="utf-8", newline="\n")
    print(f"修复 {n} 处 -> {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
