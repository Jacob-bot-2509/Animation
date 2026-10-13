# 双端沙箱实验全流程(证人机操作单,2026-10-07 修订 b 轮)

角色:**你** = 证人机(第三台物理机);**我** = 训练机(发送端)。
接收器必须用 v2 版 `witness_receiver_v2.exe`(SHA256 以 d6887098 开头)。
本轮轮次名:**lan-2026-10-07-b**、**v6-2026-10-07-b**;日志必须用新文件名(旧日志混有旧 nonce,不能复用)。

## 0. 前置:确认 exe 版本

在证人机 exe 所在目录:
```
certutil -hashfile witness_receiver_v2.exe SHA256
```
开头必须是 **d6887098**。不是的话,回训练机拷这个文件:
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

我拿到后先做本机连通性测试(宿主 TCP/UDP 到 49001/49002),通了才让你开接收器。

## 3. LAN 轮(IPv4)

**你**启动接收器:
```
witness_receiver_v2.exe --serve --bind <你的IPv4> --log lan-round-b.jsonl
```
看到 **LISTENING**(两协议都绑成功才显示)→ 马上告诉我。

**我**:跑 `--execute-native --bind <你的IPv4> --round lan-2026-10-07-b --scope lan --protocol both`
(宿主前对照 → 沙箱探针 → 21 秒观察 → 后对照,约 2 分钟)。

**你**:接收器默认 300 秒自动停;看到它退出后:
```
echo %errorlevel%
```
把 lan-round-b.jsonl 的**内容**和退出码发我。

## 4. 外部 IPv6 轮

**你**启动接收器:
```
witness_receiver_v2.exe --serve --bind <你的稳定IPv6> --log v6-round-b.jsonl
```
看到 LISTENING → 告诉我。

**我**:跑 `--execute-native --bind <你的稳定IPv6> --round v6-2026-10-07-b --scope external --protocol both`。

**你**:同样等自动停,发我 v6-round-b.jsonl 内容和退出码。

## 5. 收尾

我这边用 `--reconcile` 把两端证据对账(9 个 nonce 逐项、送达/未送达、观察窗、拓扑身份),出对账回执后交 Codex 独立验收。你那边收工。

## 注意

- 防火墙:UDP 49001、TCP 49002 入站必须放行(已放行就保持)。
- 接收器要在我的 run 全程保持监听,期间别动证人机。
- 退出码 rc0 = 采集完整,不代表沙箱隔离通过;对账和 Codex 验收说了算。
