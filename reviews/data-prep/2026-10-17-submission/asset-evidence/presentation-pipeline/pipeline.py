"""动画呈现管线 harness v2(阶段机,fail-closed)。

阶段:
  generate    独立复算校验呈现候选:记录行 SHA、模板 SHA、场景字节 SHA、分页计划
              SHA、覆盖率、几何清单;任何一项不符即拒收。不读信用 bindings 自述。
  render      真实渲染门禁:直接调用 src/animtrain/sandbox_execution.check_certificate()
              这一权威合同;本管线不重复实现门禁、不执行场景、不伪造渲染。
  review-pack 审核包组装(原子):场景片段 + 可运行包壳 + 原题 + 答案 + 规范计划 +
              绑定 + 三选一结论单;先写暂存目录,成功后整体替换,失败保留旧包与旧回执。
  receipt     回执含 run_id/时间/git/工具与输入 SHA;失败另写 *.FAILED.json,不冒充本次。
  verify      (--verify)复核审核包:哈希重算 + 结论单恰好勾一项且签署完整;未完成非零退出,
              不代签、不回写 bindings。

退出码:0=构建完成(渲染被拒是本管线的正常状态) 1=审核未完成 3=拒收/构建失败。
渲染成功与否只能由 check_certificate 与实际渲染入口证明,本管线不提供该证据。
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUBMISSION = HERE.parent
ROOT = HERE.parents[4]


@dataclass(frozen=True)
class Paths:
    root: Path
    cand: Path
    bind: Path
    template: Path
    records: Path
    out: Path


def _default_paths() -> Paths:
    return Paths(
        root=ROOT,
        cand=SUBMISSION / "presentation-candidates",
        bind=SUBMISSION / "presentation-candidates/presentation-bindings.jsonl",
        template=SUBMISSION / "template-fix-candidate/render_templates_v4_candidate.py",
        records=ROOT / "archives/reviews/codex-supervision"
                      "/2026-10-17-first-batch-exact-math-review/candidate-v2/records.jsonl",
        out=HERE / "runs",
    )


DEFAULT = _default_paths()

REQUIRED_ROW = {
    "sample_id": str,
    "corrected_record_sha256": str,
    "scene_sha256": str,
    "template_version": str,
    "template_sha256": str,
    "plan_sha256": str,
    "plan_rows": int,
    "plan_pages_provisional": int,
    "coverage_ok": bool,
    "layout_status": str,
    "geometry_objects": list,
    "render_verdict": str,
    "visual_verdict": str,
}
SID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}")
WRAPPER_HEADER = (
    '"""Auto-generated runnable shell for a text-only presentation candidate.\n\n'
    "The fragment below is authored; this shell only adds the Manim import and the\n"
    "Scene subclass so `manim -ql scene_runnable.py Candidate` can import it.\n"
    "This file has never been executed by the pipeline.\n"
    '"""\n'
    "from manim import *  # noqa: F401,F403\n\n\n"
    "class Candidate(Scene):\n"
    "    def construct(self):\n"
)
LIMITS = [
    "text-only candidate: 0 geometric primitives, 画面忠实度(F) 无证据",
    "rendered=false: R/E 指标未取证,渲染须走 check_certificate + 获准入口",
    "layout UNVERIFIED_REQUIRES_NATIVE_MEASUREMENTS: 分页为临时预算,非原生测量",
    "结论单待审核方填写;verify 只证明已签署,不证明审核正确",
]


class Refusal(RuntimeError):
    """输入或证据不满足合同,拒收。"""


# ---------------------------------------------------------------- 基础工具

def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(Path(path).read_bytes())


def canonical_plan_bytes(plan: dict) -> bytes:
    return json.dumps(plan, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def git_head(root: Path) -> str | None:
    try:
        cp = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                            capture_output=True, text=True, timeout=20)
        return cp.stdout.strip() or None if cp.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def load_template(path: Path) -> object:
    if not path.is_file():
        raise Refusal(f"template missing: {path}")
    spec = importlib.util.spec_from_file_location("_presentation_template_v3", path)
    if spec is None or spec.loader is None:
        raise Refusal(f"template cannot be loaded: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------- generate

def load_bindings(path: Path) -> tuple[list[dict], str]:
    if not path.is_file():
        raise Refusal(f"bindings missing: {path}")
    raw = path.read_text(encoding="utf-8")
    rows = []
    for lineno, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise Refusal(f"bindings line {lineno} is not JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise Refusal(f"bindings line {lineno} is not an object")
        for key, kind in REQUIRED_ROW.items():
            if key not in row:
                raise Refusal(f"bindings line {lineno} missing key {key}")
            value = row[key]
            ok = isinstance(value, bool) if kind is bool else type(value) is kind
            if not ok:
                raise Refusal(
                    f"bindings line {lineno} key {key} has type {type(value).__name__}")
        if not SID_RE.fullmatch(row["sample_id"]):
            raise Refusal(f"bindings line {lineno} illegal sample_id {row['sample_id']!r}")
        rows.append(row)
    if not rows:
        raise Refusal("bindings has no rows")
    return rows, sha_bytes(path.read_bytes())


def load_records(path: Path) -> dict[str, tuple[str, dict]]:
    if not path.is_file():
        raise Refusal(f"records missing: {path}")
    out: dict[str, tuple[str, dict]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        sid = rec.get("id") or rec.get("sample_id")
        if not isinstance(sid, str):
            raise Refusal("record without string id")
        out[sid] = (line, rec)
    if not out:
        raise Refusal("records is empty")
    return out


def wrap_fragment(fragment: str) -> str:
    return WRAPPER_HEADER + fragment


def check_wrapper(source: str, label: str) -> None:
    import ast
    try:
        tree = ast.parse(source, filename=label)
    except SyntaxError as exc:
        raise Refusal(f"{label}: wrapper does not parse: {exc.msg} (line {exc.lineno})") from exc
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    if len(classes) != 1 or classes[0].name != "Candidate":
        raise Refusal(f"{label}: wrapper must define exactly one class Candidate")
    bases = [getattr(b, "id", getattr(b, "attr", "")) for b in classes[0].bases]
    if "Scene" not in bases:
        raise Refusal(f"{label}: Candidate must subclass Scene, got {bases}")
    funcs = [n for n in classes[0].body if isinstance(n, ast.FunctionDef)]
    if [f.name for f in funcs] != ["construct"]:
        raise Refusal(f"{label}: Candidate must define only construct()")
    try:
        compile(source, label, "exec")
    except SyntaxError as exc:  # pragma: no cover - ast.parse already covers
        raise Refusal(f"{label}: wrapper does not compile: {exc.msg}") from exc


def stage_generate(paths: Paths) -> dict:
    rows, bind_sha = load_bindings(paths.bind)
    records = load_records(paths.records)
    template = load_template(paths.template)
    template_sha = sha_file(paths.template)
    version = getattr(template, "TEMPLATE_VERSION", "")
    if not version:
        raise Refusal("template does not declare TEMPLATE_VERSION")

    problems: list[str] = []
    scenes = []
    for row in rows:
        sid = row["sample_id"]
        scene_path = paths.cand / "scenes" / f"{sid}.py"
        try:
            if not scene_path.is_file():
                raise Refusal(f"{sid}: scene file missing")
            disk_sha = sha_file(scene_path)
            if disk_sha != row["scene_sha256"]:
                raise Refusal(f"{sid}: scene_sha256 mismatch ({disk_sha[:12]} != {row['scene_sha256'][:12]})")
            if row["template_sha256"] != template_sha:
                raise Refusal(f"{sid}: template_sha256 mismatch (bindings stale vs current template)")
            if row["template_version"] != version:
                raise Refusal(f"{sid}: template_version mismatch")
            if sid not in records:
                raise Refusal(f"{sid}: no matching corrected record")
            raw_line, rec = records[sid]
            if sha_bytes(raw_line.encode("utf-8")) != row["corrected_record_sha256"]:
                raise Refusal(f"{sid}: corrected_record_sha256 mismatch")
            spec = rec.get("scene_spec") or {}
            sources = [rec.get("problem", ""), *(spec.get("steps") or []), rec.get("answer", "")]
            code, plan = template.scene_blocks_v2(sources[0], sources[1:-1], sources[-1])
            scene_text = scene_path.read_text(encoding="utf-8")
            if scene_text != code:
                raise Refusal(f"{sid}: scene bytes are not reproducible from template+record")
            plan_sha = sha_bytes(canonical_plan_bytes(plan))
            if plan_sha != row["plan_sha256"]:
                raise Refusal(f"{sid}: plan_sha256 mismatch")
            if len(plan["rows"]) != row["plan_rows"] or \
                    len(plan["provisional_pages"]) != row["plan_pages_provisional"]:
                raise Refusal(f"{sid}: plan row/page counts mismatch")
            if not template.coverage_ok(sources, plan):
                raise Refusal(f"{sid}: coverage_ok recomputation failed")
            if row["coverage_ok"] is not True:
                raise Refusal(f"{sid}: coverage_ok is false")
            if row["layout_status"] != plan["layout"]:
                raise Refusal(f"{sid}: layout_status mismatch")
            if row["geometry_objects"] != (spec.get("objects") or []):
                raise Refusal(f"{sid}: geometry_objects mismatch with corrected record")
            if row["render_verdict"] != "PENDING_REVIEW" or row["visual_verdict"] != "PENDING_REVIEW":
                raise Refusal(f"{sid}: verdicts must stay PENDING_REVIEW in a candidate")

            wrapper = wrap_fragment(scene_text)
            check_wrapper(wrapper, f"{sid}/scene_runnable.py")
            scenes.append({
                "sample_id": sid,
                "record": rec,
                "plan": plan,
                "plan_sha256": plan_sha,
                "scene_sha256": disk_sha,
                "runnable_sha256": sha_bytes(wrapper.encode("utf-8")),
                "wrapper": wrapper,
            })
        except Refusal as exc:
            problems.append(str(exc))
    if problems:
        raise Refusal("generate refused:\n  " + "\n  ".join(problems))
    return {
        "rows": rows,
        "scenes": scenes,
        "bindings_sha256": bind_sha,
        "records_sha256": sha_file(paths.records),
        "template_sha256": template_sha,
        "template_version": version,
    }


# ---------------------------------------------------------------- render gate

def stage_render(paths: Paths, gate=None) -> dict:
    result = {"rendered": False, "source": "src/animtrain/sandbox_execution.py::check_certificate",
              "certificate": str(paths.root / "data/execution_evidence.json")}
    if gate is not None:
        try:
            ok, message = gate()
        except Exception as exc:  # pragma: no cover
            result.update(state="REFUSED_GATE_ERROR", message=f"gate raised: {exc}")
            return result
        result["state"] = "CERTIFICATE_VALID_RENDER_NOT_RUN" if ok else "REFUSED"
        result["message"] = message
        return result
    sys.path.insert(0, str(paths.root / "src"))
    try:
        from animtrain import sandbox_execution  # noqa: PLC0415
    except Exception as exc:  # pragma: no cover - 环境缺件时 fail-closed
        result.update(state="REFUSED_GATE_UNAVAILABLE", message=f"cannot import gate: {exc}")
        return result
    try:
        ok, message = sandbox_execution.check_certificate()
    except Exception as exc:  # pragma: no cover
        result.update(state="REFUSED_GATE_ERROR", message=f"gate raised: {exc}")
        return result
    result["state"] = "CERTIFICATE_VALID_RENDER_NOT_RUN" if ok else "REFUSED"
    result["message"] = message
    return result


# ---------------------------------------------------------------- review pack

def conclusion_sheet(sid: str, render_state: str) -> str:
    return (
        "# 目视审核结论单\n\n"
        f"- sample_id: {sid}\n"
        f"- 渲染状态: {render_state}(本管线未渲染)\n"
        "- 原题: problem.md\n"
        "- 答案: answer.md\n"
        "- 场景片段: scene.py\n"
        "- 可运行包壳: scene_runnable.py(未执行)\n"
        "- 分页计划: plan.json(layout 未原生测量)\n"
        "- 审核结论(三选一,待审核方填写):\n"
        "  - [ ] 过\n"
        "  - [ ] 不过\n"
        "  - [ ] 要改\n"
        "- 修改意见(若要改,必填):\n"
        "- 审核人:\n"
        "- 时间:\n"
    )


def stage_review_pack(paths: Paths, generated: dict, render: dict, staging: Path) -> dict:
    pack_root = staging / "review-packs"
    pack_root.mkdir(parents=True, exist_ok=True)
    rows_by_sid = {r["sample_id"]: r for r in generated["rows"]}
    packs = []
    for item in generated["scenes"]:
        sid = item["sample_id"]
        rec = item["record"]
        row = rows_by_sid[sid]
        d = pack_root / sid
        d.mkdir(parents=True, exist_ok=False)
        shutil.copyfile(paths.cand / "scenes" / f"{sid}.py", d / "scene.py")
        write_text(d / "scene_runnable.py", item["wrapper"])
        write_text(d / "problem.md", rec.get("problem", "") + "\n")
        write_text(d / "answer.md", rec.get("answer", "") + "\n")
        write_bytes(d / "plan.json", canonical_plan_bytes(item["plan"]))
        bindings = {
            "sample_id": sid,
            "corrected_record_sha256": row["corrected_record_sha256"],
            "scene_sha256": item["scene_sha256"],
            "runnable_sha256": item["runnable_sha256"],
            "plan_sha256": item["plan_sha256"],
            "template_sha256": generated["template_sha256"],
            "template_version": generated["template_version"],
            "coverage_ok": row["coverage_ok"],
            "layout_status": row["layout_status"],
            "geometry_objects": row["geometry_objects"],
            "render_state": render["state"],
            "review_status": "PENDING",
        }
        write_text(d / "bindings.json",
                   json.dumps(bindings, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        write_text(d / "conclusion-sheet.md", conclusion_sheet(sid, render["state"]))
        packs.append({"sample_id": sid, "pack_dir": f"review-packs/{sid}"})
    return {"state": "PASS", "packs": packs}


# ---------------------------------------------------------------- verify

VERDICT_LINE = re.compile(r"^\s*-\s*\[([ xX])\]\s*(过|不过|要改)\s*$")
FIELD_LINE = re.compile(r"^\s*-\s*(审核人|时间|修改意见(?:\(若要改,必填\))?)\s*[:：]\s*(.*)$")


def parse_sheet(text: str) -> dict:
    checked = []
    fields = {}
    for line in text.splitlines():
        m = VERDICT_LINE.match(line)
        if m:
            if m.group(1).lower() == "x":
                checked.append(m.group(2))
            continue
        m = FIELD_LINE.match(line)
        if m:
            fields[m.group(1).split("(")[0]] = m.group(2).strip()
    return {"checked": checked, "fields": fields}


def verify_pack(d: Path) -> dict:
    issues = []
    bindings_path = d / "bindings.json"
    if not bindings_path.is_file():
        return {"sample_id": d.name, "status": "REVIEW_INCOMPLETE", "issues": ["bindings.json missing"]}
    b = json.loads(bindings_path.read_text(encoding="utf-8"))
    checks = {
        "scene_sha256": ("scene.py", "scene_sha256"),
        "runnable_sha256": ("scene_runnable.py", "runnable_sha256"),
        "plan_sha256": ("plan.json", "plan_sha256"),
    }
    for key, (filename, field) in checks.items():
        p = d / filename
        if not p.is_file():
            issues.append(f"{filename} missing")
        elif sha_file(p) != b.get(field):
            issues.append(f"{filename} sha mismatch")
    runnable = d / "scene_runnable.py"
    if runnable.is_file():
        try:
            check_wrapper(runnable.read_text(encoding="utf-8"), f"{d.name}/scene_runnable.py")
        except Refusal as exc:
            issues.append(str(exc))
    sheet = d / "conclusion-sheet.md"
    if not sheet.is_file():
        issues.append("conclusion-sheet.md missing")
        parsed = {"checked": [], "fields": {}}
    else:
        parsed = parse_sheet(sheet.read_text(encoding="utf-8"))
    if len(parsed["checked"]) != 1:
        issues.append(f"verdict must be exactly one of 过/不过/要改, got {parsed['checked']}")
    if not parsed["fields"].get("审核人"):
        issues.append("审核人 empty")
    if not parsed["fields"].get("时间"):
        issues.append("时间 empty")
    if parsed["checked"] == ["要改"] and not parsed["fields"].get("修改意见"):
        issues.append("要改 without 修改意见")
    return {"sample_id": d.name, "status": "REVIEW_COMPLETE" if not issues else "REVIEW_INCOMPLETE",
            "issues": issues, "verdict": parsed["checked"][0] if len(parsed["checked"]) == 1 else None}


def stage_verify(paths: Paths) -> dict:
    pack_root = paths.out / "review-packs"
    if not pack_root.is_dir():
        raise Refusal(f"review packs missing: {pack_root}")
    packs = [verify_pack(d) for d in sorted(p for p in pack_root.iterdir() if p.is_dir())]
    overall = "REVIEW_COMPLETE" if packs and all(
        p["status"] == "REVIEW_COMPLETE" for p in packs) else "REVIEW_INCOMPLETE"
    verdicts = {
        "schema": "presentation-review-verdicts-v1",
        "checked_at": now(),
        "packs": packs,
        "overall": overall,
        "note": "只证明结论单已签署且包内哈希未变,不代表审核结论正确或渲染已通过",
    }
    write_text(paths.out / "verdicts.json",
               json.dumps(verdicts, ensure_ascii=False, indent=2) + "\n")
    return verdicts


# ---------------------------------------------------------------- build

def _fail_receipt(paths: Paths, run_id: str, started: str, error: str) -> None:
    payload = {
        "schema": "presentation-pipeline-receipt-v2",
        "run_id": run_id,
        "action": "build",
        "status": "FAILED",
        "started_at": started,
        "finished_at": now(),
        "error": error,
        "note": "失败回执单独成文件;上一份 pipeline-receipt.json 未被本次运行替换",
    }
    write_text(paths.out / "pipeline-receipt.FAILED.json",
               json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def build(paths: Paths, gate=None) -> dict:
    run_id = uuid.uuid4().hex[:16]
    started = now()
    staging = paths.out / f".stage-{run_id}"
    trash = paths.out / f".trash-{run_id}"
    try:
        generated = stage_generate(paths)
        render = stage_render(paths, gate)
        staging.mkdir(parents=True, exist_ok=True)
        pack_stage = stage_review_pack(paths, generated, render, staging)
        receipt = {
            "schema": "presentation-pipeline-receipt-v2",
            "run_id": run_id,
            "action": "build",
            "status": "BUILT_PENDING_RENDER",
            "started_at": started,
            "finished_at": now(),
            "git": {"head": git_head(paths.root)},
            "pipeline": {"path": str(Path(__file__)),
                         "sha256": sha_file(Path(__file__))},
            "template": {"path": str(paths.template),
                         "version": generated["template_version"],
                         "sha256": generated["template_sha256"]},
            "inputs": {
                "bindings": {"path": str(paths.bind), "sha256": generated["bindings_sha256"]},
                "records": {"path": str(paths.records), "sha256": generated["records_sha256"]},
            },
            "stages": {
                "generate": {"state": "PASS", "samples": len(generated["scenes"]),
                             "recomputed": ["record_sha", "template_sha", "scene_bytes",
                                            "plan_sha", "coverage", "geometry_objects"]},
                "render": render,
                "review_pack": {"state": pack_stage["state"], "packs": len(pack_stage["packs"])},
            },
            "scenes": [{"sample_id": s["sample_id"], "scene_sha256": s["scene_sha256"],
                        "runnable_sha256": s["runnable_sha256"], "plan_sha256": s["plan_sha256"]}
                       for s in generated["scenes"]],
            "limits": LIMITS,
            "note": "渲染被拒是本管线预期状态;本回执不构成 R/E/M/F 任一指标证据",
        }
        write_text(staging / "pipeline-receipt.json",
                   json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
        if not (staging / "review-packs").is_dir():
            raise Refusal("staging review-packs missing")
        moved = False
        final = paths.out / "review-packs"
        if final.exists():
            final.rename(trash)
            moved = True
        try:
            (staging / "review-packs").rename(final)
            os.replace(staging / "pipeline-receipt.json", paths.out / "pipeline-receipt.json")
        except Exception:
            if moved and not final.exists():
                trash.rename(final)
            raise
        shutil.rmtree(trash, ignore_errors=True)
        shutil.rmtree(staging, ignore_errors=True)
        return receipt
    except Exception as exc:
        shutil.rmtree(staging, ignore_errors=True)
        _fail_receipt(paths, run_id, started, f"{type(exc).__name__}: {exc}")
        raise


# ---------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="presentation pipeline harness v2")
    parser.add_argument("--verify", action="store_true", help="复核审核包结论单,未完成返回 1")
    parser.add_argument("--out", default="", help="覆盖 runs 目录(测试用)")
    args = parser.parse_args(argv)
    paths = DEFAULT
    if args.out:
        paths = Paths(**{**paths.__dict__, "out": Path(args.out).resolve()})
    paths.out.mkdir(parents=True, exist_ok=True)
    try:
        if args.verify:
            verdicts = stage_verify(paths)
            print(json.dumps({"overall": verdicts["overall"],
                              "packs": len(verdicts["packs"])}, ensure_ascii=False))
            return 0 if verdicts["overall"] == "REVIEW_COMPLETE" else 1
        receipt = build(paths)
        print(json.dumps({"status": receipt["status"], "run_id": receipt["run_id"],
                          "render": receipt["stages"]["render"]["state"],
                          "packs": receipt["stages"]["review_pack"]["packs"]},
                         ensure_ascii=False))
        return 0
    except Refusal as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 3
    except Exception as exc:  # pragma: no cover
        print(f"FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
