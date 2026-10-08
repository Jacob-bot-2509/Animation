"""Pure AST/in-memory tests. No native process, ACL, real trial files or runtime mutation."""
import ast,hashlib,json,os,sys,types,contextlib,io
from pathlib import Path as RealPath
HERE=RealPath(__file__).resolve().parent
text=(HERE/'file_acceptance-snapshot.py').read_text(encoding='utf-8')
tree=ast.parse(text)
FS={};DIRS=set();EVENTS=[]
class P:
 def __init__(self,p):self.s=p.s if isinstance(p,P) else str(p).replace('\\','/').rstrip('/')
 def __str__(self):return self.s
 def __truediv__(self,p):return P(self.s+'/'+str(p))
 def __repr__(self):return repr(self.s)
 def resolve(self):return self
 def is_relative_to(self,p):return self.s==p.s or self.s.startswith(p.s+'/')
 @property
 def parent(self):return P(self.s.rsplit('/',1)[0])
 def exists(self):return self.s in FS or self.s in DIRS
 def mkdir(self,**kw):DIRS.add(self.s);EVENTS.append(['mkdir',self.s])
 def read_bytes(self):
  if self.s not in FS:raise FileNotFoundError(self.s)
  return FS[self.s]
 def read_text(self,**kw):return self.read_bytes().decode('utf-8')
 def write_text(self,s,**kw):FS[self.s]=s.encode(kw.get('encoding','utf-8'));return len(s)
 def unlink(self,**kw):FS.pop(self.s,None)
 def with_suffix(self,s):return P(self.s.rsplit('.',1)[0]+s)
 def replace(self,target):FS[target.s]=FS.pop(self.s)
class U:
 def __init__(self):self.n=0
 def uuid4(self):self.n+=1;return types.SimpleNamespace(hex=f'{self.n:032x}')
def setup():
 FS.clear();DIRS.clear();EVENTS.clear()
 g={'__file__':'/support/file_acceptance.py','Path':P,'hashlib':hashlib,'json':json,'uuid':U(),'os':os,'sys':types.SimpleNamespace(executable='/runtime/python.exe',argv=['review']),'subprocess':types.SimpleNamespace(),'SUPPORT':P('/support'),'ROOT':P('/root'),'NET_RUNTIME':P('/runtime'),'CODEX_RUNTIME':P('/approved'),'EVIDENCE':P('/evidence'),'RUNTIME_KEY_FILES':['python.exe','python313.dll','Lib/socket.py','DLLs/_socket.pyd'],'ACCESS_DENIED':5,'CONTRACT':'local-file-acl-v1','KNOWN_KINDS':('granted_write','granted_read','denied_write','denied_read'),'_CLIENT':'mock client'}
 selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'_named_dir','_sha_file','_pth_ok','_assert_json_safe','_judge_case','_negative_regressions','_client_ok','_case','main'}]
 exec(compile(ast.fix_missing_locations(ast.Module(body=[ast.ImportFrom(module='__future__',names=[ast.alias(name='annotations')],level=0)]+selected,type_ignores=[])),'<v2-ast>','exec'),g)
 for rel in g['RUNTIME_KEY_FILES']:FS['/runtime/'+rel]=FS['/approved/'+rel]=b'baseline'+rel.encode()
 FS['/runtime/python313._pth']=b'Lib\nDLLs\n.\n';FS[g['__file__']]=text.encode()
 for rel in ['appcontainer.py','win_job.py','network_isolation.py']:FS['/root/src/animtrain/'+rel]=b'core source'
 def grant(p,sid,write):EVENTS.append(['grant',str(p),write])
 g['ac']=types.SimpleNamespace(appcontainer_sid=lambda:'sid',appcontainer_profile_path=lambda _:P('/profile'),_sid_sddl=lambda _:'S-1-15-2-1',grant_dir_access=grant)
 return g
def install_client(g,mode):
 calls=[]
 def run(cmd,sandbox,work,env):
  target=P(cmd[-2]);content=cmd[-1].encode();operation=cmd[-3];calls.append({'target':str(target),'sandbox':sandbox,'operation':operation})
  data={'token':{'api_ok':True,'is_appcontainer':True,'sid':'S-1-15-2-1'},'client_sha256':'client','exe_sha256':'exe','site_absent':True,'executable':'/runtime/python.exe','winerror':None}
  denied='/denied/' in str(target)
  if sandbox and denied:
   if mode=='breakthrough_then_error' and operation=='write':FS[str(target)]=content;data.update(outcome='wrote',content_hash=hashlib.sha256(content).hexdigest())
   else:data.update(outcome='denied',winerror=5,content_hash=None)
  elif operation=='write':
   if not (sandbox and mode=='preexisting_no_write'):FS[str(target)]=content
   data.update(outcome='wrote',content_hash=hashlib.sha256(content).hexdigest())
  else:
   h=hashlib.sha256(target.read_bytes()).hexdigest();data.update(outcome='read',content_hash=h)
   if sandbox and mode=='read_mutation':FS[str(target)]=b'changed after read'
  if mode=='breakthrough_then_error' and len(calls)==8:raise RuntimeError('later read failure after denied-write breakthrough')
  return {'spawned':True,'rc':0,'timed_out':False,'data':data,'command':cmd,'raw_out':'mock'}
 g['_run_client']=run
 # Standalone case cfg and all simulator output hashes agree.
 return calls
def case_test(mode):
 g=setup();calls=install_client(g,mode)
 if mode=='preexisting_no_write':FS['/work/gw-sb-00000000000000000000000000000002.bin']=b'00000000000000000000000000000002'
 cfg={'client_sha256':'client','runtime_python_sha256':'exe','runtime':P('/runtime/python.exe')}
 try:res=g['_case'](P('/work'),P('/denied'),P('/runtime/python.exe'),{},'S-1-15-2-1',P('/work/client.py'),cfg)
 except Exception as e:return {'error':repr(e),'calls':calls,'breakthrough_file_exists':any('/denied/dw-sb-' in s for s in FS),'returned_partial_record':False}
 return res
def main_test(mode):
 g=setup();runs=[]
 if mode=='selftest_false':g['_negative_regressions']=lambda:{'all_hold':False,'cases':[{'holds':False}]}
 def trial(*args):
  runs.append('case-called')
  if mode=='post_runtime_change':FS['/runtime/python313.dll']=b'changed';FS['/runtime/python313._pth']=b'import site\n';FS['/support/file_acceptance.py']=b'changed script'
  if mode=='error':raise RuntimeError('case failed with measured partial data')
  return {'overall':'PASS_LOCAL_FILE_ACL','raw':{'measured':'payload'}}
 g['_case']=trial
 with contextlib.redirect_stdout(io.StringIO()):exit_code=g['main']()
 records={s:json.loads(b) for s,b in FS.items() if s.startswith('/evidence/') and s.endswith('.json')}
 return {'exit_code':exit_code,'evidence':records,'native_calls':[],'simulated_events':EVENTS.copy(),'case_calls':runs}
g=setup();results={'simulation_only':True,'snapshot_sha256':hashlib.sha256(text.encode()).hexdigest(),'builtin':g['_negative_regressions'](),'case_baseline':case_test('baseline'),'case_read_mutation':case_test('read_mutation'),'case_preexisting_no_write':case_test('preexisting_no_write'),'case_fail_lost_after_error':case_test('breakthrough_then_error'),'main_selftest_false':main_test('selftest_false'),'main_post_runtime_change':main_test('post_runtime_change'),'main_error':main_test('error')}
assert results['builtin']['all_hold'] is True
assert results['case_baseline']['overall']=='PASS_LOCAL_FILE_ACL'
assert results['case_read_mutation']['overall']=='PASS_LOCAL_FILE_ACL'
assert results['case_read_mutation']['raw']['granted_read']['hash_before']!=results['case_read_mutation']['raw']['granted_read']['hash_after']
assert results['case_preexisting_no_write']['overall']=='PASS_LOCAL_FILE_ACL'
assert results['case_preexisting_no_write']['raw']['granted_write']['sb_pre_exists'] is True
assert results['case_fail_lost_after_error']['breakthrough_file_exists'] is True
assert results['main_selftest_false']['exit_code']==2
assert next(iter(results['main_selftest_false']['evidence'].values()))['overall']=='PASS_LOCAL_FILE_ACL'
assert results['main_post_runtime_change']['exit_code']==0
assert 'partial_results_keys' in next(iter(results['main_error']['evidence'].values()))
(HERE/'independent-fault-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'builtin_count':len(results['builtin']['cases']),'builtin_all_hold':results['builtin']['all_hold'],'read_mutation':results['case_read_mutation']['overall'],'preexisting_no_write':results['case_preexisting_no_write']['overall'],'selftest_false_exit':results['main_selftest_false']['exit_code'],'post_runtime_change_exit':results['main_post_runtime_change']['exit_code'],'breakthrough_lost':results['case_fail_lost_after_error']['breakthrough_file_exists']},ensure_ascii=False))
