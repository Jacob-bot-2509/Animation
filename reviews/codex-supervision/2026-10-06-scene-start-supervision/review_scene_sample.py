"""Independent static small-sample review. Writes fresh candidate files only."""
from pathlib import Path
import copy,json,hashlib,re,sys,datetime
import sympy as s
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'src')]
sys.stdout.reconfigure(encoding='utf-8')
from dataset_audit import Audit,check_latex
from holdout_contract import object_sha
from publish_row_patches import sorted_sha,MATH_FIELDS
from draft_io import fingerprint
raw=lambda b:hashlib.sha256(b).hexdigest()
base=json.loads((OUT/'input-audit.json').read_text(encoding='utf-8'))
bindings={r['id']:r for r in base['record_bindings']}
salvage=json.loads((OUT/'live-scene-candidates.salvaged-v1.json').read_text(encoding='utf-8'))
ids=['draft-c37-03','draft-c12-05','draft-c51-02']
lookup={p['id']:p for p in salvage['records']}
changes=[]
# Braces make legal one-token TeX fractions comply with this project's stricter guard.
def fraction_braces(text):
    def token(t,i):
        while i<len(t) and t[i].isspace():i+=1
        if i>=len(t):raise ValueError('missing frac argument')
        if t[i]=='{':
            depth=1;j=i+1
            while j<len(t) and depth:
                if t[j]=='{':depth+=1
                elif t[j]=='}':depth-=1
                j+=1
            if depth:raise ValueError('unclosed frac')
            return t[i:j],j
        if t[i].isalnum():return '{'+t[i]+'}',i+1
        raise ValueError('unexpected frac argument')
    pos=0;out=''
    for m in re.finditer(r'\\(?:frac|dfrac|tfrac)\b|\\(?:frac|dfrac|tfrac)(?=[0-9])',text):
        if m.start()<pos:continue
        a,j=token(text,m.end());b,k=token(text,j)
        out+=text[pos:m.start()]+m.group()+a+b;pos=k
    return out+text[pos:]
def walk(obj,fn):
    if isinstance(obj,str):return fn(obj)
    if isinstance(obj,list):return [walk(v,fn) for v in obj]
    if isinstance(obj,dict):return {k:walk(v,fn) for k,v in obj.items()}
    return obj
def tex_issues(rec):
    a=Audit();check_latex(a,{'path':'candidate-static-review'}, {'record':rec,'locator':rec['id']},rec['id'])
    return a.issues
patches=[];qa=[]
for pid in ids:
    patch=copy.deepcopy(lookup[pid]);b=bindings[pid]
    source=ROOT/b['source_path'];data=source.read_bytes()
    assert raw(data)==b['source_raw_sha256']
    archived=OUT/'input-snapshot'/b['source_path']
    assert archived.read_bytes()==data
    original=json.loads(data.decode('utf-8-sig').splitlines()[b['source_line']-1])
    assert original['id']==pid and object_sha(original)==b['full_record_canonical_sha256']
    assert sorted_sha(original)==patch['expected_record_sha256']
    assert fingerprint(data)['sha256']==patch['expected_selected_sha256']
    after=copy.deepcopy(original);after.update(copy.deepcopy(patch['fields']))
    before_issues=tex_issues(after)
    spec=after['scene_spec']
    if pid=='draft-c51-02':
        def bayes_fix(t):
            t=t.replace(r'\text{第四次正面}',r'H_4')
            t=t.replace('注:独立性只用于加权平均,本题算的是参数后验与后验预测,不以独立性辨析代替后验任务。',
                        '注:给定参数的条件独立性同时支持前三次的二项似然和第四次的条件预测；据此用全概率公式对后验加权。')
            return t
        spec=walk(spec,bayes_fix)
        spec['objects'].insert(2,r'事件定义卡片：记 $H_4$ 为第四次抛掷出现正面的事件；给定 $\Theta=\theta$ 时 $P(H_4\mid\Theta=\theta,K=2)=\theta$。')
        spec['steps'][4]=spec['steps'][4].replace('计算第四次为正面的预测概率:',r'计算第四次为正面的预测概率（记该事件为 $H_4$）:')
        changes.append({'id':pid,'fixes':['CJK moved outside math','conditional independence applies to both likelihood and prediction']})
    elif pid=='draft-c12-05':
        spec['objects'].insert(4,r'几何上界证明卡片：固定 $x\in(0,1)$，令 $q=1-x^2$、$a_n=n^2q^n$、$r=(1+q)/2$，则 $q<r<1$。存在 $N=N(x)$，使 $n\ge N$ 时 $a_{n+1}/a_n\le r$，递推得 $0<a_n\le a_Nr^{n-N}\to0$。')
        spec['steps'][0]=spec['steps'][0].replace(
            '④关键点:相邻比极限 $q<1$,故 $n^2q^n\\to0$,从而 $f_n(x)\\to0$。',
            r'④关键点:令 $a_n=n^2q^n$、$r=(1+q)/2$，则 $q<r<1$。由于 $a_{n+1}/a_n\to q$，存在 $N=N(x)$，使 $n\ge N$ 时 $a_{n+1}/a_n\le r$；递推给 $0<a_n\le a_Nr^{n-N}\to0$，再乘固定的 $x$，得 $f_n(x)\to0$。此处 $N$ 可依赖于 $x$，只证明逐点收敛。')
        spec['steps'][4]=spec['steps'][4].replace(
            '若 $f_n$ 在 $[0,1]$ 上一致收敛于 $f$,则',
            r'每个 $f_n$ 是多项式，故在闭区间 $[0,1]$ 上连续且黎曼可积。一般地，若每个 $f_n$ 在 $[0,1]$ 上黎曼可积且一致收敛于 $f$，则 $f$ 亦黎曼可积，且')
        spec['objects']=[t.replace('一致收敛充分条件卡片:', '黎曼可积函数在有限区间上一致收敛的充分条件卡片:') for t in spec['objects']]
        changes.append({'id':pid,'fixes':['explicit eventual geometric bound','integrability hypothesis and finite interval stated']})
    else:
        changes.append({'id':pid,'fixes':['math and nine row-column operations independently verified; no semantic correction']})
    spec=walk(spec,lambda t:fraction_braces(t).replace(r'\int_0^1',r'\int_{0}^{1}'))
    after['scene_spec']=spec
    assert all(after[k]==original[k] for k in ('problem','solution','answer'))
    assert not re.search(r'(?<![A-Za-z0-9])\d+\.\d+',json.dumps(spec,ensure_ascii=False))
    final_issues=tex_issues(after)
    hard=[x for x in final_issues if x['severity']=='hard']
    scene_hold=[x for x in final_issues if x['field']=='scene_spec' and x['severity'] in ('hard','quarantine')]
    assert not hard,(pid,hard)
    assert not scene_hold,(pid,scene_hold)
    patch.update(fields={'scene_spec':spec},
        new_math_content_sha256=sorted_sha({k:after[k] for k in MATH_FIELDS}),
        after_scene_canonical_sha256=object_sha(spec),
        semantic_review_status='STATIC_MATH_AND_SCENE_OPERATION_PASS_ONLY',
        visual_verified=False)
    patches.append(patch)
    qa.append({'id':pid,'source_path':b['source_path'],'source_raw_sha256':b['source_raw_sha256'],
       'full_record_canonical_sha256':object_sha(original),'publisher_sorted_full_record_sha256':sorted_sha(original),
       'before_guard_issues':before_issues,'after_guard_issues':final_issues,
       'mathematics_three_fields_unchanged':True,'scene_has_no_hard_or_quarantine':True,
       'scene_has_no_decimal_literals':True,'visual_verified':False})
checks=[]
def eq(name,a,b):
    assert s.simplify(a-b)==0,(name,a,b)
    checks.append({'check':name,'actual':str(a),'expected':str(b),'passed':True})
P=s.Matrix([[1,1,1],[0,0,1],[1,-1,-1]]);GE=s.diag(1,2,1);xi=s.Matrix([2,-1,2]);T=s.Matrix([[3,2],[2,1]])
G=s.Matrix([[2,0,0],[0,2,2],[0,2,4]])
eq('P determinant',P.det(),2)
for i in range(3):eq('coordinate equation '+str(i),(P*xi)[i],s.Matrix([3,2,1])[i])
for i in range(3):
    for j in range(3):eq('Gram row '+str(i+1)+' col '+str(j+1),(P.T*GE*P)[i,j],G[i,j])
eq('Gram norm squared',(xi.T*G*xi)[0],18);eq('trace norm squared',s.trace(T*T),18)
n=s.symbols('n',integer=True,positive=True);u=s.symbols('u',real=True)
eq('exact integral after substitution',n*n*s.integrate(u**n,(u,0,1))/2,n*n/(2*(n+1)))
eq('lower bound remainder',n*n/(2*(n+1))-n/4,n*(n-1)/(4*(n+1)))
assert (n*(n-1)/(4*(n+1))).is_nonnegative is True
q=s.symbols('q',positive=True);r=(1+q)/2
eq('geometric margin r-q',r-q,(1-q)/2);eq('geometric margin 1-r',1-r,(1-q)/2)
low=s.Rational(1,4);high=s.Rational(3,4);priorlo=s.Rational(2,3);priorhi=s.Rational(1,3)
liklo=3*low**2*(1-low);likhi=3*high**2*(1-high);evidence=priorlo*liklo+priorhi*likhi
eq('low likelihood',liklo,s.Rational(9,64));eq('high likelihood',likhi,s.Rational(27,64))
eq('evidence',evidence,s.Rational(15,64));postlo=priorlo*liklo/evidence;posthi=priorhi*likhi/evidence
eq('low posterior',postlo,s.Rational(2,5));eq('high posterior',posthi,s.Rational(3,5))
eq('posterior sum',postlo+posthi,1);eq('predictive probability',postlo*low+posthi*high,s.Rational(11,20))
result={'schema':'scene-small-sample-static-qa-v1','checked_at':datetime.datetime.now().astimezone().isoformat(),
        'scope':ids,'symbolic_checks':checks,'passed_checks':len(checks),'records':qa,'corrections':changes,
        'input_snapshot_raw_sha256':raw((OUT/'live-scene-candidates.salvaged-v1.json').read_bytes()),
        'visual_verified':False,'publisher_executed':False,'selector_updated':False,
        'pending':'writer stop, immutable original input restoration, remaining candidates review, real visual verification'}
def write(name,obj):
    with (OUT/name).open('x',encoding='utf-8') as f:f.write(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
write('scene-sample-codex-corrections-v1.pending.json',
      {'schema':'scene-small-sample-patches-v1','status':'STATIC_MATH_PASS_NOT_PUBLISHED_NOT_VISUALLY_VERIFIED',
       'source_hash_algorithms':{'publisher_sorted_sha':'sha256-json-ensure_ascii_false-sort_keys_true-default_spaces',
         'canonical_object_sha':'sha256-json-ensure_ascii_false-sort_keys_true-compact'},
       'records':patches})
write('scene-sample-independent-qa.json',result)
print(json.dumps({'static_checked':ids,'symbolic_checks':len(checks),
     'before_CJK_issues':sum(x['code']=='L002' for r in qa for x in r['before_guard_issues']),
     'after_scene_blockers':0,'visual_verified':False},ensure_ascii=False))
