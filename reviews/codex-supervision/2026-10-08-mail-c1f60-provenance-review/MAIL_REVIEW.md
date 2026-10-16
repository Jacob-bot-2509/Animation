# 本轮邮件来源澄清与本地诊断修复

run-c1f60bb763b243f8a0f56f1135bed611 的 packet 只有 msg_1791469332606_761。已按真实 mail_watch.message_hash 算法核对 packet 与原始邮件快照一致；本批此前没有 ACK。额外收到 msg_1791469608069_762，仅作为后续来源说明和本地材料状态上下文，不将其列入本 packet 的 RESULT 或代替用户授权。本轮没有启动或验收双端实验，也没有修改调度器或生产门禁。

## 来源和新旧版本

Claude 在 msg_761 明确说明：上一轮 receiver 目录的两份文件是聊天转写重建的本地副本，而非证人原字节；第一次存档及第二次 json.dumps 重写造成字段/字节不一致。这是作者来源说明，不证明证人机实际文件本身未被修改。旧归档 2026-10-08-lan-receiver-review 的 19 件材料逐项哈希复核通过，保留对当时副本的拒收结论，不修改旧报告或原始快照。

观察器随后于 22:25:41 记录接收文件再次变化。当前日志 SHA256 为 0f490152cc50cdfcfc5b7fa9cf050360f51baffea17bb492818142e48f52eef4；summary SHA256 为 d358fa61778cca1c5e40dd9a12486407a06e5c3e0b89ec8a82e104d783623179。当前日志哈希与 summary 声明相同，EXE 标识文本完整且与批准值相同，summary 时间间隔为 300002524700 纳秒，即 3000025247/10000000 秒，满足至少 300 秒；不是“恰好 300 秒”。这些只证明当前文件的内部一致性，不能单凭文件自称和作者结论证明原件来源或授予双端资格。发送侧保持原字节。

## Codex 已修改及独立验证

发现 Codex 上一轮 inspect_receiver.py 对所有非 created 事件强制落入 summary 的采集窗口。证人源码实际先记 finished，再计算实现 SHA、记录 closed 事件，因此合法 closed 时间可以晚于 finished。该检查会产生错误拒收。

Codex 已在本目录新建修正版本 inspect_receiver.py，保留旧冻结脚本及 before 快照。listening / payload 仍要求落入真实窗口；closed 要求不早于 finished。后续注册对账仍负责序列、完整生命周期与其它资格检查；诊断初筛通过也只到 READY_FOR_REGISTERED_RECONCILIATION。工具 SHA256：1215462aaf73f70dd698b54b2f218b6734d1975be7cd66485009cad0836c6d17。精确差异见 diagnostic-fix.patch。

10 项本地合成验证通过：健康合成材料只到对账准备状态；closed 在 finished 后合法记账；窗口外 payload 仍被拒绝；缺 rc、布尔伪零、非零 rc 均拒绝；负时长拒绝；实际 sandbox nonce 即便标记不完整仍失败；原字节不改；畸形 JSON 结构化拒收。没有进行新原生网络作业或把合成检查当作原生验收。

当前文件只读预检 rc=2，仍有 3 项实际阻断：
- 接收 bind=0.0.0.0 与发送具名端点 192.168.1.83 不匹配。
- 接收日志 0 payload，4 个宿主 before/after 健康 nonce 缺失。
- 实际接收器进程退出码及来源未提交，未假设为 0。

当前判定 NEEDS_EVIDENCE。工具在本地诊断范围合格；双端未验收，production=CLOSED，不给全 43 点通过或网络隔离失败结论。

## 对后续因果判断的约束

msg_762 以发送端 172.30.43.234/16 与证人 192.168.1.83 不同前缀推断零入账必由拓扑导致。这是待验证推断。原 sender 的 TCP before/after 均为 completed，UDP 为 sent，但 receiver_delivery_verified=false；原 tracert 四跳均超时。上述材料既不证明完整证人送达，也不足以单独确定零入账的原因，不能将“拓扑所致”记成实证或据此跳过健康对照。

本轮只修正文档/诊断中的因果和时序判断，不批准邮件提出的新轮执行。后续授权工作应使用本目录修正工具，并提交匹配的真实原件/summary/退出码及健康对照材料；需要重采时保留旧版本，用唯一新轮。不得改时间、哈希、地址来让旧材料通过。新材料由新邮件触发独立审阅，不在本批代 ACK。

RESULT.json 仅覆盖 msg_761，状态 NEEDS_EVIDENCE；实际回信含 mail_run_id、本地修复内容、资格边界和继续工作要求。冻结本目录报告与快照，活动实验及观察器目录不冻结；使用已有 mail_watch.py ack。
