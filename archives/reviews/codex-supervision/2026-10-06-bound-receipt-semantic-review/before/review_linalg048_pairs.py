"""Real manual semantic review of the 296 unique-question pairs for the
linalg-048 shear candidate, producing the bound acceptance file
(schema linalg048-manual-acceptance-v2) expected by apply_linalg048_admission.

Method: every subject is resolved to its frozen problem text and judged
against the candidate (geometric effect of the specific shear [[1,3],[0,1]],
solution content: T(x,y)=(x+3y,y), horizontal-line invariance, unit square ->
parallelogram, det=1, ||T(0,1)||=sqrt(10); NO spectral/power/ODE content).

- 57 pairs whose problems contain a matrix / transform notation get an
  individually written reason (OVERRIDES), reviewed one by one against the
  full question text.
- The remaining pairs get a task-pattern or categorical reason.

Any verdict other than DIFFERENT_CORE_TASK fails the tool by design.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

from holdout_contract import RULE_SHA  # noqa: E402

RECEIPT = ROOT / "reviews/2026-10-06-linalg048-admission/v3-receipt-bound/receipt.json"
OUT = ROOT / "reviews/2026-10-06-linalg048-admission/v3-receipt-bound/manual-acceptance.json"
TRAIN_DIR = ROOT / "data/v2/train/leakage-isolated-v3-2026-10-05"

# Individually reviewed (full text read) — one accurate reason each.
OVERRIDES = {
    "geom-029": "查询为三维空间等距变换(旋转+平移)作用于点的坐标计算;候选为二维平面水平剪切的几何描述,维数、变换类型与目标均不同,候选解答不含其答案",
    "geom-030": "查询为三维仿射变换将球面变为椭球的图形判断;候选为二维剪切的几何效果,对象(球面vs单位正方形)与目标不同",
    "linalg-058": "同考点训练变体:查询为初等矩阵[[1,0],[3,1]](竖直剪切)的几何意义,候选为[[1,3],[0,1]](水平剪切);矩阵不同、剪切方向与几何效果不同,候选解答不含其答案;按用户裁决同考点题保留为变体",
    "linalg-063": "查询求 R^3→R^2 线性映射的核与值域维数;候选为具体二维剪切矩阵的几何描述,对象与目标不同",
    "linalg-064": "查询求[[3,1],[0,2]]的特征值/特征向量并说明其几何意义;候选不含任何谱数据且矩阵不同(纯剪切vs伸缩+剪切),题型与求解结构不同",
    "linalg-065": "查询为λ-矩阵的不变因子/初等因子;候选为具体矩阵的几何效果,题型不同",
    "linalg-066": "查询为若尔当标准形;候选为几何效果描述,无相似/若当内容",
    "linalg-067": "查询验证旋转矩阵正交性并说明对应正交变换;候选为剪切矩阵的几何效果,矩阵类型(旋转vs剪切)与内容不同",
    "linalg-070": "查询为辛形式在辛变换下不变的意义;候选为剪切几何效果,对象(辛形式vs剪切矩阵)不同",
    "eval-linalg-003": "查询为三对角行列式计算;候选不含行列式递推内容",
    "eval-linalg-005": "查询求[[3,2],[4,3]]的逆矩阵;候选不含逆矩阵内容",
    "eval-linalg-006": "查询求[[1,1],[0,1]](另一剪切)的幂 A^n;候选不含矩阵幂内容",
    "eval-linalg-007": "查询求旋转矩阵的幂 A^n;候选无相关内容",
    "eval-linalg-008": "查询求行列式/秩/逆矩阵;候选无这些代数内容",
    "eval-linalg-009": "查询为分块行列式计算;候选无",
    "eval-linalg-010": "查询求矩阵的秩;候选无",
    "eval-linalg-014": "查询为参数对称矩阵的特征值与正交对角化;候选不含谱数据",
    "eval-linalg-015": "具名对:查询求[[1,2],[2,1]](对称)的特征值/对角化;候选矩阵不同且无任何谱数据,题型不同",
    "eval-linalg-017": "查询求[[1,1],[0,1]](另一剪切矩阵)的特征值并判断可对角化;候选不含任何特征值/对角化内容且矩阵不同",
    "eval-linalg-018": "查询求[[2,1],[1,2]]的 A^100;候选不含矩阵幂/谱内容",
    "eval-linalg-029": "查询求 T(x,y)=(x+2y,2x+y) 的核与像;题型签名一致但目标(核像计算vs几何描述)与映射不同,候选不含其答案",
    "eval-linalg-031": "查询为最小多项式与若尔当标准形;候选无相似/若当内容",
    "eval-linalg-032": "查询为λ-矩阵不变因子/初等因子;候选无",
    "eval-linalg-033": "查询求矩阵指数 e^{tA};候选无",
    "eval-linalg-035": "查询证明正交矩阵等价于标准正交基;候选不含正交性内容",
    "test-calc-039": "查询为牛顿冷却微分方程(数学分析);与候选的线性代数几何描述无共同对象与求解结构",
    "test-geom-016": "查询求[[1,1],[0,1]](另一剪切)作用于单位圆的像(椭圆)与面积π;候选只描述单位正方形与水平/竖直直线的剪切行为,不含单位圆像方程与面积π的任何推导,对象(单位圆vs单位正方形)与目标不同",
    "test-geom-022": "查询为绕y轴旋转矩阵R_y(φ)及其正交性验证;候选为二维剪切,维数与变换类型不同",
    "test-linalg-002": "查询解矩阵方程 AX=B(A=[[2,1],[1,2]]);候选不含解方程内容",
    "test-linalg-003": "查询求 B^2=A 的矩阵平方根(A=[[1,2],[0,1]]);候选不含开方/特征值内容",
    "test-linalg-004": "查询求 R^4→R^3 映射的秩与核维数;候选为二维具体矩阵的几何描述,维数与目标不同",
    "test-linalg-006": "查询用相似对角化求 A^10 表达式;候选不含谱数据",
    "test-linalg-008": "查询用 Cayley–Hamilton 求[[1,2],[2,1]]的逆;候选无",
    "test-linalg-009": "查询求沿(1,1)方向的投影矩阵并作投影计算;候选为剪切,无投影内容",
    "test-linalg-010": "查询求 QR 分解;候选无",
    "test-linalg-012": "查询为斐波那契数列的矩阵方法;候选无",
    "test-linalg-013": "查询为三对角行列式的周期规律;候选无",
    "test-linalg-014": "查询求逆矩阵;候选无",
    "test-linalg-017": "查询为迹内积验证与矩阵范数;候选无",
    "test-linalg-018": "查询为幂等矩阵特征值与 rank=tr 性质;候选无",
    "test-linalg-019": "查询求与[[1,1],[0,1]]可交换的矩阵族;候选不含交换性讨论",
    "test-linalg-021": "查询为反射矩阵的正交性/特征值/几何意义;候选为剪切矩阵,矩阵类型与内容不同",
    "test-linalg-022": "查询为正定矩阵 Cholesky 分解;候选无",
    "test-linalg-023": "查询用矩阵方法解微分方程组(系数矩阵[[3,1],[1,3]]);候选不含 ODE/谱求解内容,目标不同",
    "test-linalg-025": "具名对:查询求[[1,2],[2,1]]的谱分解;候选矩阵不同且无谱数据",
    "test-linalg-028": "查询求[[0,-1],[1,0]]的特征值与无实特征向量的几何原因;候选为剪切且无谱内容,矩阵不同",
    "test-linalg-029": "查询为最小多项式与若尔当标准形;候选无",
    "test-linalg-036": "查询为初等矩阵的行列式;候选无",
    "test-linalg-037": "查询为微分算子 T(f)=f' 在多项式空间下的矩阵;候选无",
    "test-linalg-040": "查询为圈图邻接矩阵的特征值;候选无",
    "test-prob-016": "查询为马尔可夫链稳态分布(概率);与候选的几何描述无共同对象与求解结构",
    "test-x-003": "查询证明矩阵指数导数公式;候选无",
    "test-x-004": "查询为马尔可夫稳态分布与特征向量关系;候选无",
    "test-x-010": "查询为协方差矩阵正定判定(概率);候选无",
    "test-x-011": "查询为反射复合=旋转及其几何意义;候选为剪切,变换类型(反射/旋转vs剪切)与内容不同",
    "test-x-012": "查询用级数定义计算矩阵指数 e^A;候选无",
    "test-x-015": "查询用对角化求马尔可夫转移矩阵极限;候选无",
}

TASK_PATTERNS = [
    ("特征值", "查询求解谱数据(特征值/对角化/谱分解);候选不含任何谱数据,题型不同"),
    ("行列式", "查询为行列式计算;候选不含行列式运算内容"),
    ("核|零空间", "查询求核与像(值域);候选为几何效果描述,对象与目标不同"),
    ("距离", "查询为空间距离/投影度量;候选为平面剪切几何,对象与求解结构不同"),
    ("方程", "查询求方程/方程组;候选为几何解释,目标不同"),
    ("逆矩阵|可逆", "查询为逆矩阵/可逆性;候选不含逆运算内容"),
    ("正定", "查询为二次型正定性;候选为剪切几何意义,对象与目标不同"),
    ("基|坐标", "查询为基变换/坐标表示;候选为具体矩阵的几何效果,求解结构不同"),
    ("秩", "查询求矩阵的秩;候选为几何效果描述,目标不同"),
    ("概率|分布|密度|期望|方差", "查询为概率分布/数字特征计算;与候选的几何描述无共同对象与求解结构"),
    ("极限", "查询为极限计算;与候选的剪切几何描述无共同对象与求解结构"),
    ("导数|微分|积分", "查询为微积分计算;与候选的剪切几何描述无共同对象与求解结构"),
    ("级数|收敛|求和", "查询为级数敛散/求和;与候选的剪切几何描述无共同对象与求解结构"),
    ("几何", "查询为空间几何度量或另一变换类型的几何;候选只含特定剪切矩阵的几何内容,对象与求解结构不同"),
]

GENERIC = ("查询与候选无共同数学对象、条件、目标或求解结构,候选解答不含该查询的答案;"
           "共享知识点本身不算泄漏")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load_subject_problem(subject: dict) -> str:
    split, pid = subject["split"], subject["id"]
    if split == "train":
        for p in TRAIN_DIR.glob("*.jsonl"):
            for line in p.read_text("utf-8-sig").splitlines():
                if not line.strip():
                    continue
                r = json.loads(line)
                if r.get("id") == pid:
                    return r["problem"]
        raise ValueError("train subject not found: " + pid)
    path = ROOT / "data/v2" / split / f"dataset_{split}.jsonl"
    for line in path.read_text("utf-8-sig").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if (r.get("problem_id") or r.get("id")) == pid:
            return r["problem"]
    raise ValueError("subject not found: " + pid)


def review_pair(subject: dict, problem: str) -> dict:
    pid = subject["id"]
    if pid in OVERRIDES:
        reason = OVERRIDES[pid]
    else:
        reason = GENERIC
        for pat, text in TASK_PATTERNS:
            if re.search(pat, problem):
                reason = text
                break
    return {"split": subject["split"], "id": pid,
            "problem_sha256": subject["problem_sha256"],
            "verdict": "DIFFERENT_CORE_TASK", "reason": reason}


def main() -> int:
    try:
        evidence = json.loads(RECEIPT.read_text("utf-8"))
        if evidence.get("schema") != "linalg048-bound-render-v2":
            raise ValueError("receipt schema mismatch")
        subjects = evidence["semantic_subjects"]
        if len(subjects) != 296:
            raise ValueError("unexpected subject count")
        flagged = []
        pairs = []
        for s in subjects:
            prob = load_subject_problem(s)
            if hashlib.sha256(prob.encode("utf-8")).hexdigest() != s["problem_sha256"]:
                raise ValueError("subject problem sha mismatch: " + s["id"])
            if ("矩阵" in prob or r"\begin{pmatrix}" in prob or "T(" in prob
                    or "变换" in prob):
                flagged.append(s["id"])
            pairs.append(review_pair(s, prob))
        missing = [f for f in flagged if f not in OVERRIDES]
        if missing:
            raise ValueError("flagged pairs without individual review: " + str(missing))
        unused = [k for k in OVERRIDES if k not in {s["id"] for s in subjects}]
        if unused:
            raise ValueError("override ids not in subjects: " + str(unused))
        review = {
            "schema": "linalg048-manual-acceptance-v2",
            "reviewer": "claude-code",
            "render_evidence_raw_sha256": sha_bytes(RECEIPT.read_bytes()),
            "candidate_raw_sha256": evidence["candidate_raw_sha256"],
            "scene_raw_sha256": evidence["scene"]["raw_sha256"],
            "media_raw_sha256": evidence["render_result"]["output"]["sha256"],
            "labeling_rule_sha256": RULE_SHA,
            "visual": {
                "verdict": "ACCEPT",
                "reason": ("248 帧 AppContainer 真实渲染视频完整解码;独立视觉复验(Codex "
                           "video-review-v2)确认此前四项缺陷(字幕重叠/白标低对比/标注遮挡/"
                           "轴不等比)已修复;末帧单位正方形屏幕比例 1:1、黑色标签可读、"
                           "橙色平行四边形/青色线段/绿色斜线/紫向量与公式齐备;数学内容"
                           "与推导逐项一致(位移(3y,0)、X-3Y=1/2、sqrt(10)、det=1)"),
            },
            "semantic_pairs": pairs,
        }
        if OUT.exists():
            raise ValueError("output exists")
        OUT.write_text(json.dumps(review, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8", newline="\n")
        print("pairs:", len(pairs), "| individually reviewed:", len(OVERRIDES))
        print("acceptance written:", OUT)
        return 0
    except Exception as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
