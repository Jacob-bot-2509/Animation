from pathlib import Path
import json,importlib.util,sys,hashlib,os
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];p=ROOT/'tools/draft_audit.py';sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'src'))
spec=importlib.util.spec_from_file_location('draft_audit_review_probe',p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
selector=ROOT/'reviews/2026-10-05-training-diversity-drafts/draft-selection.json';before=hashlib.sha256(selector.read_bytes()).hexdigest();data=json.loads(selector.read_text(encoding='utf-8'));bad=data['entries'][0]['batch'];original_sha=data['entries'][0]['sha256'];data['entries'][0]['sha256']='0'*64

for e in data['entries']:
 e['path']=os.path.relpath(selector.parent/e['path'],OUT).replace('\\','/')
 e['report_path']=os.path.relpath(selector.parent/e['report_path'],OUT).replace('\\','/')
fixture=OUT/'isolated-bad-binding-selector-rebased.json';fixture.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
mod.SELECTION=fixture.relative_to(ROOT).as_posix();code=mod.main(['--drafts','reviews/2026-10-05-training-diversity-drafts/batch-*/draft-codex-repair-v4-final.jsonl','--out',str((OUT/'binding-probe-rebased').relative_to(ROOT)).replace('\\','/')])
issues=[json.loads(x) for x in (OUT/'binding-probe-rebased/issues.jsonl').read_text(encoding='utf-8').splitlines()];summa=json.loads((OUT/'binding-probe-rebased/summary.json').read_text(encoding='utf-8'));assert hashlib.sha256(selector.read_bytes()).hexdigest()==before
result={'status':'CONFIRMED_AUDIT_BINDING_CHECK_SKIPPED','tool_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'fixture_selector':str(fixture.relative_to(ROOT)).replace('\\','/'),'only_fixture_modified':True,'actual_selector_and_author_files_unchanged':True,'deliberately_wrong_sha_batch':bad,'actual_correct_file_sha256':original_sha,'fixture_declared_sha256':'0'*64,'expected_V007_for_bad_binding':1,'actual_V007':sum(x['code']=='V007' for x in issues),'actual_V011_skips':sum(x['code']=='V011' for x in issues),'audit_reported_hard':summa['severity_counts'].get('hard',0),'tool_returncode':code,'cause':'e.path is relative to the draft root (batch-01/...), p.relative_to(ROOT) is relative to project root (reviews/.../batch-01/...). Their direct comparison is always unequal for current selector entries.'}
assert result['actual_V007']==0 and result['actual_V011_skips']==18 and result['audit_reported_hard']==0
(OUT/'binding-probe-rebased-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
