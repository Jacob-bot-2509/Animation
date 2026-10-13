from pathlib import Path
import json,hashlib,sys,os,runpy,subprocess
from datetime import datetime,timezone,timedelta
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];PRIOR=ROOT/'reviews/codex-supervision/2026-10-05-strict-batch-audit';DRAFTS=ROOT/'reviews/2026-10-05-training-diversity-drafts'
sys.path.insert(0,str(OUT));import build_repaired_batches as B
BASE=json.loads((OUT/'repair-baseline.json').read_text(encoding='utf-8'))
exact=json.loads((OUT/'exact-reverification.json').read_text(encoding='utf-8'));structure=json.loads((OUT/'structure-repair-review.json').read_text(encoding='utf-8'))
assert exact['all_pass'] and exact['revised_questions']==35 and exact['exact_checks']==120
assert exact['precision_scan']['flags']==[] and len(structure['candidate_pairs'])==71

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_map(mapping,base):
 result={p:{'before':h,'after':sha(base/p),'unchanged':sha(base/p)==h} for p,h in mapping.items()}
 assert all(v['unchanged'] for v in result.values()),{p:v for p,v in result.items() if not v['unchanged']}
 return result
verify_map(BASE['guards_before'],ROOT);verify_map(BASE['code_before'],ROOT)
verify_map(BASE['all_author_draft_sha256'],ROOT);verify_map(BASE['prior_artifact_sha256'],PRIOR)
owned_previous=json.loads((OUT/'delivery-manifest.json').read_text(encoding='utf-8')) if (OUT/'delivery-manifest.json').exists() else None
owned_ledger_sha=owned_previous['ledger']['sha256'] if owned_previous else BASE['ledger_before']
if sha(DRAFTS/'coverage_ledger.py')==owned_ledger_sha and owned_previous:
 assert (DRAFTS/'coverage_ledger.py').read_text(encoding='utf-8-sig')==(OUT/'coverage_ledger.repaired.py').read_text(encoding='utf-8-sig'),'ledger text changed concurrently'
assert sha(DRAFTS/'coverage_ledger.py') in (BASE['ledger_before'],owned_ledger_sha),'author ledger changed concurrently'
if (DRAFTS/'draft-selection.json').exists():
 assert owned_previous and sha(DRAFTS/'draft-selection.json')==owned_previous['selection']['sha256'],'selection changed concurrently'
assert not (ROOT/'data/training_diversity_evidence.json').exists()
assert not (ROOT/'data/execution_evidence.json').exists()
for batch in B.BASE['selected']:
 if (DRAFTS/batch/'draft-codex-repair-v1.jsonl').exists():
  previous=next(e for e in owned_previous['entries'] if e['batch']==batch)
  assert sha(DRAFTS/batch/'draft-codex-repair-v1.jsonl')==previous['sha256'],'reviewed draft changed concurrently'
  assert sha(DRAFTS/batch/'DRAFT_REPORT-codex-repair-v1.md')==previous['report_sha256'],'reviewed report changed concurrently'

def write_atomic(path,content):
 temp=path.with_name(path.name+'.codex-tmp')
 assert not temp.exists(),temp
 temp.write_text(content,encoding='utf-8');os.replace(temp,path)

manual={r['id']:r for r in exact['manual_general_proofs']};why={r['id']:r['reason'] for r in structure['revised_questions']}
entries=[];records=[]
for batch,source in B.BASE['selected'].items():
 p=OUT/'staged'/f'{batch}.jsonl';rows=[json.loads(l) for l in p.read_text(encoding='utf-8').splitlines()]
 assert len(rows)==source['records']
 assert [r['id'] for r in rows]==[r['id'] for r in B.OLD.values() if B.BATCH[r['id']]==batch]
 lines=[f'# {batch} 精确数学修订版','',f'版本：codex-repair-v1。本批 {len(rows)} 题，原编号、顺序和题数均保留。未加入活动训练集。','', '分数、根式、对数、反三角函数均保留精确形式。场景文字已核对；动画成品尚未渲染验收。','']
 for row in rows:
  i=row['id'];math={f:row[f] for f in ('problem','solution','answer','scene_spec')};mh=hashlib.sha256(json.dumps(math,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
  if i in B.NEW:assert mh==manual[i]['math_sha256']
  else:
   assert all(row[f]==B.normalize_math(B.OLD[i][f]) for f in math)
  # Keep provenance and known risk ancestry. No ID-risk or parent-risk reset.
  row['parent_training_ids']=B.OLD[i].get('parent_training_ids',[])
  row['revision_lineage'].update({'prior_parent_training_ids':B.OLD[i].get('parent_training_ids',[]),'historical_risk_not_reset':True})
  row['strict_review'].update({'core_math_verified':True,'text_math_fields_reviewed':True,'scene_text_reviewed':True,'math_content_sha256':mh,'math_review_evidence':str((OUT/'exact-reverification.json').relative_to(ROOT)).replace('\\','/'),'verification_basis':'NEW_GENERAL_PROOF_AND_EXACT_SYMBOLIC_RECHECK' if i in B.NEW else 'PRIOR_VERIFIED_MATH_UNCHANGED_AFTER_LATEX_NORMALIZATION','admission_disposition':'MATH_VALID_PENDING_VERSION_BOUND_USER_DIVERSITY_ASSET_ACCEPTANCE'})
  row['review_disposition']='MATH_VALID_PENDING_VERSION_BOUND_ACCEPTANCE'
  records.append({'batch':batch,'id':i,'versioned_id':row['versioned_id'],'math_content_sha256':mh,'problem_revised':i in B.NEW,'structure_review':why.get(i,'沿用既有逐题审阅范围；数学内容仅规范公式转义。'),'prior_parent_training_ids':row['parent_training_ids'],'admitted':False})
  lines.extend([f"## {i} · {row.get('concept_id','')}", '',row['problem'],'','**推导**','',row['solution'],'','**答案**','',row['answer'],'','**场景对象**','',*['- '+v for v in row['scene_spec']['objects']],'','**场景步骤**','',*['- '+v for v in row['scene_spec']['steps']],''])
 text=''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in rows)
 p.write_text(text,encoding='utf-8');(OUT/'staged'/f'{batch}.md').write_text('\n'.join(lines),encoding='utf-8')
 target=DRAFTS/batch/'draft-codex-repair-v1.jsonl';doc=DRAFTS/batch/'DRAFT_REPORT-codex-repair-v1.md'
 write_atomic(target,text);write_atomic(doc,'\n'.join(lines))
 entries.append({'batch':batch,'path':str(target.relative_to(DRAFTS)).replace('\\','/'),'sha256':sha(target),'version':'codex-repair-v1','count':len(rows),'original_id_order_preserved':True,'source_sha256':source['sha256'],'report_path':str(doc.relative_to(DRAFTS)).replace('\\','/'),'report_sha256':sha(doc),'status':'MATH_VALID_PENDING_VERSION_BOUND_ACCEPTANCE'})
selection={'schema':1,'status':'DRAFT_ONLY_NOT_TRAINING_ADMISSION','created_at':datetime.now(timezone(timedelta(hours=8))).isoformat(),'original_ids_retained':True,'deleted_questions':0,'entries':entries,'unlisted_batches':'SELECT_LATEST_NUMBERED_AUTHOR_DRAFT_PENDING_REVIEW'}
write_atomic(DRAFTS/'draft-selection.json',json.dumps(selection,ensure_ascii=False,indent=2)+'\n')
write_atomic(DRAFTS/'coverage_ledger.py',(OUT/'coverage_ledger.repaired.py').read_text(encoding='utf-8-sig'))
cp=subprocess.run([sys.executable,'-B',str(DRAFTS/'coverage_ledger.py'),'--json'],capture_output=True,text=True,encoding='utf-8',cwd=ROOT)
assert cp.returncode==0,cp.stderr
ledger=json.loads(cp.stdout);assert ledger['new_draft_admissions']==0 and ledger['formal_density_certified'] is False
selected={e['batch']:e for e in ledger['selected_files']}
for e in entries:assert selected[e['batch']]['sha256']==e['sha256']
assert sum(c['math_reviewed_drafts'] for c in ledger['concepts'])==119
assert ledger['unmapped_active_ids']==[],ledger['unmapped_active_ids']
(OUT/'ledger-after-selection.json').write_text(cp.stdout,encoding='utf-8')
assert not (ROOT/'data/training_diversity_evidence.json').exists()
gates=runpy.run_path(str(ROOT/'tools/train_loop.py'),run_name='codex_readonly_gate_check')
gate=gates['gate_ready']('codex-batch-repair-readonly')
assert gate[0] is False,gate
final={'checked_at':datetime.now(timezone(timedelta(hours=8))).isoformat(),'protected_inputs':verify_map(BASE['guards_before'],ROOT),'protected_code':verify_map(BASE['code_before'],ROOT),'author_originals':verify_map(BASE['all_author_draft_sha256'],ROOT),'prior_audit_artifacts':verify_map(BASE['prior_artifact_sha256'],PRIOR),'author_ledger_before_sha256':BASE['ledger_before'],'author_ledger_after_sha256':sha(DRAFTS/'coverage_ledger.py'),'selection_sha256':sha(DRAFTS/'draft-selection.json'),'original_count':119,'new_count':len(records),'deleted':0,'same_id_order':True,'substantive_revisions':35,'prior_math_corrected_rows':46,'exact_checks_this_round':120,'ledger_tests_passed':7,'gate_ready':{'ok':gate[0],'reason':gate[1]},'frozen_inputs_unchanged':True,'training_admitted':False,'animation_render_verified':False,'newer_author_batches_pending_review':[e['batch'] for e in ledger['selected_files'] if e['batch'] not in B.BASE['selected']]}
(OUT/'final-verification.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'published-question-review.json').write_text(json.dumps({'records':records,'all119_math_valid_under_stated_assumptions':True,'admitted':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report=['# batch01–08 修订执行与独立复验','', '按用户要求：保留119题、原编号和顺序，不删题。发现的重复题在原位置修改条件、推导、答案与场景文字。','', '原审计的46处逐题数学修正全部已并入新版本；本轮35题实质改写，其中33题来自原暂缓清单，另2题为复查发现的训练内重复。这些统计有交集，不能相加作为不同题数。','', '35题重新逐行检查一般性证明、前提和边界，120项精确符号/整数验算全部通过；其余84题与前次已核对数学内容相同，仅规范LaTeX转义。119题题干、推导、答案和场景文本无小数、数值近似、控制字符、重复公式命令或不平衡大括号。','', '本轮数学依据保留一般性证明；有限计算检查不替代无限范围证明。','', '## 返回的新版本','', '| 批次 | 题数 | JSONL SHA-256 | 文件 |','|---|---:|---|---|']
for e in entries:report.append(f"| {e['batch']} | {e['count']} | {e['sha256']} | [题目与完整推导](../../2026-10-05-training-diversity-drafts/{e['report_path']}) |")
report.extend(['','各批新文件名为 `draft-codex-repair-v1.jsonl` 和 `DRAFT_REPORT-codex-repair-v1.md`。`draft-selection.json` 绑定当前选用版本和SHA-256，旧原稿与前次审计文件保留。原 `id` 不变，另附 `versioned_id` 记录版本；父题关联和已知风险来源没有清空。','', '## 结构复核','', '对119题与450条冻结方法记录作53550次只读候选比较；通读250个不同的冻结题干，逐对复查30处历史跨集关系和71对当前候选。原稿的已知完整任务/特定子任务复用已改写，35题的实质差异逐条记录于 `structure-repair-review.json`。两个剩余训练内文字相似候选分别为不同的有理/阶乘裂项与直接积分/指定变量替换，已记录具体理由。公共定理相同不单独等于泄漏，自动检测的UNKNOWN也不等于无泄漏证明。','', '## 35题修订明细','', '| 原编号 | 实质变化及隔离依据 |','|---|---|'])
for i in B.NEW:report.append(f'| {i} | {why[i]} |')
report.extend(['','## 账本修复','', '账本现在按明确的版本选择和文件哈希读取；未显式选定的批次才使用最新编号草稿。重复编号、非法路径或选中版本哈希不一致时停止。相似度阈值与输出均使用精确分数2/5，删除同考点自动“已确认”的推断。当前活动数量从实际清单读取，草稿与数学复核分列，未验收草稿不会被计为训练达标。7项针对这些错误的测试通过。','', '## 本轮边界与最终状态','', f"21个保护输入、5个保护代码文件、{len(BASE['all_author_draft_sha256'])}个原作者草稿、{len(BASE['prior_artifact_sha256'])}个前次审计文件的哈希均未改变。训练入口只读核对仍返回关闭：{gate[1]}。本轮没有更改活动训练/评测/测试清单，没有创建训练密度或执行证书；新版本仍需版本绑定的用户、多样性和动画资产验收。",'', '本轮执行范围为已审计的batch01–08。后续作者批次属于待独立审阅队列，不能把本报告用于证明后续批次数学正确或隔离通过。','', '交接前的中间版本保存在 `before-final-weighted-cycle/`，已经被最终加权循环版本取代，不作为当前选中题集。', '', '返还给Claude Code的消息编号和时间见 `bridge-handoff.json`。'])
(OUT/'REPAIR_REPORT.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
matrix=json.loads((OUT/'repair-matrix.json').read_text(encoding='utf-8'))
for e in matrix['files']:
 target=next(v for v in entries if v['batch']==e['batch']);e['sha256']=target['sha256'];e['published_path']=str((DRAFTS/target['path']).relative_to(ROOT)).replace('\\','/')
(OUT/'repair-matrix.json').write_text(json.dumps(matrix,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
delivery={'schema':1,'scope':'batch01-08','total':119,'deleted':0,'substantive_revisions':35,'exact_checks':120,'original_ids_retained':True,'entries':entries,'selection':{'path':str((DRAFTS/'draft-selection.json').relative_to(ROOT)).replace('\\','/'),'sha256':sha(DRAFTS/'draft-selection.json')},'ledger':{'path':str((DRAFTS/'coverage_ledger.py').relative_to(ROOT)).replace('\\','/'),'sha256':sha(DRAFTS/'coverage_ledger.py')},'evidence':{p.name:sha(p) for p in [OUT/'exact-reverification.json',OUT/'structure-repair-review.json',OUT/'final-verification.json',OUT/'published-question-review.json',OUT/'repair-matrix.json',OUT/'REPAIR_REPORT.md']},'training_admitted':False}
(OUT/'delivery-manifest.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'published':len(entries),'questions':119,'deleted':0,'revised':35,'exact_checks':120,'ledger_math_reviewed':119,'selected_author_drafts':ledger['selected_drafts'],'gate':gate,'report_sha256':sha(OUT/'REPAIR_REPORT.md'),'delivery_sha256':sha(OUT/'delivery-manifest.json')},ensure_ascii=False))
