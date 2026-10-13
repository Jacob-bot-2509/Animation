from pathlib import Path
import json,copy,hashlib,sys
import sympy as s
from fractions import Fraction
R=Path(r'D:\Animation-Model-Training');O=R/'reviews/codex-supervision/2026-10-06-scene-repair-takeover'
P=R/'reviews/codex-supervision/2026-10-06-scene-start-supervision'
sys.path[:0]=[str(R/'tools')];sys.stdout.reconfigure(encoding='utf-8')
from holdout_contract import object_sha,raw_sha
# Extend the actual prior exact-check program, preserving its checks as scoped formulas.
code=(P/'verify_exact_math.py').read_text(encoding='utf-8')
prefix=code.split('result={"status"')[0]
ns={};exec(compile(prefix,'scoped_exact_formulas','exec'),ns)
checks=ns['checks'];eq=ns['eq']
a,b,d,y1,y2=s.symbols('a b d y1 y2',real=True)
A=s.Matrix([[a,b],[b,d]]);y=s.Matrix([y1,y2])
eq('correct_inverse_quadratic_chain',((A*y).T*A.inv()*(A*y))[0],(y.T*A*y)[0])
A0=s.Matrix([[2,1],[1,2]]);B0=s.diag(1,3);v=s.Matrix([1,0])
assert (v.T*A0*v)[0]==2 and (v.T*s.eye(2)*v)[0]==1
checks.append({'name':'false_old_middle_equality_counterexample','left':'2','wrong_middle':'1','exact':True})
for i in range(2):
 for j in range(2):eq('AB_row_'+str(i+1)+'_column_'+str(j+1),(A0*B0)[i,j],s.Matrix([[2,3],[1,6]])[i,j])
assert set(A0.eigenvals())=={1,3} and set(B0.eigenvals())=={1,3}
checks.append({'name':'positive_symmetric_counterexample_factors','exact':True})
assert A0*B0!=(A0*B0).T
checks.append({'name':'positive_matrix_product_not_symmetric','exact':True})
assert Fraction(99,100)**299<=Fraction(1,20)<Fraction(99,100)**298
assert Fraction(19,20)**59<=Fraction(1,20)<Fraction(19,20)**58
checks.append({'name':'FPR_iid_exact_min_zero_error_n','n':299,'exact':True})
checks.append({'name':'recall_iid_exact_min_all_success_n','n':59,'exact':True})
receipt=json.loads((O/'math-correction-receipt.json').read_text(encoding='utf-8'))
result={'status':'EXACT_FORMULAS_AND_CONCRETE_DEFECT_CHECKED','check_count':len(checks),'checks':checks,
 'math_receipt_raw_sha256':raw_sha((O/'math-correction-receipt.json').read_bytes()),
 'corrected_record_canonical_sha256':{v['id']:v['after_record_canonical_sha256'] for v in receipt['corrections']},
 'inverse_identity_condition':'a*d-b**2 != 0; symmetric A',
 'scope':'Specific formulas, nine reviewed corrections and explicit proof defect; not full 53-scene or independent calibration acceptance'}
with (O/'exact-math-verification.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
original=json.loads((P/'core-families.codex-review-v2.json').read_text(encoding='utf-8'))
original['schema']='train-core-families-corrected-v2';original['status']='CORE_CENSUS_CORRECTED_FOR_BOUND_ORIGINAL_47_MATH_ACCEPTANCE_SEPARATE'
original['math_correction_version']=(O/'math-corrected-v1').relative_to(R).as_posix()
original['notes']='Original bound 47-record core census is 46 tasks. New math version is inactive and must receive its own review/density receipts.'
target=R/'reviews/2026-10-06-core-families/core-families.corrected-v2.json'
with target.open('x',encoding='utf-8') as f:json.dump(original,f,ensure_ascii=False,indent=2);f.write('\n')
hsource=P/'holdout-design.codex-revision-v2.md'
htarget=R/'reviews/2026-10-06-holdout-design/holdout-design.corrected-v2.md'
with htarget.open('xb') as f:f.write(hsource.read_bytes())
for name,p in [('core-families.corrected-v2.json',target),('holdout-design.corrected-v2.md',htarget)]:
 with (O/name).open('xb') as f:f.write(p.read_bytes())
findings=json.loads((P/'holdout-independent-findings.json').read_text(encoding='utf-8'))
findings['revised_design_path']=htarget.relative_to(R).as_posix()
findings['revised_design_raw_sha256']=raw_sha(htarget.read_bytes())
findings['status']='DESIGN_CORRECTED_EXECUTION_BLOCKED_BY_NO_UNEXPOSED_POPULATION'
findings['calibration_eligible']=False
with (O/'holdout-readiness.corrected-v2.json').open('x',encoding='utf-8') as f:json.dump(findings,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'exact_checks':len(checks),'math_versions_written':9,'core_task_count':46,'independent_holdout_eligible_members':0}))
