"""Materialize nine source-bound exact mathematics corrections as fresh inactive files."""
from pathlib import Path
import copy,json,re,sys,hashlib
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
P=R/'reviews/codex-supervision/2026-10-06-scene-start-supervision'
sys.path[:0]=[str(R/'tools'),str(R/'src')];sys.stdout.reconfigure(encoding='utf-8')
from holdout_contract import Snapshot,object_sha,raw_sha,jsonl
from draft_io import publish_jsonl
from dataset_audit import Audit,check_latex
from scene_sweep_protocol import _invalidate
proposals=json.loads((P/'math-repair-proposals.pending.json').read_text(encoding='utf-8'))
updates={p['id']:copy.deepcopy(p) for p in proposals['records']}
updates['prob-039']['fields']['problem']=r'独立均匀地在正方形 $Q=[-1,1]^2$ 中选取 $n\ge1$ 个点，记落入单位圆 $D=\{(x,y):x^2+y^2\le1\}$ 的点数为 $m_n$。构造 $\widehat\pi_n=4m_n/n$，精确求其期望和方差，并证明 $\widehat\pi_n\xrightarrow{P}\pi$。说明有限样本的有理数 $4m_n/n$ 与符号常量 $\pi$ 的区别。'
updates['prob-042']['fields']['problem']=r'设 $X_1,X_2,\ldots$ 独立同分布，$P(X_i=1)=p$、$P(X_i=0)=1-p$，其中 $0\le p\le1$。令正面频率 $F_n=n^{-1}\sum_{i=1}^nX_i$。精确求 $E(F_n)$、$\operatorname{Var}(F_n)$，并用切比雪夫不等式证明 $F_n\xrightarrow{P}p$；说明公平硬币附加条件对应的 $p$。'
updates['prob-043']['fields']['problem']=r'设 $X_1,X_2,\ldots$ 独立同分布，$E(X_i)=\mu$、$0<\operatorname{Var}(X_i)=\sigma^2<\infty$，$\overline X_n=n^{-1}\sum_{i=1}^nX_i$。写出标准化均值的中心极限定理，并区分其分布极限与原尺度 $\overline X_n$ 的极限；说明总体正态时有限样本的精确分布。'
def walk(v,fn):
 if isinstance(v,str):return fn(v)
 if isinstance(v,list):return [walk(x,fn) for x in v]
 if isinstance(v,dict):return {k:walk(x,fn) for k,x in v.items()}
 return v
def frac_braces(t):
 def token(i):
  while i<len(t) and t[i].isspace():i+=1
  if i>=len(t):raise ValueError('missing fraction argument')
  if t[i]=='{':
   depth=1;j=i+1
   while j<len(t) and depth:
    depth+=(t[j]=='{')-(t[j]=='}');j+=1
   if depth:raise ValueError('unclosed frac argument')
   return t[i:j],j
  if t[i]=='\\':
   m=re.match(r'\\(?:[A-Za-z]+|.)',t[i:])
   if not m:raise ValueError('invalid command')
   command=m.group()
   if command in (r'\sqrt',r'\frac',r'\sum',r'\int'):raise ValueError('compound bare argument needs manual braces')
   return '{'+command+'}',i+len(command)
  return '{'+t[i]+'}',i+1
 pos=0;out=''
 for m in re.finditer(r'\\(?:frac|dfrac|tfrac)\b|\\(?:frac|dfrac|tfrac)(?=[0-9])',t):
  if m.start()<pos:continue
  a,j=token(m.end());b,k=token(j);out+=t[pos:m.start()]+m.group()+a+b;pos=k
 return out+t[pos:]
snapshot=Snapshot(R);grouped={};corrected=[];guard=[]
for pid,proposal in updates.items():
 data=snapshot.read(R/proposal['source_path']);assert raw_sha(data)==proposal['source_raw_sha256']
 original=json.loads(data.decode('utf-8-sig').splitlines()[proposal['source_line']-1])
 assert original['id']==pid and object_sha(original)==proposal['expected_record_canonical_sha256']
 row=copy.deepcopy(original);fields=walk(proposal['fields'],frac_braces);row.update(fields)
 assert not re.search(r'\d+\.\d+',json.dumps({k:row[k] for k in ('problem','solution','answer','scene_spec')},ensure_ascii=False))
 a=Audit();check_latex(a,{'path':'new exact version'},{'record':row,'locator':pid},pid)
 blockers=[x for x in a.issues if x['severity'] in ('hard','quarantine')]
 assert not blockers,(pid,blockers)
 row=_invalidate(row,'codex-exact-math-v1',object_sha(original))
 corrected.append({'id':pid,'record':row,'changed_fields':list(fields),'source_path':proposal['source_path'],
     'source_raw_sha256':proposal['source_raw_sha256'],'source_line':proposal['source_line'],
     'before_record_canonical_sha256':object_sha(original),'after_record_canonical_sha256':object_sha(row),
     'after_math_fields_canonical_sha256':object_sha({k:row[k] for k in ('problem','solution','answer','scene_spec')})})
 guard.append({'id':pid,'hard_or_quarantine':0,'issues':a.issues,'decimal_literals':0})
 grouped.setdefault(proposal['source_path'],None)
for rel in grouped:
 grouped[rel]=jsonl(snapshot.read(R/rel))
# Include the untouched fourth subject file so the candidate version has all 47 records.
geom='data/v2/train/leakage-isolated-v3-2026-10-05/dataset_geom.jsonl'
grouped[geom]=jsonl(snapshot.read(R/geom))
changes={v['id']:v['record'] for v in corrected};snapshot.check_unchanged()
dest=O/'math-corrected-v1';dest.mkdir(exist_ok=False)
files={};total=0
for rel,rows in grouped.items():
 staged=[copy.deepcopy(changes.get(row['id'],_invalidate(row,'codex-exact-math-v1',object_sha(row)))) for row in rows]
 name=Path(rel).name;fp=publish_jsonl(dest/name,staged);total+=len(staged)
 files[name]={**fp,'source_path':rel,'source_raw_sha256':raw_sha(snapshot.read(R/rel))}
snapshot.check_unchanged();assert total==47 and len(corrected)==9
result={'schema':'exact-math-corrected-version-v1','status':'MATERIALIZED_NOT_ADMITTED',
 'record_count':total,'corrected_count':len(corrected),'files':files,'corrections':corrected,
 'source_bindings':snapshot.bindings(),'formal_manifest_updated':False,'animation_verified':False,
 'unchanged_records_math_reviewed':False,'source_proposal_raw_sha256':raw_sha((P/'math-repair-proposals.pending.json').read_bytes())}
with (O/'math-correction-receipt.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
with (O/'math-correction-latex-qa.json').open('x',encoding='utf-8') as f:json.dump(guard,f,ensure_ascii=False,indent=2);f.write('\n')
md='# 九题精确数学修订稿\n\n实际新版本，未正式准入；原绑定题库不改写，动画未验收。\n'
for v in corrected:
 row=v['record'];md+='\n## '+row['id']+'\n\n题目：'+row['problem']+'\n\n过程：'+row['solution']+'\n\n答案：'+row['answer']+'\n\n场景步骤：\n\n'
 md+='\n'.join(str(i)+'. '+t for i,t in enumerate(row['scene_spec']['steps'],1))+'\n'
with (O/'math-9-corrected.md').open('x',encoding='utf-8') as f:f.write(md)
print(json.dumps({'materialized_records':total,'corrected_questions':len(corrected),'math_guard_blockers':0,'formal_manifest_updated':False}))
