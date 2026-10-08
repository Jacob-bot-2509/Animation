from pathlib import Path
import json,hashlib,copy,sys,importlib.util,collections,subprocess
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'src')]
from draft_io import fingerprint,verify_entry,NORMALIZED_HASH
D=ROOT/'reviews/2026-10-05-training-diversity-drafts';snapshot=OUT/'snapshot';selector=json.loads((snapshot/'reviews/2026-10-05-training-diversity-drafts/draft-selection.json').read_text('utf-8'))
patches=json.loads((ROOT/'reviews/codex-supervision/2026-10-05-draft-hash-compatibility/ready-row-separator-patches.json').read_text('utf-8'))['records'];pmap={p['id']:p for p in patches};checks=[];issues=[];allids=[];allrows=[]
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
for e in selector['entries']:
 path=D/e['path'];bound=verify_entry(path,e,selector['hash_algorithm']);report=D/e['report_path'];h=fingerprint(report.read_bytes());assert h['sha256']==e['report_sha256'] and h['raw_sha256']==e['report_raw_sha256']
 old=D/e['batch']/'draft-codex-repair-v4-final.jsonl';before=[json.loads(x) for x in old.read_text('utf-8').splitlines() if x.strip()];after=[json.loads(x) for x in path.read_text('utf-8').splitlines() if x.strip()];assert [r['id'] for r in before]==[r['id'] for r in after] and len(after)==e['count'];allids += [r['id'] for r in after];allrows+=after
 for original,row in zip(before,after):
  qid=row['id'];math=digest({k:row[k] for k in ['problem','solution','answer','scene_spec']});assert math==row['strict_review']['math_content_sha256']
  assert not row.get('admitted') and not row.get('animation_render_verified')
  if qid in pmap:
   patch=pmap[qid];assert digest(original)==patch['expected_record_sha256'];assert all(row[k]==v for k,v in patch['fields'].items());assert math==patch['new_math_content_sha256'];assert row['revision_lineage']['version']=='codex-repair-v5' and row['versioned_id'].startswith('codex-repair-v5-');checks.append({'id':qid,'batch':e['batch'],'expected_prepatch_record_sha_verified':True,'patch_fields_exactly_applied':True,'new_math_content_sha256':math,'versioned_id':row['versioned_id'],'selected_sha256':e['sha256']})
  else:assert row==original,(e['batch'],qid)
 # Root path aliases and source_path are part of the new hash-view contract.
 if e.get('root_path')!=path.relative_to(ROOT).as_posix():issues.append({'batch':e['batch'],'field':'root_path','current':e.get('root_path'),'expected':path.relative_to(ROOT).as_posix()})
 if e.get('root_report_path')!=report.relative_to(ROOT).as_posix():issues.append({'batch':e['batch'],'field':'root_report_path','current':e.get('root_report_path'),'expected':report.relative_to(ROOT).as_posix()})
 if e['version']=='codex-repair-v5' and e.get('source_path')!=old.relative_to(ROOT).as_posix():issues.append({'batch':e['batch'],'field':'source_path','current':e.get('source_path'),'expected':old.relative_to(ROOT).as_posix()})
assert len(checks)==7 and len(allids)==264 and len(set(allids))==264
steps=sum(len(r['scene_spec']['steps']) for r in allrows);assert steps==1176
result={'status':'SEVEN_ROW_PATCHES_INDEPENDENTLY_VERIFIED','selected_files':18,'selected_records':264,'steps':steps,'selected_versions':dict(collections.Counter(e['version'] for e in selector['entries'])),'patched_checks':checks,'all_other_records_identical_to_v4':True,'selector_alias_issues':issues,'new_pdf_exists':(ROOT/'outputs/draft-review/draft-review-selected-v5.pdf').exists(),'no_training_admission':True,'old_drafts_unchanged_by_review':True}
(OUT/'v5-content-verification.json').write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode());print(json.dumps({'verified_question_patches':len(checks),'selected_records':264,'steps':steps,'alias_issues':len(issues),'new_pdf_exists':result['new_pdf_exists']},ensure_ascii=False))
# Audit the selected mixed version set using snapshot-only glob. No code or selector edits.
import draft_audit as audit
old_root=audit.ROOT;audit.ROOT=snapshot;old_sel=audit.SELECTION;audit.SELECTION='reviews/2026-10-05-training-diversity-drafts/draft-selection.json'
# All selected files, including unchanged v4, are copied to the isolated snapshot for this run.
for e in selector['entries']:
 rel=Path(selector['draft_root'])/e['path'];p=snapshot/rel;p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():p.write_bytes((ROOT/rel).read_bytes())
 # Fixed-original comparisons and external references stay under the real project; load via temporary Root-independent glob is not needed here.
# Run per version in the real project, then merge verdicts; selected 4+14 supported without altering glob behavior.
audit.ROOT=old_root;audit.SELECTION=old_sel
PY=ROOT/'.venv/Scripts/python.exe'
for label,glob in [('v5','reviews/2026-10-05-training-diversity-drafts/batch-*/draft-codex-repair-v5.jsonl')]:
 args=[str(PY),'-B','tools/draft_audit.py','--drafts',glob,'--pool','data/v2/train/leakage-isolated-v3-2026-10-05','--eval-test','data/v2/eval','--eval-test','data/v2/test','--out',(OUT/('audit-'+label)).relative_to(ROOT).as_posix()]
 run=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,encoding='utf-8');(OUT/('audit-'+label+'-stdout.txt')).write_bytes(run.stdout.encode());(OUT/('audit-'+label+'-stderr.txt')).write_bytes(run.stderr.encode());assert run.returncode==0,run.stderr;s=json.loads((OUT/('audit-'+label)/'summary.json').read_text('utf-8'));assert s['severity_counts'].get('hard',0)==0 and s['issue_code_counts'].get('V011',0)==0;print(json.dumps({'audit':label,'totals':s['totals'],'severity':s['severity_counts'],'codes':s['issue_code_counts']},ensure_ascii=False))
