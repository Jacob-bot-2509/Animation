from pathlib import Path
import json,sys,copy,difflib
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
import core_signatures as c,native_render_pilot as n
def read(p):return json.loads(p.read_text('utf-8'))
def sha(p):return c.digest(p.read_bytes())
def save(p,v):p.write_bytes(c.encoded(v))
def jl(p,vs):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(''.join(json.dumps(v,ensure_ascii=False,sort_keys=True)+'\n' for v in vs),encoding='utf-8',newline='\n')
bound=read(O/'bound-original-math-records.json'); originals={z['record']['id']:z['record'] for z in bound}
findings=read(O/'manual-review-progress.json')['findings'];ids=[z['id'] for z in findings]
new={rid:copy.deepcopy(originals[rid]) for rid in ids}
def rep(rid,a,b,field='solution'):
 assert a in new[rid][field],(rid,a)
 new[rid][field]=new[rid][field].replace(a,b)
def sol(rid,s):new[rid]['solution']=s
rep('eval-linalg-007-s3',r'$A^n=$ 旋转 $n\theta$ 角的矩阵',new['eval-linalg-007-s3']['answer']+'，即旋转 $n\\theta$ 角的矩阵')
rep('eval-linalg-011-s1',r'该矩阵 $=(\lambda-1)I+J$',r'该系数矩阵 $A=(\lambda-1)I+J$')
rep('eval-linalg-019-s3',r'$f$ 正定 $\iff\Delta_3>0\iff a>2$',r'$A\succ0\iff\Delta_3>0\iff a>2$（$A\succ0$ 表示二次型 $f$ 正定）')
rep('eval-linalg-021-s2',r'全正 $\iff 2-a^2>0\iff |a|<\sqrt{2}$',r'全正。因此 $f\succ0\iff 2-a^2>0\iff |a|<\sqrt{2}$（$f\succ0$ 表示 $f$ 正定）')
new['eval-linalg-030-s2']['efficiency_tags']=[r'原顺序投影：$w_1=v_1$，$w_2=v_2-\frac12w_1$',r'$u_2=2w_2$，$w_3=v_3-\frac12w_1-\frac16u_2$',r'非零缩放：$u_1=w_1$，$u_2=2w_2$，$u_3=-\frac32w_3$']
rep('eval-linalg-032-s3',r'$(e_3,\ B e_3,\ B^2 e_3)=',r'$C=(e_3,\ B e_3,\ B^2 e_3)=')
rep('eval-linalg-032-s3',r'\det=1\neq 0',r'\det C=1\neq 0')
rep('eval-linalg-032-s3',r'$a$ 从 $\neq 1$ 变到 1 时',r'参数从 $a\neq1$ 变到 $a=1$ 时')
criterion=r'$A^TA=I\iff a_i^Ta_j=\delta_{ij}\quad(1\le i,j\le n)$；其中 $a_i=Ae_i$，即列向量构成 $\mathbb R^n$ 的标准正交基。'
for rid in ['eval-linalg-035-s1','eval-linalg-035-s2','eval-linalg-035-s3']:new[rid]['answer']=criterion
rep('eval-linalg-035-s1',r'$A^TA=I\iff a_i\cdot a_j=\delta_{ij}$ 对一切 $i,j$ 成立 $\iff$ 列向量两两正交且都是单位向量 $\iff$ 列向量构成标准正交基',r'$A^TA=I\iff a_i\cdot a_j=\delta_{ij}\quad(1\le i,j\le n)$，即列向量两两正交且都是单位向量，从而构成标准正交基')
sol('eval-linalg-035-s2',r'若 $A^TA=I$，则 $\|Ax\|^2=x^TA^TAx=x^Tx=\|x\|^2$ 对每个 $x\in\mathbb R^n$ 成立。反之，若 $A$ 保长，由实内积的极化恒等式得 $\langle Ax,Ay\rangle=\frac{\|A(x+y)\|^2-\|Ax\|^2-\|Ay\|^2}{2}=\langle x,y\rangle.$ 取 $x=e_i,y=e_j$，令 $a_i=Ae_i$，得 $a_i^Ta_j=\delta_{ij}$，故 $(A^TA)_{ij}=\delta_{ij}$，即 $A^TA=I$。因此 $A^TA=I\iff\|Ax\|^2=\|x\|^2\quad(\forall x\in\mathbb R^n)$。若 $\sum_i c_i a_i=0$，与 $a_j$ 取内积得 $c_j=0$；这 $n$ 个单位正交向量线性无关，构成 $\mathbb R^n$ 的标准正交基。反之，若列为标准正交基，则 $(A^TA)_{ij}=a_i^Ta_j=\delta_{ij}$，故 $A^TA=I$。')
rep('eval-prob-001-s1',r'故换门获胜概率 $=',r'记 $W$ 为换门获胜事件，故 $P(W)=')
general=r'对不附加主持人选门规则的原题，记初选门为 $I$、车门为 $C$，$q_i=P(I=i)$，$i\in\{1,2,3\}$。由题设独立性及车门均匀分布，$P(I=i,C=j)=\frac{q_i}{3}$。记 $W$ 为总是换门的获胜事件；无论主持人如何在可开的羊门中选择，$W=\{C\ne I\}$。因此 $P(W)=\sum_{i=1}^3\sum_{j\ne i}\frac{q_i}{3}=\frac23\sum_{i=1}^3q_i=\frac23.$ 坚持初选获胜概率为 $P(C=I)=\sum_{i=1}^3\frac{q_i}{3}=\frac13$。这不要求 $q_i=\frac13$，也不要求主持人等概率开门。'
rid='eval-prob-001-s2';s=new[rid]['solution'];s=s[:s.index('注意')];sol(rid,s+'上述条件概率演示仅适用于额外的公平开门规则，不把它作为原题假设。'+general)
sol('eval-prob-001-s3',general)
new['eval-prob-001-s3']['efficiency_tags']=[r'按初选 $I=i$ 分行的加权枚举：$P(I=i,C=j)=q_i/3$',r'每行两格换门获胜，合计 $P(W)=\frac23\sum_iq_i=\frac23$']
new['eval-prob-007-s2']['efficiency_tags']=[r'互异生日概率 $q_k$ 与 $1\le k\le30$',r'递推 $q_k=q_{k-1}\frac{366-k}{365}$，$q_1=1$']
rep('eval-prob-007-s3',r'\dfrac{87}{73}\approx1.19',r'\dfrac{87}{73}','efficiency_tags') if False else None
new['eval-prob-007-s3']['efficiency_tags']=[s.replace(r'\dfrac{87}{73}\approx1.19',r'\dfrac{87}{73}') for s in new['eval-prob-007-s3']['efficiency_tags']]
rep('eval-prob-011-s2',r'$N$ 第 1 行之和 $=4+2=6$',r'$N$ 第 1 行之和，即 $E_0=N_{11}+N_{12}=4+2=6$')
new['linalg-051']['efficiency_tags']=[r'差分首项决定 $\ker\Delta=\mathbb R\cdot1$',r'次数归纳构造原像与初值确定唯一解']
new['linalg-051']['scene_spec']['objects'][1]=r'二项式恒等式 $\Delta(a_nx^n)=a_n\sum_{j=0}^{n-1}\binom nj x^j$（$n\ge1$）；首项为 $na_nx^{n-1}$'
rep('linalg-054',r'若 $D=0$，两直线平行或重合，对应无解或无穷多解。',r'一般二元一次方程组记为 $Az=b$。若两方程的法向量均非零且 $D=\det A=0$，则两直线平行不重合或重合，对应无解或无穷多解。若有零法向量，该方程是 $0=b_i$，不表示直线：$b_i\ne0$ 时无解，$b_i=0$ 时为恒等式。统一判据为 $\operatorname{rank}A=\operatorname{rank}(A\mid b)$ 当且仅当有解；有解且 $D=0$ 时解空间的仿射维数为 $2-\operatorname{rank}A\ge1$。')
new['linalg-054']['answer']=r'$x=2,y=1$；$D=0$ 且两法向量均非零时，两直线平行或重合。一般情形按 $\operatorname{rank}A=\operatorname{rank}(A\mid b)$ 判定相容性；相容时解集维数为 $2-\operatorname{rank}A$。'
new['linalg-054']['scene_spec']['steps'].append(r'零行先判定 $0=b_i$ 是否相容；用 $\operatorname{rank}A=\operatorname{rank}(A\mid b)$ 覆盖退化情形。')
rep('test-geom-016',r'故椭圆面积 $=\pi\cdot|\det A|=\pi$',r'记椭圆面积为 $S$，则 $S=\pi\cdot|\det A|=\pi$')
rep('test-geom-022',r'；各列模长',r'；第二列与第三列点积为 $0$。各列模长的平方')
new['test-prob-007']['efficiency_tags']=[r'归一化的剩余寿命生存曲线与原曲线重合',r'条件概率为生存函数值比 $S(1500)/S(500)$']
sol('test-linalg-013',r'记 $T_n$ 为题设三对角矩阵，$D_n=\det T_n$，并约定 $D_0=1$。当 $n\ge2$ 时，令 $M_{12}$ 表示删去 $T_n$ 第一行和第二列后的子式行列式；其第一列只有首项 $1$ 非零，沿该列展开得 $M_{12}=D_{n-2}$。再沿 $T_n$ 第一行展开，得 $D_n=D_{n-1}-M_{12}=D_{n-1}-D_{n-2}$。初值为 $D_1=1,D_2=0$。递推得 $D_3=-1,D_4=-1,D_5=0,D_6=1$。对所有 $n\ge1$，$D_{n+3}=D_{n+2}-D_{n+1}=-D_n$，所以 $D_{n+6}=-D_{n+3}=D_n$。前六个相邻有序对为 $(1,0),(0,-1),(-1,-1),(-1,0),(0,1),(1,1)$，互不相同；因任意正周期必须使首个有序对重现，最小正周期为 $6$。')
rid='test-x-010'
s=new[rid]['solution'];tail=s[s.index('概率解释'):]
sol(rid,r'记协方差矩阵为 $\Sigma=\begin{pmatrix}\sigma_1^2&\rho\sigma_1\sigma_2\\\rho\sigma_1\sigma_2&\sigma_2^2\end{pmatrix}$。其顺序主子式为 $\sigma_1^2$ 和 $\det\Sigma=\sigma_1^2\sigma_2^2(1-\rho^2)$。由题设 $\sigma_1,\sigma_2>0$，Sylvester 判据给出 $\Sigma\succ0\iff(\sigma_1^2>0\ \land\ \det\Sigma>0)$，再得 $\Sigma\succ0\iff 1-\rho^2>0\iff|\rho|<1$。'+tail)
new[rid]['answer']=r'在 $\sigma_1,\sigma_2>0$ 的前提下，$\Sigma\succ0\iff|\rho|<1$；$\Sigma$ 为题设协方差矩阵。'
rid='test-calc-015'
a=r'$\displaystyle\int_0^1\dfrac{\ln(1+x)}{x}dx=\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n}\int_0^1x^{n-1}dx=\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n^2}$'
b=r'记 $I=\int_0^1\frac{\ln(1+x)}x\,dx$，逐项积分得 $I=\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}n\int_0^1x^{n-1}\,dx$。因 $\int_0^1x^{n-1}\,dx=\frac1n$，所以 $I=\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{n^2}$'
rep(rid,a,b)
# Synchronize duplicated complete proofs/results/tags without changing any question.
for rid,q in new.items():
 old=originals[rid]
 oldtags=old.get('efficiency_tags',[]);newtags=q.get('efficiency_tags',[])
 q['scene_spec']['steps']=[s.replace(old['solution'],q['solution']).replace(old['answer'],q['answer']) for s in q['scene_spec']['steps']]
 for i,tag in enumerate(oldtags):
  if i<len(newtags):
   q['scene_spec']['objects']=[v.replace(tag,newtags[i]) for v in q['scene_spec'].get('objects',[])]
   q['scene_spec']['steps']=[v.replace(tag,newtags[i]) for v in q['scene_spec']['steps']]
 assert q['id']==old['id'] and q['problem']==old['problem']
 if 'strict_review' in q:
  q['strict_review'].update(admitted=False,render_verified=False,math_content_sha256=c.math_digest(q),math_review_evidence=(O/'complete-proof-review.json').relative_to(R).as_posix(),verification_basis='PENDING_CURRENT_EXACT_INDEPENDENT_VERIFICATION')
save(O/'repaired-records-before.json',[originals[r] for r in ids]);save(O/'repaired-records-after.json',[new[r] for r in ids])
(O/'math-and-scene-changes.patch').write_text(''.join(difflib.unified_diff(json.dumps([originals[r]for r in ids],ensure_ascii=False,indent=2).splitlines(True),json.dumps([new[r]for r in ids],ensure_ascii=False,indent=2).splitlines(True),fromfile='repaired-records-before.json',tofile='repaired-records-after.json')),encoding='utf-8',newline='\n')
bs=[json.loads(s)for s in (O/'parent-current-record-bindings.jsonl').read_text('utf-8').splitlines()];srcs=read(O/'parent-current-source-bindings.json')
changedpaths={b['path'] for b in bs if b['id'] in new};maps={};changes=[]
for path in sorted(changedpaths):
 source=c.checked_path(R/path,R);raw=source.read_bytes();binding=next(z for z in srcs if z['path']==path)
 assert sha(source)==binding['sha256']
 rows=[json.loads(s)for s in raw.decode('utf-8').splitlines()];before=copy.deepcopy(rows)
 for i,q in enumerate(rows):
  if q['id'] in new:
   assert c.dense(q)==c.dense(originals[q['id']]);rows[i]=new[q['id']]
 target=O/'candidate-sources'/source.name;assert not target.exists();jl(target,rows)
 assert len(rows)==len(before) and [z['id']for z in rows]==[z['id']for z in before]
 assert {a['id']for a,b in zip(rows,before)if a!=b}=={b['id']for b in bs if b['path']==path and b['id']in new}
 maps[path]=(target,sha(target))
 changes.append({'before_path':path,'before_sha256':sha(source),'after_path':target.relative_to(R).as_posix(),'after_sha256':sha(target),'changed_ids':[a['id']for a,b in zip(rows,before)if a!=b]})
for b in bs:
 if b['path'] in maps:
  target,h=maps[b['path']];b.update(path=target.relative_to(R).as_posix(),source_sha256=h)
  if b['id']in new:
   q=new[b['id']];b.update(parent_binding=next(z['binding']for z in bound if z['record']['id']==b['id']),record_sha256=c.dense(q),math_sha256=c.math_digest(q),review='REPAIRED_CURRENT_BATCH_PENDING_FINAL_INDEPENDENT_VERIFICATION')
for s in srcs:
 if s['path']in maps:
  oldpath=s['path'];target,h=maps[oldpath];s.update(parent_path=oldpath,parent_sha256=s['sha256'],path=target.relative_to(R).as_posix(),sha256=h,bytes=target.stat().st_size,unchanged_source_bytes=False)
sigs=[json.loads(s)for s in (O/'parent-current-complete-signatures.jsonl').read_text('utf-8').splitlines()]
for s in sigs:
 if s['id']in new:s.update(record_sha256=c.dense(new[s['id']]),math_sha256=c.math_digest(new[s['id']]))
jl(O/'current-record-bindings.jsonl',bs);jl(O/'current-complete-signatures.jsonl',sigs);save(O/'current-source-bindings.json',srcs)
save(O/'repair-source-bindings.json',changes)
changed=[];unchanged=[]
byidx={z['id']:z for z in map(json.loads,(O/'parent-CURRENT_DELIVERY_INDEX.jsonl').read_text('utf-8').splitlines())}
for rid,q in new.items():
 f,loc=n.formula_inventory(q);oldf,_=n.formula_inventory(originals[rid])
 if f!=oldf:changed.append(rid)
 else:unchanged.append(rid)
save(O/'render-plan.json',{'rerender_ids':changed,'unchanged_formula_pixels_ids':unchanged,'changed_record_ids':ids,'question_ids_unchanged':True,'records':len(bs),'sources':len(srcs),'production':'CLOSED'})
print(json.dumps({'status':'REPAIRED_PENDING_VERIFICATION','changed':len(ids),'rerender':len(changed),'tags_only':unchanged,'sources':len(srcs),'records':len(bs)}))
