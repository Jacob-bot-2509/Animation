"""Create an immutable admission candidate with native, exact scene specifications."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("math_binding", ROOT / "tools/verify_math_corrections_30.py")
math = importlib.util.module_from_spec(spec); spec.loader.exec_module(math)
v = math.v
qa_spec = importlib.util.spec_from_file_location("format_qa", ROOT / "tools/core_scope_consistency_check.py")
qa = importlib.util.module_from_spec(qa_spec); qa_spec.loader.exec_module(qa)
TEMPLATE = Path("reviews/codex-supervision/2026-10-07-core-verifier-followup/scene-updates-v2.templates.json")
TEMPLATE_SHA = "9a2a85358bdb56c6e1e4f45e0298ebea4421b9781d58b17b63418f38a2148b3d"


def load_updates(root=ROOT):
    data = (root / TEMPLATE).read_bytes()
    if v.digest(data) != TEMPLATE_SHA:
        raise v.VerificationError("scene templates differ from reviewed version")
    result = json.loads(data.decode("utf-8"))
    if len(result) != 17:
        raise v.VerificationError("17 reviewed scene updates required")
    return result


def validate_scene(scene):
    if not isinstance(scene, dict):
        raise v.VerificationError("scene_spec must be a native object, not repr text")
    for name in ("objects", "steps"):
        values = scene.get(name)
        if not isinstance(values, list) or not values:
            raise v.VerificationError("scene objects/steps must be nonempty arrays")
        for text in values:
            if not isinstance(text, str) or not text.strip():
                raise v.VerificationError("empty or nonstring scene component")
            if any(ord(c) < 32 for c in text):
                raise v.VerificationError("damaged scene escape/control character")
            if qa.latex_issues(text) or qa.DECIMAL.search(text) or qa.APPROXIMATION.search(text):
                raise v.VerificationError("scene requires balanced exact mathematical text")


def scene_sha(scene):
    return v.digest(v.canonical(scene))


def write_json(path, value, lines=False):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        if lines:
            for row in value: stream.write(json.dumps(row, ensure_ascii=False) + "\n")
        else:
            json.dump(value, stream, ensure_ascii=False, indent=2); stream.write("\n")


def build(root, destination):
    destination = (root / destination).resolve()
    if (not destination.is_relative_to((root / "reviews").resolve())
            or destination.is_relative_to((root / v.SUP).resolve())
            or destination.is_relative_to((root / v.PACKET).resolve())):
        raise v.VerificationError("new admission version must stay in project reviews")
    if destination.exists():
        raise FileExistsError("preserve existing admission version")
    patches, sources = math.load_verified_math(root)
    updates = load_updates(root)
    by_id = {p["id"]: p for p in patches}
    if not set(updates) <= set(by_id):
        raise v.VerificationError("scene update outside corrected math scope")
    final = {}
    scene_rows = []
    record_rows = []
    for patch in patches:
        rid = patch["id"]; base = patch["corrected_record"]
        rec = dict(base)
        if rid in updates:
            rec.update({k: updates[rid][k] for k in ("scene_spec", "visual_style") if k in updates[rid]})
        validate_scene(rec["scene_spec"])
        final[rid] = rec
        math_fields = {k: rec[k] for k in ("problem", "solution", "answer")}
        final_sha = v.digest(v.canonical(rec))
        declared = {"id": rid, "source": patch["source"],
            "base_math_record_dense_sha256": patch["after_record_dense_sha256"],
            "math_fields_dense_sha256": v.digest(v.canonical(math_fields)),
            "final_record_dense_sha256": final_sha, "scene_updated": rid in updates}
        record_rows.append(declared)
        if rid in updates:
            scene_rows.append({**declared, "scene_spec": rec["scene_spec"],
                "visual_style": rec.get("visual_style"),
                "old_scene_spec_sha256": scene_sha(base["scene_spec"]),
                "new_scene_spec_sha256": scene_sha(rec["scene_spec"]),
                "scene_sha_encoding": "json-sortkeys-compact-utf8",
                "rationale": updates[rid]["rationale"]})
    destination.mkdir(parents=True, exist_ok=False)
    for b in sources:
        source = v.inside(root, b["candidate"]["path"])
        target = destination / "admission-sources" / b["before"]["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        lines = source.read_bytes().splitlines(keepends=True)
        for line in b["changed_source_lines"]:
            rec = json.loads(lines[line-1].decode("utf-8-sig"))
            if rec["id"] in updates:
                raw = lines[line-1]
                ending = b"\r\n" if raw.endswith(b"\r\n") else b"\n" if raw.endswith(b"\n") else b""
                prefix = b"\xef\xbb\xbf" if line == 1 and raw.startswith(b"\xef\xbb\xbf") else b""
                lines[line-1] = prefix + json.dumps(final[rec["id"]], ensure_ascii=False).encode("utf-8") + ending
        with target.open("xb") as stream: stream.write(b"".join(lines))
    write_json(destination / "scene-updates-candidate.jsonl", scene_rows, True)
    write_json(destination / "record-bindings.jsonl", record_rows, True)
    write_json(destination / "scene-binding-audit.json", {
        "schema": "math-admission-scene-content-review-v2", "total": 30,
        "scene_updated": len(updates), "scene_retained": 30-len(updates),
        "rows": [{"id": p["id"], "scene_updated": p["id"] in updates,
                  "scene_content_review": "CODEX_REVIEWED_SCOPED_TEXT",
                  "render_verdict": "UNVERIFIED"} for p in patches],
        "native_render_performed": False, "active_admission": "PENDING"})
    receipt = ("# 30 题正文与 17 场景的新版本绑定\n\n"
       "保留数学修订包与 v1 接入原件。30 条数学正文完全等于既有精确修订，17 个场景更新，13 个原生场景保留。\n\n"
       "修正傅里叶端点、秩零点、有向面积、圆周率估计量、中心极限定理标准化、积分与偏导的精确推导及条件生存函数归一化。"
       "场景全部使用原生 objects/steps 字典，禁止 Python repr 字符串和损坏转义。概率面积使用可精确构造的四条矩形分区。\n\n"
       "record-bindings.jsonl 区分数学正文基础记录 SHA、三个数学字段 SHA、最终含场景记录 SHA；场景 SHA 采用规范 JSON。\n\n"
       "本回执支持具名 30 条正文及场景文本的新版本绑定。没有渲染或视觉验收，有限动画不能代替数学证明，"
       "旧渲染不能证明新版。现役数据、选择器、冻结包未改；全量数学与同核心隔离仍未完成。production CLOSED。\n")
    with (destination / "ADMISSION_RECEIPT.md").open("x", encoding="utf-8", newline="\n") as stream: stream.write(receipt)
    items = []
    for path in sorted(destination.rglob("*")):
        if path.is_file():
            data = path.read_bytes()
            items.append({"path": path.relative_to(root).as_posix(),
                          "raw_sha256": v.digest(data), "bytes": len(data)})
    write_json(destination / "admission-manifest.json", {"schema": "math-admission-v2-manifest",
        "items": items, "active_admission": "PENDING", "render_verdict": "UNVERIFIED"})
    return {"result": "NEW_VERSION_CREATED", "math_records": 30, "scene_updates": len(updates),
            "path": destination.relative_to(root).as_posix(), "active_admission": "PENDING"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("reviews/2026-10-07-math-admission-v1"))
    args = parser.parse_args(argv)
    try:
        result = build(ROOT, args.out); rc = 0
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        result = {"result": "FAIL", "error": type(exc).__name__ + ": " + str(exc)}; rc = 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
