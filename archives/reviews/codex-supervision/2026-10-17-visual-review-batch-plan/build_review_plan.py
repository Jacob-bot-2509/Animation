"""Read current indexes, propose bounded review queues. No render, approval, or formal evidence writes."""
import hashlib,importlib.util,json
from pathlib import Path
R=Path(r'D:\Animation-Model-Training')
A=R/'archives/reviews/codex-supervision/2026-10-17-visual-review-batch-plan'
BASE=R/'reviews/data-prep/2026-10-17-submission'
G=BASE/'diversity-evidence/generation-6896eb72b7f2404caac8f2244e791b75'
sha=lambda b:hashlib.sha256(b).hexdigest()
enc=lambda x:json.dumps(x,ensure_ascii=True,sort_keys=True,separators=(',',':')).encode()
def read(p):
 raw=p.read_bytes();pins[p.relative_to(R).as_posix()]={'sha256':sha(raw),'bytes':len(raw)}
 return raw
pins={}
ev=json.loads(read(R/'data/asset_evidence.json'))
batch=json.loads(read(BASE/'asset-evidence/first-batch-10.v2.json'))
protocol=read(R/'docs/READINESS-EVIDENCE-PROTOCOL.md')
manifest=json.loads(read(R/'data/manifest.json'))
policy=read(R/'configs/training_diversity_policy.json')
complete=json.loads(read(G/'COMPLETE.json'))
for item in complete['artifacts']:
 raw=read(G/item['path']);assert sha(raw)==item['sha256'] and len(raw)==item['bytes']
div=[json.loads(x) for x in (G/'row-bindings.jsonl').read_bytes().splitlines()]
template=json.loads((G/'template.json').read_bytes())
pending=[json.loads(x) for x in (G/'pending-review-list.jsonl').read_bytes().splitlines()]
assert len(div)==len(template['record_reviews'])==len(pending)==47
assert len({x['sample_id'] for x in div})==47
assert all(x['user_review'] is None for x in template['record_reviews'])
assert all(x['state']=='PENDING_REVIEW' and x['user_review'] is None for x in pending)
assert template['manifest_sha256']==sha((R/'data/manifest.json').read_bytes())
assert template['policy_sha256']==sha(policy)
source={}
for row in div:
 p=R/row['project_source_path'];raw=read(p);line=raw.splitlines(keepends=True)[row['line_no']-1];obj=json.loads(line)
 assert sha(raw)==row['source_file_sha256'] and sha(line)==row['raw_line_sha256']
 assert sha(enc(obj))==row['canonical_record_sha256'] and obj['id']==row['sample_id']
 source[row['sample_id']]=row
sp=BASE/'asset-evidence/pick_first_batch_10.py';read(sp)
s=importlib.util.spec_from_file_location('review_selector',sp);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
bound,rejected,cache=m.bind_candidates(ev['records'],root=R)
for p,(raw,_,_) in cache.items():
 assert p.read_bytes()==raw
 pins[p.relative_to(R).as_posix()]={'sha256':sha(raw),'bytes':len(raw)}
existing={sid for sid,row in ev['records'].items() if row.get('math')=='verified' and row.get('semantic')=='verified' and row.get('render')=='rendered'}
assert len(existing)==ev['n_verified_assets']==1 and len(ev['records'])==ev['n_total_records']==497
allpending=set(ev['records'])-existing
bmap={x['sample_id']:x for x in bound}
assert len(bound)==482 and len(rejected)==15
assert len(allpending)==496 and existing<=set(bmap)
first=[x['sample_id'] for x in batch['records']]
assert len(first)==len(set(first))==10 and set(first)<=allpending & set(bmap)
ready=[x for x in bound if x['sample_id'] in allpending]
ready_by_id={x['sample_id']:x for x in ready}
assert len(ready)==481
ordered=first+sorted(set(ready_by_id)-set(first),
                     key=lambda sid:(-len(ready_by_id[sid]['tags']),-len(ready_by_id[sid]['errors']),sid))
def groups(rows,prefix,state):
 return [{'batch_id':prefix+str(n//10+1).zfill(3),'state':state,'user_review':None,
          'proposed_visual_decisions':['PASS','FAIL','UNVERIFIED'],'items':rows[n:n+10]}
         for n in range(0,len(rows),10)]
assetrows=[]
for sid in ordered:
 e=ev['records'][sid];row=ready_by_id[sid];p=R/row['source']['path']
 line=p.read_bytes().splitlines(keepends=True)[row['source']['line']-1]
 assetrows.append({'sample_id':sid,'binding':row['source'],'asset_input_sha256':sha(line.decode('utf-8').strip().encode('utf-8')),
                  'upstream_asset_input_sha256_claim':e['input_sha256'],
                  'math_review':None,'geometry_review':None,'native_render_review':None,'user_review':None,
                  'actual_media':None,'math_fidelity_status':'PENDING_NOT_APPROVED',
                  'fault_tags':row['tags'],'diversity_cross_reference':source.get(sid),
                  'preparation_state':'SOURCE_BOUND_ONLY_NOT_READY_FOR_USER_OR_RENDER'})
quarantined=[]
for row in sorted(rejected,key=lambda x:x['sample_id']):
 sid=row['sample_id'];assert sid in allpending
 quarantined.append({'sample_id':sid,'reason':row['reason'],'claimed_source':ev['records'][sid]['source'],
                     'claim_origin':'HISTORICAL_ASSET_EVIDENCE_NOT_CURRENT_SOURCE_VERIFICATION',
                     'user_review':None,'actual_media':None,'state':'BLOCKED_SOURCE_BINDING'})
dfirst=[sid for sid in first if sid in source]
dorder=dfirst+sorted(set(source)-set(dfirst),key=lambda sid:(source[sid]['project_source_path'],source[sid]['line_no'],sid))
drows=[]
for sid in dorder:
 drows.append({'sample_id':sid,'binding':source[sid],'user_review':None,'concept_id':None,'variant_kind':None,
               'math_review':None,'diversity_review':None,'leakage_review':None,'actual_media':None,
               'cross_reference_only_not_asset_acceptance':sid in allpending})
plan={'schema':'proposed-visual-review-batches-v1','status':'PROPOSED_NOT_EXECUTION_OR_APPROVAL',
      'source_mail_id':'msg_1792234328254_896',
      'authorization_provenance':'CLAUDE_REPORTED_USER_FULL_VISUAL_REVIEW_NOT_DIRECT_AUTHORITY',
      'capacity':10,'counts':{'asset_total':497,'existing_verified_claims_not_reaudited':1,'asset_unverified':496,
                              'source_bound_unverified':481,'source_quarantined':15,'diversity_unreviewed':47},
      'existing_verified_claim_ids':sorted(existing),
      'asset_source_bound_batches':groups(assetrows,'A','STATIC_PREPARATION_CANDIDATE_ONLY'),
      'asset_quarantine_batches':groups(quarantined,'Q','BLOCKED_SOURCE_BINDING'),
      'diversity_batches':groups(drows,'D','INDEPENDENT_REVIEW_FIELDS_PENDING'),
      'batch_count_math':{'bound_asset':'481 = 48*10 + 1','quarantined_asset':'15 = 10 + 5',
                          'diversity':'47 = 4*10 + 7','partitioned_asset_batches':51,
                          'theoretical_merged_asset_batches':50,
                          'merged_count_condition':'ONLY_IF_ALL_15_BINDINGS_REPAIRED_AND_REVIEW_PACKAGES_READY'},
      'next_action':'CONTINUE_AUTHORIZED_STATIC_MATH_GEOMETRY_PREPARATION; NO_ARBITRARY_GENERATED_EXECUTION',
      'production':'CLOSED','global_isolation':'NOT_ESTABLISHED'}
(A/'PROPOSED_BATCHES.json').write_bytes(enc(plan)+b'\n')
(A/'input-pins.json').write_bytes(enc(pins)+b'\n')
print(json.dumps({'counts':plan['counts'],'batch_sizes':{k:[len(x['items']) for x in plan[k]] for k in ['asset_source_bound_batches','asset_quarantine_batches','diversity_batches']},'first_diversity_overlap':len(dfirst)}))
