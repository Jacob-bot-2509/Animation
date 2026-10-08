"""Independent exact algebra and current training-pool checks for draft v2."""
import json
import re
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from animtrain.manifest import Manifest, canonical_problem_text
from animtrain.kp_rule import kp_signature
OUT = Path(__file__).resolve().parent

def zero_matrix(m):
    return all(s.simplify(v) == 0 for v in m)

def grams(text):
    t = re.sub(r"[\s$\\_{}\[\]()]", "", text).lower()
    return ({t} if t else set()) if len(t) < 5 else {t[i:i+5] for i in range(len(t)-4)}

def sim(left, right):
    a, b = grams(left), grams(right)
    return Fraction(len(a & b), len(a | b)) if a | b else Fraction(0)

a, lam, x, y, z = s.symbols("a lambda x y z", real=True)
results = {}
A = s.Matrix([[1,a,0],[a,1,a],[0,a,1]])
Q = s.Matrix([[1/s.sqrt(2),s.Rational(1,2),s.Rational(1,2)],
              [0,s.sqrt(2)/2,-s.sqrt(2)/2],
              [-1/s.sqrt(2),s.Rational(1,2),s.Rational(1,2)]])
assert zero_matrix(Q.T*Q-s.eye(3))
assert zero_matrix(Q.T*A*Q-s.diag(1,1+s.sqrt(2)*a,1-s.sqrt(2)*a))
assert s.expand((lam*s.eye(3)-A).det()-(lam-1)*((lam-1)**2-2*a*a)) == 0
results["014"] = {"answer_correct":True, "charpoly":str(s.factor(A.charpoly().as_expr())), "Q_orthogonal":True, "diagonalization_verified":True}

A = s.Matrix([[1,1,1],[1,2,0],[1,0,a]])
f = x*x+2*y*y+a*z*z+2*x*y+2*x*z
assert s.expand(f-((x+y+z)**2+(y-z)**2+(a-2)*z*z)) == 0
C = s.Matrix([[1,-1,-2],[0,1,1],[0,0,1]])
assert C.det() == 1 and zero_matrix(C.T*A*C-s.diag(1,1,a-2))
first = s.eye(3);first[0,1]=-1;first[0,2]=-1
intermediate = first.T*A*first
assert intermediate == s.Matrix([[1,0,0],[0,1,-1],[0,-1,a-1]])
results["019"] = {"answer_correct":True,"determinant":str(A.det()),"coordinate_C":str(C),"after_first_elimination":str(intermediate),"missing_second_elimination":"R3+=R2 and C3+=C2", "positive_definite":"a>2", "boundary_kernel":str(A.subs(a,2).nullspace())}

A=s.Matrix([[2,1,a],[1,1,0],[a,0,2]])
f=2*x*x+y*y+2*z*z+2*x*y+2*a*x*z
rhs=2*(x+y/2+a*z/2)**2+s.Rational(1,2)*(y-a*z)**2+(2-a*a)*z*z
assert s.expand(f-rhs) == 0
assert A.det() == 2-a*a
C=s.Matrix([[1,-s.Rational(1,2),-a],[0,1,a],[0,0,1]])
assert C.det() == 1 and zero_matrix(C.T*A*C-s.diag(2,s.Rational(1,2),2-a*a))
assert A.subs(a,s.sqrt(2)).rank() == 2 and A.subs(a,-s.sqrt(2)).rank() == 2
results["021"] = {"answer_correct":True,"positive_definite":"-sqrt(2)<a<sqrt(2)","boundary_rank":2,"boundary_inertia":[2,0,1],"f_equal_1_boundary_surface":"elliptic cylinder, not elliptic paraboloid","boundary_zero_vector":"(-a,a,1) for a=±sqrt(2)"}

J2=s.Matrix([[2,1],[0,2]])
wrong=s.diag(J2,2,2,3)
correct=s.diag(J2,2,3)
assert wrong.shape==(5,5) and s.trace(wrong)==11
assert correct.shape==(4,4) and s.trace(correct)==9
assert zero_matrix((correct-2*s.eye(4))**2*(correct-3*s.eye(4)))
assert not zero_matrix((correct-2*s.eye(4))*(correct-3*s.eye(4)))
assert not zero_matrix((correct-2*s.eye(4))**2)
solutions=[]
for r2 in range(2,4):
    r3=4-r2
    if 2*r2+3*r3==9: solutions.append([r2,r3])
assert solutions==[[3,1]]
results["031"]={"answer_correct":False,"written_answer_order":5,"written_answer_trace":11,"correct_answer":"diag(J2(2),2,3)","correct_order":4,"correct_trace":9,"eigenvalue_multiplicities":solutions,"unique_partition_at_2":[2,1]}

M=s.Matrix([[lam-a,1,0],[0,lam-1,1],[0,0,lam-1]])
assert M.extract([0,1],[1,2]).det()==1
det=s.factor(M.det())
assert s.expand(det-(lam-a)*(lam-1)**2)==0
T=M.copy();T.col_swap(0,1)
T[1,:]=T[1,:]-(lam-1)*T[0,:]
T[:,1]=T[:,1]-(lam-a)*T[:,0]
T.col_swap(1,2)
T[2,:]=T[2,:]-(lam-1)*T[1,:]
T[:,2]=T[:,2]+(lam-a)*(lam-1)*T[:,1]
assert zero_matrix(T-s.diag(1,1,(lam-a)*(lam-1)**2))
B=lam*s.eye(3)-M
assert B==s.Matrix([[a,-1,0],[0,1,-1],[0,0,1]])
N=B-s.eye(3)
assert N.extract([0,1],[1,2]).det()==1
assert (N.subs(a,1)**2)[0,2]==1 and zero_matrix(N.subs(a,1)**3)
results["032"]={"answer_correct":True,"invariant_factors":["1","1","(lambda-a)*(lambda-1)^2"],"elementary_factors_a_ne_1":["lambda-a","(lambda-1)^2"],"elementary_factors_a_eq_1":["(lambda-1)^3"],"Smith_row_column_steps_correct":True,"diagonalizable_for_any_a":False,"repeated_elementary_factor_for_any_a":True,"corresponding_constant_matrix":str(B)}

md=(OUT/'snapshot/EVAL-REPLACE-5-DRAFT.md').read_text(encoding='utf-8')
sections=re.split(r'^## ',md,flags=re.M)[1:]
drafts={}
for section in sections:
    pid=re.match(r"(eval-linalg-\d+)'",section).group(1)
    drafts[pid]=re.search(r'^\*\*题目\*\* (.+)$',section,re.M).group(1)
manifest=Manifest.load(ROOT/'data/manifest.json')
train=[]
for entry in manifest.entries:
    if entry.split != 'train':continue
    p=ROOT/'data'/entry.path
    for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
        if not line.strip():continue
        record=json.loads(line)
        try: signature=kp_signature(record)
        except (ValueError,TypeError,KeyError):continue
        train.append((signature,canonical_problem_text(line),f'{entry.path}:{i}',record.get('id')))
original={}
for line in (ROOT/'data/v2/eval/dataset_eval.jsonl').read_text(encoding='utf-8').splitlines():
    if line.strip():
        record=json.loads(line);original.setdefault(record['problem_id'],record)
constraint=[]
for pid,problem in drafts.items():
    record={**original[pid], 'problem':problem}
    signature=kp_signature(record);old_signature=kp_signature(original[pid])
    candidates=[(sim(problem,text),loc,ident) for sig,text,loc,ident in train if sig==signature]
    maximum=max(candidates,default=(Fraction(0),None,None),key=lambda r:r[0])
    assert signature==old_signature and maximum[0]<Fraction(2,5)
    constraint.append({'problem_id':pid,'signature':list(signature),'same_signature_train_rows':len(candidates),'max_j5':str(maximum[0]),'closest_train':maximum[1],'closest_id':maximum[2],'below_2_5':True})
results['replacement_constraints']=constraint
(OUT/'independent-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
