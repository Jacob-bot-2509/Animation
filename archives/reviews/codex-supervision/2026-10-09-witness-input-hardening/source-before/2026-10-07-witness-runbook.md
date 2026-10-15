# 双端沙箱实验全流程(证人机操作单,2026-10-08 当前采集修订)

角色:**你** = 证人机(第三台物理机);**我** = 训练机(发送端)。
接收器必须用 v2 版 `witness_receiver_v2.exe`(SHA256 以 d6887098 开头)。
当前 LAN 发送侧已经完成：轮次 **lan-2026-10-08-a**，run **remote-271e1c881c4f473fb027f5f28d4a3bd5**。应收集与此 run 对应的接收端原始材料，不能通过重命名旧日志补证。下文命令用于后续新轮，接收日志文件名和发送轮次必须使用新的唯一名称。外部 IPv6 新轮次由发送端与证人明确确认后填写，不能复用旧日期轮次。

## 0. 前置:确认 exe 版本

在证人机 exe 所在目录:
```
certutil -hashfile witness_receiver_v2.exe SHA256
```
完整 SHA256 必须等于 **d6887098ccd3b1c3b9bde1180746558b78d2b2882b3cbee25d791c5f792f1cad**。不是的话,回训练机拷这个文件:
`D:\Animation-Model-Training\reviews\codex-supervision\2026-10-06-witness-mail-review\release\witness_receiver_v2.exe`

## 1. 自检

```
witness_receiver_v2.exe --selftest
```
看到 "OK 收发通路正常" 继续;FAILED 就告诉我,别硬跑。

## 2. 确认地址并发我

```
ipconfig
```
把两样发我(照抄,别凭记忆):
- **稳定 IPv6**(不是"临时 IPv6"那一行)
- **局域网 IPv4**

先启动接收器并确认 UDP 49001、TCP 49002 均已 LISTENING，再由发送端进行宿主前对照。UDP sendto 成功不代表接收端收到；最终通路健康由原始接收日志中的前后对照 nonce 证明。

## 3. LAN 轮(IPv4)

**你**启动接收器:
```
witness_receiver_v2.exe --serve --bind <你的IPv4> --log <新的LAN日志名>.jsonl
```
看到 **LISTENING**(两协议都绑成功才显示)→ 马上告诉我。

**我**:跑 `--execute-native --bind <你的IPv4> --round <新的LAN轮次> --scope lan --protocol both`
(宿主前对照 → 沙箱探针 → 21 秒观察 → 后对照,约 2 分钟)。

**你**:接收器默认 300 秒自动停;看到它退出后:
```
echo $LASTEXITCODE
```
立即记录 PowerShell 中的 $LASTEXITCODE（若使用 cmd，则用 echo %errorlevel%）。提交 **原始 JSONL 文件、同名 .jsonl.summary.json 文件和真实退出码**，不要只提交截图、摘录或重新序列化后的文字。

## 4. 外部 IPv6 轮

**你**启动接收器:
```
witness_receiver_v2.exe --serve --bind <你的稳定IPv6> --log <新的IPv6日志名>.jsonl
```
看到 LISTENING → 告诉我。

**我**:跑 `--execute-native --bind <你的稳定IPv6> --round <新的IPv6轮次> --scope external --protocol both`。

**你**:同样等自动停，立即记录真实退出码，并提交 **原始 JSONL 文件、同名 .jsonl.summary.json 文件和真实退出码**。

## 5. 收尾

我这边用 `--reconcile` 把两端证据对账(每轮 2 协议 × 3 阶段 = 6 个 nonce 逐项、送达/未送达、观察窗、拓扑身份),出对账回执后交 Codex 独立验收。合格接收日志应包含每协议 before、after 两个对照，共 4 个完整 payload；两个 sandbox nonce 均不得出现，出现任意一个即边界 FAIL。外部 IPv6 须证明接收机不属于发送端同一 LAN /64，LAN 证人不等于外部证人。LAN / 外部单项对账也不等于全 43 点或生产放行。你那边收工。

## 注意

- 防火墙:UDP 49001、TCP 49002 入站必须放行(已放行就保持)。
- 接收器要在我的 run 全程保持监听,期间别动证人机。
- 退出码 rc0 = 采集完整,不代表沙箱隔离通过;对账和 Codex 验收说了算。
