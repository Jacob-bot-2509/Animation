from pathlib import Path
import sympy as s,json,hashlib,itertools
from fractions import Fraction as F
ROOT=Path(r'D:/Animation-Model-Training');OUT=Path(__file__).resolve().parent;checks=[]
def ck(name,left,right):
 diff=s.simplify(left-right);assert diff==0,(name,diff);checks.append({'name':name,'left':str(left),'right':str(right),'residual':str(diff),'pass':True})
x,z,u,h=s.symbols('x z u h',real=True)
ck('c52_density_integrates_to_one',s.integrate(s.Rational(1,2),(z,0,1))+s.integrate(z-1,(z,1,2)),1)
ck('c52_CDF_lower_derivative',s.diff(z/2,z),s.Rational(1,2));ck('c52_CDF_upper_derivative',s.diff(s.Rational(1,2)+(z-1)**2/2,z),z-1)
ck('c52_CDF_branches_at_one',s.Rational(1,2)+(1-1)**2/2,s.Rational(1,2));ck('c52_CDF_at_two',s.Rational(1,2)+(2-1)**2/2,1)
ck('c52_inverse_lower',2*u/2,u);ck('c52_inverse_upper',s.Rational(1,2)+s.sqrt(2*u-1)**2/2,u)
p=s.Rational(1,1000);sens=s.Rational(99,100);false=s.Rational(1,100)
post1=p*sens/(p*sens+(1-p)*false);post2=p*sens**2/(p*sens**2+(1-p)*false**2)
ck('c51_single_posterior',post1,s.Rational(11,122));ck('c51_double_posterior',post2,s.Rational(363,400));ck('c51_posterior_difference',post2-post1,s.Rational(19943,24400))
ck('c46_A_area',s.Rational(1,2)**2,s.Rational(1,4));ck('c46_B_area',s.integrate(x,(x,s.Rational(1,2),1)),s.Rational(3,8));ck('c46_total_area',s.Rational(1,4)+2*s.Rational(3,8),1)
ck('c09_outside_low_annulus',(2-h)**2-h**2,4*(1-h));ck('c09_outside_high_annulus',h**2-(h-2)**2,4*(h-1));ck('c09_inner_endpoint_zero',s.pi*(1+abs(0-1))**2,4*s.pi);ck('c09_inner_endpoint_two',s.pi*(1+abs(2-1))**2,4*s.pi);ck('c09_minimum_axis',s.pi*(1+abs(1-1))**2,s.pi)
omega=list(itertools.product('HT',repeat=2));A={w for w in omega if w[0]=='H'};B={w for w in omega if w[1]=='H'};C={w for w in omega if w[0]==w[1]}
for i,e in enumerate((A,B,C)):ck('c45_marginal_'+str(i),s.Rational(len(e),4),s.Rational(1,2))
for i,(e,f) in enumerate(((A,B),(A,C),(B,C))):ck('c45_pair_'+str(i),s.Rational(len(e&f),4),s.Rational(1,4))
ck('c45_triple',s.Rational(len(A&B&C),4),s.Rational(1,4));assert s.Rational(len(A&B&C),4)!=s.Rational(1,8)
t=s.symbols('t',real=True);ck('c07_leaf_area',s.integrate(2*s.sin(3*t)**2,(t,0,s.pi/3)),s.pi/3)
a,b=s.symbols('a b');ck('c01_continuity_residual',(1+a)-(1+b),a-b);ck('c01_smooth_tangent_at_one',(2*x+1).subs(x,1),3);ck('c01_left_derivative_at_one',s.diff(x**2+2,x).subs(x,1),2)
n=s.Matrix(s.symbols('n1:4',real=True));d=s.Matrix(s.symbols('d1:4',real=True));point=s.Matrix(s.symbols('p1:4',real=True));c=s.symbols('c',real=True);nd=n.dot(d);nn=n.dot(n)
dperp=nd*n/nn;dpar=d-dperp
ck('c15_parallel_normal_orthogonality',n.dot(dpar),0);ck('c15_projection_orthogonality',dperp.dot(dpar),0);ck('c15_normal_projection_squared_length',dperp.dot(dperp),nd**2/nn);ck('c15_intersection_lies_on_plane',n.dot(point+(c-n.dot(point))*d/nd),c)
J=s.Matrix([[0,1],[1,0]]);Q=s.Matrix([[1,1],[1,-1]])/s.sqrt(2);aa,bb=s.symbols('a b');T=aa*s.eye(2)+bb*J
for i,v in enumerate(Q.T*Q-s.eye(2)):ck('leakage_common_basis_orthogonal_'+str(i),v,0)
for i,v in enumerate(Q.T*T*Q-s.diag(aa+bb,aa-bb)):ck('leakage_common_diagonalization_'+str(i),v,0)
proofs={'c52':'分布函数单调连续，反函数各在其声明区间使用；密度端点值不改变积分概率。','c46':'三个Voronoi区域由平方距离差确定；三条平局线面积零。','c09':'内侧圆盘体积至少π，等号仅h=1；外侧|h-1|>1，体积大于4π。','c15':'d,n非零。投影为零给π/2；d·n=0时由n·p=c区分包含和平行；d×n=0保证n·d非零并给唯一交点。','production_pairs':'两题对均使用T=aI+bJ与固定正交基Q；训练的几何伸缩依赖同一谱分解核心。用户把仅换数据的同核心训练/留出题视为泄漏。'}
data={'status':'EXACT_EQUALITIES_VERIFIED_GENERAL_PROOFS_REVIEWED','exact_checks':len(checks),'passed':len(checks),'checks':checks,'proof_notes':proofs,'uses_numeric_approximations':False,'render_verified':False,'patched_c15_fields_sha256':hashlib.sha256((OUT/'ready-field-patches.json').read_bytes()).hexdigest()}
(OUT/'exact-notation-reverification.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('EXACT_CHECKS',len(checks),'PASS')
