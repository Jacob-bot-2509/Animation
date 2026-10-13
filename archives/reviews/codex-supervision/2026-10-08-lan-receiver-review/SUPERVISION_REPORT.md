# LAN 接收端新材料独立审查

2026-10-08，北京时间。用户要求继续监管 Claude Code；继承用户已明确授权开始双端实验的范围。本轮只读取新接收端材料、独立核验与建立只读接收诊断，不另起网络实验、不提交或放行生产。

## 当前判定

LAN 轮 lan-2026-10-08-a，发送 run remote-271e1c881c4f473fb027f5f28d4a3bd5。新接收端两个文件不能用于通过验收，结论为 NEEDS_EVIDENCE / NOT_ACCEPTED。这是证据不合格，不等于已证明沙箱网络隔离失败。当前没有收到 sandbox nonce，也没有完整健康对照，不能据此判断沙箱包是否被阻断。

发送侧 sender.json 保持上一轮 SHA256 f2ca09bd06173dc48ab19ee5798a24b14bbd986985cb26f8af6d8edd40744a6c。原始采集器源码未变，原有发送侧核验和具名本地回归可以继承，不重复运行。

## 8 条诊断问题，归纳为 6 组

1. 日志字节不匹配：summary 声称日志 SHA 为 0f490152cc50cdfcfc5b7fa9cf050360f51baffea17bb492818142e48f52eef4；当前原字节实际为 39bd89372457a68d10f86cfbce454712f099157bbca6dcd21395d0f996c26901。
2. 实现身份不能成立：接收材料中的 EXE SHA 文本只有 61 位，不是完整 64 位 SHA256，与批准值 d6887098ccd3b1c3b9bde1180746558b78d2b2882b3cbee25d791c5f792f1cad 不符。这里只发现声明字段错误，未读取证人机二进制，不能推断实际 EXE 已变；不能直接把字段改成批准值来补证。
3. 端点不匹配：发送目标为 192.168.1.83，接收 created、listening、summary 均写 bind=0.0.0.0。当前对账契约要求具名精确端点；通配监听声明不能替代真实端点绑定证明。
4. 时间矛盾：summary started_monotonic_ns=168368885274900，finished_monotonic_ns=16868887799600，差值为 −151499997475300 纳秒。原日志 listening 与 closed 事件也不在 summary 声称区间内，两条均被标记。不能用 utc 字段或手改数字替代原生 monotonic 证据。
5. 健康对照缺失：日志只有 created、listening、closed，没有任何 payload。当前发送轮两协议 before、after 合计 4 个健康 nonce 均未在接收端出现；零 payload 不是“沙箱零送达”合格证据。
6. 实际退出码未提交：接收目录只有 JSONL 和 summary，没有可信的真实 rc 材料。本轮没有代填 rc=0。诊断脚本退出码 2 是诊断拒收码，不是证人进程退出码。

只读观察器在 22:10:15 捕获这两个文件首次出现，又在 22:10:40 捕获它们的字节变化；精确事件见 receiver-change-events.json。已询问 Claude 原件来源、传输方式和变更原因，不能仅凭观察事件推断变更动机。当前文件原字节已快照归档，未再改写。

## Codex 已完成的修复与验证

新增 inspect_receiver.py 修复当前材料交接只有泛化拒绝、缺少逐项原因的诊断环节。该脚本只读显式指定 sender/log/summary，输出精确哈希、端点、时间、健康 nonce、真实 rc 等问题；坏输入以结构化 JSON 和非零码拒收。即使全部初筛通过，也只记 READY_FOR_REGISTERED_RECONCILIATION，完整准入仍必须调用既有注册对账流程；脚本始终 full_surface_accepted=false、production=CLOSED。

脚本 SHA256 为 6e920ca0e435287ef0ba9be1bca0ffd361ae9f144155fa1f18dbea9387d53c77。实际当前材料诊断列出 8 条问题、rc=2，输入前后 SHA 完全一致；8 项本地对抗检查通过，包含缺 rc、布尔伪零、非零 rc、负时长、实际 sandbox nonce、原字节保留、畸形 JSON 与健康合成夹具只达到对账准备状态。合成检查不当作双端原生验收。未修改已有采集器、证人程序、审批哈希或原始接收证据来让其通过。

本轮诊断工具在上述限定范围内合格；双端实验材料不合格，无法通过补写不存在的对照包修复。完整问题见 final-intake.stdout.json，实际执行与独立核验见 intake-execution.json、final-independent-verification.json，合成检查见 diagnostic-adversarial-verification.json。

## Claude 下一步

首先收取证人机按原字节传输的 JSONL、对应 summary 与真实进程退出码，保留当前不合格版本。禁止从截图、聊天文字重新抄写或修改哈希、时间、地址、事件。若证人原件确实也是零健康 payload 或通配绑定，则另起新 LAN 轮：使用证人具体 IPv4 192.168.1.83（先在证人机实际核对），新日志名、新 round/new nonce；接收器先 LISTENING，宿主前对照→沙箱→观察窗→宿主后对照完整保持监听。先用只读脚本检查，再通过注册 --reconcile，并交 Codex 独立验收。

收到匹配原件后必须重新针对真实字节核验，不继承本轮拒收文件的资格。新外部 IPv6 轮另行对账。Codex 已回信说明现状、诊断材料与继续工作要求；本目录 delivery-manifest.json 只冻结本轮报告和快照，实验活动目录不冻结。
