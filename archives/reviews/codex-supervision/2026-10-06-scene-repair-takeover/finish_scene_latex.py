from pathlib import Path
import ast,copy,json,re,sys
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path[:0]=[str(R/'tools')];sys.stdout.reconfigure(encoding='utf-8')
from scene_sweep_protocol import verify_inputs,sorted_sha,MATH_FIELDS
from dataset_audit import Audit,check_latex
from holdout_contract import object_sha,raw_sha
tree=ast.parse((O/'materialize_exact_math.py').read_text(encoding='utf-8'))
helpers=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'walk','frac_braces'}]
code=ast.unparse(ast.Module(body=helpers,type_ignores=[]))
assert 'return (t[i:j], j)' in code
code=code.replace('return (t[i:j], j)',"return ('{'+frac_braces(t[i+1:j-1])+'}',j)")
exec(compile(code,'recursive_fraction_helpers','exec'))
_,items=verify_inputs(O/'inputs-v2',root=R);byid={r['record']['id']:r['record'] for r in items}
packet=json.loads((O/'scene-candidates-merged-v3.pending.json').read_text(encoding='utf-8'))
qa=[]
for patch in packet['records']:
 spec=walk(patch['fields']['scene_spec'],frac_braces);patch['fields']['scene_spec']=spec
 row=copy.deepcopy(byid[patch['id']]);row.update(patch['fields'])
 patch['new_math_content_sha256']=sorted_sha({k:row[k] for k in MATH_FIELDS})
 a=Audit();check_latex(a,{'path':'new v4 candidate'},{'record':row,'locator':patch['id']},patch['id'])
 bad=[x for x in a.issues if x['field']=='scene_spec' and x['severity'] in ('hard','quarantine')]
 assert not bad,(patch['id'],bad)
 assert not re.search(r'\d+\.\d+',json.dumps(spec,ensure_ascii=False))
 qa.append({'id':patch['id'],'scene_guard_blockers':0,'math_three_fields_unchanged':True,'decimal_literals':0})
packet['schema']='source-bound-scene-candidate-patches-v4'
packet['status']='STATIC_LATEX_PASS_ONLY_PARTIAL_MATH_REVIEW_UNSELECTED'
packet['normalization']='Nested fraction arguments fully braced; no values or math-three fields changed.'
with (O/'scene-candidates-corrected-v4.json').open('x',encoding='utf-8') as f:json.dump(packet,f,ensure_ascii=False,indent=2);f.write('\n')
with (O/'scene-candidates-corrected-v4-latex-qa.json').open('x',encoding='utf-8') as f:json.dump({'records':qa,'scene_blockers':0,'full_math_review_complete':False},f,indent=2);f.write('\n')
print(json.dumps({'corrected_scene_candidates':len(qa),'scene_guard_blockers':0,'new_decimals':0,'full_math_acceptance':False}))
