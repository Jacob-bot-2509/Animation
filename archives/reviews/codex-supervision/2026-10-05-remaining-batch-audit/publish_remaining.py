from pathlib import Path
import json,hashlib,copy,importlib.util,os
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];DRAFTS=ROOT/'reviews/2026-10-05-training-diversity-drafts'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(r):return hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
def load(p):return [json.loads(l) for l in p.read_text(encoding='utf-8-sig').splitlines()]
BASE=json.loads((OUT/'baseline.json').read_text(encoding='utf-8'))
MATH=json.loads((OUT/'exact-reverification.json').read_text(encoding='utf-8'));STRUCT=json.loads((OUT/'structural-review.json').read_text(encoding='utf-8'));REVIEW=json.loads((OUT/'per-question-review.json').read_text(encoding='utf-8'))
assert MATH['passed']==MATH['check_count']==165 and not MATH['failed'] and not MATH['precision_or_encoding_issues']
assert len(STRUCT['records'])==145 and STRUCT['unresolved_positive_candidates']==0
mathbind={r['id']:r for r in MATH['records']};structbind={r['id']:r for r in STRUCT['records']}
notes={r['id']:r for r in REVIEW['records']}
selection=DRAFTS/'draft-selection.json'
assert digest(selection)==BASE['selection_before']['sha256'],'concurrent selector change'
assert digest(DRAFTS/'coverage_ledger.py')==BASE['ledger_sha256'],'ledger drift'

def guard():
 mismatches=[]
 for group in ('protected_inputs','protected_code','prior_artifacts_and_first8_versions'):
  for path,sha in BASE[group].items():
   if digest(ROOT/path)!=sha:mismatches.append(path)
 for batch,v in BASE['selected'].items():
  if digest(ROOT/v['source'])!=v['sha256']:mismatches.append(v['source'])
  if digest(OUT/v['snapshot'])!=v['sha256']:mismatches.append(v['snapshot'])
 assert not mismatches,('protected drift',mismatches)
 return {'protected_inputs':len(BASE['protected_inputs']),'protected_code':len(BASE['protected_code']),'prior_artifacts_and_first8_versions':len(BASE['prior_artifacts_and_first8_versions']),'raw_sources_and_snapshots':20,'unchanged':True}
before=guard(); files=[];entries=[]
for b in range(9,19):
 batch=f'batch-{b:02d}';stage=OUT/'staged'/f'{batch}.jsonl';rows=load(stage);original=load(OUT/BASE['selected'][batch]['snapshot'])
 assert len(rows)==BASE['selected'][batch]['count'] and [r['id'] for r in rows]==[r['id'] for r in original]
 for r in rows:
  assert canonical(r)==mathbind[r['id']]['record_sha256']==structbind[r['id']]['record_sha256']
  assert r['strict_review']['core_math_verified'] and r['strict_review']['scene_text_reviewed']
  assert not r['admitted'] and not r['animation_render_verified']
 jsonpath=DRAFTS/batch/'draft-codex-repair-v1.jsonl';mdpath=DRAFTS/batch/'DRAFT_REPORT-codex-repair-v1.md'
 md=[f'# {batch} 精确数学修订版','',f'本批{len(rows)}题，原编号与顺序全部保留；删除0题。用户委托的数学与场景文本审校完成。版本codex-repair-v1，尚未加入训练集。','',f'原文SHA-256：`{BASE["selected"][batch]["sha256"]}`。','']
 for r in rows:
  md += [f'## {r["id"]} · {r["concept_id"]}', '', '**题目**','',r['problem'],'','**推导**','',r['solution'],'','**答案**','',r['answer'],'','**审校说明**','',notes[r['id']]['note'],'','**场景步骤**','',*['- '+s for s in r['scene_spec']['steps']],'']
 mdtext='\n'.join(md)
 if jsonpath.exists():assert jsonpath.read_bytes()==stage.read_bytes(),'new version already differs'
 else:jsonpath.write_bytes(stage.read_bytes())
 if mdpath.exists():assert mdpath.read_text(encoding='utf-8')==mdtext,'new report already differs'
 else:mdpath.write_text(mdtext,encoding='utf-8')
 entry={'batch':batch,'path':f'{batch}/draft-codex-repair-v1.jsonl','sha256':digest(jsonpath),'version':'codex-repair-v1','count':len(rows),'original_id_order_preserved':True,'source_sha256':BASE['selected'][batch]['sha256'],'report_path':f'{batch}/DRAFT_REPORT-codex-repair-v1.md','report_sha256':digest(mdpath),'status':'MATH_VALID_PENDING_VERSION_BOUND_ACCEPTANCE'}
 entries.append(entry);files.append({**entry,'root_path':str(jsonpath.relative_to(ROOT)).replace('\\','/'),'root_report_path':str(mdpath.relative_to(ROOT)).replace('\\','/')})
assert sum(f['count'] for f in files)==145
# Only append the ten explicitly authorized versions. The original eight objects are unchanged.
sel=copy.deepcopy(BASE['selection_before']['content']);sel['entries'].extend(entries);sel['updated_by']='codex-user-delegated-math-review-2026-10-05';sel['selected_drafts']=264;sel['unlisted_batches']='ALL_18_BATCHES_EXPLICITLY_SELECTED'
assert sel['entries'][:8]==BASE['selection_before']['content']['entries'] and len(sel['entries'])==18
assert digest(selection)==BASE['selection_before']['sha256'],'concurrent selector change immediately before update'
nextpath=selection.with_name('draft-selection.codex-next.json');nextpath.write_text(json.dumps(sel,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');os.replace(nextpath,selection)
spec=importlib.util.spec_from_file_location('ledger',DRAFTS/'coverage_ledger.py');L=importlib.util.module_from_spec(spec);spec.loader.exec_module(L)
ledger=L.report();assert ledger['selected_drafts']==264 and ledger['active_train']==47 and ledger['new_draft_admissions']==0 and not ledger['formal_density_certified']
assert sum(c['math_reviewed_drafts'] for c in ledger['concepts'])==264
(OUT/'coverage-ledger-after-selection.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
after=guard()
# Verify actual published text and per-row bindings, not just staging files.
published=[]
for f in files:
 p=ROOT/f['root_path'];assert digest(p)==f['sha256'];rs=load(p)
 for r in rs:assert canonical(r)==mathbind[r['id']]['record_sha256']
 published.extend(rs)
assert len(published)==145 and len({r['id'] for r in published})==145
stats={'reviewed_questions':145,'original_ids_preserved':145,'deleted_questions':0,'substantive_rewrites':sum(r['substantive_rewrite'] for r in REVIEW['records']),'changed_math_rows':sum(bool(r['math_fields_changed']) for r in REVIEW['records']),'unchanged_math_rows':sum(not r['math_fields_changed'] for r in REVIEW['records']),'scene_texts_rebound':145,'exact_checks_passed':165,'heldout_comparisons':65250,'within_and_prior_comparisons':json.loads((OUT/'structural-screen.json').read_text(encoding='utf-8'))['within_and_prior_comparisons'],'selected_batches':18,'selected_drafts':264,'math_reviewed_selected_drafts':264,'new_admissions':0,'training_manifest_changed':False,'training_started':False,'animation_render_verified':False}
rep=['# 第09–18批精确数学修订报告','','2026-10-05。用户授权由Codex全权审校并执行修改，修订文件交给Claude Code跟进。','',f'完成145题；全部保留原ID、题数及顺序，删除0题。{stats["substantive_rewrites"]}题改写题目结构或补全题干，{stats["changed_math_rows"]}题修改至少一个数学字段，{stats["unchanged_math_rows"]}题原数学内容保留。全部145题的场景文本与最终题干、证明和答案重新绑定。','','## 修订内容','','- 删除小数答案和未经证明的近似误差，使用分数、根式、有限和、指数、Φ及Φ逆函数。有限概率与极限概率分别表述。','- 修正零分母直线式、剪切边方向、线面包含关系、平面束遗漏成员、曲面正则性与退化、交线端点及参数域。','- 补齐数域、系统相容性、多项式环单位、Jordan链、辛形式配对和随机事件独立性。柯西反例只证明删去假设后不能普遍保证结论。','- 重复题保留原ID，改成实质不同的约束或任务；同核心只换数值的题按泄漏或重复处理，历史父题与风险溯源保留。','','## 独立复验','','165项符号或有限精确复算通过，精度与编码扫描零问题。概率有限和另用整数卷积、Eulerian递推等方法核验；一般收敛、正则性和极限定理依据逐题人工证明，有限检查不充当通用证明。','','145×450=65250次冻结评测与测试方法记录对照，另对前八批、47条活动训练和当前批次作34510次两两对照。最终5条留出候选（3个不同题对）及1条草稿/活动候选均有具体人工裁决，未保留本次识别出的同核心数值变体。未校准检测器的阴性或UNKNOWN不等于无泄漏证书。','','## 各批修订文件','','| 批次 | 题数 | 新题库 | 题目、推导、答案文档 |','|---|---:|---|---|']
for f in files:
 rep.append(f'| {f["batch"]} | {f["count"]} | [JSONL](../../../2026-10-05-training-diversity-drafts/{f["path"]}) | [Markdown](../../../2026-10-05-training-diversity-drafts/{f["report_path"]}) |')
# Relative links from this review directory: codex-supervision/topic -> reviews/author requires ../../, not ../../../.
rep=[line.replace('(../../../2026-10-05-training-diversity-drafts/','(../../2026-10-05-training-diversity-drafts/') for line in rep]
rep += ['', '## 版本与边界','', 'draft-selection.json已保留前八批选择对象并追加十批，18批合计264题数学复核完成。实际账本读取264条；新增正式准入0条。现有训练、评测、测试、manifest及锁文件未改动；原始草稿、前八批交付和旧审校证据的保护哈希均保持。','', '本次不启动训练，不生成准入证书；动画只复核文本，未进行渲染验收。正式准入证据须绑定这18批新文件的实际哈希，不能沿用旧版本结论。','', '逐题依据：[per-question-review.json](per-question-review.json)；独立数学检查：[exact-reverification.json](exact-reverification.json)；结构裁决：[structural-review.json](structural-review.json)；发布哈希：[delivery-manifest.json](delivery-manifest.json)。交接消息及实际发送回执另存bridge-handoff.json，以回执为发送事实。','']
# Calculate comparison count from the screen rather than hard-code it in prose.
rep=[line.replace('34510次',str(stats['within_and_prior_comparisons'])+'次') for line in rep]
report=OUT/'REPAIR_REPORT.md';report.write_text('\n'.join(rep),encoding='utf-8')
delivery={'date':'2026-10-05','version':'codex-repair-v1','stats':stats,'report_path':str(report.relative_to(ROOT)).replace('\\','/'),'report_sha256':digest(report),'selection_sha256':digest(selection),'files':files,'protected_before':before,'protected_after':after,'formal_admission':False}
(OUT/'delivery-manifest.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'published-content-check.json').write_text(json.dumps({'records':MATH['records'],'counts_and_ids_preserved':True,'jsonl_bytes_equal_staging':True,'all_published_record_hashes_match_math_and_structure_reviews':True,'all_math_fields_and_scene_texts_reviewed':True,'stats':stats,'protected':after},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'stats':stats,'report_sha256':digest(report),'delivery_sha256':digest(OUT/'delivery-manifest.json'),'protected':after},ensure_ascii=False))
