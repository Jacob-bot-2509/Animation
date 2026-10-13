# 修改后代码独立复查（2026-10-03）

基线：HEAD `93667e6`，重点复查 `ced86a1`、`93667e6` 对上一轮反例的整改，以及未提交的 `appcontainer.py`。工作区在审查期间仍有并行编辑；结论绑定 `results.json` 的源码 SHA256 与 `source-snapshot/`，不把早期中间版本的错误算到后来版本。

结论：已有整改有效，但本轮仍有 **2 项 P1、2 项 P2**，不能关闭全部审查问题。仅留存审查与合成反例，没有修改业务源码、正式数据、冻结锁或系统目录权限，也没有启动训练、下载或安装。

## 待修复发现

### P1：生成器可直接覆盖冻结产物

位置：`tools/make_eval_test.py:275`。

大小写不敏感的 v1 路径拒绝已修复，但直接 `Path.write_text` 没有调用项目统一的冻结/别名写保护。只要输出目录不叫 v1，即使目标 `eval/dataset_eval.json` 已被有效锁覆盖，生成器仍返回 0 并改写文件。合成探针实际把已冻结的 22 字节文件改成 3 字节，随后锁校验报 SHA256 与 size 不一致。正式数据未触碰。

修复建议：在创建目录和写任何输出之前，统一检查两个目标、输入别名和自动发现的冻结锁；拒绝冻结文件及其硬链接别名，使用项目已有的可靠写入入口。只检查版本目录名无法替代冻结保护。

### P1：AppContainer 把成功 HRESULT 当失败，生成了错误的 SID

位置：`src/animtrain/appcontainer.py:162`。

`DeriveAppContainerSidFromAppContainerName` 返回 HRESULT，成功为 `S_OK=0`，现有 `if API(...)` 把成功当作假，转入自制哈希 SID 回退。独立只读系统调用实测 HRESULT=0、非空 SID、系统 SID 长度40字节；项目函数却返回28字节且与系统 SID 不同。当前注释将正常返回0解释为 Home 版 stub，不成立。错误 HRESULT 非0也会被当作成功而使用无效输出指针。

修复建议：以 HRESULT 成功/失败契约判断结果，成功后复制系统 SID 并 `FreeSid`，失败时清楚报错。移除未验证的手工 SID 回退，再验收真实进程启动和隔离。依据：[Microsoft API 文档](https://learn.microsoft.com/en-us/windows/win32/api/userenv/nf-userenv-deriveappcontainersidfromappcontainername)。系统包 SID 子权限常量也不支持当前四段哈希假设，参见 [AppContainer SID 常量](https://learn.microsoft.com/en-us/windows/win32/secauthz/app-container-sid-constants)。

本轮未运行会授权 `D:\Python` 等目录的 AppContainer 集成测试；未把只读 SID 探针当作完整沙箱验收。

### P2：其他版本的损坏锁仍能阻断当前版本

位置：`tools/preflight.py:121`。

新增的集合相交判断只过滤后续 manifest 绑定检查；其前面仍先对所有发现的锁执行 `check_frozen`，把其他版本错误计入当前 `f_problems`。合成探针中，当前有效锁单独存在通过，加入健康的另一版本锁仍通过；仅改坏另一版本文件后，当前 freeze_gate 变成失败。

修复建议：先确定与当前 manifest 数据集合相关的锁，再汇总当前门禁错误。其他版本损坏应独立报告，不能污染当前版本的冻结结论。无法解析、无法判定范围的锁需要另定清楚的保守策略。

### P2：status 仍会接受不包含当前数据的清单绑定

位置：`tools/eval_test_prep.py:49`、`:93`。

任意 `--dir` 都把全局 v1 主清单放入可接受 SHA 集合，仅判断锁中 SHA 是否属于候选集合，不验证该清单是否登记了锁覆盖的当前文件。合成候选目录的文件完全不在 v1 manifest 中，但有效锁只要写入真实 v1 manifest SHA，status 就输出“校验通过（结构/覆盖/manifest 绑定一致）”。

修复建议：按当前 base/角色选清单，并核对清单中的实际路径、哈希、大小和角色确实对应当前 JSONL；不能仅用一个候选 SHA 白名单验收关联关系。

## 已验证通过

- 指标拒绝 `parsed_strict=2/parsed_lenient=2`，原200%解析率反例关闭。
- `--out data/V1` 在解析输入和写文件前拒绝，原大小写绕过关闭。
- 当前 v1、v2 的正常 status 查询均验证各自有效锁，并把健康的另一版本锁列为 INFO。
- v1 主清单6条、v2 eval/test 子清单各1条，`data_check` 均为问题0、quarantine0。
- 执行隔离门禁仍因 network 未实施返回失败，没有因 Python socket guard 或新增但尚未接入的 AppContainer 模块而假绿。
- 常规权限测试：**361 passed + 29 subtests passed**，排除 `tests/test_appcontainer.py`；代码 `diff --check` 通过。

## 测试边界与证据

首次测试的默认临时目录不可写，属于执行环境问题。改用工作区临时目录后355项通过，6项失败分别来自受限进程的硬链接权限、LaTeX调用和临时目录嵌入 Git 仓库导致的检查顺序变化。随后在常规进程权限下、使用仓库外且可写的临时目录重新测试，得到361+29全通过；不把环境失败计作本轮代码缺陷。

- `pytest-host.log`：最终完整测试输出（上述沙箱集成测试除外）。
- `pytest.log`：受限环境测试输出，保留用于区分环境限制。
- `probe.py`、`results.json`：独立可重复合成反例、只读 SID 探针及源码哈希。
- `source-snapshot/`：探针对应版本源码。重复执行探针使用新合成目录，不重写已有冻结夹具。

测试全绿不覆盖本报告新增的四个反例。数据数学内容与300条场景的逐条验收属于另一项内容审查，本报告没有宣称完成。
