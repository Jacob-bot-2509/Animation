"""Independent screening audit. Mocks only: no model load/inference/training."""
from __future__ import annotations
import contextlib
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

inference = load("screening_probe")
qlora = load("screening_qlora_probe")
provenance = load("model_provenance")
source_paths = ["tools/screening_probe.py", "tools/screening_qlora_probe.py",
                "tools/model_provenance.py", "MODEL_SHOOTOUT_PLAN.md"]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
start_hashes = {p: sha(ROOT / p) for p in source_paths}
evidence = {"head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "source_hashes": start_hashes, "execution": "mock-only; local tokenizer read; no model execution"}

valid = json.dumps({"scene_spec": {"objects": ["axis"], "steps": ["draw"]}})
evidence["parser"] = []
for name, output in [
    ("final_json", valid),
    ("thinking_has_json_then_valid_final", '<think>{"scratch":1}</think>\n' + valid),
    ("thinking_only_no_final_answer", "<think>" + valid + "</think>"),
]:
    parsed = inference.extract_scene_spec(output)
    evidence["parser"].append({"case": name, "parsed": parsed is not None,
                              "clean": parsed is not None and not inference.check_spec(parsed)})

rows = inference.load_samples()
evidence["sample_selection"] = {
    "count": len(rows), "ids": [r["id"] for r in rows],
    "sub_categories": {c: [r.get("sub_category") for r in rows if r["category"] == c] for c in inference.SAMPLES},
}
try:
    from tokenizers import Tokenizer
    lengths = {}
    configs = {}
    for directory in sorted((ROOT / ".models").iterdir()):
        p = directory / "tokenizer.json"
        if p.is_file():
            tokenizer = Tokenizer.from_file(str(p))
            lengths[directory.name] = {
                str(n): len(tokenizer.encode("\u6570\u5b66\u52a8\u753b\u89c4\u5212 " * (n // 6)).ids)
                for n in (1024, 2048, 4096)
            }
        p = directory / "generation_config.json"
        if p.is_file():
            configs[directory.name] = json.loads(p.read_text(encoding="utf-8"))
    evidence["actual_synthetic_token_lengths"] = lengths
    evidence["local_generation_defaults"] = configs
except ImportError:
    evidence["tokenizer_read"] = "unavailable; no dependencies installed"

calls = []
class Tensor:
    def __init__(self, length=12, rank=2):
        self.shape = (1, length) if rank == 2 else (length,)
    def __getitem__(self, key):
        return Tensor(self.shape[-1], rank=1)
    def clone(self):
        return self

class Batch(dict):
    def to(self, device):
        return self

class TokenizerMock:
    eos_token_id = 99
    @classmethod
    def from_pretrained(cls, *a, **kw):
        return cls()
    def __call__(self, text, **kw):
        return Batch(input_ids=Tensor(max(2, len(text)//2)))
    def apply_chat_template(self, messages, **kwargs):
        calls.append(("chat_template", kwargs))
        return "prompt"
    def decode(self, *a, **kw):
        return valid + " " * 300

class ModelMock:
    device = "cuda:0"
    @classmethod
    def from_pretrained(cls, *a, **kw):
        calls.append(("model_load", kw))
        return cls()
    def generate(self, **kw):
        calls.append(("generate", {k:v for k,v in kw.items() if k != "input_ids"}))
        return Tensor(kw["input_ids"].shape[-1] + 5)
    def gradient_checkpointing_enable(self): pass
    def enable_input_require_grads(self): pass
    def parameters(self): return []
    def train(self): pass
    def __call__(self, **kwargs):
        calls.append(("forward_tokens", kwargs["input_ids"].shape[-1]))
        return SimpleNamespace(loss=SimpleNamespace(
            backward=lambda: calls.append(("backward", True)), item=lambda: 1.0))
    def save_pretrained(self, directory):
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "adapter_model.safetensors").write_bytes(b"synthetic mock adapter only")

class OptimizerMock:
    def __init__(self, *a, **kw): pass
    def step(self): calls.append(("optimizer_step", True))
    def zero_grad(self): pass

fake_torch = SimpleNamespace(
    bfloat16="bf16", no_grad=contextlib.nullcontext,
    manual_seed=lambda n: calls.append(("seed", n)),
    cuda=SimpleNamespace(max_memory_allocated=lambda: 123,
                         reset_peak_memory_stats=lambda: calls.append(("reset_peak", True)),
                         synchronize=lambda: calls.append(("synchronize", True))),
    optim=SimpleNamespace(AdamW=OptimizerMock))
fake_transformers = SimpleNamespace(
    AutoTokenizer=TokenizerMock, AutoModelForCausalLM=ModelMock,
    BitsAndBytesConfig=lambda **kw: kw,
    set_seed=lambda n: calls.append(("seed", n)))
fake_peft = SimpleNamespace(LoraConfig=lambda **kw: kw, get_peft_model=lambda model, conf: model)

with tempfile.TemporaryDirectory(prefix="screening-audit-") as td:
    temp = Path(td)
    with patch.dict(sys.modules, torch=fake_torch, transformers=fake_transformers, peft=fake_peft):
        with patch.object(inference, "ROOT", temp), patch.object(inference, "load_samples", return_value=[rows[0]]):
            for thinking in (False, True):
                calls.clear()
                with contextlib.redirect_stdout(io.StringIO()):
                    rc = inference.main(["--model-dir", "synthetic-model", "--tag", "mock"] +
                                        (["--thinking"] if thinking else []))
                suffix = "-thinking" if thinking else ""
                path = temp / "outputs/screening-tmp/inference" / ("mock" + suffix + ".jsonl")
                saved = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
                evidence["inference_" + str(thinking)] = {
                    "rc": rc, "calls": list(calls), "saved_fields": sorted(saved),
                    "saved_preview_length": len(saved["output_preview"]),
                    "full_output_stored": "output" in saved or "output_text" in saved}
            calls.clear()
            with contextlib.redirect_stdout(io.StringIO()):
                inference.main(["--model-dir", "synthetic-model", "--tag", "../escaped"])
            evidence["tag_escape"] = {
                "outside_inference_directory": (temp / "outputs/screening-tmp/escaped.jsonl").is_file()}
            with contextlib.redirect_stdout(io.StringIO()):
                inference.main(["--model-dir", "synthetic-model", "--tag", "mock", "--max-new-tokens", "7"])
            summary = json.loads((temp / "outputs/screening-tmp/inference/mock.summary.json").read_text())
            evidence["inference_same_tag_rerun"] = {
                "overwrites_without_force": True, "generation_settings_stored": "max_new_tokens" in summary}
        with patch.object(qlora, "ROOT", temp):
            qcalls = []
            for length in (2048, 4096):
                calls.clear()
                with contextlib.redirect_stdout(io.StringIO()):
                    qlora.main(["--model-dir", "synthetic-model", "--tag", "mock",
                                "--seq-len", str(length), "--steps", "1"])
                qcalls.append({"requested":length, "calls":list(calls)})
            summaries = list((temp / "outputs/screening-tmp/qlora-probes").glob("*.summary.json"))
            evidence["qlora"] = {
                "runs": qcalls, "surviving_summary_files": len(summaries),
                "surviving_seq_len": json.loads(summaries[0].read_text())["seq_len"],
                "checkpoint_dirs": [p.name for p in summaries[0].parent.glob("*-ckpt")]}

    partial = temp / "partial-model"
    partial.mkdir()
    (partial / "config.json").write_text("{}", encoding="utf-8")
    # Git not a model repo: subprocess returns empty, avoiding external commands.
    with patch.object(provenance.subprocess, "run", return_value=SimpleNamespace(returncode=1, stdout="")):
        with contextlib.redirect_stdout(io.StringIO()):
            rc = provenance.main(["--model-dir", str(partial), "--source", "synthetic://model"])
    info = json.loads((partial / "PROVENANCE.json").read_text())
    evidence["provenance_no_weights"] = {"rc":rc, "weight_files":info["weight_files"]}

    pointer = partial / "model.safetensors"
    pointer.write_text("version https://git-lfs.github.com/spec/v1\noid sha256:" + "0"*64 + "\nsize 999\n")
    with patch.object(provenance.subprocess, "run", return_value=SimpleNamespace(returncode=1, stdout="")):
        with contextlib.redirect_stdout(io.StringIO()):
            rc = provenance.main(["--model-dir", str(partial), "--source", "synthetic://model", "--force"])
    info = json.loads((partial / "PROVENANCE.json").read_text())
    evidence["provenance_lfs_pointer"] = {"rc":rc, "weight_files":info["weight_files"]}

    nested = ROOT / "reviews/2026-10-03-shootout-review/synthetic-non-model-repo"
    nested.mkdir(exist_ok=True)
    try:
        (nested / "config.json").write_text("{}", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            rc = provenance.main(["--model-dir", str(nested), "--source", "synthetic://model"])
        info = json.loads((nested / "PROVENANCE.json").read_text())
        evidence["provenance_parent_git"] = {"rc":rc,"reported_commit":info["git_commit"],
                                           "project_commit":evidence["head"]}
    finally:
        for name in ("config.json", "PROVENANCE.json"):
            (nested / name).unlink(missing_ok=True)
        nested.rmdir()

evidence["source_unchanged_during_probe"] = start_hashes == {p:sha(ROOT/p) for p in source_paths}
(HERE / "results.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(evidence, ensure_ascii=False, indent=2, default=str))
