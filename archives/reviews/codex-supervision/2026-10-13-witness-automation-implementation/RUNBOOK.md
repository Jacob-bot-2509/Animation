# 第二三层工具 v1 使用与接入

当前资格：本地候选已实现，28项回归通过；实际 OneDrive 传输与后台部署尚未验证。
工具位于项目 tools/：witness_pack.py、witness_consumer.py、witness_registered_adapter.py；共享依赖 witness_transfer_common.py。均为Python标准库工具。

## 交付与角色

证人侧 publisher 只观察已完成的 v3 capture，打包五份原件并发布 ZIP/READY；不能启动 receiver 或探针。
训练机 consumer 读取同步目录，校验完整快照、包成员和原件SHA，按批准的 sender_registry 预检、注册对账，写新 job、报告和冻结清单。
注册适配器复用原v3源码的验证函数，以隔离模块实例提供精确输入读回调、新job写回调；原源码与原 all43 冻结目录不改。

CLI未指定 --execute 时仅 PLAN/rc3。--execute 表示运行一次；另加 --watch 才是持续扫描，STOP文件使该worker退出。配置仍需 active=true；现役示例 active=false。

## 配置

从 configs/witness_automation.example.json 复制成独立 local 配置。不要修改归档版。填写：

- 证人 witness.capture_root、witness.sync_root、witness.staging_root。
- 训练机 consumer.sync_root；jobs_root/runtime_root已给独立项目命名空间。
- sender_registry 中每项批准绑定：round、receiver_capture_id、expected_receiver_run_id、sender_run_id、sender_path、sender_sha256、input_bindings。
- input_bindings 必须包含发送机接口原始输出/原始stderr，以及原 native transport work 的 scene.py/stdout.txt/stderr.txt 的实际SHA；不能靠时间或“最新sender”猜测配对。只读输入必须仍在本项目，缺失或变化就拒绝。
- automation_source_pins 与 v3_source_pins 使用 source-bindings.json/配置中实际版本；任何改变都须重绑并重启worker，运行中不会悄悄采纳新代码。
- 两端专用OneDrive目录权限与可达性需在接入时确认，将目录设为“始终保留在此设备上”。本轮仅本地文件夹模拟，不据此确认云端传输。

v1 使用固定上限：ZIP 1GiB、展开原件256MiB、六成员、manifest/READY各64KiB；修改限额必须另版审查，当前配置不同值会拒绝。各输入/暂存/输出根不能互相包含；暂存与消费jobs/runtime必须在本项目 reviews/witness-automation 下，且不能落在任何冻结祖先内。系统目录拒写。

实际 paths 与共享权限由 Claude 在接入阶段提供。本轮没有安装软件、登录账号、上传资料或启动背景服务。证人端须有可用Python环境；publisher只使用标准库，执行所需四个新脚本和三份原v3参考源码需保持项目相对布局/精确SHA。消费端在原训练项目运行，保持旧 sender JSON 内绝对路径不变。

## 在项目根执行

```powershell
# 默认计划：不写云盘、不启动采集
& '.\.venv\Scripts\python.exe' -X utf8 -B 'tools\witness_pack.py'
& '.\.venv\Scripts\python.exe' -X utf8 -B 'tools\witness_consumer.py'

# 实际路径、权限、配置与绑定确认后，先运行一次
& '.\.venv\Scripts\python.exe' -X utf8 -B 'tools\witness_pack.py' --config 'configs\witness_automation.local.json' --execute
& '.\.venv\Scripts\python.exe' -X utf8 -B 'tools\witness_consumer.py' --config 'configs\witness_automation.local.json' --execute

# 一次性验证成功后，隐藏启动一个消费worker；不新增系统计划任务
Start-Process -FilePath '.\.venv\Scripts\python.exe' -ArgumentList @('-X','utf8','-B','tools\witness_consumer.py','--config','configs\witness_automation.local.json','--execute','--watch') -WorkingDirectory 'D:\Animation-Model-Training' -WindowStyle Hidden
```

接收/发射启动不在这些命令中；原 start_witness_capture.ps1 仍由用户授权后 Claude 执行。
publisher 的STOP位于 witness.staging_root/runtime/STOP；consumer的STOP位于 consumer.runtime_root/STOP。停止后不自动删除文件或解除来源绑定。

## 结果与恢复

LOCAL_PUBLISHED仅为生产机本地发布；不保证对端到达。READY和ZIP到达乱序、完整SHA不符时等待；watch对等待使用5/15/45/120秒退避，最终保持轮询，不自行补造文件。
缺批准sender绑定为WAITING_SENDER_BINDING；同身份不同内容为CONFLICT；来源变化为VERSION_DRIFT类拒绝。
consumer完成后每个job有SUMMARY/REPORT、预检、适配器回执、注册结果和冻结清单。重复交付核验完整冻结清单后继承回执，不加写旧job。实际沙箱nonce收到记FAILED；其他缺证据/预检拒绝记NEEDS_EVIDENCE，不当作通过。

若已有完全验证的ADAPTER_RECEIPT但summary/journal未提交，恢复时重核输入和分项结果，不生成第二个随机注册结果。
仅有ADAPTER_INTENT而无完成回执时记RECOVERY_REQUIRED，不盲目重跑。证据/输出/清单变动会拒绝复用，不能删锁或覆写旧job强行通过。

OneDrive云标签仅在同步边界读写时允许明确CLOUD类型，名称替代链接/junction/未知标签拒绝；落到新job普通文件后再进入原严格路径验证器。实际云文件接入尚待对端确认，不能据本机普通文件夹测试称已通过。

## 资格

本地原件回放限定PASS_BOUND_LAN_D9_TCP_UDP_REGISTERED_WINDOW_ONLY，四个健康nonce、完整观测和未收到沙箱nonce已核对；UDP因果机制未建立。
D1/D7不是本材料的点位，仍缺旧IPv4联合策略的外部IPv6依赖；D2/D8延期GAP不阻塞训练准备。全局、生产与开训资格不由本工具放行，production=CLOSED。
