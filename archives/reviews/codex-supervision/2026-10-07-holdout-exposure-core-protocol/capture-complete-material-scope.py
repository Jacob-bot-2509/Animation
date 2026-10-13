from pathlib import Path
import os,json,hashlib,collections,subprocess,stat,tarfile
R=Path(r'D:\Animation-Model-Training');O=R/'reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol'
def sha(b):return hashlib.sha256(b).hexdigest()
def hashfile(p):
 before=p.stat();h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
 after=p.stat()
 assert (before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns)
 return h.hexdigest(),after.st_size
def write(name,obj):
 with (O/name).open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def emit(f,obj):f.write(json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\n')
def loadlines(p):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines()]
initial={'data','reviews','docs','holdout-sources','configs','assets','src','tools','tests'}
runtime={'.git','.venv','.sandbox-runtime','.models','.tools','.vscode','.pytest_cache'}
extras=sorted(p.name for p in R.iterdir() if p.is_dir() and p.name not in initial|runtime)
skip={'.git','.venv','__pycache__','node_modules','.pytest_cache','.sandbox-runtime'}
extra=[];exclusions=[];errors=[]
with (O/'extra-filesystem-inventory.jsonl').open('x',encoding='utf-8',newline='\n') as f:
 for root in extras:
  for directory,dirs,names in os.walk(R/root,followlinks=False):
   keep=[]
   for d in sorted(dirs):
    p=Path(directory)/d
    if d in skip or d.lower().startswith(('edge-profile','chrome-profile','browser-profile')) or p.is_symlink() or p.stat(follow_symlinks=False).st_file_attributes&stat.FILE_ATTRIBUTE_REPARSE_POINT:
     exclusions.append(p.relative_to(R).as_posix())
    else:keep.append(d)
   dirs[:]=keep
   for name in sorted(names):
    p=Path(directory)/name
    if p.is_symlink() or p.stat(follow_symlinks=False).st_file_attributes&stat.FILE_ATTRIBUTE_REPARSE_POINT:continue
    try:h,n=hashfile(p)
    except (OSError,AssertionError) as e:
     errors.append({'path':p.relative_to(R).as_posix(),'error':type(e).__name__});continue
    row={'path':p.relative_to(R).as_posix(),'actual_bound_path':p.relative_to(R).as_posix(),'sha256':h,'bytes':n,'category':'historical_audit_output_or_render_material','exposure_state':'ROLE_EXPOSURE_UNKNOWN','content_emitted_to_model':False}
    extra.append(row);emit(f,row)
  print('supplement hashed',root,'files',len(extra),flush=True)
write('extra-filesystem-scope.json',{'roots':extras,'excluded_root_runtime_directories':sorted(runtime),'excluded_subdirectories':exclusions,'files_bound':len(extra),'capture_errors':errors,'complete_declared_available_material_scope':not errors,'qualified_count':None})
fs=loadlines(O/'filesystem-inventory.jsonl')+extra
previous=loadlines(O/'git-history-inventory.jsonl')
previous+=json.loads((O/'git-html-supplement.json').read_text(encoding='utf-8'))['rows']
by_sha=collections.defaultdict(set)
for row in fs+previous:by_sha[row['sha256']].add(row['actual_bound_path'])
commits=(O/'git-commits.raw.txt').read_text(encoding='ascii').splitlines()
objects=collections.defaultdict(set)
for commit in commits:
 cp=subprocess.run(['git','-c','core.quotepath=false','ls-tree','-r','-z',commit],cwd=R,capture_output=True,timeout=60)
 assert cp.returncode==0
 for entry in cp.stdout.split(b'\0'):
  if not entry:continue
  meta,name=entry.split(b'\t',1);mode,kind,oid=meta.decode('ascii').split();path=name.decode('utf-8')
  parts=Path(path).parts
  if kind!='blob' or mode=='120000' or parts[0] in runtime or any(x in skip or x.lower().startswith(('edge-profile','chrome-profile','browser-profile')) for x in parts):continue
  objects[oid].add(path)
known={x['git_object_id'] for x in previous}
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
additional=[]
with (O/'git-all-material-supplement.jsonl').open('x',encoding='utf-8',newline='\n') as f:
 for oid,paths in sorted(objects.items()):
  if oid in known:continue
  proc.stdin.write((oid+'\n').encode('ascii'));proc.stdin.flush()
  header=proc.stdout.readline().decode('ascii').split();assert header[1]=='blob'
  n=int(header[2]);b=proc.stdout.read(n);assert len(b)==n and proc.stdout.read(1)==b'\n'
  assert hashlib.sha1(b'blob '+str(n).encode('ascii')+b'\0'+b).hexdigest()==oid
  h=sha(b)
  if by_sha.get(h):actual=sorted(by_sha[h])[0];storage='existing_exact_bytes'
  else:
   p=O/'git-history/blobs'/(h+'.bin')
   if not p.exists():
    with p.open('xb') as out:out.write(b)
   assert sha(p.read_bytes())==h
   actual=p.relative_to(R).as_posix();storage='materialized_original_git_blob';by_sha[h].add(actual)
  row={'git_object_id':oid,'logical_paths':sorted(paths),'sha256':h,'bytes':len(b),'actual_bound_path':actual,'storage':storage,'role_exposure':'UNKNOWN'}
  additional.append(row);emit(f,row)
proc.stdin.close();assert proc.wait(timeout=30)==0
refs=loadlines(O/'reference-closure-authoritative.jsonl')
expected={x['expected_sha256'] for x in refs if x['status']=='EXPECTED_HASH_UNRESOLVED'}
archive_rows=[];archive_errors=[]
for row in fs:
 if not row['path'].endswith('.tar') or not row['path'].startswith('reviews/codex-supervision/history-from-code/'):continue
 p=R/row['actual_bound_path']
 try:
  with tarfile.open(p,'r:*') as archive:
   for member in archive:
    if not member.isfile():continue
    stream=archive.extractfile(member)
    b=stream.read();h=sha(b)
    if h not in expected:continue
    dest=O/'git-history/blobs'/(h+'.bin')
    if not dest.exists():
     with dest.open('xb') as out:out.write(b)
    assert sha(dest.read_bytes())==h
    by_sha[h].add(dest.relative_to(R).as_posix())
    archive_rows.append({'archive_path':row['path'],'archive_raw_sha256':row['sha256'],'member_name':member.name,'member_sha256':h,'actual_bound_path':dest.relative_to(R).as_posix(),'extracted_to_content_addressed_file_only':True})
 except (OSError,tarfile.TarError) as e:archive_errors.append({'archive_path':row['path'],'error':type(e).__name__})
write('archive-member-resolution.json',{'matching_original_members':archive_rows,'errors':archive_errors,'archive_paths_never_used_as_output_paths':True})
for row in refs:
 if row['status']=='EXPECTED_HASH_UNRESOLVED' and by_sha.get(row['expected_sha256']):
  row['status']='EXACT_RAW_BYTES_AVAILABLE'
  row['actual_matching_raw_paths']=sorted(by_sha[row['expected_sha256']])
with (O/'reference-closure-complete-scope.jsonl').open('x',encoding='utf-8',newline='\n') as f:
 for row in refs:emit(f,row)
unresolved=[r for r in refs if r['status']=='EXPECTED_HASH_UNRESOLVED']
stats={'initial_files':len(fs)-len(extra),'additional_files':len(extra),'total_available_material_files':len(fs),'reachable_commits':len(commits),
 'unique_relevant_git_blobs_all_formats':len(objects),'additional_git_blobs':len(additional),'current_materialized_original_versions':len(list((O/'git-history/blobs').glob('*.bin'))),
 'archive_members_recovered':len(archive_rows),'reference_states':dict(collections.Counter(x['status'] for x in refs)),
 'unresolved_reference_occurrences':len(unresolved),'distinct_unresolved_reference_versions':len({x['expected_sha256'] for x in unresolved}),
 'unresolved':unresolved,'scope_capture_errors':errors,'material_scope_complete':not errors,
 'complete_role_exposure_proof':False,'qualified_count':None,'core_associations_decided':0,'candidate_count':391,
 'new_questions':0,'production_gate':'CLOSED'}
write('COMPLETE_SCOPE_STATUS.json',stats)
print(json.dumps({k:v for k,v in stats.items() if k not in {'unresolved','scope_capture_errors'}},ensure_ascii=False),flush=True)
