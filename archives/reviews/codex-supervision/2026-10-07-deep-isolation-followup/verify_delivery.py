"""Read-only audit of frozen mathematical delivery, local pair and real-formula evidence."""
from pathlib import Path
import argparse,ast,hashlib,importlib.util,json,sys

ROOT=Path(__file__).resolve().parents[3]
REVIEW=Path(__file__).resolve().parent
CORE=REVIEW/'effective-core-v3'
PARENT=ROOT/'reviews/codex-supervision/2026-10-07-semantic-signature-supervision'
OLDER=ROOT/'reviews/codex-supervision/2026-10-07-continuous-math-review/current-core'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def rows(path):return [json.loads(x) for x in path.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def frozen(directory,expected):
    manifest=directory/'delivery-manifest.json'
    assert digest(manifest)==expected,('Manifest mismatch',directory)
    entries=read(manifest)['artifacts']
    assert len(entries)==len({x['path'] for x in entries})
    for e in entries:
        relative=Path(e['path'])
        assert not relative.is_absolute() and '..' not in relative.parts
        p=directory/relative
        assert p.is_file() and not p.is_symlink() and not getattr(p.lstat(),'st_file_attributes',0)&0x400
        assert digest(p)==e['sha256'] and p.stat().st_size==e['bytes'],p
    return len(entries)
def core_module(name,path,directory):
    m=module(name,path);m.ROOT=ROOT;m.CORE=directory
    return m

def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);a=p.parse_args()
    outer=frozen(REVIEW,a.manifest_sha256)
    parent=frozen(PARENT,'4e2ae6741592386d93be6cf01cbe8cabb13e3fd002d99b0617675d37a4ea24a5')
    older=frozen(OLDER,'972bd216b713bec7c48896e8f144d999dd6385b8c0e3e00a4c0116dfd1bbca22')
    meta=read(REVIEW/'v3-core-freeze.json')
    inner=frozen(CORE,meta['core_manifest_sha256'])
    old=core_module('old_core_snapshot',REVIEW/'bound-before-tools/tools/core_signatures.py',PARENT/'effective-core-v2')
    current=core_module('current_core_snapshot',REVIEW/'final-source-snapshot/tools/core_signatures.py',CORE)
    old_refs=old.load_record_bindings();old_by={b['id']:b for b in old_refs}
    refs=current.load_record_bindings();by={b['id']:b for b in refs}
    sigpath=REVIEW/'revised-complete-signatures-v3.jsonl'
    assert digest(sigpath)==meta['signatures_sha256']
    sigs,_=current.read_signature_inputs([sigpath],by)
    assert len(sigs)==761 and {s['id'] for s in sigs}==set(by)
    changed={rid for rid in by if by[rid]['record_sha256']!=old_by[rid]['record_sha256']}
    assert changed=={'linalg-051','draft-c36-03','draft-c30-01','draft-c37-05'}
    assert len(by)-len(changed)==757
    old_sigs={s['id']:s for s in rows(PARENT/'revised-complete-signatures-v2.jsonl')}
    assert sum(s!=old_sigs[s['id']] for s in sigs)==4
    for s in sigs:
        if s['id'] not in changed:assert s==old_sigs[s['id']]
    for item in read(CORE/'mathematical-before-after.json'):
        rid=item['id']
        assert current.dense(item['after'])==by[rid]['record_sha256']
        assert old.dense(item['before'])==old_by[rid]['record_sha256']
    proof=read(CORE/'exact-proof.json')
    assert proof['symbolic_checks']==46 and len(proof['general_proof_obligations'])==6
    assert all(x['result']=='PASS' for x in proof['checks'])
    assert proof['verifier_sha256']==digest(REVIEW/'prove_four_exact.py')==digest(CORE/'proof-source.snapshot.py')
    for rid,b in proof['version_bindings'].items():
        for k in ['record_sha256','math_sha256','source_sha256','path','source_line']:assert b[k]==by[rid][k]
    # Recompute both bounded candidate channels using the exact archived code and actual frozen sources.
    for label,m,folder,snapshot,expected_count in [
        ('before',old,'bound-before-v2','bound-before-tools',12),
        ('after',current,'bound-after-v3','final-source-snapshot',6)]:
        sys.modules['core_signatures']=m
        d=module('deep_'+label,REVIEW/snapshot/'tools/deep_isolation_candidates.py')
        report=read(REVIEW/folder/'deep-candidates.json')
        input_path=ROOT/report['input_bindings'][0]['path']
        population,inputs,records=d.population(input_path)
        computed=d.build_report(population,inputs,records)
        computed['generator_sha256']=digest(REVIEW/snapshot/'tools/deep_isolation_candidates.py')
        assert report==computed
        assert report['candidate_count']==expected_count and report['family_pairs_total']==1131
        assert report['all_record_pairs']==139950 and report['outside_family_pairs_not_screened']==138819
        assert report['filter']['steps_jaccard_minimum']=='1/4' and report['nonflagged_semantic_verdict']=='NOT_REVIEWED'
        for c in report['candidates']:assert isinstance(c['steps_jaccard'],str)
    before=read(REVIEW/'independent-before-disposed-v2/deep-candidates-disposed.json')
    after=read(REVIEW/'independent-after-disposed-v3/deep-candidates-disposed.json')
    assert before['flagged_pairs']==12 and before['same_core']==6 and before['different_core']==6
    assert after['flagged_pairs']==6 and after['same_core']==0 and after['different_core']==6
    assert all(r['disposition'] in ('SAME_CORE','DIFFERENT_CORE') and r['pairwise_reason'].strip() for r in before['rows'])
    repaired=read(REVIEW/'repaired-pair-dispositions-v3.json')
    assert len(repaired['pairs'])==12 and repaired['core_manifest_sha256']==meta['core_manifest_sha256']
    for r in repaired['pairs']:
        assert r['train_id'] in changed
        assert r['train_record_sha256']==by[r['train_id']]['record_sha256']
        assert r['eval_record_sha256']==by[r['eval_id']]['record_sha256']
        assert r['train_math_sha256']==by[r['train_id']]['math_sha256']
        assert r['eval_math_sha256']==by[r['eval_id']]['math_sha256']
        assert r['verdict']=='PASS_ONLY_THIS_REVISED_PAIR_DISTINCT_CORE'
    for b in read(REVIEW/'received-bindings.json')['bindings']:
        assert digest(ROOT/b['archive_path'])==b['sha256']
    audit=read(REVIEW/'native-received-audit.json')
    assert len(audit['rows'])==162
    for row in audit['rows']:
        archived=ROOT/row['archived_scene_path']
        assert digest(archived)==row['archived_scene_sha256']
        calls=[n for n in ast.walk(ast.parse(archived.read_bytes())) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='MathTex']
        assert len(calls)==1 and isinstance(calls[0].args[0],ast.Constant) and calls[0].args[0].value==''
    sys.modules['core_signatures']=current
    n=module('verified_native_renderer',REVIEW/'final-source-snapshot/tools/native_render_pilot.py')
    receipt_path=REVIEW/'native-real-samples/receipt.json'
    receipt=read(receipt_path)
    assert receipt['summary']=={'total':7,'rendered':7,'failed':0}
    total=occurrences=0
    for r in receipt['results']:
        rec=current.load_record(by,r['id'])
        work=receipt_path.parent/('render-'+r['id'])
        assert r['record_sha256']==by[r['id']]['record_sha256'] and r['math_sha256']==by[r['id']]['math_sha256']
        assert (work/'scene.py').read_text(encoding='utf-8')==n.build_scene(rec)
        assert digest(work/'scene.py')==r['scene_py_sha256']
        formulas,locations=n.formula_inventory(rec)
        inventory=read(work/'formula-inventory.json')
        assert inventory=={'unique_formulas':formulas,'source_occurrences':locations}
        assert current.dense(formulas)==r['formulas_sha256']
        assert r['unique_formulas']==len(formulas) and r['source_formula_occurrences']==len(locations)
        assert digest(work/r['mp4_path'])==r['mp4_sha256'] and (work/r['mp4_path']).stat().st_size>0
        assert digest(work/'stdout.bin')==r['stdout_sha256'] and digest(work/'stderr.bin')==r['stderr_sha256']
        assert r['rc']==0 and r['timed_out'] is False
        total+=len(formulas);occurrences+=len(locations)
    assert total==180 and occurrences==250
    req=read(REVIEW/'native-resubmission-requirements.json')
    assert req['current_required_unique_ids']==163 and len(req['claude_required_ids'])==156
    assert len(set(req['claude_required_ids']))==156
    for b in req['bindings']:assert b==by[b['id']]
    assert req['codex_sample_receipt_sha256']==digest(receipt_path)
    for file,count in [('scoped-tests.stderr.bin',46),('native-tool-tests.stderr.bin',15)]:
        text=(REVIEW/file).read_text(encoding='utf-8')
        assert 'Ran '+str(count)+' tests' in text and '\nOK' in text
    q=read(REVIEW/'QUALIFICATION.json')
    assert q['tool_tests']['total']==61 and q['changed_training_records']==4
    assert q['original_formula_render_acceptance']=='FAIL_ALL_162_EMPTY_MATHTEX_ARGUMENT'
    assert q['global_semantic_isolation']=='NOT_ESTABLISHED' and q['production']=='CLOSED' and not q['PASS_CORE_SCOPE_issued']
    assert 'DOUBLE_ENDPOINT_EXPERIMENT_OUT_OF_SCOPE' in q['user_scope']
    print(json.dumps({'archive_integrity':'PASS','outer_artifacts':outer,'parent_artifacts':parent,'older_artifacts':older,'current_core_artifacts':inner,'records':761,'sources':24,'changed_math_records':4,'unchanged_full_records':757,'scoped_tool_tests':61,'new_exact_checks':46,'general_proof_obligations':6,'original_empty_mathtex_runs':162,'actual_formula_samples':7,'actual_formula_entries':180,'pending_claude_formula_render_records':156,'semantic_isolation':'NOT_ESTABLISHED','production':'CLOSED','PASS_CORE_SCOPE_issued':False}))
if __name__=='__main__':main()
