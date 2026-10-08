"""Synthetic composite-ID asset coverage counterexample; no rendering/training."""
import copy, hashlib, json, sys, tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/"src"))
from animtrain.preflight import check_asset_evidence
from animtrain.manifest import Manifest
from animtrain.validate import validate_manifest
with tempfile.TemporaryDirectory(prefix="prep-asset-audit-") as folder:
    folder=Path(folder)
    rows=[json.loads(x) for x in (root/"data/v1/raw/dataset_calc.jsonl").read_text(encoding="utf-8").splitlines()[:2]]
    rows[1].pop("id")
    rows[1].update(problem_id="independent-p2",solution_id="solution-1",method="synthetic-method")
    lines=[json.dumps(x,ensure_ascii=False) for x in rows]
    path=folder/"samples.jsonl"
    path.write_text("\n".join(lines)+"\n",encoding="utf-8")
    manifest=json.loads((root/"data/v1/manifest-train.json").read_text(encoding="utf-8"))
    entry=copy.deepcopy(manifest["entries"][0])
    entry.update(path="samples.jsonl",sha256=hashlib.sha256(path.read_bytes()).hexdigest(),size=path.stat().st_size)
    manifest["entries"]=[entry]
    mp=folder/"manifest.json"
    mp.write_text(json.dumps(manifest,ensure_ascii=False),encoding="utf-8")
    (folder/"scene.json").write_bytes(b"{}")
    evidence={"manifest_sha256":hashlib.sha256(mp.read_bytes()).hexdigest(),
              "n_total_records":1,"n_verified_assets":1,
              "records":{rows[0]["id"]:{"input_sha256":hashlib.sha256(lines[0].encode("utf-8")).hexdigest(),
                "output":{"path":"scene.json","sha256":hashlib.sha256(b"{}").hexdigest(),"size":2},
                "math":"verified","render":"rendered"}}}
    (folder/"asset_evidence.json").write_text(json.dumps(evidence),encoding="utf-8")
    observed={"actual_samples":2,"evidence_samples":1,
              "manifest_validation":validate_manifest(Manifest.load(mp),mp.parent),
              "asset_check":check_asset_evidence(mp)}
    print(json.dumps(observed,ensure_ascii=False,indent=2))
