# 整体协调性检查与直接修补

基线：ace3d33；期间 Claude Code 提交 394bcd6，合入本轮四个 CLI、文档与测试。最终验证针对 394bcd6 + Codex 的 fs_guard fullmatch 小补丁；源码哈希见 final_snapshot.json。
结论：CLI 修补通过，整体 L0–L7 仍 BLOCKED。

## Codex 已直接修复
1. make_manifest：修正未声明 args.force 引发的正常调用崩溃；main(argv) 使用传入参数。输出清单必须位于数据根目录，避免 entry.path 根错位；拒绝已有输出；以 x 模式创建，避免检查后意外覆盖。空目录失败。
2. check_fields：--force 也不得让报告指向输入（包括同文件别名）；空 required 参数被拒；读写错误给出非零结果；新报告使用独占创建。
3. check_code：缺目录/零匹配文件不再默认通过；默认白名单锚定项目根；明确打印 UNVERIFIED 和 PASS:STATIC，避免把静态检查误当数学/渲染验收。
4. data_check：manifest/scan/dry-run 互斥；缺失目录、空扫描、空 manifest 不再 CLI 放行；阈值限有限 [0,1]；dry-run 明示仅 schema 说明。
5. fs_guard：valid_run_id 改为 fullmatch，拒绝末尾换行。独立测试覆盖长度、空白、路径分隔符。
6. README/data README 对齐实际入口、路径/许可/覆盖规则、退出码与未实现范围，去除过时测试数量；保留历史项目决策。补齐本地密钥、权重、数据、缓存和临时桥文件的忽略规则，不改变已跟踪文件。

测试：新增 tests/test_cli_contracts.py（12 个测试）和 tests/test_run_id_contract.py（2 个测试）。CLI 补丁前出现正常命令异常、输入覆盖和空输入误通过；补丁后完整测试 86 passed, 22 subtests passed in 2.09s。git diff --check 通过；忽略规则用 git check-ignore --no-index 检查通过。

## 394bcd6 邮件回报核对
| 声称的修复 | 本地实测 |
|---|---|
| .json 整文件解析 | 通过：pretty JSON 返回 ok=true |
| null/数组/标量结构化处理 | 部分：null 不再崩溃，但返回 ok=true，没有 problems/quarantine；内部 <non-object> 标记没进入报告 |
| CLI 默认清单路径校验 | 通过：check 无 --manifest 时读取记录路径并对缺文件返回 1；核心 check_record 的默认调用语义仍待统一 |
| 空 split 不再写文件/登记 | 未生效：eval.jsonl/test.jsonl 仍存在，且仍误报相同空文件 hash；该提交 tools/split_data.py 无差异 |

证据：third-round/results.json。validate.py 存在两份同名 _load_sample_ids，后者覆盖前者；需移除重复实现并统一解析契约。

## 核心接口仍不协调
- [P1] CLI 拒绝空清单，但 validate_manifest(Manifest(name='empty')) 返回 ok=true；preflight 直接调用核心，CLI 防护不能代表全链路防护。必要数据集应在核心契约中定义。
- [P1] 文件大小错误、source 仅空白仍通过；schema、实际文件与必填语义不一致。synthetic entry 的 size=999999，实文件十几字节，结果仍 ok=true。
- [P1] JSON 非对象/ID 类型验证不完整；null 标记不进入问题清单，未证明字段/样本合法。
- [P1] near_dup 只取共享 shingle 数最多的前 20 个候选：20 个长噪声文本先插入、完全相同 query 后插入，max_sim(query)=0.042 而不是 1.0。校准阈值无法单独修复该漏检，需全候选正确最大值或可证明不漏报的剪枝。
- [P2] fields 的“非空”与数据契约不一致：problem=[]、solution={} 仍通过。每种数据类型应明确允许的值类型，不能把所有非 None 值都视作合格。
- [P2] 空 split 策略尚未落地，且 split plan/输入哈希、来源许可证继承、冻结锁、原子发布未完整。
- [P2] run_record init 相对路径按启动目录解析，但默认 check 按项目根解析，需要记录绝对路径或明确统一根/运行 cwd。
- [P2] configs/data_check.example.json 并未被 CLI 加载；记录它的哈希不能证明执行使用了该配置。现文档已明确“说明示例”，后续需记录真实有效参数。
- L5 seed/config 内容 hash/dirty 快照、严格 L1–L5 证据聚合、L7 冻结评测集及指标契约待实现。近重复校准、实际 API/数学/渲染待验证。

probe_results.json 保存核心反例与当时源码哈希；run_id_trailing_newline=true 是修前结果，third-round/results.json 的 false 是修后结果。所有持久证据限定动画项目内；测试只使用合成数据，未训练、下载或安装。

## 分工与后续
四个 CLI 及文档已由 Claude Code 合入 394bcd6；fs_guard 一行补丁、其测试和本报告等待主实现者合并。剩余核心问题直接发给 Claude Code 主修；不得覆盖双方在途修改。后续以具体反例关闭与版本化证据验收，不以测试数量或提交标题代替整体通过。
