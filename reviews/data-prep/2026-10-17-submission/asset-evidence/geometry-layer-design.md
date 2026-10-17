# 几何层设计(首批 10 题)

状态:DESIGN(设计先行,不实现、不渲染)。依据 Codex 907 §五/六:
"几何层请先出设计(哪些题、哪类模板、F 指标如何取证)再实现;渲染不得绕开
check_certificate;不要用存在/进程/退出码当渲染或数学证据。"

范围:首批 10 题(修正记录 archives/.../2026-10-17-first-batch-exact-math-review/
candidate/records.jsonl)。全量模板库待题目池定型后按本设计扩展。

## 一、哪些题 → 哪类几何模板

| 题 | 几何需求(修正 scene_spec objects 已精确定义) | 模板类 |
|---|---|---|
| calc-limit-006 | 单位圆 u²+v²=1、O/A/B/C/D 五点坐标、扇形 OAB、△OAB、△OAC、射线、切线 u=1 | `unit_circle_squeeze`:圆+点+扇形+三角形+精确面积标注 |
| eval-prob-007-s1 | 365 格、30 个带序号人物、逐项可选数 365−k | `birthday_grid`:格阵+带序占位+逐项计数动画 |
| prob-046 | 半开矩形族 R_k=(2⁻ᵏ,2¹⁻ᵏ]×[0,1]、零面积边界 R₀、部分和 S_N=1−2⁻ᴺ | `partition_rectangles`:半开矩形族+端点归属+部分和 |
| prob-042 | F_n 折线轨迹、y=1/2 水平线、ε 阈值带、方差 1/(4n) 展示 | `frequency_trajectory`:折线+水平线+阈值带+公式栏 |
| prob-043 | U[0,1] 演示总体、n=2 精确分段密度 4t/4(1−t)、两横轴对比、正态比较曲线 | `density_comparison`:密度函数族+双轴+比较曲线 |
| calc-double-integral-004 | 圆盘 D、曲顶 z=1−x²−y²、极坐标 r dr dθ、有限黎曼柱 | `riemann_cylinders`:圆盘+曲顶+有限柱+面积元 |
| calc-green-005 | 圆周 L、向量场 F=(−y,x)、圆盘 D、偏导差 Q_x−P_y=2 | `vector_field_circle`:圆周+向量场箭头+圆盘填充 |
| calc-series-015 | 交错项 (−1)ⁿ/√n、部分和 S_N、余项界、发散下界柱状图 | `alternating_bars`:交错柱+部分和折线+界带 |
| calc-series-017 | 部分和族 S_N(x)、上下界 ±π²/6、误差带 S₂₀₀±E₂₀₀ | `uniform_bound_band`:曲线族+界带+误差带 |
| calc-vol-012 | y=arcsin x 区域、绕 x 轴旋转、截面圆盘半径 arcsin x | `solid_of_revolution`:区域+旋转体+截面圆盘 |

## 二、每类模板的 F(画面忠实度)取证合同

F 定义(协议 §6.3):逐题锁定语义清单,对实际完整画面核对对象、坐标/曲线、
步骤顺序、视觉关系与叙述;每项有时间/帧定位与判定理由。

每类模板须产出 `fidelity-checklist.json`(渲染前锁定),逐项格式:
{item_id, what, expected_value(精确分数/符号/坐标), frame_range, verdict,
 reason}。渲染后由审核方逐项核对真实帧并填 verdict;清单缺失或未核对 → F=UNVERIFIED。

各模板 F 取证要点(示例,实现时逐题细化):

| 模板 | F 必查项(核心) |
|---|---|
| unit_circle_squeeze | 圆心 (0,0)、半径 1;A=(1,0)、B=(cos x,sin x)、C=(1,tan x)、D=(cos x,0) 的坐标落点;扇形与两三角形填充正确;面积标注 sin x/2、x/2、tan x/2 与对应图形一致 |
| birthday_grid | 365 格数、30 个占位序号、第 k+1 人可选数 365−k 的逐项显示与格数一致 |
| partition_rectangles | R_k 半开边界(左开右闭)视觉可辨;S_N=1−2⁻ᴺ 标注与已画矩形总面积一致;有限帧不冒充无穷 |
| frequency_trajectory | 折线点按真实序列计算(无真实序列时只显示公式,不伪造点);阈值带 ±ε 位置正确 |
| density_comparison | n=2 均值的精确分段密度 4t（0≤t≤1/2）与 4(1−t)（1/2≤t≤1），分界 1/2；双横轴标注不混用；正态曲线仅作比较且标注"比较" |
| riemann_cylinders | 柱采样点高度 (1−ξᵢ²−ηᵢ²)ΔAᵢ 与曲面一致;有限柱标注"黎曼和,非精确实体" |
| vector_field_circle | 箭头方向与 (−y,x) 逐点一致(抽样点可复核);圆盘面积标注 πa² |
| alternating_bars | 交错项符号与柱色;余项界 1/√(N+1) 标注;发散下界 2(√(N+1)−1) 与柱高和一致 |
| uniform_bound_band | 上下界 ±π²/6;S₂₀₀±E₂₀₀ 误差带夹住部分和曲线;S₂₀₀ 标注为有限多项式 |
| solid_of_revolution | 区域 0≤y≤arcsin x 边界;截面圆盘半径=arcsin x 的位置对应;旋转体轮廓与区域一致 |

## 三、实现顺序与门禁

1. 本设计经 Codex 审查定稿;
2. 逐模板实现(独立候选目录,每模板带 F 清单生成器+纯逻辑自测);
3. 渲染一律走 check_certificate() + 获准入口(exec_isolation 验收后);
4. 真实渲染 → 逐帧 F 核对(Codex 数学/质量 + 用户目视)→ F 取证入证据;
5. 不缩字冒充可读、不做通用几何声明(逐题绑定)、失败显式。

## 四、如实边界

- 本设计不解决 layout(原生测量 UNVERIFIED)、不解决数学审核、不解决渲染许可;
- 几何模板覆盖仅首批 10 题;496 条与补充题的模板扩展待题目池定型;
- F 取证依赖真实帧,夹具只能验证清单结构与纯逻辑,不能验证画面。

## 五、与文字候选的合成边界（Codex 补，2026-10-17）

- 现模板 `scene_blocks_v2` 的段落以 `if self.mobjects: raise candidate_requires_dedicated_empty_canvas` 开头，只能在空白画布上独占一页；几何模板不能与文字行同屏拼贴。
- 合成方式二选一，实现时须写明并具名：
  1. **分场**：几何场景与文字场景是两个独立 `Scene`，同题视频由页序列拼接，F 清单按帧区间分别记录；
  2. **模板 v4**：几何块输出为可组合 `VGroup` 并接收"已有内容"参数，同时替换空白画布前置断言；须新版本文件 + 回归，不覆盖 v2/v3。
- 未合成前，审核包里的 `scene.py` 仍只是文字候选；不得把本设计当成已实现或已渲染。

## 六、呈现保真硬约束（Codex 补，2026-10-17）

- **等比例**：几何场景不得非等比例缩放（squeeze 的面积比较、圆周/切线位置都依赖真实比例）；确需缩放时必须在 F 清单记录比例因子并逐项核对。
- **精确值**：F 清单必须含该题精确结论值，并核对画面标注一致：calc-limit-006 `1`；calc-double-integral-004 `π/2`；calc-green-005 `2πa²`；calc-series-015 条件收敛，`|S−S_N|≤1/√(N+1)`；calc-series-017 `E_N=π²/6−Σ_{n=1}^N 1/n²→0`；calc-vol-012 `π³/4−2π`；eval-prob-007-s1 `1−365!/(335!·365³⁰)`；prob-042 `P(|F_n−½|≥ε)≤1/(4nε²)`；prob-043 `√n(X̄_n−μ)/σ →d N(0,1)`；prob-046 `S_N=1−2⁻ᴺ→1`。不得用近似小数替代。
- **三维**：`solid_of_revolution` 与 `riemann_cylinders` 若用 ThreeDScene，须锁定相机角度/焦距并在 F 清单记录，否则轮廓随视角变化无法复核。

