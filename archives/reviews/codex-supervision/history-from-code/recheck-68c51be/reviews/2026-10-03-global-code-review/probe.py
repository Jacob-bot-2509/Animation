"""Read-only project audit; destructive probes use disposable synthetic files."""
import contextlib, hashlib, importlib.util, io, json, pathlib, random, string, subprocess, sys, tempfile
from unittest.mock import patch
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
from animtrain.dataset_intake import check_intake_file, check_record, convert_array_to_jsonl, intake_report
from animtrain.fields import check_jsonl
from animtrain.freeze import check_frozen, freeze_set
from animtrain.manifest import Entry, Manifest, sha256_file
from animtrain.near_dup import jaccard, shingles
from animtrain.preflight import run_preflight
from animtrain.validate import validate_manifest
from tests.test_dataset_intake import clean_record

def load_cli(name):
    spec = importlib.util.spec_from_file_location("review_" + name, ROOT / "tools" / (name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def cli_result(mod, argv):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        try:
            code = mod.main(argv)
            result = {"exit_code": code}
        except (Exception, SystemExit) as exc:
            result = {"exception": type(exc).__name__, "detail": str(exc)}
    return {**result, "stdout": output.getvalue()}

def manifest_for(d, paths):
    return Manifest(name="synthetic-global-review", entries=[
        Entry(path=p.name, sha256=sha256_file(p), size=p.stat().st_size,
              source="synthetic-review", license="internal-generated", split="train")
        for p in paths])

def run():
    r = {"head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()}
    actual = sorted((ROOT / "data/v1/raw").glob("*.jsonl"))
    r["real_input_hashes"] = {p.relative_to(ROOT).as_posix(): sha256_file(p) for p in actual}
    r["source_hashes"] = {p.relative_to(ROOT).as_posix(): sha256_file(p)
        for folder in ["src/animtrain", "tools"] for p in sorted((ROOT / folder).glob("*.py"))
        if p.name != "dataset_audit.py"}
    intake = load_cli("dataset_intake")
    data_cli = load_cli("data_check")
    fields_cli = load_cli("check_fields")
    r["G1_entry_disagreement"] = {}
    with tempfile.TemporaryDirectory(prefix="codex-global-review-") as tmp:
        d = pathlib.Path(tmp)
        cases = {
            "train.txt": "not a dataset",
            "empty.jsonl": "",
            "idonly.jsonl": '{"id":"one"}\n',
            "duplicate.jsonl": "\n".join(json.dumps(clean_record(id="one", problem=p))
                for p in ["problem alpha", "problem beta"]) + "\n",
        }
        for name, text in cases.items():
            p = d / name
            p.write_text(text, encoding="utf-8")
            m = manifest_for(d, [p])
            mp = d / "manifest.json"
            m.save(mp)
            r["G1_entry_disagreement"][name] = {
                "core_manifest": validate_manifest(m, d),
                "data_check_cli": cli_result(data_cli, ["--manifest", str(mp)]),
                "intake": check_intake_file(p),
                "fields": check_jsonl(p) if p.suffix == ".jsonl" else None,
            }
            if name == "empty.jsonl":
                r["G1_entry_disagreement"][name]["fields_cli"] = cli_result(fields_cli, ["--jsonl", str(p)])
        for name, files in {
            "same_file": ["one.jsonl"],
            "same_split_cross_file": ["left.jsonl", "right.jsonl"],
        }.items():
            paths = []
            for filename in files:
                p = d / filename
                if name == "same_file":
                    rows = [clean_record(id="dup", problem="alpha"), clean_record(id="dup", problem="beta")]
                else:
                    rows = [clean_record(id="dup", problem=filename)]
                p.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
                paths.append(p)
            r["G1_entry_disagreement"][name] = {
                "core_manifest": validate_manifest(manifest_for(d, paths), d),
                "intake": intake_report(paths),
            }

        r["G2_frozen_overwrite"] = {}
        for case in ["convert", "report_data", "report_lock"]:
            folder = d / case
            folder.mkdir()
            target = folder / "eval.jsonl"
            target.write_text(json.dumps(clean_record(id="original")) + "\n", encoding="utf-8")
            lock = folder / "eval.lock.json"
            freeze_set([target.resolve()], lock, meta={"synthetic": True})
            source = folder / "input.jsonl"
            source.write_text(json.dumps(clean_record(id="input")) + "\n", encoding="utf-8")
            initial = {"target": target.read_bytes(), "lock": lock.read_bytes(), "source": source.read_bytes()}
            if case == "convert":
                array = folder / "input.json"
                array.write_text(json.dumps([clean_record(id="replacement")]), encoding="utf-8")
                try:
                    outcome = convert_array_to_jsonl(array, target, force=True)
                except Exception as exc:
                    outcome = {"exception": type(exc).__name__, "detail": str(exc)}
            else:
                out = lock if case == "report_lock" else target
                outcome = cli_result(intake, ["report", str(source), "--out", str(out), "--force"])
            r["G2_frozen_overwrite"][case] = {
                "outcome": outcome,
                "target_changed": target.read_bytes() != initial["target"],
                "lock_changed": lock.read_bytes() != initial["lock"],
                "source_unchanged": source.read_bytes() == initial["source"],
                "post_lock_problems": check_frozen(lock),
            }

        rng = random.Random(7)
        texts = []
        entries = []
        paths = []
        for role in ["train", "eval"]:
            row = clean_record(id=role, problem="Compute 2 + 2.", solution="2 + 2 = 4.", answer="4",
                function_family="".join(rng.choices(string.ascii_letters, k=3000)))
            p = d / ("same_task_" + role + ".jsonl")
            line = json.dumps(row)
            p.write_text(line + "\n", encoding="utf-8")
            paths.append(p)
            texts.append(line)
            entries.append(Entry(path=p.name, sha256=sha256_file(p), size=p.stat().st_size,
                source="synthetic-review", license="internal-generated", split=role))
        r["G3_same_task_different_metadata"] = {
            "same_task_fields": ["problem", "solution", "answer", "scene_spec"],
            "different_fields": ["id", "function_family"],
            "core_manifest": validate_manifest(Manifest(name="synthetic", entries=entries), d),
            "intake": intake_report(paths),
            "whole_json_jaccard": jaccard(shingles(texts[0]), shingles(texts[1])),
        }

        r["G4_field_shapes"] = []
        for overrides in [
            {"scene_spec": {"objects": [], "steps": []}},
            {"scene_spec": {"objects": [None], "steps": [False]}},
            {"category": ["wrong"], "sub_category": {"x": 1}, "source": {"bad": 1},
             "function_family": True, "visual_style": 17, "efficiency_tags": "not-a-list"},
        ]:
            problems, quarantines = check_record(clean_record(**overrides), 1)
            r["G4_field_shapes"].append({"case": overrides, "problems": problems, "quarantines": quarantines})
    with patch("animtrain.preflight.check_gpu", return_value=(True, "synthetic GPU")), \
         patch("animtrain.preflight.check_model_dir", return_value=(True, "synthetic model")):
        r["known_B2_core_ready_missing_assets"] = run_preflight(
            pathlib.Path("synthetic-model"), ready=True,
            extra_checks=[("data_manifest", (True, "synthetic data")), ("run_snapshot", (True, "synthetic record"))])
    mp = ROOT / "data/v1/manifest.json"
    r["current_real_intake"] = intake_report(actual)
    r["current_real_manifest"] = validate_manifest(Manifest.load(mp), mp.parent)
    r["real_inputs_unchanged"] = {
        p.relative_to(ROOT).as_posix(): sha256_file(p) == r["real_input_hashes"][p.relative_to(ROOT).as_posix()]
        for p in actual}
    r["source_unchanged"] = {
        name: sha256_file(ROOT / name) == digest for name, digest in r["source_hashes"].items()}
    r["baseline_tests"] = {"passed": 186, "subtests": 29, "seconds": 6.35}
    return r

if __name__ == "__main__":
    result = run()
    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).with_name("results.json")
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "head": result["head"],
        "G1_manifest_passes": {k: v["core_manifest"]["ok"] for k, v in result["G1_entry_disagreement"].items()},
        "G2_changed": {k: {"data": v["target_changed"], "lock": v["lock_changed"]} for k, v in result["G2_frozen_overwrite"].items()},
        "G3_passes": result["G3_same_task_different_metadata"]["core_manifest"]["ok"],
        "G3_jaccard": result["G3_same_task_different_metadata"]["whole_json_jaccard"],
        "real_n": result["current_real_intake"]["n_records"],
        "real_manifest_ok": result["current_real_manifest"]["ok"],
        "real_inputs_unchanged": all(result["real_inputs_unchanged"].values()),
        "source_unchanged": all(result["source_unchanged"].values()),
    }, ensure_ascii=False, indent=2))
