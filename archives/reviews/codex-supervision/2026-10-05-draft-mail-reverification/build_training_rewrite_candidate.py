from pathlib import Path
import json,hashlib,copy,sys
import sympy as s
from fractions import Fraction
ROOT=Path(r'D:/Animation-Model-Training');OUT=Path(__file__).resolve().parent;dst=OUT/'training-rewrite';dst.mkdir(exist_ok=True);sys.path.insert(0,str(ROOT/'src'))
from animtrain.structural_leakage import compare,implementation_sha256
from animtrain.near_dup import shingles
source=ROOT/'data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl';old=next(json.loads(x) for x in source.read_text(encoding='utf-8').splitlines() if json.loads(x)['id']=='linalg-048');row=copy.deepcopy(old)
row.update(problem=r'设线性变换$T:\mathbb R^2\to\mathbb R^2$由$T(x,y)=(x+2y,0)$给出，$D=\{(x,y):x^2+y^2\le1\}$为闭单位圆盘。求$\ker T$与$\operatorname{im}T$，确定集合$T(D)$。对每个$q=(a,b)\in\mathbb R^2$，完整描述$D\cap T^{-1}(q)$：判定何时为空、为单点或为线段；在线段情形给出精确端点与长度，并解释圆盘在该变换下的几何变化。',solution=r'$T(x,y)=0$当且仅当$x+2y=0$，故$\ker T=\operatorname{span}\{(-2,1)\}$。任意实数$a$都有$T(a,0)=(a,0)$，故$\operatorname{im}T=\mathbb R\times\{0\}$。由柯西不等式，$(x+2y)^2\le(1^2+2^2)(x^2+y^2)\le5$，所以$T(D)\subset[-\sqrt5,\sqrt5]\times\{0\}$。反之，若$|a|\le\sqrt5$，点$p_a=\frac a5(1,2)$满足$\|p_a\|^2=a^2/5\le1$且$T(p_a)=(a,0)$，故两集合相等。若$b\ne0$，原像为空。若$b=0$，方程$x+2y=a$的全部解为$p_a+t v$，其中$v=\frac1{\sqrt5}(-2,1)$、$t\in\mathbb R$；$\|v\|=1$且$p_a\cdot v=0$，所以$\|p_a+tv\|^2=a^2/5+t^2$。当$|a|>\sqrt5$时不存在属于$D$的解；当$|a|=\sqrt5$时仅$t=0$，原像为单点$p_a$；当$|a|<\sqrt5$时，$|t|\le\sqrt{1-a^2/5}$，原像为端点$p_a\pm\sqrt{1-a^2/5}\,v$之间的闭线段，长度为$2\sqrt{1-a^2/5}$。因此，变换沿核方向把每条这样的弦压缩为一个点，将整个二维圆盘压缩为横轴上的闭线段，其二维面积为$0$。',answer=r'$\ker T=\operatorname{span}\{(-2,1)\}$，$\operatorname{im}T=\mathbb R\times\{0\}$，$T(D)=[-\sqrt5,\sqrt5]\times\{0\}$。记$p_a=\frac a5(1,2)$、$v=\frac{(-2,1)}{\sqrt5}$。若$b\ne0$或$|a|>\sqrt5$，则$D\cap T^{-1}(a,b)=\varnothing$；若$b=0$且$|a|=\sqrt5$，原像为$\{p_a\}$；若$b=0$且$|a|<\sqrt5$，原像端点为$p_a\pm\sqrt{1-a^2/5}\,v$，长度为$2\sqrt{1-a^2/5}$。',method='核像分析、柯西不等式与约束原像的正交分解',visual_style='圆盘压缩与原像纤维',efficiency_tags=['核方向追踪','约束原像分类'],draft_status='TRAINING-REWRITE-CANDIDATE-NOT-ADMITTED',admitted=False,animation_render_verified=False)
row['scene_spec']={'objects':[row['problem'],row['answer'],r'原像弦方向$(-2,1)$与横轴像线段$[-\sqrt5,\sqrt5]\times\{0\}$'],'steps':[r'第一步：展示$T(x,y)=(x+2y,0)$与圆盘$D$，标出核方向$(-2,1)$。',r'第二步：用$(x+2y)^2\le5(x^2+y^2)$给出像的范围，并用$p_a=\frac a5(1,2)$证明区间内每点可达。',r'第三步：写原像$p_a+t\frac{(-2,1)}{\sqrt5}$，利用正交关系得到$a^2/5+t^2\le1$。',r'第四步：按$b\ne0$、$|a|>\sqrt5$、$|a|=\sqrt5$、$|a|<\sqrt5$完整分类空集、单点、线段。',r'第五步：高亮精确端点和弦长$2\sqrt{1-a^2/5}$，展示各原像弦压缩为一个像点。']}
row['revision_lineage']={'original_id':'linalg-048','source_path':str(source.relative_to(ROOT)).replace('\\','/'),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_record_sha256':hashlib.sha256(json.dumps(old,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),'confirmed_leakage_with':['eval-linalg-015-s1','test-linalg-025'],'historical_risk_not_reset':True,'structural_change':'二阶平衡对称矩阵固定主轴谱分解，改为非可逆映射下闭圆盘的像与约束原像纤维分类','version':'candidate-codex-20261005-fiber-rewrite'}
q=dst/'linalg-048-replacement.jsonl';q.write_text(json.dumps(row,ensure_ascii=False)+'\n',encoding='utf-8')
a,t=s.symbols('a t',real=True);pa=s.Matrix([a/5,2*a/5]);v=s.Matrix([-2,1])/s.sqrt(5);M=s.Matrix([[1,2],[0,0]])
checks={'kernel':M*s.Matrix([-2,1]),'center_image':M*pa-s.Matrix([a,0]),'orthogonal':s.simplify(pa.dot(v)),'unit_direction':s.simplify(v.dot(v)-1),'squared_norm':s.simplify((pa+t*v).dot(pa+t*v)-(a*a/5+t*t))}
assert all(z==s.zeros(*z.shape) if isinstance(z,s.MatrixBase) else z==0 for z in checks.values())
refs=[]
for p in [ROOT/'data/v2/eval/dataset_eval.jsonl',ROOT/'data/v2/test/dataset_test.jsonl']+list((ROOT/'data/v2/train/leakage-isolated-v3-2026-10-05').glob('*.jsonl')):
 for x in p.read_text(encoding='utf-8').splitlines():
  z=json.loads(x)
  if z['id']!='linalg-048':refs.append(z)
D=ROOT/'reviews/2026-10-05-training-diversity-drafts';selector=json.loads((D/'draft-selection.json').read_text(encoding='utf-8'))
for e in selector['entries']:refs.extend(json.loads(x) for x in (D/e['path']).read_text(encoding='utf-8').splitlines())
left=shingles(row['problem']);hits=[];best=(Fraction(0),None)
for z in refs:
 right=shingles(z['problem']);score=Fraction(len(left&right),len(left|right)) if left|right else Fraction(0);comp=compare(row['problem'],z['problem'])
 if score>best[0]:best=(score,z['id'])
 if comp['candidate'] or score>=Fraction(2,5):hits.append({'id':z['id'],'jaccard':str(score),'structure':comp})
evidence={'candidate_file_sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'source_sha256':row['revision_lineage']['source_sha256'],'exact_checks':{k:str(z) for k,z in checks.items()},'comparisons':len(refs),'detector_sha256':implementation_sha256(),'positive_candidates':hits,'maximum_text_similarity':str(best[0]),'maximum_text_similarity_id':best[1],'manual_structure_review':'固定aI+bJ谱分解改为秩一映射下圆盘约束原像。留出唯一弦长相关题test-x-006为随机取弦的三种概率模型，未使用本题的确定性线性像与原像分类；不属于同核心换数值。共享正交分解或柯西不等式等通用定理不等于同一任务结构。','detector_unmatched':'UNKNOWN','production_manifest_modified':False,'formal_admission':False,'render_verified':False}
(dst/'candidate-verification.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(dst/'linalg-048-replacement.md').write_text('\n'.join(['# linalg-048 结构隔离改写候选','','保留原题ID；原训练、评测、测试与清单未改动。此候选未准入、未渲染验收。','','## 题目','',row['problem'],'','## 推导','',row['solution'],'','## 答案','',row['answer'],'','## 场景步骤','',*['- '+z for z in row['scene_spec']['steps']],'','原谱分解任务已改为非可逆线性映射的圆盘像及纤维分类；并非仅改矩阵数值。','']),encoding='utf-8')
print(json.dumps(evidence,ensure_ascii=False,indent=2))
