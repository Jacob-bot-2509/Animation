"""测量训练/评测行 token 长度分布(驱动 max_seq_length 与 epochs 定案)。"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

PROMPT_TMPL = (
    "你是数学动画规划师。根据题目与解法,输出动画规划 JSON(scene_spec),"
    "格式:{{\"objects\": [\"...\"], \"steps\": [\"...\"]}}。\n"
    "要求:objects/steps 均为非空字符串列表;公式用 $...$ 包裹;"
    "steps 覆盖解法全部关键推理步骤;只输出 JSON,不要解释。\n"
    "题目:{problem}\n解法({method}):{solution}\n")


def load_rows(manifest: Path, split: str) -> list[dict]:
    m = json.loads(manifest.read_text(encoding="utf-8"))
    rows = []
    for e in m["entries"]:
        if e["split"] != split:
            continue
        p = (manifest.parent / e["path"]).resolve()
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main() -> int:
    from transformers import AutoTokenizer
    manifest = ROOT / "data/manifest.json"
    tok = AutoTokenizer.from_pretrained(str(ROOT / ".models/qwen3-4b"))
    report = {}
    for split in ("train", "eval", "test"):
        rows = load_rows(manifest, split)
        lens = []
        ok_target = 0
        for r in rows:
            spec = r.get("scene_spec")
            if isinstance(spec, dict) and all(
                isinstance(spec.get(k), list) and spec[k] and
                all(isinstance(v, str) and v.strip() for v in spec[k])
                for k in ("objects", "steps")):
                ok_target += 1
            prompt = PROMPT_TMPL.format(problem=r.get("problem", ""),
                                        solution=r.get("solution", ""),
                                        method=r.get("method", "常规解法"))
            target = json.dumps(spec, ensure_ascii=False,
                                separators=(",", ":")) if ok_target == 0 or spec else ""
            user = [{"role": "user", "content": prompt}]
            # transformers 4.51: tokenize=True 返回 BatchEncoding,取 input_ids
            prefix = tok.apply_chat_template(
                user, tokenize=True, add_generation_prompt=True,
                enable_thinking=False)["input_ids"]
            full = tok.apply_chat_template(
                user + [{"role": "assistant", "content": target}],
                tokenize=True, add_generation_prompt=False,
                enable_thinking=False)["input_ids"]
            lens.append((len(prefix), len(full)))
        report[split] = {
            "rows": len(rows),
            "valid_scene_spec": ok_target,
            "prompt_tokens": {"min": min(p for p, _ in lens),
                              "p50": sorted(p for p, _ in lens)[len(lens) // 2],
                              "p90": sorted(p for p, _ in lens)[int(len(lens) * 0.9)],
                              "max": max(p for p, _ in lens)},
            "full_tokens": {"min": min(f for _, f in lens),
                            "p50": sorted(f for _, f in lens)[len(lens) // 2],
                            "p90": sorted(f for _, f in lens)[int(len(lens) * 0.9)],
                            "max": max(f for _, f in lens)},
        }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
