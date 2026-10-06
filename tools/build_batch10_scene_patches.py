# -*- coding: utf-8 -*-
"""Build batch-10 named scene patches (final 3 questions) per OPERATING_GUIDE.
Only scene_spec changes; math three fields byte-identical; every computation
independently re-derived. Scenes are inline raw strings."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
OUT = ROOT / "reviews/2026-10-06-scene-standard-sweep/batch10-patches.json"

NEW_SCENES = {
    "draft-c50-03": {
        "objects": [
            r"题面卡:$\operatorname{Exp}(1)$ 和 $S_{100}>110$ 的精确式与极限",
            r"板书一:密度 $\frac{e^{-s}s^{n-1}}{(n-1)!}$ 与分部积分递推",
            r"高亮框:关键点——递推 $T_n(t)=\frac{e^{-t}t^{n-1}}{(n-1)!}+T_{n-1}(t)$ 逐次累加",
            r"板书二:泊松等价的分布律对照",
            r"结论卡:精确尾 $e^{-110}\sum_{k=0}^{99}\frac{110^k}{k!}$;极限 $1-\Phi(a)$",
        ],
        "steps": [
            r"第一步:密度:卷积或归纳给 $S_n$ 的密度 $f_n(s)=\frac{e^{-s}s^{n-1}}{(n-1)!}$($s>0$)。",
            r"第二步:尾积分递推(逐步,高亮):记 $T_n(t)=\int_t^\infty\frac{e^{-s}s^{n-1}}{(n-1)!}ds$;分部积分:$\int_t^\infty e^{-s}s^{n-1}ds=[-e^{-s}s^{n-1}]_t^\infty+(n-1)\int_t^\infty e^{-s}s^{n-2}ds=e^{-t}t^{n-1}+(n-1)\int_t^\infty e^{-s}s^{n-2}ds$;除以 $(n-1)!$ 得 $T_n(t)=\frac{e^{-t}t^{n-1}}{(n-1)!}+T_{n-1}(t)$;$T_1(t)=e^{-t}$。",
            r"第三步:递推展开(逐步):从 $T_1$ 逐次递推到 $T_{100}$,每步累加一项 $\frac{e^{-t}t^k}{k!}$;故 $T_{100}(110)=e^{-110}\sum_{k=0}^{99}\frac{110^k}{k!}$;即 $P(S_{100}>110)=e^{-110}\sum_{k=0}^{99}\frac{110^k}{k!}$(高亮)。",
            r"第四步:泊松等价(依据,高亮):泊松分布律 $P(\operatorname{Pois}(110)\le99)=e^{-110}\sum_{k=0}^{99}\frac{110^k}{k!}$,与上式逐项相同。",
            r"第五步:极限(逐步):$EX_i=\operatorname{Var}X_i=1$;CLT 给 $\frac{S_n-n}{\sqrt n}\Rightarrow N(0,1)$;故 $\lim P(S_n>n+a\sqrt n)=\lim P(\frac{S_n-n}{\sqrt n}>a)=1-\Phi(a)$;注意:该定理不提供 $n=100$ 的误差大小,不能凭未验证小数宣称有限误差很小(高亮)。",
        ],
    },
    "draft-c50-04": {
        "objects": [
            r"题面卡:$B(n,\frac12)$ 的整数阈值与半单位移动",
            r"板书一:精确概率 $2^{-100}\sum_{j=0}^{55}\binom{100}j$",
            r"高亮框:关键点——事件等价 $\{X_n\le k\}=\{X_n\le k+\frac12\}$",
            r"板书二:$|z_n-a|\le\frac2{\sqrt n}$ 与半单位移动增 $\frac1{\sqrt n}$ 的推导",
            r"结论卡:两个标准化阈值均给极限 $\Phi(a)$",
        ],
        "steps": [
            r"第一步:精确概率:$P(X_{100}\le55)=2^{-100}\sum_{j=0}^{55}\binom{100}j$。",
            r"第二步:半单位移动(事件等价,高亮):$X_n$ 只取整数,故对整数 $k$:$\{X_n\le k\}=\{X_n\le k+\frac12\}$,只是事件等价,不改变概率。",
            r"第三步:标准化:$Z_n=\frac{X_n-n/2}{\sqrt n/2}$,CLT 给 $Z_n\Rightarrow N(0,1)$;对 $k_n=\lfloor n/2+a\sqrt n/2\rfloor$,记阈值 $z_n=\frac{k_n-n/2}{\sqrt n/2}$。",
            r"第四步:阈值估计(推导,高亮):$|z_n-a|=\frac{|k_n-(n/2+a\sqrt n/2)|}{\sqrt n/2}\le\frac1{\sqrt n/2}=\frac2{\sqrt n}$(取整误差不超过 $1$);移动半单位后阈值增加 $\frac{1/2}{\sqrt n/2}=\frac1{\sqrt n}$;二者都趋于 $a$。",
            r"第五步:夹逼(逐步,高亮):对固定 $\varepsilon>0$,最终 $z_n\in(a-\varepsilon,a+\varepsilon)$;于是 $P(Z_n\le a-\varepsilon)\le P(X_n\le k_n)\le P(Z_n\le a+\varepsilon)$;两边取极限得 $\Phi(a-\varepsilon)\le\liminf\le\limsup\le\Phi(a+\varepsilon)$;由 $\Phi$ 的连续性令 $\varepsilon\to0$,得极限 $\Phi(a)$;有限事件等价不能推出其概率等于正态 CDF,连续性论证才是极限依据。",
        ],
    },
    "draft-c50-05": {
        "objects": [
            r"题面卡:柯西反例——去掉矩条件后样本均值不集中",
            r"板书一:经典 CLT 的充分矩条件与标准化",
            r"高亮框:关键点——特征函数 $(e^{-|t|/n})^n=e^{-|t|}$,样本均值仍为标准柯西",
            r"板书二:$P(|\overline X_n|\le1)=\frac12$ 与 $P(|\overline X_n-c|\le\frac\pi8)\le\frac14$",
            r"结论卡:反例只说明充分性,不能推断所有 CLT 的必要条件",
        ],
        "steps": [
            r"第一步:经典条件(高亮):$EX=\mu$、$0<\operatorname{Var}X=\sigma^2<\infty$,标准化为 $\frac{\sum X_i-n\mu}{\sigma\sqrt n}$;零方差是退化情形。",
            r"第二步:柯西的矩:标准柯西的 $E|X|$ 与 $EX^2$ 发散,均值不存在;特征函数(逐步):$\phi(t)=\frac1\pi\int_{-\infty}^{\infty}\frac{e^{itx}}{1+x^2}dx=e^{-|t|}$。",
            r"第三步:样本均值特征函数(逐步,高亮):独立和的特征函数相乘:$\phi_{\overline X_n}(t)=(\phi(t/n))^n=(e^{-|t|/n})^n=e^{-|t|}$;故 $\overline X_n$ 仍为标准柯西(高亮核心结论)。",
            r"第四步:不集中到零(逐步):$P(|\overline X_n|\le1)=P(|X|\le1)=\frac2\pi\int_0^1\frac{dx}{1+x^2}=\frac2\pi\cdot\frac\pi4=\frac12$,对所有 $n$ 成立。",
            r"第五步:不集中到任何常数(逐步):密度 $f\le\frac1\pi$,故 $P(|\overline X_n-c|\le\frac\pi8)\le\frac1\pi\cdot\frac{2\pi}8=\frac14$;反例的逻辑范围:只说明有限正方差是经典 $\sqrt n$ 规范化 CLT 的充分假设,不能由该反例推断所有 CLT 形式的必要条件(高亮)。",
        ],
    },
}


def sorted_sha(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def main() -> int:
    try:
        control = set(chr(c) for c in range(0, 32)) - {"\t"}
        for cid, scene in NEW_SCENES.items():
            for s in scene["objects"] + scene["steps"]:
                if any(ch in control for ch in s):
                    raise ValueError("control char in " + cid)
        sel_path = DRAFTS / "draft-selection.json"
        sel = json.loads(sel_path.read_text("utf-8-sig"))
        if sel.get("schema") != 2:
            raise ValueError("schema2 selector required")
        found = {}
        for entry in sel["entries"]:
            path = DRAFTS / entry["path"]
            for line in path.read_text("utf-8-sig").splitlines():
                if not line.strip():
                    continue
                rec = json.loads(line)
                if rec["id"] in NEW_SCENES and rec["id"] not in found:
                    found[rec["id"]] = (entry, rec)
        if len(found) != len(NEW_SCENES):
            raise ValueError("missing records: " + str(set(NEW_SCENES) - set(found)))
        patches = []
        for cid, scene in NEW_SCENES.items():
            entry, rec = found[cid]
            old_scene = rec["scene_spec"]
            if old_scene == scene or (
                    sorted(old_scene.get("objects", [])) == sorted(scene.get("objects", []))
                    and old_scene.get("steps") == scene.get("steps")):
                raise ValueError("scene unchanged: " + cid)
            expected_record_sha256 = sorted_sha(rec)
            new_rec = dict(rec)
            new_rec["scene_spec"] = scene
            for k in ("problem", "solution", "answer"):
                if new_rec[k] != rec[k]:
                    raise ValueError("math field drift: " + cid)
            new_math = {"problem": rec["problem"], "solution": rec["solution"],
                        "answer": rec["answer"], "scene_spec": scene}
            patches.append({
                "batch": entry["batch"],
                "id": cid,
                "expected_selected_path": entry["path"],
                "expected_hash_algorithm": sel["hash_algorithm"],
                "expected_selected_sha256": entry["sha256"],
                "expected_selected_raw_sha256": entry["raw_sha256"],
                "expected_record_sha256": expected_record_sha256,
                "new_math_content_sha256": sorted_sha(new_math),
                "fields": {"scene_spec": scene},
            })
        out = {
            "schema": "scene-patches-batch-v1",
            "status": "PENDING_CODEX_REVIEW",
            "normalization": "sorted-json-default-separators",
            "records": patches,
        }
        if OUT.exists():
            raise ValueError("output exists")
        with OUT.open("x", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
        print("patches:", len(patches))
        for p in patches:
            print(" -", p["id"], "| batch:", p["batch"])
        return 0
    except Exception as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
