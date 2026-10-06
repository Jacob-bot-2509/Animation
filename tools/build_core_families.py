"""Build the 47-question core-family identification (pending, for Codex review).

Method: manual pairwise semantic analysis of the 47 active train records
(objects/conditions/targets/solving structure), NOT keyword clustering.
Same-core family = core math object, conditions, target and solving structure
unchanged; only data/symbols/axis/wording differ (user definition). Numeric/
axis swaps do not add independent samples or variant forms.

Family status: CONFIRMED (pure data/substitution mapping) or PROPOSED
(structure-isomorphic but dimension/task-extent mapped; Codex adjudicates).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "reviews/2026-10-06-core-families/train-47-raw.json"
OUT = ROOT / "reviews/2026-10-06-core-families/core-families.pending.json"

FAMILIES = [
    {
        "family_id": "F1-area-between-curves",
        "status": "CONFIRMED",
        "members": ["calc-area-007", "calc-area-010", "calc-area-011", "calc-area-013"],
        "core": {
            "object": "两条曲线围成的平面封闭区域及其面积",
            "conditions": "给定两条相交曲线方程(直角坐标)",
            "target": "求围成区域的面积数值",
            "solving_structure": "联立求交点→定积分∫(上曲线-下曲线)dx→求值",
        },
        "equivalence_mapping": ("曲线数据替换:y=x² 与 y=x+2(007)↔y=ln x 与 y=-x+e+1(010)↔"
                               "y=|x²-1| 与 y=1(011)↔y=xe^{-x} 与 x=1(013);"
                               "交点与积分限随之变化,求解结构不变"),
        "evidence": "四题均为「计算由曲线…所围成的封闭图形的面积」,解法同为求交点+定积分",
        "forms_note": "四成员曲线类型不同(抛物线/对数/绝对值/指数),按数据变体计 1 个独立样本;"
                     "是否算「真正不同变体形式」留 Codex 裁定",
    },
    {
        "family_id": "F2-improper-convergence-value",
        "status": "CONFIRMED",
        "members": ["calc-improper-002", "calc-param-improper-003"],
        "core": {
            "object": "无穷限反常积分及其收敛性与值",
            "conditions": "给定被积函数与无穷积分限(003 含参数 α>0)",
            "target": "判定收敛并求出积分值",
            "solving_structure": "求原函数→代入变上限→取极限 b→+∞→收敛值与参数表达式",
        },
        "equivalence_mapping": ("被积函数替换:1/(1+x²)↔e^{-αx};答案 π/2↔1/α;"
                               "原函数 arctan x↔-(1/α)e^{-αx},求解结构不变"),
        "evidence": "两题均为「判断/求反常积分是否收敛并求值」,解法同为原函数+取极限",
        "forms_note": "003 含参数为条件参数化,按数据变体计 1 个独立样本",
    },
    {
        "family_id": "F3-shear-geometric-meaning",
        "status": "CONFIRMED",
        "members": ["linalg-048", "linalg-058"],
        "core": {
            "object": "单位剪切矩阵(单个非对角元 k)对应的平面线性变换及其几何意义",
            "conditions": "给定 III 型初等矩阵(剪切参数 3)",
            "target": "描述该变换的几何影响(固定轴、不变线族、面积保持)",
            "solving_structure": "变换公式→固定轴与网格线行为→单位正方形像→det 面积保持",
        },
        "equivalence_mapping": ("轴互换(关于 y=x 的镜像/转置):A=[[1,3],[0,1]]↔E=[[1,0],[3,1]];"
                               "水平剪切↔竖直剪切;x↔y 互换后答案互给;"
                               "二者同为 III 型初等矩阵、det=1"),
        "evidence": "与 Codex msg_542 独立复核一致:PAP=E、det=1、同核心训练变体",
        "forms_note": "轴互换不增加独立样本或变体形式(按 Codex msg_544 口径)",
    },
    {
        "family_id": "F4-determinant-geometric-meaning",
        "status": "PROPOSED",
        "members": ["linalg-050", "linalg-053"],
        "core": {
            "object": "行列式作为线性变换体积缩放因子的几何意义",
            "conditions": "给定行列式(050 为一般二阶式,053 为具体三阶数值式)",
            "target": "用几何图形解释行列式的几何意义",
            "solving_structure": "列向量张成平行体→体积/面积=行列式绝对值",
        },
        "equivalence_mapping": "维度映射:二阶↔三阶;面积↔体积;一般式 ad-bc↔具体值 10",
        "evidence": ("两题题型/目标/求解结构同构(张成图形体积=|det|);"
                     "差异为维度 2→3 与具体数值;二阶公式与三阶展开的运算细节不同"),
        "forms_note": "维度映射是否构成实质差异由 Codex 裁定;若拆分则各为独立样本",
    },
    {
        "family_id": "F5-quadric-surface-identification",
        "status": "PROPOSED",
        "members": ["geom-024", "geom-026"],
        "core": {
            "object": "空间直角坐标系中二次曲面方程的图形类型",
            "conditions": "给定曲面方程(024:x²+y²=4;026:z=x²+2y²)",
            "target": "识别曲面类型并描述其几何特征(024 含画图,026 含截线分析)",
            "solving_structure": "方程特征→标准型识别(024:缺 z→柱面;026:标准型→椭圆抛物面)",
        },
        "equivalence_mapping": ("曲面替换:圆柱面(缺变量)↔椭圆抛物面(标准型);"
                               "026 附加截线代入分析为扩展目标"),
        "evidence": "两题均为「由方程指出曲面类型」,识别路径同为方程→标准型;附加目标不同",
        "forms_note": "附加目标(画图 vs 截线)不同,是否同核心由 Codex 裁定",
    },
]

SINGLETONS = {
    "calc-area-008": "极坐标面积公式(求解结构与 F1 不同:½∫r²dθ)",
    "calc-area-009": "参数方程(摆线)面积(参数积分公式,独立求解结构)",
    "calc-vol-012": "旋转体体积(π∫f²dx,目标为体积而非面积)",
    "calc-derivative-001": "导数+切线方程",
    "calc-double-integral-004": "二重积分几何意义(曲顶柱体体积,极坐标换元)",
    "calc-green-005": "格林公式曲线积分",
    "calc-limit-006": "夹逼定理求极限",
    "calc-series-015": "交错级数敛散与绝对/条件收敛判别",
    "calc-series-017": "函数项级数一致收敛判别",
    "calc-series-020": "傅里叶级数展开",
    "geom-020": "直线与平面夹角(几何度量)",
    "geom-022": "过三点平面方程(方程构造)",
    "geom-028": "椭圆抛物面直纹性判断(证明性任务,与 F5 目标不同)",
    "geom-029": "等距变换下点的坐标计算(对象为点)",
    "geom-030": "仿射变换下球面的像(对象为曲面像,与 029 点坐标不同)",
    "geom-031": "维维安尼曲线参数方程(交线参数化)",
    "linalg-051": "多项式因式分解与复平面根分布",
    "linalg-054": "Cramer 法则解方程组(求解结构:行列式比值)",
    "linalg-055": "方程组解的情况讨论(增广矩阵/秩判断)",
    "linalg-056": "齐次方程组基础解系(与 054/055 求解结构不同)",
    "linalg-062": "子空间和与交的维数(维数公式)",
    "linalg-063": "线性映射核与值域维数",
    "linalg-064": "特征值/特征向量及其几何意义",
    "linalg-065": "λ-矩阵不变因子/初等因子(与 066 链式相关但目标不同)",
    "linalg-066": "若尔当标准形(依赖 065 的不变因子,但目标为若当形矩阵)",
    "linalg-067": "旋转矩阵正交性验证与对应正交变换(与 F3 剪切矩阵类型不同)",
    "linalg-069": "对偶基计算",
    "linalg-070": "辛形式在辛变换下的不变性",
    "prob-038": "条件概率计算",
    "prob-039": "几何概型估算圆周率",
    "prob-040": "二项分布泊松近似说明",
    "prob-041": "正态密度参数对形状的影响",
    "prob-042": "伯努利大数定律(频率→概率)",
    "prob-043": "中心极限定理(样本均值分布)",
    "prob-046": "可列可加性几何展示",
}


def main() -> int:
    try:
        raw = json.loads(RAW.read_text("utf-8"))
        ids = [r["id"] for r in raw["records"]]
        if len(ids) != 47 or len(set(ids)) != 47:
            raise ValueError("raw record list invalid")
        member_ids = [m for f in FAMILIES for m in f["members"]]
        for m in member_ids:
            if m not in ids:
                raise ValueError("family member not in records: " + m)
        if len(set(member_ids)) != len(member_ids):
            raise ValueError("family membership overlap")
        claimed = set(member_ids) | set(SINGLETONS)
        if claimed != set(ids):
            raise ValueError("coverage mismatch: missing=" + str(set(ids) - claimed))
        independent_tasks = len(SINGLETONS) + len(FAMILIES)
        report = {
            "schema": "train-core-families-v1",
            "status": "PENDING_CODEX_REVIEW",
            "bindings": {
                "manifest_sha256": raw["manifest_sha256"],
                "record_shas": {r["id"]: r["record_sha256"] for r in raw["records"]},
                "raw_source": str(RAW.relative_to(ROOT)),
                "raw_sha256": hashlib.sha256(RAW.read_bytes()).hexdigest(),
            },
            "families": FAMILIES,
            "singletons": SINGLETONS,
            "counts": {
                "records": 47,
                "families": len(FAMILIES),
                "family_members": len(member_ids),
                "singletons": len(SINGLETONS),
                "independent_tasks": independent_tasks,
                "note": "独立样本计数=每族 1 + 每单体 1;数值/轴互换不增加样本或形式",
            },
            "unresolved": [
                "F4(050/053)与 F5(024/026)是否同核心族待 Codex 裁定",
                "F1 四种曲线是否算「真正不同变体形式」待裁定",
                "47 题小样本描述不能宣称 53 考点全达标(仅描述现役训练池内部结构)",
            ],
        }
        if OUT.exists():
            raise ValueError("output exists")
        with OUT.open("x", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(report, ensure_ascii=False, indent=1) + "\n")
        print(json.dumps(report["counts"], ensure_ascii=False, indent=1))
        print("out:", OUT)
        return 0
    except Exception as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
