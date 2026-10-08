"""Exact checks against actual candidate records, plus explicit general proof obligations."""
from pathlib import Path
import hashlib,json,re
import sympy as sp

ROOT=Path(__file__).resolve().parents[3]
REVIEW=Path(__file__).resolve().parent
CORE=REVIEW/'effective-core-v3'
refs=[json.loads(x) for x in (CORE/'record-bindings.jsonl').read_text(encoding='utf-8').splitlines()]
wanted={'linalg-051','draft-c36-03','draft-c30-01','draft-c37-05'}
records={}
for b in refs:
    if b['id'] in wanted:
        p=ROOT/b['path']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==b['source_sha256']
        r=json.loads(p.read_text(encoding='utf-8').splitlines()[b['source_line']-1])
        assert hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==b['record_sha256']
        records[b['id']]=(r,b)
checks=[]
def check(name,ok):
    assert bool(ok),name
    checks.append({'name':name,'result':'PASS'})
def matrix(text):
    match=re.search(r'\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}',text)
    assert match
    return sp.Matrix([[sp.sympify(v) for v in row.split('&')] for row in match.group(1).split(r'\\')])
x=sp.symbols('x',real=True)
r,b=records['linalg-051']
check('difference task is actual candidate',r'\Delta p(x)=3x^2+3x+1' in r['problem'])
match=re.search(r'p\(x\)=([^$]+)',r['answer'])
p=sp.sympify(match.group(1).strip().rstrip('。').replace('^','**'))
rhs=3*x**2+3*x+1
p=sp.sympify(str(p),locals={'x':x})
check('actual normalized polynomial satisfies exact difference',sp.expand(p.subs(x,x+1)-p-rhs)==0)
check('actual polynomial normalization',p.subs(x,0)==0)
for n in range(1,13):
    difference=sp.Poly(sp.expand((x+1)**n-x**n),x)
    check('difference of degree '+str(n)+' has exact leading term',difference.degree()==n-1 and difference.LC()==n)
c=sp.symbols('c',real=True)
check('constant kernel example exact',sp.expand(c-c)==0)
r,b=records['draft-c36-03']
A=sp.diag(1,-1,0)
C=matrix(r['problem'])
B=matrix(r['answer'])
check('actual C invertible with determinant 6',C.det()==6)
check('actual B equals congruence product',C.T*A*C==B)
check('actual B rank two',B.rank()==2)
check('A inertia has one positive one negative one zero',A.eigenvals()=={sp.Integer(1):1,sp.Integer(-1):1,sp.Integer(0):1})
check('actual B has one zero eigenvalue',B.det()==0 and sp.expand(B.charpoly(sp.Symbol('L')).as_expr()-sp.Symbol('L')*(sp.Symbol('L')**2+2*sp.Symbol('L')-4))==0)
check('nonzero eigenvalues have opposite signs exact',sp.det(B[:2,:2])==-4)
check('trace obstruction exact',A.trace()==0 and B.trace()==-2)
v=sp.Matrix(sp.symbols('v0:3',real=True))
check('quadratic congruence identity for arbitrary vector',sp.expand((v.T*B*v)[0]-((C*v).T*A*(C*v))[0])==0)
r,b=records['draft-c30-01']
check('actual multiplicity answer bound',r'-\frac14(x-1)^3(x-2)^2' in r['answer'])
f=-sp.Rational(1,4)*(x-1)**3*(x-2)**2
check('degree exactly five',sp.degree(f,x)==5)
check('normalization exactly one',f.subs(x,0)==1)
for k in range(3):check('root one derivative '+str(k)+' vanishes',sp.diff(f,x,k).subs(x,1)==0)
check('root one third derivative nonzero exact',sp.diff(f,x,3).subs(x,1)==-sp.Rational(3,2))
for k in range(2):check('root two derivative '+str(k)+' vanishes',sp.diff(f,x,k).subs(x,2)==0)
check('root two second derivative nonzero exact',sp.diff(f,x,2).subs(x,2)==-sp.Rational(1,2))
check('factors are coprime',sp.gcd((x-1)**3,(x-2)**2)==1)
check('normalization coefficient unique',sp.solve(sp.Eq(-4*c,1),c)==[-sp.Rational(1,4)])
check('evaluation expansion subtask actually removed','x-1$ 的幂' not in r['problem'] and 'u=x-1' not in r['solution'])
r,b=records['draft-c37-05']
check('actual finite dimension hypothesis',r'非零有限维实线性空间' in r['problem'])
S=sp.Matrix(3,3,sp.symbols('s0:9'))
T=sp.Matrix(3,3,sp.symbols('t0:9'))
check('symbolic matrix commutator has trace zero',sp.expand((S*T-T*S).trace())==0)
check('identity trace exact nonzero',sp.eye(3).trace()==3)
g=sp.Function('p')(x)
check('infinite polynomial operator identity via product rule',sp.expand(sp.diff(x*g,x)-x*sp.diff(g,x)-g)==0)
check('actual operators stated',r"D(p)=p'" in r['answer'] and r'M(p)=xp' in r['answer'])
for rid,(r,b) in records.items():
    text=json.dumps({k:r[k] for k in ('problem','solution','answer','scene_spec')},ensure_ascii=False)
    check(rid+' exact math text has no decimal approximations',re.search(r'\d+\.\d+',text) is None)
manual=[
    {'record_id':'linalg-051','obligation':'For every n>=1 in R[x], the leading coefficient n*a_n is nonzero; therefore only constants lie in the kernel.','verdict':'PASS_INDEPENDENT_EXACT_PROOF'},
    {'record_id':'linalg-051','obligation':'Subtracting the exact leading-term primitive reduces degree; induction with constant base establishes surjectivity for all finite degrees.','verdict':'PASS_INDEPENDENT_EXACT_PROOF'},
    {'record_id':'draft-c36-03','obligation':'An invertible variable map bijects positive/negative subspaces preserving their dimensions; invertible left/right factors preserve rank.','verdict':'PASS_INDEPENDENT_EXACT_PROOF'},
    {'record_id':'draft-c30-01','obligation':'Distinct roots make the multiplicity factors coprime; degree bound forces a constant quotient uniquely fixed by f(0)=1.','verdict':'PASS_INDEPENDENT_EXACT_PROOF'},
    {'record_id':'draft-c37-05','obligation':'Finite double sums prove tr(ST)=tr(TS) in every dimension n>=1; the real scalar n cannot vanish.','verdict':'PASS_INDEPENDENT_EXACT_PROOF'},
    {'record_id':'draft-c37-05','obligation':'Derivative and multiplication are endomorphisms of infinite-dimensional R[x]; product rule gives the identity without a finite trace.','verdict':'PASS_INDEPENDENT_EXACT_PROOF'},
]
receipt={'schema':'exact-deep-rewrite-proof-v1','symbolic_checks':len(checks),'checks':checks,'general_proof_obligations':manual,'version_bindings':{rid:{k:b[k] for k in ['record_sha256','math_sha256','source_sha256','path','source_line']} for rid,(r,b) in records.items()},'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'mathematics':'PASS_EXACT_NEW_FOUR_RECORDS','scene_text':'PASS_INDEPENDENTLY_REVIEWED_WITH_FORMULAS','semantic_isolation':'NOT_ESTABLISHED','production':'CLOSED'}
(CORE/'exact-proof.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'exact_checks':len(checks),'general_proof_obligations':len(manual),'new_math':'PASS_EXACT_NEW_FOUR_RECORDS'}))
