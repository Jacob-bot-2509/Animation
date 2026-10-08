"""Exact symbolic verification for scoped core decisions and repair formulas."""
from pathlib import Path
import json
import sympy as s
x,a,b,c,d=s.symbols("x a b c d", real=True)
alpha=s.symbols("alpha",positive=True)
n,N,k=s.symbols("n N k",integer=True,positive=True)
p=s.symbols("p",positive=True)
checks=[]
def eq(name,actual,expected):
    assert s.simplify(actual-expected)==0,(name,actual,expected)
    checks.append({"name":name,"actual":s.sstr(s.simplify(actual)),"expected":s.sstr(expected),"exact":True})
eq("area007",s.integrate(x+2-x*x,(x,-1,2)),s.Rational(9,2))
eq("area010_piecewise",s.integrate(s.log(x),(x,1,s.E))+s.integrate(-x+s.E+1,(x,s.E,s.E+1)),s.Rational(3,2))
eq("area011_absolute_piecewise",2*(s.integrate(x*x,(x,0,1))+s.integrate(2-x*x,(x,1,s.sqrt(2)))),8*(s.sqrt(2)-1)/3)
eq("area013_by_parts",s.integrate(x*s.exp(-x),(x,0,1)),1-2/s.E)
eq("improper002",s.integrate(1/(1+x*x),(x,0,s.oo)),s.pi/2)
eq("improper003_parameter",s.integrate(s.exp(-alpha*x),(x,0,s.oo)),1/alpha)
eq("conditional_A_given_B",s.Rational(1,5)/s.Rational(2,5),s.Rational(1,2))
eq("conditional_B_given_A",s.Rational(1,5)/s.Rational(3,5),s.Rational(1,3))
eq("pi_estimator_mean",(4/n)*(n*s.pi/4),s.pi)
eq("pi_estimator_variance",(4/n)**2*n*(s.pi/4)*(1-s.pi/4),s.pi*(4-s.pi)/n)
eq("bernoulli_frequency_variance",n*p*(1-p)/n**2,p*(1-p)/n)
eq("uniform_example_mean",s.integrate(x,(x,0,1)),s.Rational(1,2))
eq("uniform_example_variance",s.integrate(x*x,(x,0,1))-s.Rational(1,2)**2,s.Rational(1,12))
eq("fourier_sine_coefficient",2/s.pi*s.integrate(x*s.sin(n*x),(x,0,s.pi)),2*(-1)**(n+1)/n)
eq("fourier_endpoint_terms",s.sin(n*s.pi),0)
eq("absolute_series_integral_bound",s.integrate(x**(-s.Rational(1,2)),(x,1,N+1)),2*(s.sqrt(N+1)-1))
eq("dyadic_rectangle_width",(1-2**(-k))-(1-2**(-(k-1))),2**(-k))
eq("dyadic_partial_area",s.summation(2**(-k),(k,1,N)),1-2**(-N))
A=s.Matrix([[a,b],[c,d]]);J=s.Matrix([[0,1],[-1,0]])
assert s.simplify(A.T*J*A-A.det()*J)==s.zeros(2)
checks.append({"name":"signed_symplectic_area_identity","exact":True})
assert s.zeros(2).rank()==0 and s.Matrix([[1,2],[2,4]]).rank()==1
checks.append({"name":"zero_determinant_rank0_and_rank1","exact":True})
P=s.Matrix([[0,1],[1,0]]);H=s.Matrix([[1,3],[0,1]]);V=s.Matrix([[1,0],[3,1]])
assert P*H*P==V
checks.append({"name":"shear_axis_swap_equivalence","exact":True})
eq("specific_3d_determinant",s.Matrix([[1,2,0],[0,1,3],[2,1,1]]).det(),10)
result={"status":"EXACT_SYMBOLIC_CHECKS_PASSED","check_count":len(checks),"checks":checks,
        "scope":"Exact formulas only; no live scene, global leakage, CLT empirical fit or training certification"}
out=Path(__file__).resolve().parent
with (out/"exact-math-verification.json").open("x",encoding="utf-8") as f:f.write(json.dumps(result,indent=2)+"\n")
print(json.dumps({"status":result["status"],"check_count":len(checks)}))
