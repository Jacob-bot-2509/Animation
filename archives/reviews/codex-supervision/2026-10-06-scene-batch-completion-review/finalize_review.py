import copy,datetime,hashlib,json,sys
from pathlib import Path
ROOT=Path(r'D:\Animation-Model-Training');OUT=Path(__file__).resolve().parent;OLD=OUT.parent/'2026-10-06-scene-repair-takeover';sys.path.insert(0,str(ROOT/'tools'))
from scene_sweep_protocol import verify_inputs
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat();sha=lambda b:hashlib.sha256(b).hexdigest()
prior=json.loads((OLD/'final-verification.json').read_text('utf-8'));verified=[]
for rel,item in prior['source_bindings'].items():
 data=(ROOT/rel).read_bytes();assert sha(data)==item['raw_sha256'] and len(data)==item['bytes'],rel;verified.append(rel)
before=json.loads((OUT/'source-bindings.before.json').read_text('utf-8'))
for rel,item in before.items():
 data=(ROOT/rel).read_bytes();assert sha(data)==item['raw_sha256'] and len(data)==item['bytes'],rel
receipt=json.loads((ROOT/'reviews/2026-10-06-linalg048-admission/v3-receipt-bound/receipt.json').read_text('utf-8'))
for rel,item in receipt['source_bindings'].items():
 data=(ROOT/rel).read_bytes();assert sha(data)==item['raw_sha256'] and len(data)==item['bytes'],rel
_,rows=verify_inputs(OLD/'inputs-v2');records={x['record']['id']:x['record'] for x in rows};patches=json.loads((OUT/'scene-candidates-corrected-v5.json').read_text('utf-8'))['records'];changes={p['id']:p['fields']['scene_spec'] for p in patches};candidate=OUT/'scene-candidates-144-v5';selection=json.loads((candidate/'draft-selection.candidate.json').read_text('utf-8'));count=0
for entry in selection['entries']:
 for line in (candidate/entry['path']).read_text('utf-8').splitlines():
  rec=json.loads(line);old=records[rec['id']];assert all(rec[k]==old[k] for k in ('problem','solution','answer'));assert rec['scene_spec']==changes.get(rec['id'],old['scene_spec']);assert all(rec.get(k) is False for k in ('admitted','training_admitted','render_verified','animation_verified'));count+=1
assert count==264
fixed=json.loads((OUT/'corrections.json').read_text('utf-8'));ids=sorted({x['id'] for x in fixed if x['kind']!='fraction_braces'});md=['# 精确场景修订稿','以下为本轮十一题的新场景；原始题干、过程、答案与来源绑定。直角边界的题干修订另存 math-wording-c27-04.candidate.jsonl。完整视觉验收未执行。']
for pid in ids:
 rec=records[pid];md+=['## '+pid,'题目：'+rec['problem'],'答案：'+rec['answer'],'修订场景：']+changes[pid]['steps']
(OUT/'SCENE_CORRECTIONS.md').write_text('\n\n'.join(md)+'\n',encoding='utf-8',newline='\n')
report=r'''# 十批场景补齐：独立复验与修复

Claude 的 msg565/566/567 已实际处理。十批补丁为 93 个唯一 ID，覆盖原待补清单全部 90 条；额外三条为 c11-01、c11-04、c23-01，其中前两条覆盖此前候选。因此旧 53 与新 93 的并集为 144，生成完整 264 记录的 scene-candidates-144-v5。仅暂存，未切换选择器、未准入。

## 数学与证明修复

本轮逐题核对新 93 条的题干目标、答案和场景关键公式，修复 11 题的运算、证明或完整性问题。完整修订见 SCENE_CORRECTIONS.md；逐项 before/after 与依据见 corrections.json。

| 题目 | 已修复内容 |
|---|---|
| c07-03 | 换元等式两端均写出定积分上下限 |
| c10-05 | 删除对任意 m,l 不成立的奇子列链，按 m≤l/m>l 证明交叉序 |
| c17-04 | 补齐任意给定点的平面束分类，而非只算指定点 |
| c20-04 | 修正 Wc=(6t/11)n、交叉项系数；补精确特征方程 |
| c25-05 | 用交线上四个点证明不存在包含整条曲线的平面 |
| c26-01 | 补核与像的双向包含证明 |
| c27-04 | 明确 k=0 是直角；题干“锐夹角”另存完整记录修订候选 |
| c34-05 | 保持右乘次序，修正 e23 e12=0，而非错误的 e12 e23 |
| c43-03 | 将“其余同理”改为全部九个配对值 |
| c48-04 | a²=81/16；方差逐式得到117/4 |
| c49-05 | 对平均尾部用Markov，替代不能消失的并集界 |

c49-05 的修正链：先对固定 M 控制截断偏差，再由
\[
P(|\overline X_n-\mu|\ge\varepsilon)
\le\frac{3\tau_M}{\varepsilon}+\frac{9M^2}{n\varepsilon^2},
\quad \tau_M=E(|X_1|\mathbf1_{|X_1|>M})\to0,
\]
先令 n→∞，再令 M→∞。没有增加有限方差假设。

原补丁公式审计发现 370 个 L009 格式项，涉及 54 题。新合并版递归补全所有分数参数花括号；144 条 scene 公式 hard/quarantine 为零，无小数文字。这里的格式项不等同于数学错误。完整264数学/语义验收及此前保留的51条候选的完整独立复核仍未完成。

## 工具与历史证据

修复 tools/audit_staged_scenes.py：制表符不再被排除；缺目录/清单/文件、空输入、坏哈希、覆盖数不符、陈旧来源和验收标志均失败。读取末尾复查选择器、回执、来源和候选字节。合法说明文字换行保留；公式内换行和其他损坏控制字符拒绝。工具仅判断来源/字节及控制字符，不宣称数学或视觉验收。

批次六曾将同名补丁和 staged-v1 从 c46d5e1 改写为 3abef1d。已从 Git 保全失效前版21文件到 batch6-invalid-c46d5e1：18个候选文件的原rawSHA均与旧选择器匹配，补丁rawSHA与旧回执匹配；独立复现41条损坏字符串。旧回执原字节保留，未重签。当前十批原文件均保持本轮读取时的字节。

## 复验范围与当前状态

55 项代码回归通过（新增16项+既有39项）；55 项具名精确公式/反例检查通过。十批264记录及合并264记录共2904条通过来源/字节与控制字符检查。它们不是2904个独立数学样本，也不是全量数学证书。

完整新版本的数学三字段264/264与原选版本一致。c27-04的题干用词修正单独生成完整记录 math-wording-c27-04.candidate.jsonl，未激活，以免伪装成数学三字段不变的scene-only补丁。

正式 manifest、train/eval/test、双锁、资产文件、活动草稿选择器、原生回执及32来源绑定保持不变。原始只读输入验证通过。生产隔离 CLOSED，资产 1/497 NOT READY，训练未启动；没有本轮原生渲染或视觉验收。现有留出设计合格总体仍为0，未声称独立校准完成。

实际证据：preflight-results.json、corrected-scene-qa.json、exact-math-checks.json、suite-final-result.json、staged-integrity-final.stdout.raw.txt、batch6-invalid-archive-manifest.json、final-verification.json、delivery-manifest.json。
'''
(OUT/'FIX_REPORT.md').write_text(report,encoding='utf-8',newline='\n')
board=ROOT/'docs/项目总览/进度看板.md';old=board.read_bytes();(OUT/'progress-board.before.md').write_bytes(old);text=old.decode('utf-8-sig');first=text.splitlines()[0];text=text.replace(first,'# 进度看板(更新于 '+now[:16].replace('T',' ')+')',1)
oldrow=next(line for line in text.splitlines() if line.startswith('| 264 题人工审阅'))
newrow='| 264 题人工审阅 | 原题人工审阅已记录；场景独立验收未完成 | 新93补丁覆盖待补90条；合并144场景修订的新264记录候选。Codex修复11题运算/证明与分数格式，55代码回归及55精确检查通过；数学/视觉全量验收未完成，未发布 |';text=text.replace(oldrow,newrow,1)
text=text.replace('## Codex 接手修复检查点','## 2026-10-06 14:53 接手检查点（历史，当前状态见下）',1)
text+='\n## '+now[:16].replace('T',' ')+' 场景补齐复验\n\n- 待补90条均有候选；93唯一补丁与旧53重叠2条，合并144条。实际完整新版本scene-candidates-144-v5含264记录，数学三字段与原来源一致。\n- 已修复11题的运算/证明或目标遗漏，并补全分数括号；直角边界题干另存新候选。55代码回归、55具名精确数学检查通过，完整264数学/视觉未验收。\n- 批次六被覆盖的失效前版21文件已从Git保全；旧SHA匹配，复现41条损坏字符串。当前10批与新合并版共2904记录的来源/字节与控制字符复验通过。\n- 新候选未切selector；正式数据、锁及原生证据保持；隔离CLOSED、资产1/497 NOT READY、训练未启动。\n\n[修复报告](../../reviews/codex-supervision/2026-10-06-scene-batch-completion-review/FIX_REPORT.md) · [十一题精确场景](../../reviews/codex-supervision/2026-10-06-scene-batch-completion-review/SCENE_CORRECTIONS.md)\n'
assert board.read_bytes()==old;board.write_text(text,encoding='utf-8',newline='\n')
watch=ROOT/'reviews/codex-supervision/2026-10-04-live-watch/watch_claude.py';oldwatch=watch.read_bytes();(OUT/'watch_claude.before.py').write_bytes(oldwatch);added=['tools/audit_staged_scenes.py','tests/test_audit_staged_scenes.py']
for n in range(1,11):
 added += [f'reviews/2026-10-06-scene-standard-sweep/batch{n}-patches.json',f'reviews/2026-10-06-scene-standard-sweep/batch{n}-staged-v1/stage-receipt.json',f'reviews/2026-10-06-scene-standard-sweep/batch{n}-staged-v1/draft-selection.candidate.json']
added += [p.relative_to(ROOT).as_posix() for p in candidate.rglob('*') if p.is_file()]
added += [(OUT/name).relative_to(ROOT).as_posix() for name in ('scene-candidates-corrected-v5.json','math-wording-c27-04.candidate.jsonl','math-wording-c27-04-receipt.json','FIX_REPORT.md','SCENE_CORRECTIONS.md')]
code=oldwatch.decode('utf-8');anchor="write('watcher.json',{'pid'";idx=code.index(anchor);code=code[:idx]+'watched=sorted(set(watched)|set('+repr(added)+'))\n'+code[idx:];watch.write_text(code,encoding='utf-8',newline='\n');(OUT/'watch-paths-added.json').write_text(json.dumps(added,indent=2)+'\n',encoding='utf-8')
verification={'checked_at':now,'protected_formal_bindings_verified':len(verified),'old_native_sources_verified':len(receipt['source_bindings']),'original_received_bindings_unchanged':len(before),'input_records_verified':264,'merged_scene_changes':144,'staged_records':264,'math_three_fields_unchanged':264,'new_scene_latex_blockers':0,'regression_tests':55,'exact_formula_checks':55,'full_264_math_and_visual_acceptance':False,'production_gate':'CLOSED','training_started':False,'board_before_raw_sha256':sha(old),'board_after_raw_sha256':sha(board.read_bytes()),'watch_paths_added':len(added)};(OUT/'final-verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(verification,ensure_ascii=False))