"""Independent exact checks on handwritten expressions, never parse/evaluate dataset strings."""
import hashlib,json
from fractions import Fraction
from math import factorial
from pathlib import Path
import sympy as s
R=Path(r'D:\Animation-Model-Training');A=R/'archives/reviews/codex-supervision/2026-10-17-first-batch-exact-math-review'
checks=[]
def check(name,condition):
 assert condition,name
 checks.append({'name':name,'result':'PASS'})
x,t,r,u,a,eps=s.symbols('x t r u a eps',positive=True)
n,N=s.symbols('n N',integer=True,positive=True)
pi=s.pi
check('unit_circle_limit_two_sided',s.limit(s.sin(x)/x,x,0)==1)
check('unit_circle_inner_area',s.det(s.Matrix([[1,0],[s.cos(x),s.sin(x)]]))/2==s.sin(x)/2)
check('unit_circle_outer_area',s.det(s.Matrix([[1,0],[1,s.tan(x)]]))/2==s.tan(x)/2)
check('unit_circle_point_B',s.simplify(s.cos(x)**2+s.sin(x)**2)==1)
q=Fraction(1)
for k in range(30):q*=Fraction(365-k,365)
qfactor=Fraction(factorial(365),factorial(335)*365**30)
check('birthday_complement_product_factorial',q==qfactor)
check('birthday_at_least_one_collision',0<1-q<1)
check('birthday_thirty_choices_last_day',365-29==336)
check('bernoulli_variance_exact',Fraction(1,2)*(1-Fraction(1,2))==Fraction(1,4))
check('bernoulli_mean_frequency_variance',s.simplify((n*s.Rational(1,4))/n**2-1/(4*n))==0)
check('chebyshev_fixed_epsilon_bound_vanishes',s.limit(1/(4*n*eps**2),n,s.oo)==0)
density1=4*t;density2=4*(1-t)
mass=s.integrate(density1,(t,0,s.Rational(1,2)))+s.integrate(density2,(t,s.Rational(1,2),1))
mean=s.integrate(t*density1,(t,0,s.Rational(1,2)))+s.integrate(t*density2,(t,s.Rational(1,2),1))
variance=s.integrate((t-s.Rational(1,2))**2*density1,(t,0,s.Rational(1,2)))+s.integrate((t-s.Rational(1,2))**2*density2,(t,s.Rational(1,2),1))
check('uniform_two_mean_triangular_density_normalized',mass==1)
check('uniform_two_mean_expectation',mean==s.Rational(1,2))
check('uniform_two_mean_variance',variance==s.Rational(1,24))
check('uniform_population_variance',s.integrate((t-s.Rational(1,2))**2,(t,0,1))==s.Rational(1,12))
check('geometric_partition_width',s.simplify(2**(1-n)-2**(-n)-2**(-n))==0)
check('geometric_partial_sum_exact',s.simplify(s.summation(2**(-n),(n,1,N))-(1-2**(-N)))==0)
check('geometric_remainder_vanishes',s.limit(2**(-N),N,s.oo)==0)
polar=2*pi*s.integrate((1-r**2)*r,(r,0,1))
substitute=pi*s.integrate(1-u,(u,0,1))
check('paraboloid_polar_integral',polar==pi/2)
check('paraboloid_independent_u_substitution',substitute==polar)
check('polar_jacobian',s.simplify(s.det(s.Matrix([[s.cos(t),-r*s.sin(t)],[s.sin(t),r*s.cos(t)]]))-r)==0)
px=a*s.cos(t);py=a*s.sin(t)
integrand=s.simplify(px*s.diff(py,t)-py*s.diff(px,t))
check('green_circle_parametric_integrand',integrand==a**2)
check('green_circle_integral',s.integrate(integrand,(t,0,2*pi))==2*pi*a**2)
xx,yy=s.symbols('xx yy',real=True)
check('green_curl',s.diff(xx,xx)-s.diff(-yy,yy)==2)
check('alternating_terms_decreasing',s.diff(1/s.sqrt(x),x)==-1/(2*x**s.Rational(3,2)))
check('alternating_terms_to_zero',s.limit(1/s.sqrt(n),n,s.oo)==0)
check('absolute_sum_divergent_lower_bound',s.integrate(x**(-s.Rational(1,2)),(x,1,N+1))==2*s.sqrt(N+1)-2)
check('absolute_sum_lower_bound_unbounded',s.limit(2*(s.sqrt(N+1)-1),N,s.oo)==s.oo)
H200=sum((Fraction(1,k*k) for k in range(1,201)),Fraction(0))
check('uniform_tail_exact_basel_sum',s.summation(1/n**2,(n,1,s.oo))==pi**2/6)
check('uniform_tail_at_x_one_positive_terms',s.simplify((s.Integer(1)**n)/n**2-1/n**2)==0)
check('uniform_tail_200_symbolic_no_float',not (pi**2/6-s.Rational(H200.numerator,H200.denominator)).has(s.Float))
F=x*s.asin(x)**2+2*s.sqrt(1-x**2)*s.asin(x)-2*x
check('rotation_volume_primitive',s.simplify(s.diff(F,x)-s.asin(x)**2)==0)
check('rotation_volume_endpoint_one',s.limit(F,x,1,dir='-')==pi**2/4-2)
check('rotation_volume_endpoint_zero',s.limit(F,x,0,dir='+')==0)
alt=s.integrate(t*t*s.cos(t),(t,0,pi/2))
check('rotation_independent_arcsin_substitution',s.simplify(alt-(pi**2/4-2))==0)
check('rotation_volume_exact_answer',s.expand(pi*alt)==pi**3/4-2*pi)
# These checks support, not replace, theorem hypotheses and handwritten proof review.
result={'schema':'exact-first-batch-proof-checks-v1','sympy_version':s.__version__,
 'checks':checks,'check_count':len(checks),'birthday_exact_collision_probability':str(1-q),
 'scope':'HANDWRITTEN_CONSTANT_EXPRESSIONS_ONLY_NO_DATASET_EVAL_NO_RENDER',
 'theorem_review':'Squeeze geometry, pairwise-disjoint half-open partition, Chebyshev under IID, CLT under IID and positive finite variance, Leibniz and M-test with tail argument are reviewed in candidate proofs.'}
(A/'exact-proof-results.json').write_text(json.dumps(result,ensure_ascii=True,indent=2),encoding='utf-8')
print(json.dumps({'checks':len(checks),'all':'PASS','sympy':s.__version__}))
