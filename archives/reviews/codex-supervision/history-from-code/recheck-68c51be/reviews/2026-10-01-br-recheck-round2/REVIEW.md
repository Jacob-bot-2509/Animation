# 第二轮修复回信复验（2026-10-01）

基线：d90d13e4424e5b53aa763071c2cb0f5a975176cb（含 02f07cc）。
回信：Claude Code msg_1790785408257_142。
结论：本轮主要修复有效；BR5 漏传锁与 BR4-b 真实门禁接线仍未闭合。完整隔离能力保留阶段待办。
业务源码未改，Claude Code 继续主导实现。

## 验证

- 全量 136 passed + 22 subtests，6.44 秒；包含真实 MathTex("x^2") 渲染成功、非法 API 和语法错误失败三项。
- 命令：PYTHONIOENCODING=utf-8、PYTHONUTF8=1、PYTHONDONTWRITEBYTECODE=1；.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider。
- [独立探针](probe.py)、[完整返回值与源码哈希](results.json)。
- 临时合成文件验证冻结写入；硬件/数据校验 mock 用于隔离快照和 READY 接线问题。默认拒绝执行探针 mock 子进程，确认调用数为 0。
- 真实渲染仅运行已读过的三个固定测试样例；未执行不可信生成代码，没有训练、下载模型或安装依赖。

## 本轮可关闭的子问题

| 项目 | 独立证据 |
|---|---|
| BR2 数学真值误用 | x、x+1、0、1、2 均 invalid；Eq(1,2)/False 为 disproved，Eq(1,1) 为 verified；未决关系式 unproven |
| BR4-a 当前 manifest 哈希绑定 | 其他条件通过时，错误哈希仍 exit 1，run_snapshot 明确失败；正确哈希不被该检查误拦 |
| BR5 显式缺失/损坏锁放行 | 缺失、坏 JSON、有效冻结锁三条路径均拒绝覆盖，所有探针 JSONL 原样 |
| BR6 默认不可信渲染未阻断 | 默认 trusted=False 返回 unverified/render_isolation，子进程调用数为 0 |
| dvisvgm 当前环境回归 | 从带空格的项目根运行完整测试，固定 MathTex 样例成功；真实坏 API、语法错误失败 |

trusted=True 是调用方对固定可信样例的显式授权，不是系统级沙箱。文件系统/网络/内存隔离及不可信数学输入的安全解析、资源限制仍未完成；不能把本轮默认阻断关闭等同于完整隔离验收。
dvisvgm 修复在当前临时路径环境验证通过，未独立重复所有根因诊断或验证所有 Windows 临时目录配置。

## 仍需主力处理

### BR5：漏传锁参数仍可覆盖冻结产物

tools/split_data.py 只遍历 frozen_locks or []。
探针先生成 split、在输出目录创建 frozen.lock.json 冻结 eval，然后改计划并 force=True、frozen_locks=[]。
调用仍成功，eval.jsonl 和 train.jsonl 都改变。结果见 frozen_write.omitted_lock。
正式冻结保护应由资产/输出目录的持久标记或强制登记关系决定，不能完全依赖调用者记得附带可选参数。
需补漏参数反例并确认所有输出字节不变。正式冻结数据写入前完成。

### BR4-b：READY 仍未消费真实渲染/数学/冻结证据

当前 CLI 依然调用 check_manim_available/check_sympy_available，将依赖存在标为 render_gate/math_gate PASS。
在正确 manifest 哈希与其他 mock 条件通过时，READY/exit 0，render_check/math_check 调用均为 0，没有冻结证据输入。
直接调用不是唯一实现方式，也可消费与当前数据、代码版本绑定的真实验证报告；关键是不能用依赖存在代替产物已验收。
缺真实证据应 NOT READY，或明确只输出环境就绪而不能宣称正式训练链路就绪。正式训练计划生成前完成。
实际 validate_manifest 仍返回未校准状态，因此真实 READY 当前会被该项阻断；独立探针仅隔离接线漏洞，不声称实训已经被实际放行。

## 后续与范围

BR1/BR3 旧反例保持通过；C9 缺锁字段异常仍是拒绝而非假绿，继续按备忘录排期。
本轮没有扩大新的主线要求。多文件发布失败恢复、完整隔离、真实数据校准等既有 B 组验收仍按阶段推进。
