# -*- coding: utf-8 -*-
"""扫描考研题源结构:统计每年题面md的题号标记数与解析md的【答案】数,
判定可自动配对的年份。只读,不产生输出文件(结果打印)。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "holdout-sources/kaoyan-math1"
PAPERS = SRC / "papers"
SOLUTIONS = SRC / "solutions"

NUM_RE = re.compile(r"^\s*(\d{1,2})[.、．]\s*\S")
ANS_RE = re.compile(r"^\s*[\(（]\s*(\d{1,2})\s*[\)）]\s*【答案】")


def count_paper_numbers(text: str) -> list:
    nums = []
    for line in text.splitlines():
        m = NUM_RE.match(line)
        if m:
            n = int(m.group(1))
            if 1 <= n <= 23 and n not in nums:
                nums.append(n)
    return nums


def count_solution_answers(text: str) -> list:
    nums = []
    for line in text.splitlines():
        m = ANS_RE.match(line)
        if m:
            nums.append(int(m.group(1)))
    return nums


def main() -> int:
    years = []
    for paper in sorted(PAPERS.glob("*.md")):
        m = re.match(r"(\d{4})", paper.name)
        if not m:
            continue
        year = m.group(1)
        pnums = count_paper_numbers(paper.read_text(encoding="utf-8"))
        sol = SOLUTIONS / f"{year}年解析"
        sfile = None
        if sol.is_dir():
            cands = list(sol.glob("*.md"))
            if cands:
                sfile = cands[0]
        anums = count_solution_answers(sfile.read_text(encoding="utf-8")) if sfile else []
        full = sorted(set(range(1, 23)))
        years.append((year, pnums, anums,
                      len(pnums), len(anums),
                      sorted(set(pnums) & set(anums))))
    print(f"{'year':6} {'paper#':>7} {'sol#':>5} {'common':>6}  paper_markers")
    for y, p, a, lp, la, common in years:
        flag = "OK" if lp == la and lp >= 20 else ("PART" if lp >= 15 else "GAP")
        print(f"{y:6} {lp:7} {la:5} {len(common):6}  {flag}  {p[:8]}{'...' if len(p) > 8 else ''}")
    ok = sum(1 for *_, lp, la, _ in years if lp == la and lp >= 20)
    print("auto-pairable years:", ok, "/", len(years))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
