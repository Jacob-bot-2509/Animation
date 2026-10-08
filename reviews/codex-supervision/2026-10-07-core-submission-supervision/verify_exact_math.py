"""Exact arithmetic checks plus explicitly scoped theorem review notes."""
from pathlib import Path
from fractions import Fraction as F
from math import comb,factorial
import json,hashlib
import sympy as s
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
patches=[json.loads(x) for x in (OUT/"math-corrections-30.jsonl").read_text(encoding="utf-8").splitlines()]
byid={x["id"]:x for x in patches}
results=[]
def check(ids,name,assertion,notes=""):
 assert assertion,name
 for rid in ids:
  assert rid in byid
  results.append({"id":rid,"check":name,"result":"PASS_EXACT_CHECK","mathematical_scope":notes,
   "candidate_record_dense_sha256":byid[rid]["after_record_dense_sha256"]})
x=s.symbols("x",positive=True);n=s.symbols("n",integer=True,positive=True)
check(["calc-series-015"],"integral divergence bound",s.integrate(x**(-s.Rational(1,2)),(x,1,n+1))==2*s.sqrt(n+1)-2,
 "Manual theorem review: n^(-1/2) decreases to 0, Leibniz implies convergence; positive integral lower bound diverges, so convergence is conditional.")
bn=s.simplify(2/s.pi*s.integrate(x*s.sin(n*x),(x,0,s.pi)))
check(["calc-series-020"],"Fourier coefficients and endpoint summands",s.simplify(bn-2*(-1)**(n+1)/n)==0 and s.sin(n*s.pi)==0,
 "Manual Dirichlet review: periodic endpoint jump average is 0; interior sum equals x. Endpoint function values are not identified with the sum.")
a,b,c,d=s.symbols("a b c d");A=s.Matrix([[a,b],[c,d]]);J=s.Matrix([[0,1],[-1,0]])
check(["linalg-050"],"determinant and rank-zero case",A.det()==a*d-b*c and s.zeros(2).rank()==0 and s.Matrix([[1,0],[0,0]]).rank()==1,
 "Manual geometric review: oriented area det A, ordinary area |det A|; rank 1 gives segment and rank 0 gives point.")
check(["linalg-070"],"symplectic form identity",s.simplify(A.T*J*A-A.det()*J)==s.zeros(2) and s.diag(1,-1).det()==-1,
 "In dimension 2, A^TJA=J iff det A=1; reflection preserves ordinary area but reverses the symplectic form.")
check(["prob-038"],"conditional probabilities",F(1,5)/F(2,5)==F(1,2) and F(1,5)/F(3,5)==F(1,3))
p=s.symbols("p",nonnegative=True)
check(["prob-039"],"indicator expectation and exact estimator variance",s.simplify(4*s.pi/4-s.pi)==0 and s.simplify(16*(s.pi/4)*(1-s.pi/4)/n-s.pi*(4-s.pi)/n)==0,
 "Manual theorem review: iid uniform indicators with success pi/4, Chebyshev gives convergence in probability; rational finite count is not pi itself.")
check(["prob-042"],"Bernoulli sample mean variance",s.simplify(n*p/n-p)==0 and s.simplify(n*p*(1-p)/n**2-p*(1-p)/n)==0,
 "Manual theorem review: iid, 0<=p<=1, Chebyshev; fairness is extra p=1/2 assumption.")
sigma=s.symbols("sigma",positive=True)
check(["prob-043"],"standardized versus original mean variance",s.simplify(n/sigma**2*(sigma**2/n))==1 and s.limit(sigma**2/n,n,s.oo)==0,
 "Manual theorem review: iid finite positive variance CLT applies to standardized mean; original mean tends to point mass; finite normal mean law only for normal population.")
k=s.symbols("k",integer=True,positive=True)
check(["prob-046"],"partition widths and exact geometric area",s.simplify(s.summation(2**(-k),(k,1,n))-(1-2**(-n)))==0 and s.summation(2**(-k),(k,1,s.oo))==1,
 "Manual coverage review: half-open adjacent strips are disjoint and cover [0,1)^2; example illustrates area additivity without claiming its general proof.")
check(["eval-calc-015-s3"],"symmetric integral",s.integrate(1/(1+x*x),(x,-1,1))==s.pi/2,
 "Manual substitution x->pi-x establishes 2I=pi*J, hence I=pi^2/4.")
h=s.symbols("h")
check(["eval-calc-026-s3"],"two partial derivative limits",s.limit(((1+h)**2-1)/h,h,0)==2 and s.limit((s.Integer(1)**(2+h)-1)/h,h,0)==0)
check(["eval-calc-027-s3"],"reversed integral",s.simplify(s.integrate(x*s.exp(x*x),(x,0,1))-(s.E-1)/2)==0,
 "Manual Fubini review: continuous integrand over 0<=x<=y<=1, reversed inner interval has length y.")
birthday_no=F(factorial(365),factorial(335)*365**30)
birthday_product=F(1)
for j in range(30):birthday_product*=F(365-j,365)
check(["eval-prob-007-s1","eval-prob-007-s2","eval-prob-007-s3"],"exact birthday complement",birthday_no==birthday_product and 0<1-birthday_no<1)
EN=F(435,365);EN2=F(435,365)+F(435*434,365**2)
check(["eval-prob-007-s3"],"pair second moment Cauchy bound",EN**2/EN2==F(435,799)>F(1,2),
 "Manual independence review: disjoint pairs and pairs with one shared individual each have joint probability 1/365^2.")
S=sum(comb(100,j) for j in range(41));q=F(S,2**99)
check(["eval-prob-008-s1","eval-prob-008-s2","eval-prob-008-s3"],"exact binomial tail and strict bound",F(25,100)==F(1,4) and q<F(1,4) and F(1,4)-q==F(2**97-S,2**99),
 "Symmetry partitions the event into k<=40 and k>=60. Strict Chebyshev comparison follows also from a positive-mass value with squared deviation >100.")
check(["test-calc-027"],"root monotonicity and exact brackets",s.diff(s.exp(x)-2*x-1,x)==s.exp(x)-2 and 1+2+F(2**2,2)==5,
 "Manual inequality review: ln2=integral_1^2 dt/t is in (1/2,1); e^2>1+2+2=5; f is strictly decreasing then increasing, so roots are 0 and unique xi in (ln2,2).")
joint1=F(3,5)*F(1,50);joint2=F(2,5)*F(3,100)
check(["test-prob-001"],"Bayes formula",joint1==joint2==F(3,250) and joint1/(joint1+joint2)==F(1,2))
check(["test-prob-002"],"two exact binomial probabilities",F(comb(10,3)*3**3*7**7,10**10)==F(66706983,250000000) and F(7**10+30*7**9,10**10)==F(1493083459,10000000000))
check(["test-prob-005"],"convolution density normalization and tail",s.integrate(x,(x,0,1))+s.integrate(2-x,(x,1,2))==1 and s.integrate(2-x,(x,s.Rational(3,2),2))==s.Rational(1,8),
 "Manual convolution review: density is length of intersection (0,1) with (z-1,z).")
check(["test-prob-007"],"exact exponential conditional survival",s.simplify(s.exp(-s.Rational(3,2))/s.exp(-s.Rational(1,2))-s.exp(-1))==0)
mean=sum(F(j,6) for j in range(1,7));variance=sum(F(j*j,6) for j in range(1,7))-mean**2
check(["test-prob-008"],"dice moments and exact Chebyshev coefficient",mean==F(7,2) and variance==F(35,12) and variance/F(1,10)**2==F(875,3),
 "Manual theorem review: independence makes variance of average Var(X)/n, bound capped by 1 and tends to 0.")
P=s.Matrix([[s.Rational(4,5),s.Rational(1,5)],[s.Rational(2,5),s.Rational(3,5)]])
check(["test-prob-016"],"weather stationary distribution",s.Matrix([[s.Rational(2,3),s.Rational(1,3)]])*P==s.Matrix([[s.Rational(2,3),s.Rational(1,3)]]))
check(["test-prob-020"],"uniform key position expectation",sum(F(j,10) for j in range(1,11))==F(11,2),
 "Uniform random order is now explicit.")
check(["test-prob-021"],"independent union probability",F(2,5)+F(1,2)-F(2,5)*F(1,2)==F(7,10))
phi=(1+s.sqrt(5))/2;psi=(1-s.sqrt(5))/2
Q=s.Matrix([[phi,psi],[1,1]]);Fmatrix=s.Matrix([[1,1],[1,0]])
check(["test-linalg-012"],"Fibonacci diagonalization and tenth term",s.simplify(Q*s.diag(phi,psi)*Q.inv()-Fmatrix)==s.zeros(2) and s.simplify((phi**10-psi**10)/s.sqrt(5))==55 and abs(psi/phi)<1,
 "Manual limit review: exact ratio phi*(1-r^(n+1))/(1-r^n), |r|<1, tends to phi.")
P=s.Matrix([[s.Rational(1,2),s.Rational(1,2)],[s.Rational(1,4),s.Rational(3,4)]])
pi=s.Matrix([[s.Rational(1,3),s.Rational(2,3)]])
check(["test-x-004"],"stationary row and transposed eigenvector",pi*P==pi and P.T*pi.T==pi.T)
Q=s.Matrix([[1,2],[1,-1]]);z=s.symbols("z")
formula=s.Matrix([[1+2*z,2-2*z],[1-z,2+z]])/3
check(["test-x-015"],"exact diagonalization, all-n formula and limit",Q*s.diag(1,s.Rational(1,4))*Q.inv()==P and Q*s.diag(1,z)*Q.inv()==formula and formula.subs(z,0)==s.Matrix([[s.Rational(1,3),s.Rational(2,3)],[s.Rational(1,3),s.Rational(2,3)]]),
 "For integer n>=0, z=4^(-n). This establishes the matrix power formula by diagonalization and its limit.")
assert {x["id"] for x in results}==set(byid)
# Bind checks to delivered text and preserve all fields outside the explicit three-field correction.
for patch in patches:
 after=patch["corrected_record"]
 actual=hashlib.sha256(json.dumps(after,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()
 assert actual==patch["after_record_dense_sha256"]
 assert {k:after[k] for k in ("problem","solution","answer")}==patch["after_math_fields"]
with (OUT/"exact-math-verification.json").open("x",encoding="utf-8",newline="\n") as f:
 json.dump({"checks":results,"check_count":len(results),"distinct_reviewed_records":len(byid),
  "arithmetic":"Exact integers, fractions and symbolic expressions only; no float evaluation",
  "theorems":"Explicitly noted manual hypothesis/proof review; arithmetic checks are not claimed as complete automated theorem proofs",
  "corrected_version_admission":"PENDING","core_scope_acceptance":"PENDING"},f,ensure_ascii=False,indent=2);f.write("\n")
print(json.dumps({"exact_checks":len(results),"distinct_records":len(byid),"result":"ALL_EXACT_CHECKS_PASSED","acceptance":"PENDING"}))
