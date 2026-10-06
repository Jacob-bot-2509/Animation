# -*- coding: utf-8 -*-
"""考研真题三件套提取器(1987-2021):
  题面 = papers/<year>.md 按（大题节,局部题号）切题
  答案+解析 = solutions/<year>年解析/*.md 按 (n)【答案】/【解】切
  仅当 (节, 题号) 两侧都能对上且三成分齐全才出记录——缺题面/缺解析一律不要。
输出 holdout-sources/extracted/kaoyan-triples.jsonl(不入库)。"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "holdout-sources/kaoyan-math1"
OUT_DIR = ROOT / "holdout-sources/extracted"
OUT = OUT_DIR / "kaoyan-triples.jsonl"

SECTION_RE = re.compile(r"^#+\s*([一二三四五六七八九十]+)\s*[、.．]\s*(.+)$")
QNUM_RE = re.compile(r"^[（(]\s*(\d{1,2})\s*[)）]")
ANS_RE = re.compile(r"^[（(]\s*(\d{1,2})\s*[)）]\s*【答案】\s*(.*)$")
SOL_RE = re.compile(r"^【解】(.*)$")
SUB_RE = re.compile(r"^[（(](\d{1,2})[)）](?:\s*(?:本题满分\d+分|本小题满分\d+分))?")


def cn_num(name: str) -> str:
    return name.replace(" ", "").replace("．", "、")


def section_key(name: str):
    """归一化节名 → (中文数字, 类型词) 或 None。只认填空题/选择题。"""
    n = name.replace(" ", "").replace("．", "、")
    m = re.match(r"([一二三四五六七八九十]+)、(.+)", n)
    if not m:
        return None
    tail = m.group(2)
    if "填空" in tail:
        return (m.group(1), "填空")
    if "选择" in tail:
        return (m.group(1), "选择")
    return None


def split_sections(text: str):
    """按中文数字大题节头拆成 [(key, name, body)]。"""
    sections = []
    current = None
    buf = []
    for line in text.splitlines():
        m = SECTION_RE.match(line.strip())
        if m:
            if current is not None:
                sections.append((current, "\n".join(buf)))
            current = (m.group(1), m.group(2))
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections.append((current, "\n".join(buf)))
    return sections


def paper_questions(body: str):
    """题面节内按（n）切题,返回 {局部号: 题面文本}。"""
    items = {}
    cur_num = None
    cur_lines = []
    for line in body.splitlines():
        s = line.strip()
        m = QNUM_RE.match(s) or (SUB_RE.match(s) and len(s) < 60 and QNUM_RE.match(s))
        if QNUM_RE.match(s):
            if cur_num is not None:
                items[cur_num] = "\n".join(cur_lines).strip()
            cur_num = int(QNUM_RE.match(s).group(1))
            cur_lines = [s]
        elif cur_num is not None:
            cur_lines.append(s)
    if cur_num is not None:
        items[cur_num] = "\n".join(cur_lines).strip()
    return items


def solution_items(body: str):
    """解析节内按 (n)【答案】切,返回 {局部号: {answer, solution}}。"""
    items = {}
    cur = None
    cur_ans = ""
    cur_sol = []
    for line in body.splitlines():
        s = line.strip()
        m = ANS_RE.match(s)
        if m:
            if cur is not None:
                items[cur] = {"answer": cur_ans.strip(), "solution": "\n".join(cur_sol).strip()}
            cur = int(m.group(1))
            cur_ans = m.group(2)
            cur_sol = []
        elif cur is not None:
            sm = SOL_RE.match(s)
            if sm:
                cur_sol.append(sm.group(1))
            elif s:
                cur_sol.append(s)
    if cur is not None:
        items[cur] = {"answer": cur_ans.strip(), "solution": "\n".join(cur_sol).strip()}
    return items


def main() -> int:
    OUT_DIR.mkdir(exist_ok=True)
    if OUT.exists():
        raise ValueError("preserve previous output")
    records = []
    year_report = []
    for paper in sorted((SRC / "papers").glob("*.md")):
        ym = re.match(r"(\d{4})", paper.name)
        if not ym:
            continue
        year = ym.group(1)
        sol_dir = SRC / f"solutions/{year}年解析"
        sol_md = list(sol_dir.glob("*.md")) if sol_dir.is_dir() else []
        if not sol_md:
            year_report.append((year, 0, "no solution md"))
            continue
        paper_secs = {}
        for (num, name), body in split_sections(paper.read_text(encoding="utf-8")):
            key = section_key(num + "、" + name)
            if key and key not in paper_secs:
                paper_secs[key] = body
        sol_secs = {}
        for (num, name), body in split_sections(sol_md[0].read_text(encoding="utf-8")):
            key = section_key(num + "、" + name)
            if key and key not in sol_secs:
                sol_secs[key] = body
        made = 0
        for key, pbody in paper_secs.items():
            if key not in sol_secs:
                continue
            pqs = paper_questions(pbody)
            sits = solution_items(sol_secs[key])
            for num in sorted(set(pqs) & set(sits)):
                sit = sits[num]
                if not pqs[num].strip() or not sit["answer"].strip() or not sit["solution"].strip():
                    continue  # 三成分缺一不要
                records.append({
                    "id": f"holdout-src-kaoyan-{year}-{num:02d}",
                    "year": year, "section": key[0] + "、" + key[1], "number": num,
                    "problem": pqs[num], "answer": sit["answer"],
                    "solution": sit["solution"],
                    "source": "kaoyan-math1",
                    "source_path": str(paper.relative_to(SRC)),
                    "license": "CC-BY-NC-SA-4.0; 真题版权归出题单位; 仅内部评测使用",
                })
                made += 1
        year_report.append((year, made, "ok"))
    with OUT.open("w", encoding="utf-8", newline="\n") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("total triples:", len(records))
    for y, n, flag in year_report:
        print(f"  {y}: {n} {flag}")
    print("output:", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
