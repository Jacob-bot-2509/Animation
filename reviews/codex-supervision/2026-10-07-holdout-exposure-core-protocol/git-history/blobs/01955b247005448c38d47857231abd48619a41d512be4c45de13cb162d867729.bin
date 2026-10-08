# HARNESS_PARALLEL_RENDER_REPORT.md

**src/animtrain 并行渲染验证报告**
**日期**：2026-10-01 00:5x (Etc/GMT-8)
**起始 git HEAD**：`a81223ea46def98b16699fc45ba058b9d7e393ec` · **结束时 HEAD**：`d90d13e4424e5b53aa763071c2cb0f5a975176cb`
**执行者**：DSH 自动化 agent（DeepSeek-V4-Flash / `deepseek-official/deepseek-flash`）
**环境**：Python 3.13.13 · manim 0.21.0 · sympy 1.14.0 · ffmpeg `D:\Settings\ffmpeg\bin`
**前提**：用户报告 MiKTeX 已更新，`MathTex` / `Tex` 崩溃问题已修复（本报告 §2 已独立复核）

> 本文件为**新建**文件。**我本人未修改**任何现有源代码或文档。
> ⚠️ 执行期间工作区存在**另一个并发写入者**：它提交了新 commit，并改动了 5 个受版本控制的文件。`git status` 中除本报告与 `reviews/2026-10-01-br-recheck-round2/` 之外的改动**都不是我造成的** —— 详见 **§10**。

---

## 0. 摘要

| 项目 | 结果 |
|---|---|
| `src/animtrain` 下 Manim **场景文件** | **0 个** |
| 实际执行的渲染场景 | 8 个（验证矩阵） |
| **渲染成功** | **7** |
| **渲染失败** | **1**（**预期失败**：中文进 TeX） |
| 8 路并行总墙钟 | **4.27 s** |

**两句话结论**：

1. **MiKTeX 修复已确认生效** —— 4 个此前必然失败的 `MathTex` / `Tex` 场景现在**全部渲染成功**（§3、§5.1）。
2. **但 `src/animtrain` 里依然没有任何 Manim 场景文件**（§1），所以"对包含场景类的文件渲染"没有原生对象；本报告用一组验证场景覆盖了第 3 步真正要确认的问题。

---

## 1. 扫描结果：`src/animtrain` 无渲染目标

按要求扫描 `src/animtrain` 下全部 `.py`（排除 `__pycache__`），共 **14 个文件**：

```
__init__.py  atomic_write.py  calibrate.py  code_gate.py  fields.py  freeze.py
fs_guard.py  manifest.py  near_dup.py  preflight.py  render_gate.py
run_record.py  scan.py  validate.py
```

| 检查 | 方法 | 结果 |
|---|---|---|
| 是否定义 Manim 场景类 | AST 遍历所有 `ClassDef` 的基类（`Scene`/`ThreeDScene`/`MovingCameraScene`） | **0 个** |
| 是否含 `MathTex` / `Tex` | 全文正则 | **共 2 处**，均在 `code_gate.py`（`L7`、`L37`），均为**静态检查逻辑**，非场景代码 |
| 是否有可渲染的 `construct()` | AST | **0 个** |
| 是否有真正的 `MathTex(...)` / `Tex(...)` 调用 | AST `Call` 节点 | **0 个** |

`code_gate.py` 里那两处的原文分别是：

```
L7 :   3. 中文-LaTeX: MathTex/Tex/Title 等 LaTeX 家族字符串里含中文 → 报        （模块 docstring）
L37:   LATEX_CALLS = {"MathTex", "Tex", "Title", "BulletedList", "DecimalNumber",   （静态检查的名字集合）
```

`L37` 的集合被 `code_gate.py:113-114` 的正则用来**扫描别人代码的源文本**。两者都是**检查别人代码的规则**，本身不会被 manim 渲染。

> **更正**：本节初版写作"仅 1 处"，漏了 `L37`。已按独立审计子智能体的指正修正为 **2 处**（结论不变：均非场景代码）。

其余 13 个文件是清单 / 校验 / 拆分 / 冻结 / 近重复 / 运行记录等纯标准库模块。

**结论**：第 2 步"对包含 Manim 场景类的文件并行运行 manim"在本目录下**没有原生对象**。这不是执行失败，而是目录性质如此 —— `src/animtrain` 是**渲染门禁本身**（`render_gate.py` 的执行对象是**运行时传入的代码字符串**，不是磁盘上的场景文件）。

因此，本报告改为对**一组验证场景**执行 8 路并行 `manim -ql`，正好覆盖第 3 步指定的重点：**确认环境修复后 `MathTex` / `Tex` 能否正常渲染**。

---

## 2. 环境修复复核（先证明前提成立）

| 检查 | 修复前（2026-09-30 23:44 实测） | 修复后（本次实测） |
|---|---|---|
| 最小 LaTeX 文档 | `latex` 退出码 **-1073740791**（`0xC0000409` 栈溢出），DVI 却已产出 | **退出码 0**，DVI 正常产出 |
| `MathTex(r"f'(x) = 2x")` | **失败** exit=1（`latex error converting to dvi`） | **成功** exit=0，mp4 产出 |

```powershell
# 最小文档
latex -interaction=nonstopmode m.tex
# 修复前: exit=-1073740791 (DVI 已产出)   修复后: exit=0
```

**前提成立**：MiKTeX 崩溃确实已修复。

---

## 3. 并行渲染矩阵结果（8 路并行，实测）

命令统一为：`manim -ql --media_dir <scratch>\out <scene>.py ConceptScene`
并行方式：`ThreadPoolExecutor(max_workers=8)` —— **8 个 manim 进程真正同时运行**。

| # | 场景 | 验证用途 | 退出码 | 产出 mp4 | 耗时 | 错误 |
|---|---|---|---|---|---|---|
| 1 | `01_mathtex_ascii` | `MathTex(r"f' (x) = 2x")` | **0** | ✅ | 4.26 s | — |
| 2 | `02_tex_plain` | `Tex(r"$E = mc^2$")` | **0** | ✅ | 3.88 s | — |
| 3 | `03_mathtex_aligned` | `MathTex(r"\int_0^1 x^2 \, dx = \frac{1}{3}")` | **0** | ✅ | 4.24 s | — |
| 4 | `04_mathtex_matrix` | `MathTex(r"\begin{pmatrix} a & b \\ c & d \end{pmatrix}")` | **0** | ✅ | 3.60 s | — |
| 5 | `05_mathtex_chinese` | `MathTex(r"\text{斜率}")` | **1** | ❌ | 2.94 s | `ValueError: latex error converting to dvi`（**预期**） |
| 6 | `06_text_chinese` | `Text("导数 = 切线斜率")` | **0** | ✅ | 3.06 s | — |
| 7 | `07_axes_plot` | `Axes` + `plot(x**2)` | **0** | ✅ | 2.72 s | — |
| 8 | `08_combined_mathtex` | 中文 `Text` 标题 + `Axes` + 抛物线 + 切线 + `MathTex` 公式 | **0** | ✅ | 4.05 s | — |

**汇总：8 个场景，成功 7 个，失败 1 个。总墙钟 4.27 s**（8 路并行；若串行，各场景耗时之和约 28.8 s）。

> **注意第 5 项是"预期失败"**：中文进 TeX 受 TeX 无 CJK 的物理限制，修复 MiKTeX 也**不会**让它通过。这正是项目 `check_latex_cjk` 规则要拦的情况。

### 场景源码（可复现）

```python
# 01
from manim import *
class ConceptScene(Scene):
    def construct(self):
        self.play(Write(MathTex(r"f' (x) = 2x")))

# 03
        self.play(Write(MathTex(r"\int_0^1 x^2 \, dx = \frac{1}{3}")))

# 04
        self.play(Write(MathTex(r"\begin{pmatrix} a & b \\ c & d \end{pmatrix}")))

# 05
        self.play(Write(MathTex(r"\text{斜率}")))

# 08
        ax = Axes(x_range=[-1.5, 2.5], y_range=[-1, 5], x_length=5.0, y_length=3.2)
        curve = ax.plot(lambda x: x ** 2, x_range=[-1.2, 2.2], color=BLUE)
        tan = ax.plot(lambda x: 2 * x - 1, x_range=[0, 2], color=YELLOW)
        title = Text("导数 = 切线斜率", font_size=30).to_edge(UP)
        formula = MathTex(r"f' (x) = 2x", font_size=40).to_corner(DR, buff=0.5)
        self.play(Write(title), run_time=0.8)
        self.play(Create(ax), Create(curve), run_time=1.2)
        self.play(Create(tan), Write(formula), run_time=1.2)
```

---

## 4. 失败项完整错误日志

### 4.1 `05_mathtex_chinese`（唯一失败，预期）

```
File "…\manim\utils\tex_file_writing.py", line 218, in compile_tex
    raise ValueError(
ValueError: latex error converting to dvi. See log output above or the log
file: D:\Animation Model Training\.render_matrix\05_mathtex_chinese\out\Tex\24eb86309c16d910.log
```

**判定**：这是**预期失败**，不是环境故障。TeX/pdfTeX 不含 CJK 字体与排版规则，`\text{斜率}` 必然编译失败。**修复 MiKTeX 不改变这一点**。项目"中文用 `Text()`"的约定此时**依然必须遵守**。

**正确做法**（本矩阵第 8 项已验证可行）：中文用 `Text()`，公式用 `MathTex()`，两者可以混用在同一个场景里。

---

## 5. 关键结论

### 5.1 MiKTeX 修复确认：`MathTex` / `Tex` 已恢复可用

修复前失败、现在成功的 4 个场景：

| 场景 | 修复前 | 现在 |
|---|---|---|
| `01_mathtex_ascii` | ❌ `latex error converting to dvi` | ✅ exit 0，4.26 s |
| `02_tex_plain` | ❌ 同上 | ✅ exit 0，3.88 s |
| `03_mathtex_aligned`（积分/分式） | ❌ 同上 | ✅ exit 0，4.24 s |
| `04_mathtex_matrix`（矩阵） | ❌ 同上 | ✅ exit 0，3.60 s |

**目视确认**（抽帧检查，非仅看退出码）：

- `01_mathtex_ascii` 渲染帧中正确显示数学斜体的 **`f'(x) = 2x`**
- `04_mathtex_matrix` 渲染帧中正确显示带括号的 **2×2 矩阵** `(a b; c d)`

即：不只是"退出码 0"，**字形确实正确渲染出来了**。

### 5.2 中文进 TeX 的约束**仍然成立**

- `05_mathtex_chinese` 依然失败。
- 因此 `code_gate.py` 的 `check_latex_cjk` 规则**依然必要且正确**，不应因 MiKTeX 修复而放宽。
- `06_text_chinese`（中文走 Pango）成功 → **中文的正确通道仍然是 `Text()`**。

### 5.3 性能观察

8 个场景（含 4 个 LaTeX 场景）在 8 路并行下总墙钟仅 **4.27 s**；单个 LaTeX 场景约 3.6–4.3 s、纯 `Text`/`Axes` 场景约 2.7–3.1 s。**MiKTeX 修复后没有明显性能退化**。

---

## 6. 关于并行方式与 `dsh-tool-retry`（如实说明）

### 6.1 并行方式

- **实际并行**：8 个 `manim -ql` **进程**通过 `ThreadPoolExecutor(max_workers=8)` 真正同时执行（这正是"最多 8 个并行"要达成的效果）。
- **未启用 8 个 LLM 子智能体**：本任务的渲染目标是**不存在**的（§1），且 8 次调用都是**亚秒到数秒级的 CLI 进程**。用 8 个 LLM 子智能体去跑 8 条命令，开销远大于收益，记录也更难保证精确。
- **另派出 2 个 DeepSeek-V4-Flash 子智能体做独立验证**（§9），用的正是指定模型：一个独立复核 MiKTeX 修复与 `MathTex` 渲染，一个对抗性复查"是否真的不存在场景文件"。

### 6.2 `dsh-tool-retry`

**未触发**，且**不应触发**：本次唯一的失败（`05_mathtex_chinese`）根因是 **TeX 不支持 CJK** 这一物理约束，不是"代码写错导致渲染崩了"。重试或"自动修复"只会重复失败；正确处置是**改用 `Text()`**（§5.2）。

---

## 7. 复现命令

```powershell
# 环境复核
latex -interaction=nonstopmode m.tex        # 期望 exit=0

# 单场景渲染
$env:PATH = 'D:\Settings\ffmpeg\bin;' + $env:PATH
& '.\.venv\Scripts\python.exe' -m manim -ql --media_dir <scratch>\out <scene>.py ConceptScene

# 抽取帧目视确认
ffmpeg -ss <t> -i <mp4> -frames:v 1 -y out.png
```

## 8. 未覆盖 / 限制（不做假绿）

- **`src/animtrain` 内的场景渲染**：**不存在可渲染对象**（§1），故未执行，也**不能**声称"该目录下的文件全部渲染通过"。
- **`05_mathtex_chinese`**：按预期失败，**不计入"环境问题"**；若按"成功/失败"机械统计，失败数为 1。
- **其他 LaTeX 家族对象**（`Tex` 的多行/自定义宏、`MathTex` 的 `substrings_to_isolate`、`BulletedList` 等）未逐一覆盖。
- **高负载下的并行**：本次 8 路并发对 LaTeX 场景未见资源问题，但**未做**更高并发或长时动画（`-qh`、长 `run_time`）的压力测试。
- 本报告验证的是**渲染能力**；不等于某份生成代码已通过 L4 全部门禁（那还需语法 / API / 数学分项与输入 hash 记录）。

---

## 9. 独立验证子智能体结论

本次派出 2 个 DeepSeek-V4-Flash 子智能体做独立验证（均在工作区**只读**运行）。

### 9.1 子智能体 B —— 对抗性复查"是否存在 Manim 场景文件"

**结论：`src/animtrain` 部分 CONFIRMED（无法证伪）**，与 §1 一致。关键增量证据：

- AST 遍历 14 个文件：`calibrate.py:19 CalibrationReport`、`manifest.py:25 Entry`、`manifest.py:43 Manifest`、`near_dup.py:41 ShingleIndex`、`run_record.py:19 RunRecord` —— **全部基类为空**，**没有任何类继承 Manim 场景类型**。
- AST `Call` 节点扫描：14 个文件中 **`MathTex(...)` / `Tex(...)` 调用数为 0**。
- 字符串字面量扫描（防"场景代码藏在字符串里"）：14 个文件中 **0 处**。
- 全项目（排除 `.venv`）49 个 `.py` + 225 个其他文本文件的忽略感知全量扫描：**没有独立场景文件**。
- git：205 个受控文件无场景文件；全历史无场景路径；已删除文件中也无场景文件。
- 明确排除 `.venv\Lib\site-packages\manim\`（上游库，168 个 `.py`）并说明了排除理由。

**它给出一个重要更正**：本报告初版称 `code_gate.py` 中 `MathTex` "仅 1 处"是**错的**，实为 **2 处**（`L7` docstring + `L37` `LATEX_CALLS`）—— 已在 §1 更正。

> 它还把我在 `.render_matrix/` 下**临时生成、随后删除**的 8 个验证场景列为"字面意义上的反例"，并明确指出这些是**审计期间由并发写入者创建并删除的临时文件**，不属于项目内容。这个区分是准确的。

### 9.2 子智能体 A —— 独立复核 MiKTeX 修复与 `MathTex` 渲染

（结果回传后补入；本报告 §2–§5 的全部数据均为主执行者**本人实测**，不依赖子智能体。）

---

## 10. ⚠️ 执行期间工作区被并发写入（重要）

本次执行**不是**在静止的工作区里完成的。执行窗口内检测到**另一个写入者**：

| 观察 | 内容 |
|---|---|
| `git HEAD` 变化 | `a81223ea` → **`d90d13e`**（提交信息："dvisvgm 根因修复:render_check 的 cwd 含空格导致转换崩溃(msg_141)"） |
| 新增 commit | `d90d13e`、`02f07cc`、`fa18092`、`a24c0d7` 等（BR2/4/5/6 复验修复、渲染隔离标注等） |
| 未提交的受控文件改动 | `REVIEW_BACKLOG.md`、`src/animtrain/freeze.py`、`tests/test_freeze.py`、`tools/preflight.py`、`tools/split_data.py`（`git diff --stat`：+127 / −21） |
| 新增目录 | `reviews/2026-10-01-br-recheck-round2/`（`probe.py`、`results.json`、`REVIEW.md`） |

**这些改动全部不是本报告作者所为。** 按项目既定规则"未知或无关改动保留"，我**没有触碰**其中任何一个文件。

### 10.1 一个需要你知道的瞬时故障（现已自愈）

子智能体 B 在 `00:53:54` 观察到 `tools/preflight.py` **语法损坏**（`SyntaxError: line 87: unterminated string literal`），疑为并发写入者**写到一半**的状态。我在 `00:5x` 复核时 **`ast.parse` 已通过、语法正常** —— 该损坏是**瞬时的**，写入者已完成写入。

交叉验证：对 `src/`、`tools/`、`tests/` 下全部 `.py` 做语法检查，**0 个语法错误**。

### 10.2 对本人结论的影响

- §1 的场景扫描已在 **`d90d13e`** 上**重新复核**：仍是 **14 个文件、0 个场景类** —— 结论不受并发改动影响。
- 但请注意：**`src/animtrain/render_gate.py` 已经演进**（现签名为 `render_check(code, python=None, trusted=False)`，默认 `trusted=False` 时**拒绝执行**，属 fail-closed 设计）。因此我此前另一份报告 `RENDER_GATE_VERIFICATION.md` 是针对**旧版** `render_gate.py`（无 `trusted` 参数）写的，**该报告已部分过时**，若要作为依据需按新代码重跑。

### 10.3 根因归因分歧（如实记录）

- 我 §2 的实测证明：修复前**用最朴素的 `latex m.tex`**（完全不涉及 manim、不涉及 `render_check`）也会崩溃（退出码 `-1073740791`，DVI 却已产出），修复后退出码 0 → 指向 **MiKTeX 层面的故障**。
- 并发写入者的 commit 信息则把根因归为"**`render_check` 的 cwd 含空格**导致转换崩溃"。

两者**并不互斥**（可能先后存在两个不同故障），但**根因归属尚未统一**。本报告只声明我能直接证明的部分：**修复后 `MathTex` / `Tex` 确实能正常渲染**（§3–§5：7/8 成功，含 4 个 LaTeX 场景）。根因的最终归属建议由该项目主责实现者统一结论。
