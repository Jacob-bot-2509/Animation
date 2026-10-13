# 邮件793：第二三层本地实现与LAN分项裁决

本批：run-41159ad68a324267a1eea5321644bafd，来源 msg_1791898274355_793。
裁决：**REPAIRED_PASS，限定本地工具与具名LAN材料范围。**
探针、原v3源码、冻结原件和正式门禁没有改动。实际OneDrive同步路径/权限尚未交付，未部署后台消费worker，未开训。

## 交付与修复

Codex已新增：

- tools/witness_pack.py：完成采集的五原件无损打包、严格SHA、排他发布ZIP/READY、按源/目的上下文去重；不启动接收器或探针。
- tools/witness_consumer.py：完整双样本快照、六成员ZIP校验、批准sender配对、预检、对账、分项报告、单worker锁和幂等/恢复；不执行包内或邮件代码。
- tools/witness_registered_adapter.py：按原验证函数进行只读注册回放，精确白名单输入，新job唯一写入。原driver文件不改；原模块及其他实例不改，内层只读验证根仅绑定本次job。
- tools/witness_transfer_common.py：路径/重解析标签、句柄路径、冻结目录与系统目录拒写、真实回执与JSON形状、来源版本、读写及锁。
- tests/test_witness_automation.py、configs/witness_automation.example.json。
- 当前AGENTS、TASK与邮箱README的实现阶段说明；完整前后版本见active-document-bindings.json。

修复过程中实际发现并关闭的缺陷：首次冻结清单写成后重复按“可写”检查而误报失败；publisher提前使用非对象proof；发布缓存缺源/目的上下文；运行中源码可能悄悄变版；中断回执恢复需验证结果scope/point/nonce；stdout/summary损坏与JSON对象形状检查。首版、失败日志、改后版保留，不删除失败证据。

完整实现补充见 DESIGN_ADDENDUM.md；实际命令、环境与接入字段见 RUNBOOK.md。原冻结DESIGN v1不覆盖。

## 独立验证

最终28项新回归全部通过（tests-final.json rc=0，完整stdout/stderr保留），覆盖：

- 默认/导入仅PLAN；实际三个CLI均rc3，不发射或写云盘。
- 原件无损、真实非零退出码保留、bool码/缺stderr/形状错误/坏stdout拒绝。
- READY乱序、截断ZIP、额外/重复/穿越成员与成员SHA错误拒绝。
- 唯一sender/native依赖绑定、同身份异内容冲突、发布目的变更和重复消费。
- 系统/冻结目录拒写，未知/名称替代重解析标签拒绝，worker互斥。
- 完整回执/冻结job的中断恢复不重签第二份；未完成INTENT不盲目重跑；伪造OPEN恢复输出拒绝。
- 实际收到沙箱nonce记FAILED，而不是缺证据。
- 对已提交真实LAN快照的回放同时拦截socket和subprocess启动，调用数均0。

代码/配置/测试最终SHA见source-bindings.json，snapshot逐字节保留；三个原v3源码SHA保持原绑定。源码diff格式与实际默认CLI核验通过。

这些测试限定本地普通文件夹与提交快照。OneDrive CLOUD路径处理有标签单元检查，但真实云端下载、共享权限和持续运行恢复仍需接入验收，不能从28项测试推断已通过。未安装软件或更改系统配置。

## LAN正式分项裁决

在新的独立作业目录对原件做一次真实注册回放，并与作者已提交reconciled-6b9ae9ce回执逐项比较。nonce、端点、原件SHA、父进程回执SHA、source/transport、实现绑定、协议、观测和point等一致；差异只为具名新作业的派生文件路径。

资格：**PASS_BOUND_LAN_D9_TCP_UDP_REGISTERED_WINDOW_ONLY**。

- TCP和UDP各有before/after健康控制，共四个nonce精确匹配。
- 同一完整窗口未收到相应沙箱nonce；TCP原发送端状态为os_denied/10013，UDP原状态为sent。UDP缺送达的因果机制仍NOT_ESTABLISHED，不称“静默拦截实锤”。
- 原source观测时长为 21000477800 ns，即 105002389/5000000 秒，使用整数/分数；两端monotonic_ns不跨机比较。
- registered代码真实映射为D9/lan_peer，两协议均保持这一映射。
- D1仍缺联合策略的D2外部IPv6依赖，D7仍缺D8依赖，不把D9改名成D1/D7。
- D2/D8保留延期GAP，按用户直接口径不阻塞训练准备。数据准备可按既有范围推进，但正式训练没有被本回信许可。
- whole_surface_accepted=false、production=CLOSED；主全局/原生资格未从这份LAN材料改绿。

原始材料、独立新job的14项快照和具名路径映射见 LAN_REPLAY_VERIFICATION.json、lan-job-snapshot-map.json。源身份和原哈希不重写；旧all43根不追加文件。

## 待接入与交接

配置模板 active=false，witness.capture_root/sync_root 与 consumer.sync_root 仍为空。Claude在接入阶段提供这些实际路径、共享权限及证人侧Python环境后，先验证一次性材料传递，再启用隐藏watch。运行期间仍不发射、启动采集或安排并发实验。

已先发真实所有权通知 msg_1791898724251_794。最终回信收据归档后冻结本轮清单，再由既有mail_watch ACK核验报告SHA与真实发送记录；ACK实际时间以本批runs目录为准。当前只读观察器最近已核对worker7616心跳，后台记录不等于模型自动批准。

Claude应核对交付SHA，按Codex新工具版本继续后续已授权工作，不重复修改Codex已完成部分；探针仍归用户授权后Claude执行。历史设计、旧邮件裁决和ACK保持原样。
