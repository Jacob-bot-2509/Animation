from pathlib import Path
import json,re,datetime,hashlib,sys
R=Path(r'D:\Animation-Model-Training');O=R/'reviews/codex-supervision/2026-10-06-scene-repair-takeover'
sys.stdout.reconfigure(encoding='utf-8')
p=R/'docs/项目总览/进度看板.md';before=p.read_bytes();text=before.decode('utf-8')
now=datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M')
text=re.sub(r'^# 进度看板\(更新于 .*?\)', '# 进度看板(更新于 '+now+')',text,count=1)
old='原输入被覆盖、旧清单 SHA 失效，须停写并保全候选后恢复原始输入'
assert old in text;text=text.replace(old,'原输入及清单已恢复，历史 SHA 匹配；输入只读，后续修订落独立新版本')
text=text.replace('linalg-048:Codex 复验 296 对(进行中)→ 协议 v3 实施(Codex)→ 密度账本(我:47 题核心族全量识别)→ 一致发布',
 'linalg-048:296 身份/覆盖已核验，Codex 3 对重点复验，其余 293 对待逐条复核→ 协议 v3 已实现→ 47 题核心分组纠正为 46 任务→ 完整密度/独立验收后再考虑发布')
marker='## Codex 本轮监督检查点'
assert text.count(marker)==1
text=text.split(marker)[0].rstrip()+r'''

## Codex 接手修复检查点

- Claude 已确认 Task wjo6lp5tq 完成并停止写入；105 个后续智能体因余额不足失败。作者全量审计覆盖 264 题，判定 143 条需改写；不能称全部改写或独立验收完成。
- 原 20 个 chunk 与 listing 共 21 文件已恢复历史原字节，SHA 全匹配，并验证普通写入被可撤销只读保护拒绝；18 条原地改写完整保全。
- 新 inputs-v2：20 个非空、只读分块，包含 264 条完整记录和逐条来源绑定。新暂存入口只生成新候选；旧纯 scene 自动切换 selector 路径已停用。
- 工作流返回 39 条修订，与保全结果合并后有 53 条候选。Codex 修正正定逆证明漏掉 A 的错误及公式问题；53 条 scene 公式无阻断项，但完整独立数学与视觉验收仍未完成；还有 90 条没有改写候选。
- 九道旧训练题的题干、过程、答案已落成实际新版本 math-corrected-v1（全 47 条，修订 9 条），另有 math-9-corrected.md；不是仅提案，原绑定题库及正式 manifest 未改。
- 37 项代码回归通过，32 项精确公式/证明缺陷检查通过；三类小样既有 26 项符号检查仍为具名范围证据，不扩为全量验收。
- 核心分组修正版计 46 任务；独立留出规范已纠正。现有成员按未曝光排除规则的合格总体为 0，需新辅助总体、角色隔离及最终验证；没有校准结论。
- 正式数据、评测/测试锁和旧原生回执保持；资产 1/497 NOT READY，生产隔离 CLOSED，训练未启动。

修复详情：[FIX_REPORT.md](../../reviews/codex-supervision/2026-10-06-scene-repair-takeover/FIX_REPORT.md)。
精确九题：[math-9-corrected.md](../../reviews/codex-supervision/2026-10-06-scene-repair-takeover/math-9-corrected.md)。
'''
text=text.replace('数据/数学审计已有记录 → 人工审阅 ⏳(你)；训练门禁未全通过',
 '原题审阅记录已有 → 场景改写与独立验收 ⏳；训练门禁未全通过')
with (O/'progress-board.before.md').open('xb') as f:f.write(before)
assert p.read_bytes()==before,'Concurrent board update'
p.write_bytes(text.encode('utf-8'))
with (O/'progress-board-fix.json').open('x',encoding='utf-8') as f:
 json.dump({'path':p.relative_to(R).as_posix(),'before_raw_sha256':hashlib.sha256(before).hexdigest(),
  'after_raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'updated_at':now},f,ensure_ascii=False,indent=2)
w=R/'reviews/codex-supervision/2026-10-04-live-watch/latest.json'
data=w.read_bytes();d=json.loads(data)
with (O/'watcher-after.original.json').open('xb') as f:f.write(data)
print(json.dumps({'board_updated':now,'watcher_pid':d['watcher_pid'],'heartbeat':d['time'],
 'watched_paths':len(d['hashes']),'core_drift':d['core_drift']},ensure_ascii=False))
