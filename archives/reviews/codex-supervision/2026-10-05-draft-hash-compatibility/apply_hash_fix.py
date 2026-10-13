from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
BASE=json.loads((OUT/'before.json').read_text('utf-8'))
def write(rel,text):
 p=ROOT/rel
 if rel in BASE['mutable_before']:
  assert hashlib.sha256(p.read_bytes()).hexdigest()==BASE['mutable_before'][rel], f'Concurrent edit: {rel}'
 else: assert not p.exists(), f'New file already exists: {rel}'
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(text.encode('utf-8'))
write('tools/draft_io.py',r'''"""Portable draft hashes and exclusive UTF-8/LF publication; no admission rules."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
from typing import Iterable

NORMALIZED_HASH = "sha256-utf8-sig-splitlines-lf-v1"
RAW_HASH = "sha256-raw-bytes-v1"
_SHA = re.compile(r"[0-9a-f]{64}\Z")


def normalized_bytes(data: bytes) -> bytes:
    """Exact v1 contract: UTF-8-sig decode, splitlines, LF join, UTF-8 encode.

    Only the leading BOM and splitlines-recognized line separators are folded.
    One terminal line separator is omitted; internal/trailing empty lines and
    other whitespace remain significant. No JSON sorting or number conversion.
    Invalid UTF-8 is rejected, never replaced.
    """
    return "\n".join(data.decode("utf-8-sig").splitlines()).encode("utf-8")


def fingerprint(data: bytes) -> dict:
    return {"sha256": hashlib.sha256(normalized_bytes(data)).hexdigest(),
            "raw_sha256": hashlib.sha256(data).hexdigest(),
            "hash_algorithm": NORMALIZED_HASH}


def selected_path(drafts: Path, entry: dict) -> Path:
    batch, rel = entry.get("batch"), entry.get("path")
    if not isinstance(batch, str) or not re.fullmatch(r"batch-\d{2}", batch):
        raise ValueError("invalid draft batch")
    if not isinstance(rel, str) or not rel or Path(rel).is_absolute():
        raise ValueError(f"invalid selected path: {batch}")
    root = drafts.resolve()
    path = (root / rel).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"selected path outside draft root: {batch}") from exc
    if path.parent != (root / batch).resolve() or path.suffix != ".jsonl":
        raise ValueError(f"invalid selected path: {batch}")
    return path


def verify_entry(path: Path, entry: dict, hash_algorithm: str | None = None) -> dict:
    algorithm = entry.get("hash_algorithm", hash_algorithm or RAW_HASH)
    if hash_algorithm is not None and algorithm != hash_algorithm:
        raise ValueError("entry/manifest hash algorithm conflict")
    if algorithm not in (NORMALIZED_HASH, RAW_HASH):
        raise ValueError(f"unsupported draft hash algorithm: {algorithm}")
    expected = entry.get("sha256")
    if not isinstance(expected, str) or not _SHA.fullmatch(expected):
        raise ValueError("missing or malformed selected SHA-256")
    data = path.read_bytes()
    raw = hashlib.sha256(data).hexdigest()
    if algorithm == NORMALIZED_HASH:
        expected_raw = entry.get("raw_sha256")
        if not isinstance(expected_raw, str) or not _SHA.fullmatch(expected_raw):
            raise ValueError("normalized draft entry requires archival raw_sha256")
        actual = fingerprint(data)["sha256"]
    else:
        actual = raw
    if actual != expected:
        raise ValueError(f"selected version hash mismatch: {entry.get('batch')} ({algorithm})")
    return {"sha256": actual, "raw_sha256": raw, "hash_algorithm": algorithm,
            "raw_bytes_match_manifest": raw == entry.get("raw_sha256", expected)}


def write_utf8_lf(path: Path, text: str, *, exclusive: bool = False) -> None:
    """Write without platform newline translation; reject BOM, normalize CR/LF."""
    if text.startswith("\ufeff"):
        raise ValueError("publisher text must not start with a BOM")
    data = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb" if exclusive else "wb") as stream:
        stream.write(data)


def publish_jsonl(path: Path, records: Iterable[dict]) -> dict:
    """Publish a NEW version only. Existing versions can never be overwritten."""
    rows = list(records)
    ids = [r.get("id") if isinstance(r, dict) else None for r in rows]
    if not rows or any(not isinstance(i, str) or not i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("draft records require nonempty unique string IDs")
    text = "\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":"),
                              allow_nan=False) for r in rows) + "\n"
    write_utf8_lf(path, text, exclusive=True)
    return {**fingerprint(path.read_bytes()), "count": len(rows)}


def require_legacy_selection(path: Path) -> None:
    """Retired repair scripts must not downgrade a migrated selector or evidence."""
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if data.get("schema", 1) >= 2 or data.get("hash_algorithm") not in (None, RAW_HASH):
        raise ValueError("Retired raw-hash repair tool: publish a new version with draft_io; "
                         "do not rewrite signed history or the normalized selector")
''')
write('tools/publish_draft.py',r'''"""Publish a new draft through the shared LF/no-BOM writer; does not select/admit."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from draft_io import publish_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = [json.loads(s) for s in args.source.read_text(encoding="utf-8-sig").splitlines()
            if s.strip()]
    result = publish_jsonl(args.output, rows)
    print(json.dumps({"path": args.output.as_posix(), **result}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''')
# General loader remains strict by default; only the draft auditor opts into BOM compatibility.
rel='tools/dataset_audit.py';s=(ROOT/rel).read_text('utf-8')
assert 'def load_file(path: Path) -> dict:' in s
s=s.replace('def load_file(path: Path) -> dict:', 'def load_file(path: Path, *, allow_utf8_bom: bool = False) -> dict:',1)
assert 'text = raw.decode("utf-8")' in s
s=s.replace('text = raw.decode("utf-8")','text = raw.decode("utf-8-sig" if allow_utf8_bom else "utf-8")',1)
write(rel,s)
rel='tools/draft_audit.py';s=(ROOT/rel).read_text('utf-8')
s=s.replace('from animtrain.near_dup import norm_text, shingles  # noqa: E402','from animtrain.near_dup import norm_text, shingles  # noqa: E402\nfrom draft_io import NORMALIZED_HASH, RAW_HASH, fingerprint, selected_path, verify_entry  # noqa: E402',1)
s=s.replace('p.read_text(encoding="utf-8").splitlines()', 'p.read_text(encoding="utf-8-sig").splitlines()')
s=s.replace('info = load_file(p)','info = load_file(p, allow_utf8_bom=True)',1)
s=s.replace('sel.read_text(encoding="utf-8")','sel.read_text(encoding="utf-8-sig")',1)
old='''            # 账本 path 相对草稿目录;统一转成相对项目根的 posix 再比较
            rel = p.relative_to(ROOT).as_posix()
            expected = (Path(DRAFT_GLOB.split("/batch-")[0])
                        / e.get("path", "")).as_posix()
            if e.get("path") and expected != rel:
                audit.add("info", "V011", SELECTION, batch,
                          f"被审文件 {rel} 不是账本选中版本({e.get('path')}),跳过哈希核对")
                continue
            actual = sha256_bytes(p.read_bytes())
            if actual != e.get("sha256"):
                audit.add("hard", "V007", SELECTION, batch,
                          f"{batch} 哈希与 draft-selection.json 不符"
                          f"(清单 {str(e.get('sha256'))[:12]}… vs 实际 {actual[:12]}…)")
'''
new='''            # Explicit project-relative draft_root also permits isolated selector fixtures.
            root = ROOT / d.get("draft_root", Path(DRAFT_GLOB).parent.parent.as_posix())
            try:
                expected = selected_path(root, e)
            except (ValueError, TypeError) as error:
                audit.add("hard", "V010", SELECTION, batch, str(error))
                continue
            if expected != p.resolve():
                audit.add("info", "V011", SELECTION, batch,
                          f"被审文件 {p.relative_to(ROOT).as_posix()} 不是账本选中版本({e.get('path')}),跳过哈希核对")
                continue
            try:
                binding = verify_entry(p, e, d.get("hash_algorithm"))
            except (OSError, ValueError, TypeError) as error:
                audit.add("hard", "V007", SELECTION, batch, str(error))
            else:
                if not binding["raw_bytes_match_manifest"]:
                    audit.add("info", "V013", SELECTION, batch,
                              "规范化内容哈希相符；原始字节与归档不同（换行/BOM 等价），不代表新增准入")
'''
assert old in s, 'audit binding changed concurrently';s=s.replace(old,new,1)
old='''            hash_files.append({"file": str(p.relative_to(ROOT)).replace("\\\\", "/"),
                               "sha256": sha256_bytes(b), "size": len(b)})'''
new='''            is_draft = p.suffix == ".jsonl" and p.parent.parent == ROOT / Path(DRAFT_GLOB).parent.parent
            hashes = fingerprint(b) if is_draft else {"sha256": sha256_bytes(b),
                "raw_sha256": sha256_bytes(b), "hash_algorithm": RAW_HASH}
            hash_files.append({"file": p.relative_to(ROOT).as_posix(), **hashes, "size": len(b)})'''
assert old in s;s=s.replace(old,new,1)
s=s.replace('"tool": "tools/draft_audit.py (只读)",','"tool": "tools/draft_audit.py (只读)",\n        "draft_hash_algorithm": NORMALIZED_HASH,\n        "raw_hash_listing": "file_hashes.sha256 (raw bytes; portable draft hashes are in file_hashes.json)",',1)
s=s.replace('f"{h[\'sha256\']}  {h[\'file\']}"','f"{h[\'raw_sha256\']}  {h[\'file\']}"',1)
# Every newly generated audit text uses UTF-8/LF; old outputs are never regenerated here.
s=s.replace('encoding="utf-8")','encoding="utf-8", newline="\\n")')
write(rel,s)
rel='reviews/2026-10-05-training-diversity-drafts/coverage_ledger.py';s=(ROOT/rel).read_text('utf-8')
s=s.replace("DRAFTS=ROOT/'reviews/2026-10-05-training-diversity-drafts'","DRAFTS=ROOT/'reviews/2026-10-05-training-diversity-drafts'\nsys.path.insert(0,str(ROOT/'tools'))\nfrom draft_io import NORMALIZED_HASH, fingerprint, selected_path, verify_entry",1)
s=s.replace("selection=drafts/'draft-selection.json';explicit={}","selection=drafts/'draft-selection.json';explicit={};algorithm=None",1)
s=s.replace("data=json.loads(selection.read_text(encoding='utf-8'))","data=json.loads(selection.read_text(encoding='utf-8-sig'));algorithm=data.get('hash_algorithm')",1)
old="""   e=explicit.pop(batch);path=(drafts/e['path']).resolve()
   if path.parent!=directory.resolve() or path.suffix!='.jsonl':raise ValueError(f'invalid selected path: {batch}')
   if not path.is_file() or digest(path)!=e['sha256']:raise ValueError(f'selected version hash mismatch: {batch}')
   method='EXPLICIT_HASH_BOUND_SELECTION'"""
new="""   e=explicit.pop(batch);path=selected_path(drafts,e)
   binding=verify_entry(path,e,algorithm)
   method='EXPLICIT_HASH_BOUND_SELECTION'"""
assert old in s;s=s.replace(old,new,1)
s=s.replace("path=max(candidates,key=lambda item:item[0])[1];method='LATEST_NUMBERED_AUTHOR_DRAFT_PENDING_REVIEW'","path=max(candidates,key=lambda item:item[0])[1];method='LATEST_NUMBERED_AUTHOR_DRAFT_PENDING_REVIEW';binding={**fingerprint(path.read_bytes()),'raw_bytes_match_manifest':None}",1)
s=s.replace("'sha256':digest(path),'selection':method","**binding,'selection':method",1)
s=s.replace("'selected_sha256':entry['sha256']}","'selected_sha256':entry['sha256'],'selected_raw_sha256':entry['raw_sha256'],'selected_hash_algorithm':entry['hash_algorithm']}",1)
write(rel,s)
# Append narrow attributes after the broad *.jsonl text rule. No Git index changes.
rel='.gitattributes';s=(ROOT/rel).read_text('utf-8').rstrip()+'''\n\n# Draft versions retain original bytes. New publications use UTF-8/LF/no BOM.
reviews/2026-10-05-training-diversity-drafts/batch-*/draft*.jsonl -text !eol
reviews/codex-supervision/**/staged/*.jsonl -text !eol
''';write(rel,s)
# Disable retired schema-1 mutation paths before any writes. Their old signed snapshots stay untouched.
for rel in ['tools/update_selection_sha.py','tools/update_selection_v2.py','tools/build_repair_v3.py','tools/restore_repair_originals.py','tools/fix_repair_issues.py','tools/build_repair_v2.py']:
 s=(ROOT/rel).read_text('utf-8');s=s.replace('from pathlib import Path','from pathlib import Path\nfrom draft_io import require_legacy_selection',1)
 selector='SEL' if '\nSEL = ' in s else 'DRAFTS / "draft-selection.json"'
 assert 'def main() -> int:\n' in s
 s=s.replace('def main() -> int:\n','def main() -> int:\n    require_legacy_selection('+selector+')\n',1);write(rel,s)
print('Applied shared draft hashing, BOM-compatible draft parsing, dual audit hashes, coverage verification, Git attributes, new writer and six retired-tool guards.')
