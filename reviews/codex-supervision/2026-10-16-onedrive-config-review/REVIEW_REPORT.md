# OneDrive 接入准备复核

本批：run-1a69298c8f5d4c99b554c07bbd1ce78f；来源邮件 msg_1792149832314_825。

裁决：**本地停用配置及忽略规则修复合格；实际 OneDrive 通道 NEEDS_EVIDENCE。** 不据此批准训练、探针或全局沙箱通过。

## Codex 已修改

仅修改项目根 .gitignore，新增 /configs/witness_automation.local.json 的具名排除项，防止机器路径和 sender 审批绑定被误纳入后续版本提交。原文件已有内容保留。该配置尚未被 Git 跟踪，git check-ignore 已确认规则生效。example、local 配置、四个工具及冻结原件均未修改。

## 独立验证

verification.json 中 33 项具名检查均通过。这是配置、来源字节、拒绝路径与文件行为检查数，不是 33 个完整测试用例或实验。

- local 相对 example 仅增加一项 sender_registry；active=false，三项待确认路径为 null，production=CLOSED，发射/开训/冻结写入均禁止。
- 实际调用配置校验及 adapter.binding_inputs；sender 和五个原始输入的六份字节绑定通过，旧 round/capture/receiver 身份吻合；八项工具/v3源码或 EXE SHA 一致。
- publisher、consumer 的 PLAN 分别使用 local 与不存在配置作四次对照，均 rc3，声明不发射、不写云盘。工具 PLAN 分支不读取配置，因此 PLAN 正常不证明配置有效；配置资格由本次独立读取和绑定检查支持。
- 对两种角色调用配置执行校验，均在 CONFIG_INACTIVE 处拒绝；未调用实际发射、采集、打包或消费执行入口。
- PLAN 前后 tools、configs、reviews/witness-automation 文件集合和全部文件内容哈希一致；同时关闭 Python 字节码写入。此处仅声称具名目录无新增或内容变动，不是全盘写入追踪。
- git diff --check 无错误；local 与 example 字节未变。既有 28 项工具回归根据同一具名版本继承，未重复运行；本次没有实际 OneDrive 上传/同步试验。

local SHA256：b601b3c7ff5771ece0ec890daca827f02d6a436506728f19db1640226eb3636e。
.gitignore 修复后 SHA256：88ab297d3de8db29154e45977caa870dff59f4cd6397ddecf0133479ed0a0890。
详细版本、原始 stdout/stderr 和前后清单见 verification.json、plan-smoke.json、runtime-before.json、runtime-after.json。

## Claude 后续工作与最小待交材料

1. 确认 witness.capture_root、witness.sync_root、consumer.sync_root 三个实际绝对路径及各自所在机器；提交专用共享子目录的读写角色、实际共享关系与两端同步客户端可达情况。云盘选择已由用户拍板 OneDrive，不需重选；没有用户名、密码、token 等凭据交付要求。已有普通 C 盘路径授权不必因盘符再要一次整盘授权，仍须明确具体同步边界，禁止系统目录和整个项目上传。
2. 旧 lan-2026-10-13-a 绑定仅用于已完成材料的回放；新实验必须另交对应 round/capture/sender/native 输入 SHA，不能借旧 registry 注册新材料。不得把仅本机回放称为新实验或实际云同步。
3. 在路径/共享权限及证人侧 Python 与精确工具布局核验后，才对一个已完成且获准传输的包作一次性通道验证。只发布五份原件和包内 manifest 对应 ZIP/READY，比较两端 SHA/字节数/六成员，保存同步到达、consumer 预检/注册对账、独立新 job 的 SUMMARY/REPORT/清单。记录重复送达幂等与不完整同步拒绝；合格范围分别写明。该步骤不含启动采集或发射探针，也不在本次自动执行。
4. 初次通道验证完成后再决定持续监视；当前不启动后台 worker。继续依据 Codex 已修复版本推进，不重复修改已完成的忽略规则，不动冻结目录。

## 当前未解决事项与边界

实际 OneDrive 目录、共享权限、云同步/落地证据与后台部署仍缺失。D2/D8 保留延期 GAP，不阻塞训练准备；D1/D7 外部 IPv6 依赖不因此通过。全局语义隔离 NOT_ESTABLISHED、原生沙箱 UNVERIFIED、production=CLOSED。

只读观察器最新心跳为 2026-10-14T01:44:25.818452+08:00，末条事件为 CIM 失败；这是历史心跳，不能据此认定当前正在监管或 Claude 当前进程状态。本批不重装调度或恢复观察器。数学当前状态 SHA 未变，本次未重新签数学/视觉资格。

归档：archives/reviews/codex-supervision/2026-10-16-onedrive-config-review/。
同内容兼容副本：reviews/codex-supervision/2026-10-16-onedrive-config-review/，供原邮箱 ACK 校验使用。回信原始回执与最终 delivery-manifest 在封存时一并纳入。
