"""Exact symbolic verification of the revised alternating-projection task."""
import hashlib,json
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent
def digest(data):return hashlib.sha256(data).hexdigest()
rows=[json.loads(x) for x in (R/'record-bindings.jsonl').read_text(encoding='utf8').splitlines() if x.strip()]
ref=next(x for x in rows if x['id']=='draft-c18-02')
root=next(p for p in R.parents if p.name=='Animation-Model-Training')
record=json.loads((root/ref['path']).read_text(encoding='utf8').splitlines()[ref['source_line']-1])
assert digest(json.dumps(record,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==ref['record_sha256']
a,b,c=s.symbols('a b c',real=True);n=s.symbols('n',integer=True,positive=True)
I=s.eye(3);B1=s.diag(0,1,1);B2=s.Matrix([[s.Rational(1,2),-s.Rational(1,2),0],[-s.Rational(1,2),s.Rational(1,2),0],[0,0,1]])
A=B1*B2;P0=s.Matrix([a,b,c]);Q=s.Matrix([0,0,c]);Fn=s.Matrix([[0,0,0],[-2**(-n),2**(-n),0],[0,0,1]])
e2=s.Matrix([0,1,0]);zero=s.zeros(3);checks=[]
def eq(name,x,y):
 z=x-y
 ok=all(s.simplify(t)==0 for t in z) if isinstance(z,s.MatrixBase) else s.simplify(z)==0
 checks.append({'name':name,'passed':bool(ok)})
 assert ok,name
eq('B1 symmetric',B1.T,B1)
eq('B1 idempotent',B1*B1,B1)
eq('B2 symmetric',B2.T,B2)
eq('B2 idempotent',B2*B2,B2)
eq('B1 image lies in x=0',(B1*P0)[0],0)
eq('B2 image lies in x+y=0',(B2*P0)[0]+(B2*P0)[1],0)
eq('B1 displacement normal',P0-B1*P0,s.Matrix([a,0,0]))
eq('B2 displacement normal',P0-B2*P0,(a+b)/2*s.Matrix([1,1,0]))
eq('ordered composition',A,s.Matrix([[0,0,0],[-s.Rational(1,2),s.Rational(1,2),0],[0,0,1]]))
eq('first iterate',A*P0,s.Matrix([0,(b-a)/2,c]))
eq('power induction base',Fn.subs(n,1),A)
eq('power induction step',A*Fn,Fn.subs(n,n+1))
eq('positive-index iterate',Fn*P0,s.Matrix([0,(b-a)/2**n,c]))
eq('zero-index must use identity',A**0,I)
eq('initial squared error',(P0-Q).dot(P0-Q),a*a+b*b)
err=Fn*P0-Q
eq('positive-index squared error',err.dot(err),(b-a)**2/4**n)
eq('componentwise exact limit',s.Matrix([s.limit(v,n,s.oo) for v in Fn*P0]),Q)
eq('intersection projector',s.diag(0,0,1)*P0,Q)
eq('equal-input branch reaches at step one',(A*P0-Q).subs(b,a),s.zeros(3,1))
eq('non-idempotence witness first',A*e2,e2/2)
eq('non-idempotence witness second',A*A*e2,e2/4)
assert A*A!=A
checks.append({'name':'non-idempotence difference','passed':True})
manual=[
 {'name':'finite termination at index zero','argument':'Over R, a^2+b^2=0 iff a=b=0.'},
 {'name':'first arrival at index one','argument':'If a=b!=0, P0 is outside the common line but P1=Q.'},
 {'name':'no finite arrival when a!=b','argument':'For every integer n>=1, 2^n>0 and |b-a|>0; exact error is positive.'},
 {'name':'Euclidean error from square','argument':'The norm is the nonnegative square root: |b-a|/2^n.'}
]
out={'schema':'exact-alternating-projection-proof-v1','id':ref['id'],'record_sha256':ref['record_sha256'],'math_sha256':ref['math_sha256'],
 'source_sha256':ref['source_sha256'],'proof_script_sha256':digest(Path(__file__).read_bytes()),'symbolic_checks':checks,'symbolic_passed':len(checks),
 'manual_real_domain_implications':manual,'math_content':'PASS_EXACT_REVISED_TASK','scene_text':'PASS_MATCHES_EXACT_TASK',
 'signature_isolation':'NOT_ESTABLISHED','visual':'NOT_REVIEWED','native':'UNVERIFIED','production':'CLOSED','PASS_CORE_SCOPE_issued':False}
p=R/'exact-proof.json'
if p.exists():raise FileExistsError('Preserve the archived proof')
p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'symbolic_checks':len(checks),'math_content':out['math_content'],'record_sha256':ref['record_sha256']}))
