from pathlib import Path
import json,sys,subprocess,shutil,hashlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];sys.path.insert(0,str(ROOT/'tools'))
from draft_io import fingerprint,verify_entry,NORMALIZED_HASH
src=OUT/'git-roundtrip-source';dest=OUT/'git-roundtrip-clone';assert not src.exists() and not dest.exists();src.mkdir()
def git(args,cwd):
 r=subprocess.run(['git',*args],cwd=cwd,capture_output=True,text=True,encoding='utf-8');assert r.returncode==0,(args,r.stderr);return r.stdout.strip()
git(['init','--quiet'],src);shutil.copyfile(ROOT/'.gitattributes',src/'.gitattributes')
selection=json.loads((ROOT/'reviews/2026-10-05-training-diversity-drafts/draft-selection.json').read_text('utf-8'))
for e in selection['entries']:
 rel=Path(selection['draft_root'])/e['path'];p=src/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,p)
# Copy a CRLF historical v1 too; it must not be modified by current filters.
old=Path(selection['draft_root'])/'batch-01/draft-codex-repair-v1.jsonl';shutil.copyfile(ROOT/old,src/old)
selector=Path(selection['draft_root'])/'draft-selection.json';shutil.copyfile(ROOT/selector,src/selector)
git(['add','.'],src);git(['-c','user.name=Draft portability test','-c','user.email=draft-test@invalid.local','commit','--quiet','-m','isolated draft portability fixture'],src)
git(['clone','--quiet','--no-hardlinks',str(src),str(dest)],OUT)
checks=[]
for e in selection['entries']:
 rel=Path(selection['draft_root'])/e['path'];a=(ROOT/rel).read_bytes();b=(dest/rel).read_bytes();assert a==b
 binding=verify_entry(dest/rel,e,NORMALIZED_HASH);assert binding['raw_bytes_match_manifest']
 checks.append({'batch':e['batch'],'raw_preserved':True,'canonical_bound':True,**fingerprint(b)})
assert (ROOT/old).read_bytes()==(dest/old).read_bytes()
# Previously committed v1 blobs were LF-normalized: they remain valid in the NEW content view.
legacy=[]
for p in (ROOT/selection['draft_root']).glob('batch-*/draft-codex-repair-v1.jsonl'):
 rel=p.relative_to(ROOT).as_posix();run=subprocess.run(['git','show','HEAD:'+rel],cwd=ROOT,capture_output=True);assert run.returncode==0
 actual=p.read_bytes();index=run.stdout;assert fingerprint(actual)['sha256']==fingerprint(index)['sha256']
 legacy.append({'path':rel,'raw_changed_in_existing_commit':actual!=index,'normalized_equivalent':True})
result={'status':'PASS','fixture_commit_only':True,'production_repo_committed':False,'final_draft_clone_cases':checks,'historical_v1_clone_case_raw_preserved':True,'existing_historical_committed_blob_cases':legacy,'definition':"sha256('\\n'.join(data.decode('utf-8-sig').splitlines()).encode('utf-8'))"}
(OUT/'git-roundtrip-validation.json').write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode());print(json.dumps({'status':'PASS','clone_raw_and_canonical_cases':len(checks),'existing_v1_blob_equivalence':len(legacy),'old_index_raw_differences':sum(e['raw_changed_in_existing_commit'] for e in legacy),'project_git_index_modified':False}))
