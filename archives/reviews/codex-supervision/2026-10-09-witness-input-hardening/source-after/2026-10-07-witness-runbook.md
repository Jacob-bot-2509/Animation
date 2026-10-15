# 证人机操作单：v3 输入与原件绑定修订

本单用于后续新轮次人工采集。Codex 本次只修复和验证本地工具，不执行或验收双端实验。旧 LAN-a、LAN-b、LAN-c 原件保留原判定，不重命名、不补写、不因工具升级自动合格。

## 1. 准备两份文件

把下面目录内的 witness_receiver_v3.exe 和 start_witness_capture.ps1 复制到证人机同一目录，或复制同一归档内 witness-v3-package.zip 后解压。旧 v2 不覆盖。

    D:\Animation-Model-Training\reviews\codex-supervision\2026-10-09-witness-input-hardening\release

v3 EXE 完整 SHA256 必须为：

    02d781bc22286b1e8417ddb119ec6b529e5a9101b1fad758a41a06fbc2eb44bf

在两份文件所在目录打开 PowerShell，整块复制：

    Get-FileHash -LiteralPath .\witness_receiver_v3.exe -Algorithm SHA256
    powershell.exe -NoProfile -File .\start_witness_capture.ps1

第二条默认打印 PLAN: no process started，退出码 3，不启动监听。启动器显式执行前会校验 EXE 完整哈希，错配拒绝启动。若本机策略拦截脚本，保留完整错误交给负责人处理，不自行修改系统策略。

## 2. 本机自检

    powershell.exe -NoProfile -File .\start_witness_capture.ps1 -Execute -SelfTest

成功时最终 JSON 的 failures 为 []，IPv4、IPv6 两个 case 的 rc 均为 0，最后显示 CAPTURE_FINISHED ... exit_code=0。实际退出码由父启动器写入新目录的 process-exit.json，不需要另用 echo 转述。

自检只用本机回环，不能证明 LAN、外部 IPv6 或沙箱隔离。其 mode=SELFTEST，检查器拒绝将它用于正式 SERVE 轮次。

## 3. 确认地址和唯一新轮次

列出证人机当前地址：

    Get-NetIPAddress | Where-Object { $_.AddressState -eq 'Preferred' } | Select-Object InterfaceAlias,AddressFamily,IPAddress,PrefixLength

与发送端确认具体地址及唯一新轮次。IPv4 用本机 LAN 单播地址；外部 IPv6 用经确认的稳定全局单播地址，另保留拓扑材料。禁用 0.0.0.0、::、回环、多播、链路本地地址。

下面整块复制，只在提示出现时输入已确认的地址和轮次，不编辑命令参数：

    $witnessBind = Read-Host '输入本机已确认的具体单播 IP'
    $witnessRound = Read-Host '输入与发送端一致的新轮次名，仅字母数字下划线连字符'
    if (-not $witnessRound) { throw '轮次不能为空' }
    $parsedWitness = [System.Net.IPAddress]::Parse($witnessBind)
    $localWitness = @(Get-NetIPAddress | Where-Object { $_.IPAddress -eq $parsedWitness.ToString() -and $_.AddressState -eq 'Preferred' })
    if ($localWitness.Count -ne 1) { throw '地址不是唯一的本机有效地址；停止并核对' }
    powershell.exe -NoProfile -File .\start_witness_capture.ps1 -Execute -Bind ($parsedWitness.ToString()) -Round $witnessRound

启动器自动新建 captures\轮次-随机标识，固定本轮文件名。正式模式固定 UDP 49001、TCP 49002、观察 300 秒，不覆盖旧日志。两个协议都绑定成功才输出 kind=listening 和两个 endpoint；必须显示具体 IP。看到后将完整输出、本轮地址和轮次交给发送端。

发送端使用当前 tools/sandbox_external_test_driver.py，按已登记流程采集。默认 PLAN；不得因本单自动执行实验。后宿主对照失败时当前修订会返回 2 并保留失败材料，不记采集完整。

## 4. 完成和原件传输

等待自动结束。CAPTURE_FINISHED 的 exit_code=0 只证明接收进程成功结束，健康通路仍需接收日志中的前后 nonce。

正式 SERVE 新目录必须包含以下五份原件及各自 .b64：

- receiver.jsonl：原始事件，不编辑或重新序列化。
- receiver.jsonl.summary.json：同一接收 run 的完整摘要。
- stdout.bin、stderr.bin：子进程原始输出。
- process-exit.json：父启动器记录命令、轮次、进程标识、实际退出码、EXE 前后哈希、启动器哈希和上述四份原件哈希。

优先提交完整目录。若只能聊天传输，逐份提交完整 .b64 的内容、原文件名和原目录名；不要加省略号，不转抄退出码。Base64 是原字节的单行编码，无证书头，也不表示认证。

单份解码的可复制命令：

    $encodedFile = Read-Host '输入收到的 b64 文件完整路径'
    $rawOutput = Read-Host '输入要新建的原文件完整路径'
    $rawBytes = [Convert]::FromBase64String([IO.File]::ReadAllText($encodedFile))
    $rawStream = [IO.File]::Open($rawOutput,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
    try { $rawStream.Write($rawBytes,0,$rawBytes.Length) } finally { $rawStream.Dispose() }

输出文件必须不存在；不得覆盖已有原件。解码后的每份材料仍要核对完整 SHA256。Base64 无损搬运不能证明远程来源真实。

## 5. 训练机只读材料检查

把新接收目录和原始 sender.json 放入已登记的 reviews/codex-supervision/2026-10-06-all43-sandbox-repair 范围，保留接收目录原名。在项目根目录复制：

    $senderOriginal = Read-Host '输入 sender.json 原件完整路径'
    $captureOriginal = Read-Host '输入本轮接收目录完整路径'
    & .\.venv\Scripts\python.exe -X utf8 -B .\tools\inspect_witness_evidence.py --sender $senderOriginal --capture-directory $captureOriginal

检查器不接受手工 --receiver-rc。命令、版本、轮次、日志 run、具体 endpoint、生命周期、前后 nonce 和原件哈希都必须对应。缺件或错配为 NOT_ACCEPTED，退出码 2；完全对应也仅为 READY_FOR_REGISTERED_RECONCILIATION，还须按登记规则检查发送端和原生传输，不能解读为沙箱通过。

旧归档 inspect_receiver.py 保持冻结；新入口是 tools/inspect_witness_evidence.py。旧材料缺少新回执时保留原判定，不人工制造回执。

新版本正式对账入口必须使用 --receiver-capture 指向同一目录；手填 --receiver-rc 不能绕过新回执。旧版本保留历史入口的原约束，不因此自动获得新资格。

## 6. 判定边界

both 轮每个协议应收到 before、after 两个精确 nonce，共四个健康对照。任意 sandbox nonce 出现在原始 payload 中即边界失败；未出现不能替代健康对照、窗口、拓扑证明。

host_pretest_witness.py 只诊断当前命名 IPv4 节点。LOCAL_CONNECT_COMPLETED、CONNECTION_REFUSED、TIMEOUT_UNCONFIRMED 或 UDP send 成功均不能证明 nonce 已到达。它保留整数纳秒与精确毫秒分数，不估算。正式监听后的健康对照必须用驱动生成的 nonce；不要把 pretest payload 混入正式接收日志。

父启动器回执是哈希绑定的本地采集记录，不是远程认证或时钟同步证明。不同主机时间数值重叠不单独证明同步；PyInstaller 父启动器 PID 与子接收器 PID 可以不同。外部 IPv6 须独立证明接收端不在发送端同一 LAN /64，LAN 材料不替代。

本次工具修复不使全 43 点或生产自动放行；保持 production=CLOSED、原生沙箱 UNVERIFIED、全局隔离 NOT_ESTABLISHED。
