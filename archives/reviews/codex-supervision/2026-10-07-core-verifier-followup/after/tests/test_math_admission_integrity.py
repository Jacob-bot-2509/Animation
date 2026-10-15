import importlib.util
import json
import shutil
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("admission_verify", ROOT / "tools/verify_math_admission_v1.py")
av = importlib.util.module_from_spec(spec); spec.loader.exec_module(av)
b = av.b
v = av.v
V2 = ROOT / "reviews/codex-supervision/2026-10-07-core-verifier-followup/admission-v2"


def test_native_scene_preserves_latex():
    scene = {"objects": [r"$\frac{1}{2}$"], "steps": [r"$S_N(\pi)=0$"]}
    b.validate_scene(scene)
    assert "\\" in scene["objects"][0]


@pytest.mark.parametrize("scene", [
    "{'objects':['x'],'steps':['y']}",
    {"objects": [], "steps": ["ok"]},
    {"objects": ["ok"], "steps": ["\f rac"]},
    {"objects": ["ok"], "steps": [r"$\frac{1}{2$"]},
    {"objects": ["ok"], "steps": ["$0.5$"]},
    {"objects": ["ok"], "steps": [r"$\pi\approx4m/n$"]},
    {"objects": ["ok"], "steps": [None]},
])
def test_repr_control_approximation_and_malformed_scene_fail(scene):
    with pytest.raises(v.VerificationError):
        b.validate_scene(scene)


def test_existing_output_directory_is_not_rebuilt(tmp_path):
    out = tmp_path / "reviews/existing"
    out.mkdir(parents=True)
    marker = out / "original.json"
    marker.write_bytes(b"original evidence")
    with pytest.raises(FileExistsError):
        b.build(tmp_path, out)
    assert marker.read_bytes() == b"original evidence"


@pytest.mark.parametrize("relative", ["../outside", "outside"])
def test_builder_stays_in_review_root(tmp_path, relative):
    with pytest.raises(v.VerificationError):
        b.build(tmp_path, Path(relative))


def test_30_source_reconstruction_is_complete():
    patches, bindings = b.math.load_verified_math()
    assert len(patches) == 30 and len(bindings) == 5
    assert v.correction_counts(patches)["by_group"] == {"train": 9, "eval": 9, "test": 12}


def test_input_failure_is_not_print_only(monkeypatch):
    monkeypatch.setattr(b.math.v, "verify", lambda root: {"overall": "FAIL", "checks": {"AB": "MISMATCH"}})
    with pytest.raises(v.VerificationError):
        b.math.load_verified_math(ROOT)


def test_original_v1_is_not_accepted_as_native_corrected_version():
    with pytest.raises(v.VerificationError, match="legacy"):
        av.verify_admission(ROOT, Path("reviews/2026-10-07-math-admission-v1"))


def copied_package(tmp_path):
    dest = tmp_path / "candidate"
    shutil.copytree(V2, dest)
    manifest = json.loads((dest / "admission-manifest.json").read_text(encoding="utf-8"))
    for item in manifest["items"]:
        original = ROOT / item["path"]
        copied = dest / original.relative_to(V2)
        item["path"] = copied.relative_to(ROOT).as_posix()
    (dest / "admission-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    return dest


def refresh_manifest(dest):
    manifest_path = dest / "admission-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for item in manifest["items"]:
        raw = (ROOT / item["path"]).read_bytes()
        item["raw_sha256"] = v.digest(raw)
        item["bytes"] = len(raw)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")


@pytest.mark.parametrize("fault", ["duplicate_scene", "scene_repr", "record_sha",
                                   "unlisted_line_change", "false_render", "empty_manifest"])
def test_fresh_hashes_do_not_hide_structural_or_scope_corruption(tmp_path, fault):
    dest = copied_package(tmp_path)
    if fault in ("duplicate_scene", "scene_repr"):
        path = dest / "scene-updates-candidate.jsonl"
        rows = v.read_jsonl(path)
        if fault == "duplicate_scene":
            rows[1]["id"] = rows[0]["id"]
        else:
            rows[0]["scene_spec"] = str(rows[0]["scene_spec"])
        path.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows)+"\n", encoding="utf-8")
    elif fault == "record_sha":
        path = dest / "record-bindings.jsonl"
        rows = v.read_jsonl(path)
        rows[0]["final_record_dense_sha256"] = "0" * 64
        path.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows)+"\n", encoding="utf-8")
    elif fault == "unlisted_line_change":
        path = dest / "admission-sources/data/v2/eval/dataset_eval.jsonl"
        lines = path.read_bytes().splitlines(keepends=True)
        row = json.loads(lines[0].decode("utf-8-sig"))
        row["solution"] = "unauthorized change"
        lines[0] = json.dumps(row, ensure_ascii=False).encode("utf-8")+b"\n"
        path.write_bytes(b"".join(lines))
    elif fault == "false_render":
        path = dest / "scene-binding-audit.json"
        audit = json.loads(path.read_text(encoding="utf-8"))
        audit["native_render_performed"] = True
        path.write_text(json.dumps(audit, ensure_ascii=False), encoding="utf-8")
    else:
        path = dest / "admission-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["items"] = []
        path.write_text(json.dumps(manifest), encoding="utf-8")
    refresh_manifest(dest)
    with pytest.raises(v.VerificationError):
        av.verify_admission(ROOT, dest)


def test_live_v2_complete_reconstruction_and_no_release():
    result = av.verify_admission(ROOT, V2)
    assert result["mathematical_records"] == 30
    assert result["updated_native_scenes"] == 17
    assert result["retained_native_scenes"] == 13
    assert result["full_source_records_preserved"] == 489
    assert result["native_render"] == "UNVERIFIED"
    assert result["active_admission"] == "PENDING"
    assert result["PASS_CORE_SCOPE_issued"] is False


def test_scene_content_scoped_exact_checks():
    from fractions import Fraction as F
    import sympy as s
    regions = [F(2,5),F(1,5),F(1,5),F(1,5)]
    assert sum(regions) == 1
    assert regions[1]/(regions[1]+regions[2]) == F(1,2)
    assert regions[1]/(regions[0]+regions[1]) == F(1,3)
    t = s.symbols("t", nonnegative=True)
    assert s.simplify(s.exp(-(500+t)/1000)/s.exp(-s.Rational(1,2))-s.exp(-t/1000)) == 0
    n = s.symbols("n", integer=True, positive=True)
    assert s.sin(n*s.pi) == 0
    assert s.zeros(2).rank() == 0
