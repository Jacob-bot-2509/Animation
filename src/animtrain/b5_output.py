"""Project-only exclusive output directories for B5 candidate material.
Not an approval or publication interface; existing directories are immutable here.
"""
from pathlib import Path
import re
PROJECT=Path(__file__).absolute().parents[2]
DEVICES={"con","prn","aux","nul",*(f"com{i}" for i in range(1,10)),*(f"lpt{i}" for i in range(1,10))}

def new_output_dir(value):
    p=Path(value)
    if not p.is_absolute():p=PROJECT/p
    if ".." in p.parts or not p.is_relative_to(PROJECT) or p==PROJECT:
        raise ValueError("B5 output must stay in a fresh project directory")
    for part in p.relative_to(PROJECT).parts:
        if (not re.fullmatch(r"[A-Za-z0-9_.-]+",part) or part in (".","..")
            or part.endswith(("."," ")) or part.split(".")[0].casefold() in DEVICES):
            raise ValueError("Noncanonical Windows output path")
    for q in (p,*p.parents):
        if q.is_symlink():raise ValueError("Reparse output path")
        if q.exists():
            st=q.lstat()
            if getattr(st,"st_file_attributes",0)&0x400:
                raise ValueError("Reparse output path")
            if q.is_dir() and (q/"delivery-manifest.json").exists():
                raise ValueError("Frozen output directory")
        if q==PROJECT:break
    if p.exists():raise FileExistsError("Existing B5 output is never overwritten")
    p.parent.mkdir(parents=True,exist_ok=True)
    p.mkdir()  # Exclusive claim; a partial failed output is retained, never reused.
    return p
