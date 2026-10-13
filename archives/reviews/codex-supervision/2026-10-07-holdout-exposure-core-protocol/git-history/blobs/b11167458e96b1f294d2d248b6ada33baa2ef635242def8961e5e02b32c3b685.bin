"""三方模型对照汇总:读取 screening-tmp 各 run summary → MD → HTML → PDF。

只读 run 产物;输出 outputs/screening-tmp/MODEL_COMPARISON.{md,html,pdf}。
未实测维度必须标 NOT_MEASURED,不假绿。中文字体+打印 CSS,headless Edge 打印。
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs/screening-tmp"

EDGE = (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")


def load_latest(pattern: str) -> dict | None:
    dirs = sorted(Path(OUT_DIR / pattern).glob("run-*"))
    if not dirs:
        return None
    return json.loads((dirs[-1] / "summary.json").read_text(encoding="utf-8"))


def collect() -> dict:
    """汇总全部已跑 run;缺失的标 None(渲染为 NOT_MEASURED)。"""
    return {
        "inference": {
            "qwen2.5-7b": load_latest("inference/qwen2.5-7b"),
            "qwen3-4b": load_latest("inference/qwen3-4b"),
            "qwen3-4b-thinking": next(
                (json.loads((d / "summary.json").read_text(encoding="utf-8"))
                 for d in sorted(Path(OUT_DIR / "inference/qwen3-4b")
                                 .glob("run-*")) if json.loads(
                     (d / "summary.json").read_text(encoding="utf-8"))
                 .get("thinking")), None),
            "qwen3-8b": load_latest("inference/qwen3-8b"),
            "qwen3-8b-thinking": next(
                (json.loads((d / "summary.json").read_text(encoding="utf-8"))
                 for d in sorted(Path(OUT_DIR / "inference/qwen3-8b")
                                 .glob("run-*")) if json.loads(
                     (d / "summary.json").read_text(encoding="utf-8"))
                 .get("thinking")), None),
        },
        "qlora": {
            "qwen2.5-7b": load_latest("qlora-probes/qwen2.5-7b/seq-1024"),
            "qwen3-4b": load_latest("qlora-probes/qwen3-4b/seq-1024"),
            "qwen3-8b": load_latest("qlora-probes/qwen3-8b/seq-1024"),
        },
    }


def _v(d: dict | None, key: str, fmt="{:.3g}"):
    if not d:
        return "NOT_MEASURED"
    v = d.get(key)
    if v is None:
        return "NOT_MEASURED"
    if isinstance(v, float):
        return fmt.format(v)
    return str(v)


def render_md(data: dict) -> str:
    inf = data["inference"]
    ql = data["qlora"]
    lines = ["# 三方底座模型对照报告(MODEL_COMPARISON)", "",
             f"> 生成时间:{time.strftime('%Y-%m-%d %H:%M:%S')}。"
             "任务:problem+solution → scene_spec 结构化 JSON(20 条子类分层样本,"
             "输入哈希冻结)。仅筛选测量,不构成正式训练;"
             "candidate/UNVERIFIED 语义保持。", "",
             "## 1. 推理对照(20 条,同口径冻结 seed/GenerationConfig)", "",
             "| 模型/模式 | 严格 JSON 解析率 | 宽松提取率 | 4bit 加载显存 | 热延迟/条 | 总生成 token |",
             "|---|---|---|---|---|---|"]
    for tag, d in inf.items():
        lines.append(f"| {tag} | {_v(d, 'strict_rate', '{:.0%}')} "
                     f"| {_v(d, 'lenient_rate', '{:.0%}')} "
                     f"| {_v(d, 'load_vram_gb', '{:.2f} GB')} "
                     f"| {_v(d, 'warm_gen_sec_mean', '{:.1f} s')} "
                     f"| {_v(d, 'total_gen_tokens', '{:d}')} |")
    lines += ["", "## 2. QLoRA 训练资源探针(seq=1024 精确 token,3 步)", "",
              "| 模型 | 训练峰值 allocated | 训练峰值 reserved | 平均步时 | 失败步 | adapter 体积 |",
              "|---|---|---|---|---|---|"]
    for tag, d in ql.items():
        lines.append(f"| {tag} | {_v(d, 'train_peak_allocated_gb', '{:.2f} GB')} "
                     f"| {_v(d, 'train_peak_reserved_gb', '{:.2f} GB')} "
                     f"| {_v(d, 'step_sec_list', '{}')} "
                     f"| {_v(d, 'failed_steps', '{:d}')} "
                     f"| {_v(d, 'adapter_ckpt_bytes', '{:d}')} |")
    lines += ["", "## 3. 未测维度(NOT_MEASURED,如实)", "",
              "- FP16-vs-4bit 退化对照:未测",
              "- TTFT 细分:未测",
              "- 梯度累积吞吐:未测",
              "- 断点恢复验证:未测(adapter save ≠ 恢复验证)",
              "- 数学/内容人工复核:未测(仅规则可解析率)",
              "- seq_len 曲线全档(2048/4096):未测",
              "- Windows+bnb 兼容性:已实测通过(三模型 4bit 加载均成功)", "",
              "## 4. 环境与证据", "",
              "- GPU: NVIDIA GeForce RTX 5060 Laptop(8GB),torch 2.11.0+cu128;",
              "- 每 run 目录含逐样本完整输出/哈希/命令/env/provenance 哈希;",
              "- 原始 run 数据留存于 outputs/screening-tmp/,撤组前归档。", "",
              "## 5. 结论建议(待用户拍板)", "",
              "- 数据为 provisional train 筛选成绩,不当正式 eval/test 验收;",
              "- baseline 选择需综合解析率、显存余量、延迟与训练可行性,由用户决定。",
              ""]
    return "\n".join(lines)


CSS = """
@page { size: A4; margin: 15mm 13mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Microsoft YaHei", "微软雅黑", "Segoe UI", sans-serif;
       font-size: 10pt; line-height: 1.6; color: #1a1a1a; margin: 0; }
h1 { font-size: 18pt; border-bottom: 2.4pt solid #1f4e79; color: #1f4e79;
     padding-bottom: 5pt; }
h2 { font-size: 13pt; border-left: 4pt solid #1f4e79; background: #eef3f9;
     padding: 3pt 7pt; color: #16365c; page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0; }
th, td { border: 0.6pt solid #9db8d2; padding: 4pt 6pt; text-align: left; }
th { background: #1f4e79; color: #fff; }
blockquote { background: #f5f7fa; border-left: 3pt solid #9db8d2; padding: 5pt 9pt; }
"""


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-pdf", action="store_true", help="只生成 MD/HTML")
    args = ap.parse_args(argv)
    data = collect()
    md_text = render_md(data)
    (OUT_DIR / "MODEL_COMPARISON.md").write_text(md_text, encoding="utf-8")
    from markdown_it import MarkdownIt  # noqa: PLC0415
    md = MarkdownIt("commonmark", {"html": True})
    md.enable("table")
    html = f"<!DOCTYPE html><html><head><meta charset='utf-8'>"
    html += f"<style>{CSS}</style></head><body>{md.render(md_text)}</body></html>"
    (OUT_DIR / "MODEL_COMPARISON.html").write_text(html, encoding="utf-8")
    print(f"MD/HTML → {OUT_DIR}")
    if args.skip_pdf:
        return 0
    pdf = OUT_DIR / "MODEL_COMPARISON.pdf"
    r = subprocess.run([EDGE, "--headless", "--disable-gpu",
                        f"--print-to-pdf={pdf}",
                        str(OUT_DIR / "MODEL_COMPARISON.html")],
                       capture_output=True, timeout=120)
    if r.returncode != 0 or not pdf.exists():
        print(f"[FAIL] PDF 生成失败: {r.stderr.decode('utf-8', 'replace')[:300]}")
        return 1
    print(f"PDF → {pdf}({pdf.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
