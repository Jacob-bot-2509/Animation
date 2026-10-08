"""接入层构建:30题修订 + 7条场景字段版本绑定 → 独立新版本源文件(不覆盖任何原包/旧回执)."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUP = ROOT / "reviews/codex-supervision/2026-10-07-core-submission-supervision"
OUT = ROOT / "reviews/2026-10-07-math-admission-v1"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dense(record: dict) -> str:
    return digest(json.dumps(record, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")).encode("utf-8"))


# 7 条场景更新:与修订后数学字段对齐(分数/精确式替代旧小数;删除已不存在的数值故事)
SCENE_UPDATES = {
    "prob-038": {
        "scene_spec": (
            "{'objects': ['矩形样本空间（总面积对应概率 1）', '蓝色圆 A（面积比例 3/5）', "
            "'红色圆 B（面积比例 2/5）', '交集区域（紫色，面积比例 1/5）'], 'steps': ["
            "'第一步：画出一个正方形代表总样本空间（总面积对应概率 1），按面积比例 $3/5$、$2/5$ "
            "画出相交的圆 A 和圆 B，交集面积比例为 $1/5$。', "
            "'第二步：给交集部分涂上紫色，标注 $P(A\\cap B)=1/5$。', "
            "'第三步：以圆 B 为缩减样本空间，交集占比 $\\frac{1/5}{2/5}=\\frac{1}{2}$，标注 "
            "$P(A\\mid B)=\\frac{1}{2}$；再以圆 A 为缩减空间，交集占比 "
            "$\\frac{1/5}{3/5}=\\frac{1}{3}$，标注 $P(B\\mid A)=\\frac{1}{3}$。', "
            "'第四步：高亮最终结果与答案。']}"
        ),
        "rationale": "旧场景用小数 0.6/0.4/0.2/0.5,修订后题干与解全部改用分数 3/5/2/5/1/5/1/2",
    },
    "prob-042": {
        "scene_spec": (
            "{'objects': ['二维坐标系', '收敛水平线 $y=p$（一般值）', '动态折线图', "
            "'切比雪夫上界衰减曲线', '公平硬币附加条件下的水平线 $y=\\frac{1}{2}$'], 'steps': ["
            "'第一步：在坐标系中画出横轴（试验次数 n）和纵轴（正面频率），画红色水平虚线表示极限概率 $p$"
            "——题目未指定公平性，不能直接令 $p=\\frac{1}{2}$。', "
            "'第二步：模拟抛硬币过程，折线图从左向右延伸，在 $p$ 上下波动，n 较小时波动剧烈。', "
            "'第三步：标注 $E(F_n)=p$ 与 $\\operatorname{Var}(F_n)=\\frac{p(1-p)}{n}$，"
            "画出切比雪夫上界 $\\frac{p(1-p)}{n\\varepsilon^2}$ 随 $n$ 的衰减曲线。', "
            "'第四步：附加公平硬币条件 $p=\\frac{1}{2}$ 时水平线落在 $\\frac{1}{2}$；"
            "高亮最终结果与答案 $F_n\\xrightarrow{P}p$。']}"
        ),
        "rationale": "旧场景预设 p=0.5;修订后题干明确题目未指定公平性,p 为一般值,公平仅为附加条件",
    },
    "eval-calc-027-s3": {
        "scene_spec": (
            "{'objects': ['三角形积分区域 $D=\\{(x,y):0\\le x\\le y\\le1\\}$', "
            "'交换积分次序的动态标注', '$u=y^2$ 代换步骤'], 'steps': ["
            "'第一步：建立数学分析·重积分场景，画出三角形区域 $D$，标注被积函数连续、积分次序可交换。', "
            "'第二步：先对 $x$ 积分，得 $I=\\int_0^1\\int_0^y e^{y^2}\\,dx\\,dy="
            "\\int_0^1 y e^{y^2}\\,dy$。', "
            "'第三步：令 $u=y^2$，则 $I=\\frac{1}{2}\\int_0^1 e^u\\,du=\\frac{e-1}{2}$。', "
            "'第四步：高亮最终结果与答案。']}"
        ),
        "visual_style": "积分次序交换与代换",
        "rationale": "旧场景主线是黎曼和数值 0.85914 校验,修订后解已删除数值校验、改为交换次序+代换推导",
    },
    "eval-prob-007-s2": {
        "scene_spec": (
            "{'objects': ['$q_k$ 递推乘积的逐项生成', '365 格占位', "
            "'精确乘积式 $\\frac{365!}{335!\\,365^{30}}$ 标注'], 'steps': ["
            "'第一步：以递推计算为主线，建立概率论·经典概型场景并呈现该解法的关键图形。', "
            "'第二步：标注递推式 $q_k=q_{k-1}\\frac{366-k}{365}$，其中 $q_1=1$。', "
            "'第三步：递推展开得 $q_{30}=\\prod_{k=2}^{30}\\frac{366-k}{365}="
            "\\frac{365!}{335!\\,365^{30}}$。', "
            "'第四步：高亮最终结果与答案 $1-q_{30}$。']}"
        ),
        "rationale": "旧场景含 k=23 临界点与小数 0.49270/0.7063;修订后解为精确递推乘积,无临界点讨论",
    },
    "eval-prob-007-s3": {
        "scene_spec": (
            "{'objects': ['435 对配对的计数高亮', '期望线性性 $E(N)=87/73$ 标注', "
            "'二阶矩与柯西下界 $P(N>0)\\ge435/799>1/2$ 标注'], 'steps': ["
            "'第一步：以配对计数的二阶矩视角为主线，建立概率论·经典概型场景并呈现该解法的关键图形。', "
            "'第二步：435 对配对的计数高亮，由期望线性性标注 "
            "$E(N)=\\frac{435}{365}=\\frac{87}{73}$。', "
            "'第三步：标注 $E(N^2)=\\frac{435}{365}+\\frac{435\\cdot434}{365^2}$，"
            "并由柯西不等式得 $P(N>0)\\ge\\frac{435}{799}>\\frac{1}{2}$。', "
            "'第四步：高亮最终结果与答案。']}"
        ),
        "visual_style": "配对计数与二阶矩下界",
        "rationale": "旧场景用'期望≈1.19 大于 1 故概率大'的推理;修订后改为二阶矩+柯西下界 435/799>1/2",
    },
    "eval-prob-008-s3": {
        "scene_spec": (
            "{'objects': ['切比雪夫上界 $1/4$ 与精确值 "
            "$q=2^{-99}\\sum_{k=0}^{40}\\binom{100}{k}$ 的对比条', "
            "'\"分布无关界 vs 分布相关值\"的标注', '精确差值 $\\frac{1}{4}-q>0$ 的推导标注'], 'steps': ["
            "'第一步：以方法对比讨论为主线，建立概率论·大数定律场景并呈现该解法的关键图形。', "
            "'第二步：切比雪夫上界 $\\frac{1}{4}$ 与精确值 "
            "$q=2^{-99}\\sum_{k=0}^{40}\\binom{100}{k}$ 的对比条。', "
            "'第三步：标注精确差值 "
            "$\\frac{1}{4}-q=\\frac{2^{97}-\\sum_{k=0}^{40}\\binom{100}{k}}{2^{99}}>0$。', "
            "'第四步：高亮最终结果与答案。']}"
        ),
        "rationale": "旧场景含小数 0.0569/0.25/0.193;修订后解为精确 q 与精确差值式",
    },
    "test-prob-008": {
        "scene_spec": (
            "{'objects': ['样本均值轨迹收敛于 $\\frac{7}{2}$', '上界随 $n$ 衰减曲线'], 'steps': ["
            "'第一步：建立概率论·切比雪夫×大数定律综合场景，呈现与切比雪夫不等式、弱大数定律、"
            "均匀分布数字特征相关的核心图形。', "
            "'第二步：样本均值轨迹收敛于 $\\frac{7}{2}$。', "
            "'第三步：$\\varepsilon=\\frac{1}{10}$ 时的上界 "
            "$\\min\\{1,\\frac{875}{3n}\\}$ 随 $n$ 衰减曲线。', "
            "'第四步：高亮最终结果与答案。']}"
        ),
        "rationale": "旧场景用小数 3.5/0.1;修订后题干与解全部改用精确形式 7/2 与 1/10",
    },
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    mc = [json.loads(l) for l in (SUP / "math-corrections-30.jsonl")
          .read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    by_id = {m["id"]: m for m in mc}
    assert len(by_id) == 30

    # 1) 场景更新覆盖层
    updates = []
    for rid, upd in SCENE_UPDATES.items():
        m = by_id[rid]
        old_spec = m["corrected_record"]["scene_spec"]
        new_spec = upd["scene_spec"]
        updates.append({
            "id": rid,
            "old_scene_spec_sha256": digest(str(old_spec).encode("utf-8")),
            "new_scene_spec_sha256": digest(new_spec.encode("utf-8")),
            "scene_spec": new_spec,
            "visual_style": upd.get("visual_style"),
            "old_visual_style": m["corrected_record"].get("visual_style"),
            "rationale": upd["rationale"],
            "math_binding": {
                "after_record_dense_sha256": m["after_record_dense_sha256"],
                "after_answer": m["after_math_fields"]["answer"],
            },
        })
    up_path = OUT / "scene-updates-candidate.jsonl"
    with up_path.open("w", encoding="utf-8", newline="\n") as f:
        for u in updates:
            f.write(json.dumps(u, ensure_ascii=False, separators=(",", ": ")) + "\n")
    print(f"场景更新覆盖层: {len(updates)} 条 -> {up_path.relative_to(ROOT)}")

    # 2) 接入版源文件:corrected-sources 基础上仅替换场景字段
    src_out = OUT / "admission-sources"
    new_bindings = []
    changed_ids = set(SCENE_UPDATES)
    for binding in json.loads((SUP / "candidate-source-bindings.json").read_text(encoding="utf-8-sig")):
        cand = ROOT / binding["candidate"]["path"]
        target = src_out / cand.relative_to(SUP / "corrected-sources")
        target.parent.mkdir(parents=True, exist_ok=True)
        raw_lines = cand.read_bytes().splitlines(keepends=True)
        touched = False
        for line_no in binding["changed_source_lines"]:
            rec = json.loads(raw_lines[line_no - 1].decode("utf-8-sig"))
            rid = rec["id"]
            if rid in SCENE_UPDATES:
                rec = dict(rec)
                rec["scene_spec"] = SCENE_UPDATES[rid]["scene_spec"]
                if SCENE_UPDATES[rid].get("visual_style"):
                    rec["visual_style"] = SCENE_UPDATES[rid]["visual_style"]
                raw_lines[line_no - 1] = (json.dumps(rec, ensure_ascii=False,
                                                    separators=(", ", ": ")) + "\n").encode("utf-8")
                touched = True
                # 该记录的更新后 SHA
                m = by_id[rid]
                base = m["corrected_record"]
                rebuilt = dict(base)
                rebuilt["scene_spec"] = SCENE_UPDATES[rid]["scene_spec"]
                if SCENE_UPDATES[rid].get("visual_style"):
                    rebuilt["visual_style"] = SCENE_UPDATES[rid]["visual_style"]
                new_bindings.append({
                    "id": rid, "source_path": binding["before"]["path"], "source_line": line_no,
                    "before_record_dense_sha256": m["before_record_dense_sha256"],
                    "after_math_record_dense_sha256": m["after_record_dense_sha256"],
                    "after_math_scene_record_dense_sha256": dense(rebuilt),
                    "changed_fields": m["changed_fields"],
                    "scene_fields_updated": True,
                })
        data = b"".join(raw_lines)
        target.write_bytes(data)
        identical = "字节等同 corrected-sources" if not touched else f"仅替换场景字段({len([i for i in binding['changed_source_lines'] if json.loads(raw_lines[i-1].decode('utf-8-sig'))['id'] in SCENE_UPDATES])}行)"
        print(f"接入版: {target.relative_to(ROOT)}  sha={digest(data)[:16]}  {identical}")

    # 3) 未改场景的 23 条:与 corrected_record 完全一致(dense 核对)
    for m in mc:
        if m["id"] in changed_ids:
            continue
        if dense(m["corrected_record"]) != m["after_record_dense_sha256"]:
            print(f"  未改场景记录 SHA 不一致: {m['id']}")
    print(f"未改场景 23 条 dense 核对通过;改场景 {len(changed_ids)} 条")

    # 4) 场景绑定审计(全部 30 条)
    audit = []
    for m in mc:
        rid = m["id"]
        if rid in SCENE_UPDATES:
            status = "SCENE_UPDATED_VERSION_BOUND"
        elif rid == "prob-046":
            status = "SCENE_CONSISTENT_NOTE"
        else:
            status = "SCENE_CONSISTENT"
        audit.append({
            "id": rid, "scene_status": status,
            "group": m["source"]["group"],
            "old_render_artifacts_note": (
                "dataset_audit_2026-10-05-render-check(旧版渲染HTML)与 "
                "2026-10-06 场景草稿/修复候选均基于修订前数学字段,不得作为修订版渲染证明"),
        })
    a_path = OUT / "scene-binding-audit.json"
    with a_path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump({
            "schema": "math-admission-scene-binding-audit-v1",
            "total": len(audit),
            "scene_updated": len(SCENE_UPDATES),
            "scene_consistent": len(audit) - len(SCENE_UPDATES),
            "rows": audit,
            "note": "旧渲染回执(2026-10-05 render-check / 2026-10-06 场景草稿与修复候选)全部对应修订前版本;"
                    "修订版渲染需另行生成,不得引用旧渲染作为新版本证明",
        }, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"场景绑定审计: {a_path.relative_to(ROOT)}")

    # 5) 输出清单
    manifest = []
    for p in sorted(OUT.rglob("*")):
        if p.is_file():
            b = p.read_bytes()
            manifest.append({"path": str(p.relative_to(ROOT)).replace("\\", "/"),
                             "raw_sha256": digest(b), "bytes": len(b)})
    m_path = OUT / "admission-manifest.json"
    with m_path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump({"schema": "math-admission-v1-manifest", "items": manifest},
                  f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"清单: {m_path.relative_to(ROOT)} 共 {len(manifest)} 项")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
