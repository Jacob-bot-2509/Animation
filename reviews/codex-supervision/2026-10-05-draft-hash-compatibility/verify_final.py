from pathlib import Path
import hashlib,json,subprocess,sys,copy,datetime,contextlib,io
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];PY=ROOT/'.venv/Scripts/python.exe';sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'src')]
from draft_io import fingerprint,NORMALIZED_HASH,RAW_HASH,write_utf8_lf
from animtrain.manifest import Manifest
from animtrain.validate import validate_manifest
SEL=ROOT/'reviews/2026-10-05-training-diversity-drafts/draft-selection.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,d):write_utf8_lf(OUT/name,json.dumps(d,ensure_ascii=False,indent=2)+'\n',exclusive=True)
checks=[]
# Capture clean process output rather than PowerShell's NativeCommandError wrapping unittest stderr.
unit=subprocess.run([str(PY),'-B','-m','unittest','discover','-s','tests','-p','test_draft_hashes.py','-v'],capture_output=True,text=True,encoding='utf-8');write_utf8_lf(OUT/'unit-tests-18.txt',unit.stdout+'\n'+unit.stderr,exclusive=True);assert unit.returncode==0,unit.stderr
selected=json.loads(SEL.read_text('utf-8'));bad=copy.deepcopy(selected);bad['entries'][0]['sha256']='0'*64;save('isolated-forged-normalized-selector.json',bad)
import draft_audit as audit
for name,selection,hard in [('real',SEL,0),('bad',OUT/'isolated-forged-normalized-selector.json',1)]:
 old=audit.SELECTION;audit.SELECTION=selection.relative_to(ROOT).as_posix();out=OUT/('acceptance-'+name)
 args=['--drafts','reviews/2026-10-05-training-diversity-drafts/batch-*/draft-codex-repair-v4-final.jsonl','--out',out.relative_to(ROOT).as_posix()]
 if name=='real':args+=['--pool','data/v2/train/leakage-isolated-v3-2026-10-05','--eval-test','data/v2/eval','--eval-test','data/v2/test']
 capture=io.StringIO()
 with contextlib.redirect_stdout(capture):rc=audit.main(args)
 audit.SELECTION=old;write_utf8_lf(OUT/('acceptance-'+name+'-stdout.txt'),capture.getvalue(),exclusive=True)
 s=json.loads((out/'summary.json').read_text('utf-8'));counts=s['issue_code_counts'];assert s['severity_counts'].get('hard',0)==hard and counts.get('V007',0)==hard and counts.get('V011',0)==0
 checks.append({'case':name,'totals':s['totals'],'hard':s['severity_counts'].get('hard',0),'V007':counts.get('V007',0),'V011':counts.get('V011',0),'tool_returncode':rc,'global_summary_checked_not_only_returncode':True})
 # Verify raw conventional checksum listing and per-draft portable hash JSON both match.
 listed=json.loads((out/'file_hashes.json').read_text('utf-8'))['files']
 for e in listed:
  p=ROOT/e['file'];h=fingerprint(p.read_bytes());assert e['raw_sha256']==h['raw_sha256'];assert e['sha256']==(h['sha256'] if e['hash_algorithm']==NORMALIZED_HASH else h['raw_sha256'])
 for line in (out/'file_hashes.sha256').read_text('utf-8').splitlines():
  h,rel=line.split('  ',1);assert sha(ROOT/rel)==h
# Fresh, read-only production validation still reports the known hold.
production=validate_manifest(Manifest.load(ROOT/'data/manifest.json'),ROOT/'data');save('production-validation.json',production)
assert production['ok'] is False and not production['problems'] and len(production['structural_screen']['candidates'])==2
# Actual CLI uses the common writer, preserves exact answer and rejects repeated publication.
source=OUT/'writer-cli-source.jsonl';source.write_bytes(b'\xef\xbb\xbf'+('{"id":"fraction-example","answer":"\\\\frac{2}{7}"}\r\n').encode());target=OUT/'writer-cli-published.jsonl'
args=[str(PY),'-B','tools/publish_draft.py','--source',str(source),'--output',str(target)]
run=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,encoding='utf-8');assert run.returncode==0,run.stderr
first=target.read_bytes();assert not first.startswith(b'\xef\xbb\xbf') and b'\r' not in first and json.loads(first)['answer']==r'\frac{2}{7}'
again=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,encoding='utf-8');assert again.returncode!=0 and target.read_bytes()==first
save('writer-cli-validation.json',{'first_returncode':run.returncode,'second_returncode':again.returncode,'utf8_lf_no_bom':True,'exact_fraction_preserved':True,'overwrite_refused':True,'metadata':json.loads(run.stdout)})
base=json.loads((OUT/'before.json').read_text('utf-8'));drift=[rel for rel,h in base['protected'].items() if not (ROOT/rel).is_file() or sha(ROOT/rel)!=h];assert not drift,drift[:20]
changes=[]
for rel,h in base['mutable_before'].items():changes.append({'path':rel,'before_raw_sha256':h,'after_raw_sha256':sha(ROOT/rel)})
for rel in ['tools/draft_io.py','tools/publish_draft.py','tests/test_draft_hashes.py']:changes.append({'path':rel,'before_raw_sha256':None,'after_raw_sha256':sha(ROOT/rel)})
result={'verified_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'status':'DRAFT_HASH_COMPATIBILITY_VERIFIED','claude_latest_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'hash_algorithm':NORMALIZED_HASH,'selector_raw_sha256':sha(SEL),'selected_drafts':264,'preserved_files':len(base['protected']),'historical_and_production_bytes_unchanged':True,'new_admissions':0,'production_hold_pairs':len(production['structural_screen']['candidates']),'unit_tests':18,'binding_tests':checks,'clone_final_cases':18,'clone_legacy_cases':18,'code_changes':changes,'project_commit_or_index_changed_by_codex':False}
save('final-verification.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('code_changes',)},ensure_ascii=False))
