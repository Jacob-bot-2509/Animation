import hashlib,json,os,re,subprocess,sys
from pathlib import Path
ROOT=Path(r'D:\Animation-Model-Training');OUT=Path(__file__).resolve().parent;env=dict(os.environ,PYTHONIOENCODING='utf-8')
def run(name,argv):
 r=subprocess.run(argv,cwd=ROOT,env=env,capture_output=True);(OUT/(name+'.stdout.raw.txt')).write_bytes(r.stdout);(OUT/(name+'.stderr.raw.txt')).write_bytes(r.stderr);return r
r=run('suite-final',[sys.executable,'-X','utf8','-B','-m','unittest','tests.test_audit_staged_scenes','tests.test_scene_sweep_protocol','tests.test_dataset_audit_latex_delimiters','tests.test_draft_hashes','-v']);m=re.search(rb'Ran (\d+) tests',r.stderr);summary={'returncode':r.returncode,'tests':int(m.group(1)) if m else None,'passed':r.returncode==0};(OUT/'suite-final-result.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print('TESTS',summary);assert r.returncode==0
argv=[sys.executable,'-X','utf8','-B',str(ROOT/'tools/audit_staged_scenes.py')]
for n in range(1,11):argv+=['--staged',str(ROOT/f'reviews/2026-10-06-scene-standard-sweep/batch{n}-staged-v1')]
argv+=['--staged',str(OUT/'scene-candidates-144-v5')];r=run('staged-integrity-final',argv);v=json.loads(r.stdout);print('INTEGRITY',r.returncode,'dirs',len(v['results']),'records',sum(x.get('records',0) for x in v['results']),'corrupt',sum(len(x.get('control_corruption',[])) for x in v['results']));assert r.returncode==0
# Recover the committed invalid predecessor without touching current paths or re-signing evidence.
commit='c46d5e1';prefix='reviews/2026-10-06-scene-standard-sweep/';paths=subprocess.check_output(['git','ls-tree','-r','--name-only',commit,'--',prefix+'batch6-staged-v1',prefix+'batch6-patches.json'],cwd=ROOT).decode('utf-8').splitlines();archive=OUT/'batch6-invalid-c46d5e1';archive.mkdir(exist_ok=False);items=[]
for rel in paths:
 data=subprocess.check_output(['git','show',commit+':'+rel],cwd=ROOT);p=archive/rel.removeprefix(prefix);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);items.append({'git_path':rel,'git_commit':commit,'archived_path':p.relative_to(ROOT).as_posix(),'raw_sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
selector=json.loads((archive/'batch6-staged-v1/draft-selection.candidate.json').read_text('utf-8'));matches=[];corrupt=[]
for e in selector['entries']:
 p=archive/'batch6-staged-v1'/e['path'];data=p.read_bytes();matches.append(hashlib.sha256(data).hexdigest()==e['raw_sha256'])
 for line in data.decode('utf-8').splitlines():
  if not line.strip():continue
  rec=json.loads(line)
  for key in ('objects','steps'):
   for value in rec['scene_spec'][key]:
    bad=[f'U+{ord(c):04X}' for c in value if ord(c)<32]
    if bad:corrupt.append({'id':rec['id'],'field':key,'codepoints':bad})
receipt=json.loads((archive/'batch6-staged-v1/stage-receipt.json').read_text('utf-8'));patchhash=hashlib.sha256((archive/'batch6-patches.json').read_bytes()).hexdigest();history={'git_commit':commit,'items':items,'archived_files':len(items),'staged_raw_sha_matches_old_selection':sum(matches),'staged_raw_sha_total':len(matches),'patch_raw_sha_matches_old_receipt':patchhash==receipt['patches_raw_sha256'],'corrupt_strings':corrupt,'status':'INVALID_GIT_PREDECESSOR_ARCHIVED_NOT_ACCEPTANCE','notes':'Git blobs preserved verbatim. Raw-match comparisons explicitly distinguish archive bytes from original worktree claims; old receipt never re-signed.'};(OUT/'batch6-invalid-archive-manifest.json').write_text(json.dumps(history,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('ARCHIVE',len(items),'staged_matches',sum(matches),len(matches),'patch_receipt_match',history['patch_raw_sha_matches_old_receipt'],'corrupt_strings',len(corrupt))