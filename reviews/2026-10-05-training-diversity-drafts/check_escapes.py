"""批次级 LaTeX 双重转义排查:解析后字符串中出现「两个反斜杠+已知命令名」
(如 \\frac)即命令双重转义,渲染会出换行残字;矩阵换行 \\ 后跟行内容
(数字/字母/&)是合法 LaTeX,不报警。
用法: <venv>/Scripts/python.exe -X utf8 tools/runpy.py
      reviews/2026-10-05-training-diversity-drafts/check_escapes.py [batch-dir...]
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CMDS = ("frac|sqrt|int|sum|oint|begin|end|det|cdot|times|le|ge|ne|neq|to|in|"
        "pi|ln|exp|lim|left|right|infty|partial|cos|sin|tan|cdots|quad|text|"
        "mathsf|mathbb|Delta|Theta|Phi|alpha|beta|gamma|theta|lambda|varphi|"
        "sigma|omega|varepsilon|parallel|angle|prod|pm|mp|circ|prime|"
        "downarrow|uparrow|subseteq|subset|cup|cap|oplus|ast|ast|choose|"
        "binom|over|underbrace|overline|underline|vec|hat|bar|tilde|mid|"
        "nmid|setminus|wedge|vee|forall|exists|nabla")
PAT = re.compile(r"(?<!\\)\\\\(" + CMDS + r")")  # 恰好两个反斜杠+命令名(第三个反斜杠=矩阵换行,合法)


def main(argv: list[str]) -> int:
    dirs = [HERE / a for a in argv] if argv else sorted(
        HERE.glob("batch-*/"))
    bad = []
    for d in dirs:
        p = d / "draft.jsonl"
        if not p.is_file():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            for k, v in r.items():
                if isinstance(v, str) and PAT.search(v):
                    bad.append((r["id"], k))
                elif isinstance(v, dict):
                    for k2, v2 in v.items():
                        if isinstance(v2, list):
                            for s in v2:
                                if isinstance(s, str) and PAT.search(s):
                                    bad.append((r["id"], "scene." + k2))
    if bad:
        print("双重转义字段:")
        for rid, k in bad:
            print(f"  {rid} {k}")
        return 1
    print("无双重转义")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
