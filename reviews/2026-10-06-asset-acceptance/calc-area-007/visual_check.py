# -*- coding: utf-8 -*-
"""calc-area-007 视觉核验:对渲染 mp4 抽帧,统计主色直方图 + 目标色信号。
manim 标准色:BLUE=#58C4DD(青),RED=#FC6255,YELLOW=#FFFF00,ORANGE=#FF862F。
输出视觉证据 visual-check.json。"""
import json
from pathlib import Path

import av

HERE = Path(__file__).parent
EVIDENCE = json.loads((HERE / "render-evidence.json").read_text(encoding="utf-8"))
MP4 = Path(EVIDENCE["output"]["path"])
FRAME_IDXS = [20, 90, 160, 210]


def classify(r, g, b):
    if b > 150 and g > 150 and r < 150:
        return "cyan_blue"       # manim BLUE #58C4DD
    if r > 150 and g < 120 and b < 120:
        return "red"             # manim RED #FC6255
    if r > 200 and g > 200 and b < 120:
        return "yellow"          # manim YELLOW #FFFF00
    if 80 < r < 210 and 80 < g < 210 and b < 70 and abs(r - g) < 50:
        return "yellow_dim"      # 半透明黄混黑(≈115,115,0)
    if r > 200 and 120 <= g <= 180 and b < 120:
        return "orange"          # manim ORANGE #FF862F
    if r > 200 and g > 200 and b > 200:
        return "white"
    if r < 50 and g < 50 and b < 50:
        return "black"
    return "other"


def main():
    results = {}
    with av.open(str(MP4)) as container:
        stream = container.streams.video[0]
        frames = [f for f in container.decode(stream)]
    total = len(frames)
    for idx in FRAME_IDXS:
        if idx >= total:
            continue
        img = frames[idx].to_image()
        counts = {}
        for y in range(0, img.height, 4):
            for x in range(0, img.width, 4):
                r, g, b = img.getpixel((x, y))[:3]
                cls = classify(r, g, b)
                counts[cls] = counts.get(cls, 0) + 1
        top = sorted(counts.items(), key=lambda kv: -kv[1])[:6]
        results[str(idx)] = {"top_colors": top, "full": counts}
    signals = {}
    for name, key in [("blue_curve", "cyan_blue"), ("red_line", "red"),
                      ("yellow_area", "yellow"), ("yellow_area_dim", "yellow_dim"),
                      ("orange_rect", "orange"), ("white_formula", "white")]:
        signals[name] = any(v["full"].get(key, 0) > 5 for v in results.values())
    report = {
        "mp4": str(MP4),
        "mp4_sha256": EVIDENCE["output"]["sha256"],
        "total_frames": total,
        "frame_samples": results,
        "signals": signals,
    }
    (HERE / "visual-check.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("total frames:", total)
    for k, v in results.items():
        print(k, v["top_colors"])
    print("signals:", json.dumps(signals, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
