from pathlib import Path
import json,hashlib,math,difflib
from fractions import Fraction
from datetime import datetime
R=Path('.').resolve();O=R/'reviews/codex-supervision/2026-10-08-dual-endpoint-supervision'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,s):p.write_bytes(s.encode('utf-8'))
p=R/'NEWRELEASE.md';before=p.read_bytes();assert before==(O/'before-NEWRELEASE.md').read_bytes()
s=before.decode('utf-8');s=s.replace('沙箱双端实验为本版本后唯一剩余验收项（2026-10-08 下午执行）。','沙箱双端实验现已开始采集，尚待双端原始材料对账；后续资格以各项独立验收结论为准。')
s=s.replace('（2663 条按题去重公式、5212 处原文出现）','（2711 条按题去重公式、5320 处原文出现，以当前交付索引汇总）')
s=s.replace('3840×2160、逐页 PNG 与视频首帧逐像素一致','3840×2160；本轮 19 条重渲染的 75 个页面起始帧与 PNG 逐像素一致，其余视频继承父交付验证并核对当前 SHA')
s=s.replace('用户三条高清硬标准定量全过：分辨率全 4K、完整页占用槽位代理最小 92px（远超 24px 阈值）、165 条全覆盖。占用代理不作最小字形认证。','定量记录：分辨率全 4K、165 条全覆盖，559 个完整页的每项占用包围盒高度代理最小为 92px。该代理不等同于最小字形高度，不能凭其大于 24px 宣称最小字形标准通过；逐页图像审阅资格另以 Codex 当前回执为准。')
s=s.replace('（完整页 min 92 / p10 161.3 / median 219 px 占用代理）','（559 个完整页：最小值 92px / 第十分位最近秩 484/3 px / 中位数 658/3 px，均为每项占用包围盒高度代理）')
s=s.replace('沙箱双端实验（2026-10-08 下午）：LAN IPv4 证人 + 外部 IPv6 证人，新轮次 lan/v6-2026-10-07-b，操作单 reviews/2026-10-07-witness-runbook.md。','沙箱双端实验：当前 LAN 采集轮次 lan-2026-10-08-a，run remote-271e1c881c4f473fb027f5f28d4a3bd5，发送侧 complete=true、UNVERIFIED；收齐证人原始 JSONL、对应 summary 和真实退出码后对账。外部 IPv6 须另起唯一轮次并核实外部拓扑，不能沿用旧日期轮次。操作单 reviews/2026-10-07-witness-runbook.md。')
assert s!=before.decode('utf-8');write(p,s);(O/'after-NEWRELEASE.md').write_bytes(p.read_bytes())
p=R/'reviews/2026-10-07-witness-runbook.md';before2=p.read_bytes();assert before2==(O/'before-2026-10-07-witness-runbook.md').read_bytes()
s=before2.decode('utf-8')
s=s.replace('2026-10-07 修订 b 轮','2026-10-08 当前采集修订')
s=s.replace('本轮轮次名:**lan-2026-10-07-b**、**v6-2026-10-07-b**;日志必须用新文件名(旧日志混有旧 nonce,不能复用)。','当前 LAN 发送侧已经完成：轮次 **lan-2026-10-08-a**，run **remote-271e1c881c4f473fb027f5f28d4a3bd5**。应收集与此 run 对应的接收端原始材料，不能通过重命名旧日志补证。下文命令用于后续新轮，接收日志文件名和发送轮次必须使用新的唯一名称。外部 IPv6 新轮次由发送端与证人明确确认后填写，不能复用旧日期轮次。')
s=s.replace('开头必须是 **d6887098**。','完整 SHA256 必须等于 **d6887098ccd3b1c3b9bde1180746558b78d2b2882b3cbee25d791c5f792f1cad**。')
s=s.replace('我拿到后先做本机连通性测试(宿主 TCP/UDP 到 49001/49002),通了才让你开接收器。','先启动接收器并确认 UDP 49001、TCP 49002 均已 LISTENING，再由发送端进行宿主前对照。UDP sendto 成功不代表接收端收到；最终通路健康由原始接收日志中的前后对照 nonce 证明。')
s=s.replace('lan-round-b.jsonl','<新的LAN日志名>.jsonl').replace('v6-round-b.jsonl','<新的IPv6日志名>.jsonl')
s=s.replace('lan-2026-10-07-b','<新的LAN轮次>').replace('v6-2026-10-07-b','<新的IPv6轮次>')
s=s.replace('echo %errorlevel%','echo $LASTEXITCODE')
s=s.replace('把 <新的LAN日志名>.jsonl 的**内容**和退出码发我。','立即记录 PowerShell 中的 $LASTEXITCODE（若使用 cmd，则用 echo %errorlevel%）。提交 **原始 JSONL 文件、同名 .jsonl.summary.json 文件和真实退出码**，不要只提交截图、摘录或重新序列化后的文字。')
s=s.replace('同样等自动停,发我 <新的IPv6日志名>.jsonl 内容和退出码。','同样等自动停，立即记录真实退出码，并提交 **原始 JSONL 文件、同名 .jsonl.summary.json 文件和真实退出码**。')
s=s.replace('9 个 nonce 逐项','每轮 2 协议 × 3 阶段 = 6 个 nonce 逐项')
s=s.replace('出对账回执后交 Codex 独立验收。你那边收工。','出对账回执后交 Codex 独立验收。合格接收日志应包含每协议 before、after 两个对照，共 4 个完整 payload；两个 sandbox nonce 均不得出现，出现任意一个即边界 FAIL。外部 IPv6 须证明接收机不属于发送端同一 LAN /64，LAN 证人不等于外部证人。LAN / 外部单项对账也不等于全 43 点或生产放行。你那边收工。')
assert s!=before2.decode('utf-8');write(p,s);(O/'after-2026-10-07-witness-runbook.md').write_bytes(p.read_bytes())
patch=''
for name,old,new in [('NEWRELEASE.md',before.decode('utf-8'),(R/'NEWRELEASE.md').read_text('utf-8')),('reviews/2026-10-07-witness-runbook.md',before2.decode('utf-8'),s)]:
 patch+=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=name+' before',tofile=name+' after'))
write(O/'documentation-changes.patch',patch)
receipt={'status':'PASS_DOCUMENTATION_CORRECTED','updated_at':datetime.now().astimezone().isoformat(),'files':[{'path':name,'sha256':sha(R/name)}for name in ['NEWRELEASE.md','reviews/2026-10-07-witness-runbook.md']],'driver_unchanged':sha(R/'tools/sandbox_external_test_driver.py')==json.loads((O/'source-and-evidence-before.json').read_text('utf-8'))['driver_sha256']}
assert receipt['driver_unchanged'];write(O/'documentation-repair-receipt.json',json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,ensure_ascii=False))
