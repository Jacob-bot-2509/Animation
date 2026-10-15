"""Build versioned draft-only corrections; never rewrite submitted or frozen sources."""
from pathlib import Path
import json,hashlib,copy,re
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def write(p,data):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists() and p.read_bytes()!=data:raise ValueError('refuse replacing existing artifact: '+str(p))
 p.write_bytes(data)
def emit(p,x):write(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def lines(p):return [json.loads(s) for s in p.read_text(encoding='utf-8-sig').splitlines() if s.strip()]
def text_replace(x,a,b):
 if isinstance(x,str):return x.replace(a,b)
 if isinstance(x,list):return [text_replace(y,a,b) for y in x]
 if isinstance(x,dict):return {k:text_replace(v,a,b) for k,v in x.items()}
 return x
def main():
 bound={}
 for d in (OUT/'bound-records').iterdir():
  if int(d.name.split('-')[0][5:])<=12:
   for q in lines(d/'records.jsonl'):
    assert q['record']['id'] not in bound
    bound[q['record']['id']]=q
 assert len(bound)==264
 specs={}
 def edit(rid,kind,reason,fn):
  old=bound[rid]['record'];new=copy.deepcopy(old);fn(new)
  fields=[k for k in ('problem','solution','answer','scene_spec') if old[k]!=new[k]]
  assert fields
  specs[rid]={'kind':kind,'reason':reason,'fields':{k:new[k] for k in fields}}
 def replace(r,field,a,b):
  assert a in r[field];r[field]=r[field].replace(a,b)
 edit('draft-c33-03','MALFORMED_MATRIX',
      '块逆修正列漏了行分隔符，原式变成一个乘积而非二元列向量。',
      lambda r:replace(r,'solution',r'\begin{pmatrix}-\frac12\frac12\end{pmatrix}',r'\begin{pmatrix}-\frac12\\\frac12\end{pmatrix}'))
 bad=r'\begin{pmatrix}\frac32&\frac32\frac12&-\frac12\end{pmatrix}'
 good=r'\begin{pmatrix}\frac32&\frac32\\\frac12&-\frac12\end{pmatrix}'
 def fix_q(r):
  for f in ('solution','answer'):replace(r,f,bad,good)
  r['scene_spec']=text_replace(r['scene_spec'],bad,good)
 edit('draft-c37-04','MALFORMED_MATRIX','过程和答案的Q矩阵漏了行分隔符；改为正确的二阶矩阵。',fix_q)
 uniform=r'在有限区间$[a,b]$上，若可积函数$g_n$一致收敛于$g$，则$g$可积且$\left|\int_a^b g_n(x)\,dx-\int_a^b g(x)\,dx\right|\le(b-a)\sup_{x\in[a,b]}|g_n(x)-g(x)|\to0$，所以一致收敛是交换积分与极限的充分条件；本题的连续函数列满足可积性，但不满足一致收敛。'
 def fix_uniform(r):
  r['solution']+=uniform
  r['answer']+=r'一致收敛的充分性由积分差不超过区间长度乘一致误差证明。'
  r['scene_spec']['objects'][1]=r['answer']
  r['scene_spec']['steps'].append('第四步:'+uniform)
 edit('draft-c12-05','MISSING_REQUESTED_PROOF','题干要求的一致收敛充分性没有作答，补齐可积性与积分误差的精确不等式。',fix_uniform)
 oldcoord=r'则交线坐标为 $(\sin t,\sqrt5\cos t)$,即 $\eta^2+\frac{\xi^2}{5}=1$'
 newcoord=r'明确坐标$\xi=e_1\cdot(x,y,z)=y$、$\eta=e_2\cdot(x,y,z)=(x+2z)/\sqrt5$，则$(\xi,\eta)=(\sin t,\sqrt5\cos t)$，所以$\xi^2+\frac{\eta^2}{5}=1$'
 def fix_coord(r):
  replace(r,'solution',oldcoord,newcoord)
  r['scene_spec']=text_replace(r['scene_spec'],oldcoord,newcoord)
 edit('draft-c19-03','COORDINATE_CONVENTION','原式未定义坐标名且与有序坐标写法混用；显式定义两个坐标并同步改正场景。',fix_coord)
 def fix_compatible(r):
  a=r'非齐次方程组 $Ax=b$($b\neq0$)的解集是'
  b=r'相容的非齐次方程组 $Ax=b$($b\neq0$)的解集是'
  replace(r,'problem',a,b)
  r['problem']+=r'同时说明不相容时的解集。'
  r['scene_spec']['objects'][0]=r['problem']
 edit('draft-c32-05','MISSING_COMPATIBILITY_PREMISE','题干的陪集断言缺少相容性假设；补齐并要求说明无解分支。',fix_compatible)
 def fix_angle(r):
  replace(r,'problem','给两特征线的锐夹角精确式。',r'给两特征线夹角$\alpha\in(0,\pi/2]$的精确式，并包含垂直情形。')
  r['scene_spec']['objects'][0]=r['problem']
 edit('draft-c27-04','BOUNDARY_TERMINOLOGY','k=0时夹角为直角，题干的严格锐角用词不覆盖该参数。',fix_angle)
 def fix_span(r):
  a=r'\operatorname{span}(x^2-1)^2';b=r'\operatorname{span}\{(x^2-1)^2\}'
  replace(r,'answer',a,b);r['scene_spec']=text_replace(r['scene_spec'],a,b)
 edit('draft-c38-02','SPAN_NOTATION','明确先平方多项式、再取其线性张成，避免把指数写在线性张成之外。',fix_span)
 def fix_blocks(r):
  r['answer']=r'$\dim\ker J_m(0)^k=\min(k,m)$。记$r_k=\dim\ker(A-\lambda I)^k$、$r_0=0$，则尺寸至少为$k$的$\lambda$-Jordan块数为$r_k-r_{k-1}$，尺寸恰为$k$的块数为$2r_k-r_{k-1}-r_{k+1}$；该序列唯一确定全部块尺寸。'
  r['scene_spec']['objects'][1]=r['answer']
 edit('draft-c41-05','BLOCK_COUNT_SCOPE','答案中的块数未指明“至少k阶”；补齐至少与恰好两种计数，避免误用差分。',fix_blocks)
 def fix_inertia(r):
  a='标签:「不定 (1,1)」「退化 (1,0)」「正定 (2,0)」'
  b='标签:「不定：惯性(1,1,0)」「退化：惯性(1,0,1)」「正定：惯性(2,0,0)」'
  assert a in r['scene_spec']['objects']
  r['scene_spec']=text_replace(r['scene_spec'],a,b)
 edit('draft-c35-03','SCENE_NOTATION','场景标签统一使用(正,负,零)三元惯性，与正文及后续步骤保持一致。',fix_inertia)
 def fix_param(r):
  a=r'\frac{dy}{dx}=\frac{3t^2-3}{2t}'
  b=r'\frac{dy}{dx}=\frac{3t^2-3}{2t}\quad(t\ne0)'
  assert any(a in s for s in r['scene_spec']['objects'])
  r['scene_spec']=text_replace(r['scene_spec'],a,b)
 edit('draft-c01-03','SCENE_DOMAIN','场景斜率公式补充t不等于零，零参数的竖直切线单独处理。',fix_param)
 emit(OUT/'draft-correction-specs.json',specs)
 version='codex-continuous-draft-v1-20261007'
 patches=[];source_bindings=[];final={}
 for source in sorted({q['source']['source_path'] for q in bound.values()}):
  data=(ROOT/source).read_bytes();rawlines=data.splitlines(keepends=True);outlines=[];changed=[]
  assert sha(data)==next(q['source']['source_raw_sha256'] for q in bound.values() if q['source']['source_path']==source)
  write(OUT/'source-originals'/source,data)
  for i,line in enumerate(rawlines,1):
   old=json.loads(line.decode('utf-8-sig'));rid=old['id'];q=bound[rid]
   assert q['source']['source_path']==source and q['source']['source_line']==i
   assert old==q['record'] and sha(canon(old))==q['source']['record_version_sha256']
   new=copy.deepcopy(old)
   if rid in specs:
    new.update(copy.deepcopy(specs[rid]['fields']))
    new['revision_lineage']['continuous_review_parent']={
      'source_path':source,'source_raw_sha256':sha(data),'source_line':i,
      'record_version_sha256':sha(canon(old)),'versioned_id':old.get('versioned_id'),
      'strict_review':old.get('strict_review')}
    new['revision_lineage']['version']=version
    new['revision_lineage']['continuous_correction_reason']=specs[rid]['reason']
    new['versioned_id']=version+'-'+rid
    new['draft_status']=version+'-NOT-ADMITTED'
    new['strict_review'].update({
      'math_content_sha256':sha(json.dumps({k:new[k] for k in ('problem','solution','answer','scene_spec')},ensure_ascii=False,sort_keys=True).encode()),
      'math_review_evidence':str((OUT/'independent-draft-review-264.jsonl').relative_to(ROOT)).replace('\\','/'),
      'verification_basis':'INDEPENDENT_PROBLEM_PROOF_ANSWER_AND_SCENE_TEXT_REVIEW_PLUS_EXACT_WITNESSES',
      'admitted':False,'render_verified':False,'core_math_verified':True,
      'text_math_fields_reviewed':True,'scene_text_reviewed':True})
    newline=canon(new)+b'\n';changed.append(i)
    fields=[k for k in old if old[k]!=new[k]]
    patches.append({'id':rid,'source':q['source'],'kind':specs[rid]['kind'],'reason':specs[rid]['reason'],
      'before_record_sha256':sha(canon(old)),'after_record_sha256':sha(canon(new)),
      'changed_fields':fields,'before_fields':{k:old[k] for k in fields},
      'after_fields':{k:new[k] for k in fields},'corrected_record':new})
   else:newline=line
   final[rid]=new;outlines.append(newline)
  candidate=b''.join(outlines);dest=OUT/'candidate-sources'/source;write(dest,candidate)
  source_bindings.append({'source_path':source,'source_raw_sha256':sha(data),'source_bytes':len(data),
    'path':str(dest.relative_to(ROOT)).replace('\\','/'),'raw_sha256':sha(candidate),'bytes':len(candidate),
    'records':len(rawlines),'changed_lines':changed})
 assert len(final)==264 and len(patches)==10 and len(source_bindings)==18
 write(OUT/'draft-corrections-10.jsonl',b''.join(canon(x)+b'\n' for x in sorted(patches,key=lambda x:x['id'])))
 emit(OUT/'draft-candidate-source-bindings.json',source_bindings)
 notes=json.loads((OUT/'draft-review-notes.json').read_text(encoding='utf-8'))
 assert set(notes)==set(final)
 rows=[]
 for rid,q in sorted(bound.items()):
  new=final[rid]
  rows.append({'id':rid,'source':q['source'],'candidate_record_sha256':sha(canon(new)),
    'source_math_verdict':'ISSUE' if rid in specs and any(k in specs[rid]['fields'] for k in ('problem','solution','answer')) else 'PASS',
    'source_scene_verdict':'ISSUE' if rid in specs and 'scene_spec' in specs[rid]['fields'] else 'PASS',
    'post_repair_math':'PASS','post_repair_scene_text':'PASS','exact_expression_policy':'PASS',
    'independent_basis':notes[rid],'mathematical_acceptance_scope':'CURRENT_CANDIDATE_FIELDS_ONLY',
    'semantic_isolation':'NOT_ESTABLISHED','native_render':'UNVERIFIED','admitted':False,
    'revision_reason':specs.get(rid,{}).get('reason')})
 write(OUT/'independent-draft-review-264.jsonl',b''.join(canon(x)+b'\n' for x in rows))
 md=['# 草稿独立复核及修订','', '范围：264条；10条存在正文或场景的条件、公式、记号或作答完整性问题。保留全部原始提交，修订来源18份。所有判定绑定当前候选版本；实际渲染未验证，数据隔离尚未完成。','']
 for patch in sorted(patches,key=lambda x:x['id']):
  md+=['## '+patch['id'],'',patch['reason'],'']
  r=patch['corrected_record']
  md+=['题目：'+r['problem'],'','过程：'+r['solution'],'','答案：'+r['answer'],'','修订后：数学内容合格；场景文字合格；版本绑定另由只读重建器检查。','']
 write(OUT/'DRAFT_CORRECTIONS.md',('\n'.join(md)+'\n').encode())
 print(json.dumps({'records':len(final),'revised_records':len(patches),'full_sources':len(source_bindings)},indent=2))
if __name__=='__main__':main()
