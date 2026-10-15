"""Read-only archive integrity, lineage and qualification verification."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
D=Path(__file__).resolve().parent
R=next(p for p in D.parents if p.name=='Animation-Model-Training')
N=D/'effective-core-v2';O=R/'reviews/codex-supervision/2026-10-07-continuous-math-review/current-core'
H=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def verify_manifest(base,expected):
 p=base/'delivery-manifest.json';raw=p.read_bytes();assert H(raw)==expected,'manifest changed'
 manifest=json.loads(raw);seen=set()
 for item in manifest['artifacts']:
  rel=item['path'];assert rel not in seen and '..' not in Path(rel).parts;seen.add(rel)
  p=base/rel;assert p.absolute().is_relative_to(base.absolute())
  b=p.read_bytes();assert H(b)==item['sha256'] and len(b)==item['bytes'],rel
 return len(seen)
ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256',required=True);args=ap.parse_args()
outer=verify_manifest(D,args.manifest_sha256)
parent=verify_manifest(O,'972bd216b713bec7c48896e8f144d999dd6385b8c0e3e00a4c0116dfd1bbca22')
pin=read(D/'successor-pin.json');successor=verify_manifest(N,pin['core_manifest_sha256'])
sp=importlib.util.spec_from_file_location('archived_signature_checker',D/'final-tool-snapshot/tools/core_signatures.py')
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
m.ROOT=R;m.CORE=N
assert m.CORE_MANIFEST_SHA256==pin['core_manifest_sha256']
refs=m.load_record_bindings();by={r['id']:r for r in refs}
sigs,_=m.read_signature_inputs([D/'revised-complete-signatures-v2.jsonl'],by)
reviews=[json.loads(l) for l in (D/'signature-review.jsonl').read_text(encoding='utf8').splitlines() if l.strip()]
originals=[json.loads(l) for l in (D/'received-complete-signatures.jsonl').read_text(encoding='utf8').splitlines() if l.strip()]
assert len(refs)==len(sigs)==len(reviews)==len(originals)==761
old={r['id']:r for r in [json.loads(l) for l in (O/'record-bindings.jsonl').read_text(encoding='utf8').splitlines() if l.strip()]}
orig={x['id']:x for x in originals}
unchanged=sum(x['record_sha256']==old[x['id']]['record_sha256'] for x in refs)
assert unchanged==760 and set(old)==set(by)==set(orig)
review={x['id']:x for x in reviews};changes=0
for sig in sigs:
 rid=sig['id'];row=review[rid];before=orig[rid]
 assert row['after_signature_sha256']==m.dense(sig)
 assert row['before_signature_sha256']==m.dense(before)
 assert row['after_record_sha256']==by[rid]['record_sha256']
 assert row['after_math_sha256']==by[rid]['math_sha256']
 assert row['output_manifest_sha256']==pin['core_manifest_sha256']
 assert row['disposition']=='PASS_SIGNATURE_FIDELITY_TO_CURRENT_TASK'
 assert row['semantic_isolation']=='NOT_ESTABLISHED'
 changes+=int(row['changed'])
assert changes==67
for item in read(D/'received-bindings.json'):
 b=(R/item['archived_path']).read_bytes()
 assert H(b)==item['sha256'] and len(b)==item['bytes']
proof=read(N/'exact-proof.json');ref=by['draft-c18-02']
assert proof['record_sha256']==ref['record_sha256'] and proof['math_sha256']==ref['math_sha256']
assert proof['proof_script_sha256']==H((N/'prove_c18_exact.py').read_bytes())
assert proof['symbolic_passed']==22 and len(proof['symbolic_checks'])==22 and all(x['passed'] for x in proof['symbolic_checks'])
assert len(proof['manual_real_domain_implications'])==4
qual=read(D/'QUALIFICATION.json')
assert qual['signature_changed_records']==67 and qual['math_rewrites']==1
assert qual['semantic_isolation']=='NOT_ESTABLISHED' and qual['native']=='UNVERIFIED; OUT_OF_CURRENT_EXPERIMENT_SCOPE'
assert qual['production']=='CLOSED' and qual['PASS_CORE_SCOPE_issued'] is False
receipt=read(D/'revised-full-cross-screen-v2/cross-candidates.json')
assert receipt['signature_coverage']=='COMPLETE' and receipt['candidates']==[]
assert receipt['candidate_generation_exhaustive'] is False and receipt['semantic_isolation']=='NOT_ESTABLISHED'
assert receipt['core_manifest_sha256']==pin['core_manifest_sha256']
pairs=read(D/'known-pair-dispositions.json')
assert pairs['global_isolation']=='NOT_ESTABLISHED'
for pair in pairs['pairs']:
 assert pair['eval_record_sha256']==by[pair['eval_id']]['record_sha256']
 assert (pair.get('train_record_after') or pair.get('train_record_sha256'))==by[pair['train_id']]['record_sha256']
test_tail=(D/'successor-tool-tests.stderr.bin').read_text(encoding='utf8')
assert 'Ran 27 tests' in test_tail and test_tail.rstrip().endswith('OK')
print(json.dumps({'archive_integrity':'PASS','archive_artifacts':outer,'parent_artifacts':parent,'successor_artifacts':successor,
 'actual_records':761,'actual_sources':24,'reviewed_signature_versions':761,'changed_signatures':67,'unchanged_full_records':unchanged,
 'new_symbolic_checks':22,'tool_regressions':27,'semantic_isolation':'NOT_ESTABLISHED','native':'UNVERIFIED','production':'CLOSED','PASS_CORE_SCOPE_issued':False}))
