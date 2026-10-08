
from pathlib import Path
import json,hashlib
R=Path(r'D:\Animation-Model-Training');O=R/'reviews/codex-supervision/2026-10-07-core-evidence-digest'
def sha(b):return hashlib.sha256(b).hexdigest()
def jl(n):return [json.loads(l) for l in (O/n).read_text(encoding='utf-8-sig').splitlines()]
def write(n,x):
 with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
P=R/'reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol'
ts=jl('historical-task-corpus.jsonl');ss={x['source_raw_sha256']:x for x in jl('source-files.jsonl')}
fixture=[x for x in ts if (x['problem'],x['solution'],x['answer'])==('p','s','1')]
assert len(fixture)==1
x=fixture[0];fixture_sources=[ss[h] for h in x['source_raw_sha256s']]
assert any('2026-09-30-initial/fixtures/fields.jsonl' in a for s in fixture_sources for a in s['available_physical_paths'])
write('synthetic-fixture-classification.json',{'task_sha256':x['task_sha256'],'fields':{k:x[k] for k in ['problem','solution','answer']},'source_bindings':[{'raw_sha256':s['source_raw_sha256'],'paths':s['available_physical_paths']} for s in fixture_sources],'kind':'SYNTHETIC_FIELDS_TEST_RECORD','count':1,'not_a_real_math_question':True,'original_bytes_kept':True,'not_a_new_core_association_decision':True})
counts=json.loads((O/'scope-and-counts.json').read_text(encoding='utf-8-sig'));counts['exact_field_triples']=counts['exact_math_triples'];counts['synthetic_fields_test_records']=1;counts['mathematical_question_content_records']=1059
with (O/'scope-and-counts.json').open('w',encoding='utf-8',newline='\n') as f:json.dump(counts,f,ensure_ascii=False,indent=2);f.write('\n')
f=O/'03-history-only-complete.md';s=f.read_text(encoding='utf-8')
s=s.replace('# 其他已恢复完整数学版本','# 其他已恢复历史记录',1).replace('共 299 份题干、过程、答案。','共 299 份原始内容记录，其中 298 份题目内容、1 份合成字段测试记录（id=ok，p/s/1）。',1)
s=s.replace('. ok\n','. ok（合成字段测试记录）\n',1)
with f.open('w',encoding='utf-8',newline='\n') as q:q.write(s)
inv=[]
for n in ['git-history-inventory.jsonl','git-all-material-supplement.jsonl']:
 for l in (P/n).read_text(encoding='utf-8-sig').splitlines():
  a=json.loads(l)
  if any(p in ['tools/screening_probe.py','tools/screening_qlora_probe.py','tools/data_probe.py'] for p in a['logical_paths']):
   inv.append({**a,'usage_binding_to_deleted_run':'PENDING','current_filename_does_not_prove_old_schema':True})
write('producer-version-leads.json',{'versions':inv,'is_schema_or_run_coverage_proof':False})
notes=[
 'reviews/codex-supervision/2026-10-05-batch-repair-execution/REPAIR_REPORT.md',
 'reviews/codex-supervision/2026-10-05-remaining-batch-audit/REPAIR_REPORT.md',
 'reviews/codex-supervision/2026-10-05-strict-batch-audit/batch-08-corrected.md',
 'reviews/codex-supervision/2026-10-06-scene-repair-takeover/math-9-corrected.md',
 'reviews/codex-supervision/2026-10-06-scene-batch-completion-review/SCENE_CORRECTIONS.md']
nb=[];(O/'key-history-notes').mkdir()
for p in notes:
 f=R/p
 if not f.is_file():nb.append({'path':p,'status':'NOT_CURRENTLY_FOUND'});continue
 b=f.read_bytes();h=sha(b);dst='key-history-notes/'+h+'-'+f.name
 (O/dst).write_bytes(b);nb.append({'original_path':p,'raw_sha256':h,'bytes':len(b),'captured_path':dst,'scope':'Historical repair note, not complete reversible patch chain or new review acceptance.'})
write('key-history-note-bindings.json',{'notes':nb})
print(json.dumps({'fixture':len(fixture),'producer_versions':len(inv),'key_notes_captured':sum('raw_sha256' in x for x in nb)},ensure_ascii=False))
