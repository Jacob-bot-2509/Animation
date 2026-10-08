# batch-01 首批 15 道补充题起草报告 v3

- 版本链:v1(`draft.jsonl`)→ v2(3 题重写+12 题修正,用户批准)→ Codex 复审发现 c52-05 新目标与冻结题分布重合 → v3(本版)
- 文件:`draft-v3.jsonl`(15 行 JSONL),SHA256 = `d4a722d596042f6bb3db4c2b64b0f4f816e161b00f474bc03a7f8716f67d4fb4`
- 生成器:`build_draft_v3.py`(v2 基础上按 id 吸收 Codex 提案三行);v1/v2 原字节保留
- 声明:起草过程非盲测(本会话已接触冻结评测材料的相关讨论);Codex 复审发现 v2 的 c52-05 目标分布 f=3x²(0<x<1) 与冻结 test-prob-004 的 CDF 核心相同,故按 Codex 提案改为分段目标;其余 12 题保留 v2 内容

## 本版三处修改(全部取自 Codex 提案 draft-v3-review-proposal.jsonl)

| 题号 | 修改 |
|---|---|
| draft-c01-02 | 题干补「具有有限斜率的切线」,明确可微性对应有限斜率 |
| draft-c36-01 | 题干前置正定约定:「本题正定矩阵指实对称且二次型对所有非零实向量为正的矩阵」 |
| draft-c52-05 | 整体重写:目标改为分段密度 $g(z)=\frac12(0<z<1)$、$z-1(1<z<2)$;PIT 定理放宽为连续分布函数+严格递增区间假设;构造分段逆 $T(u)=2u(u\le\frac12)$、$1+\sqrt{2u-1}(u>\frac12)$,并解释必须分段 |

### c52-05 独立验算(作者复核 Codex 提案)

- 归一化:$\int_0^1\frac12\,dz+\int_1^2(z-1)\,dz=\frac12+\frac12=1$ ✓
- CDF:$G(z)=z/2(0<z\le1)$、$\frac12+\frac{(z-1)^2}{2}(1<z<2)$、外侧 $0/1$;在 $z=1$ 处 $G(1)=\frac12$ 两侧一致,连续无跳跃、无原子 ✓
- 反函数:$u=z/2\Leftrightarrow z=2u$(适用 $z\le1\Leftrightarrow u\le\frac12$)✓;$u=\frac12+\frac{(z-1)^2}{2}\Leftrightarrow z=1+\sqrt{2u-1}$(取 $z>1$ 正支,适用 $u>\frac12$)✓
- 事件等价:$T(U)\le z$ ⟺ $U\le G(z)$ 逐段验证 ✓;故 $Z=T(U)$ 的分布恰为 $G$,密度为 $g$ ✓
- PIT 假设:$F$ 连续、在 $I$ 上严格递增、$P(X\in I)=1$、$F(I)=(0,1)$ ⟹ 除零概率事件外 $F(X)\le y\Leftrightarrow X\le F_I^{-1}(y)$,得 $P(Y\le y)=y$ ✓

## 状态与后续

- 全部 15 题 `draft_status = draft-v3-…-待用户审阅`;未入库、未改活动清单/锁/资产证据/训练工具;未开训
- 本版 c52-05 内容为新改写,须用户重新逐题审阅(v2 认可不自动延续到新内容)
- 用户审阅 + Codex 对 v3 复验通过后,由 Codex 走入场冻结流程
