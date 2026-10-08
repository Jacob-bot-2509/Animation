# 双端沙箱实验操作单：修订 v3

本单对应当前发布接收器及发送驱动。证人机须与训练机为不同主机。本文修正操作与材料要求，未执行实验；执行日期以用户最新安排为准。

## 1. 核对完整版本与本机自检

在证人机 PowerShell、接收器所在目录运行：

~~~powershell
Get-FileHash -LiteralPath '.\witness_receiver_v2.exe' -Algorithm SHA256
~~~

完整 SHA256 必须等于：

~~~text
d6887098ccd3b1c3b9bde1180746558b78d2b2882b3cbee25d791c5f792f1cad
~~~

训练机发布原件位于：

~~~text
D:\Animation-Model-Training\reviews\codex-supervision\2026-10-06-witness-mail-review\release\witness_receiver_v2.exe
~~~

在证人机运行自检并立即保存退出码：

~~~powershell
$witnessTag = Get-Date -Format 'yyyyMMdd-HHmmss'
.\witness_receiver_v2.exe --selftest --output ".\selftest-$witnessTag"
$selftestRc = $LASTEXITCODE
$selftestRc
~~~

实际输出是 JSON。检查 failures 为空且退出码为 0；不存在原单描述的“OK 收发通路正常”文本。自检仅验证证人机宿主回环 TCP/UDP、IPv4/IPv6 通路，不能作为沙箱或外部阻断证据。

## 2. 确认拓扑和新文件名

证人机保存 ipconfig 原始输出，并提供本次 LAN IPv4、IPv6 地址及主机身份。外部轮必须使用真实全局 IPv6 地址，且位于训练机 LAN/同一 IPv6 前缀之外；同一 LAN 上另一台主机的稳定全局 IPv6 仍不能作为外部证人。fe80:: 链路本地地址、ULA、回环地址不满足外部条件。

双方先确认拓扑和本轮唯一名称。每轮使用新的日志路径、发送端轮次名和输出目录；保留旧轮原件，不合并旧 nonce。完整版本和地址确认后，先启动接收器，再测发送端宿主连通性。UDP sendto 返回成功不能单独证明送达，须以接收日志核实。

端口为 UDP 49001、TCP 49002。证人机须具备对应入站许可；不要为了实验关闭整体防火墙。

## 3. LAN IPv4 轮

证人机 PowerShell：先用本轮新的标记，再把占位符替换为实际 LAN IPv4：

~~~powershell
$lanWitnessTag = Get-Date -Format 'yyyyMMdd-HHmmss'
.\witness_receiver_v2.exe --serve --bind '<证人机实际LAN IPv4>' --udp-port 49001 --tcp-port 49002 --seconds 300 --log ".\lan-$lanWitnessTag.jsonl"
$lanReceiverRc = $LASTEXITCODE
$lanReceiverRc | Set-Content -LiteralPath ".\lan-$lanWitnessTag.rc.txt" -Encoding ASCII
~~~

看到 JSON 中 kind 为 listening 且 endpoints 同时列出 udp、tcp，再通知训练机启动。真实提示为小写 listening，不是固定大写 LISTENING 文本。

训练机在 D:\Animation-Model-Training 的 PowerShell 中运行：

~~~powershell
$lanSenderTag = Get-Date -Format 'yyyyMMdd-HHmmss'
& '.\.venv\Scripts\python.exe' -X utf8 -B '.\tools\sandbox_external_test_driver.py' --execute-native --bind '<证人机实际LAN IPv4>' --round "lan-$lanSenderTag" --scope lan --protocol both --observe-seconds 21 --out '.\reviews\codex-supervision\2026-10-06-all43-sandbox-repair\external-tests'
$lanSenderRc = $LASTEXITCODE
~~~

接收器必须覆盖宿主前对照、沙箱探针、完整观察窗及宿主后对照全过程。默认 300 秒到期后正常结束；若发送迟到或接收器提前结束，重跑新轮，不把不完整窗口认定为阻断。无需凭操作单预估总耗时作验收。

证人机将以下原始文件完整交回：

- lan-<本轮标记>.jsonl
- lan-<本轮标记>.jsonl.summary.json
- lan-<本轮标记>.rc.txt
- 接收器本轮 stdout/stderr、完整 EXE SHA256 和对应地址/主机身份材料

以原文件传输，保留字节与全部事件，不只粘贴 payload 行或聊天摘录。总结须保持与原日志的 SHA256 绑定。

## 4. 外部 IPv6 轮

只有拓扑满足第二节要求时才执行。证人机用全新文件名：

~~~powershell
$v6WitnessTag = Get-Date -Format 'yyyyMMdd-HHmmss'
.\witness_receiver_v2.exe --serve --bind '<证人机真实外部全局IPv6>' --udp-port 49001 --tcp-port 49002 --seconds 300 --log ".\v6-$v6WitnessTag.jsonl"
$v6ReceiverRc = $LASTEXITCODE
$v6ReceiverRc | Set-Content -LiteralPath ".\v6-$v6WitnessTag.rc.txt" -Encoding ASCII
~~~

收到 listening JSON 后，训练机运行：

~~~powershell
$v6SenderTag = Get-Date -Format 'yyyyMMdd-HHmmss'
& '.\.venv\Scripts\python.exe' -X utf8 -B '.\tools\sandbox_external_test_driver.py' --execute-native --bind '<证人机真实外部全局IPv6>' --round "v6-$v6SenderTag" --scope external --protocol both --observe-seconds 21 --out '.\reviews\codex-supervision\2026-10-06-all43-sandbox-repair\external-tests'
$v6SenderRc = $LASTEXITCODE
~~~

证人机提交同样的完整 JSONL、自动生成的 .jsonl.summary.json、真实 rc、stdout/stderr、版本与拓扑材料。IPv6 接收器为 IPv6-only，不能把双栈 IPv4 结果混作此轮证据。

## 5. 对账：每轮 6 个 nonce

当前驱动对每协议产生 before、sandbox、after 三个互异 nonce。--protocol both 为两个协议，共 2×3=6 个 nonce；不是 9 个。沙箱 nonce 未收到可以是正常候选结果，须同时核对前后宿主对照确实送达、完整观察窗、日志采集完整及操作系统拒绝证据。任何探针运行错误不能当作拒绝。

接收端原件须复制到已注册的 all43 根内本轮独立材料目录，保留原文件字节。所有 --reconcile、--receiver-log、--receiver-summary 路径必须在：

~~~text
D:\Animation-Model-Training\reviews\codex-supervision\2026-10-06-all43-sandbox-repair
~~~

运行完整对账命令（替换三份原始文件的实际相对路径，填入真实整数 rc，不能假定为 0）：

~~~powershell
& '.\.venv\Scripts\python.exe' -X utf8 -B '.\tools\sandbox_external_test_driver.py' --reconcile '<注册根内本轮sender.json路径>' --receiver-log '<注册根内接收原件.jsonl路径>' --receiver-summary '<注册根内接收原件.jsonl.summary.json路径>' --receiver-rc <接收器真实整数退出码>
$reconcileRc = $LASTEXITCODE
~~~

必须交付该轮发送报告及其引用的全部接口、探针 stdout/stderr/rc 与场景绑定文件，以及接收原件三件和生成的对账回执，交 Codex 独立复核。

rc=0 仅表示相应采集或对账环节成功，不是生产许可。LAN IPv4、真实外部 IPv6及本机 IPv4证据须按用户批准的联合策略逐协议重算；不足项保持 UNVERIFIED，production=CLOSED。

## 当前绑定与修订结论

- 发送驱动 SHA256：99324c8a5343ab1379f290f1c9b2b46f70ae13e3a3f346e23249f6c1bc236292。
- 接收器 Python 原件 SHA256：571f4ce31465a84147395abd9778845194ac591371234737ccf2abeebc6be75e。
- 发布 EXE 完整 SHA256：d6887098ccd3b1c3b9bde1180746558b78d2b2882b3cbee25d791c5f792f1cad。
- 本单命令参数、事件、自检及 nonce 数按当前源码核对；操作单文字修复合格，实际双端证据尚未提交或验收。本轮没有启动监听器、沙箱或网络发送。
