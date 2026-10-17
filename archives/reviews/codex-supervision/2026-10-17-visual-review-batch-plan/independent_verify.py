"""Independent proposal verifier: direct byte/hash/set/partition checks; no builder import."""
import hashlib,json
from pathlib import Path
R=Path(r'D:\Animation-Model-Training');A=R/'archives/reviews/codex-supervision/2026-10-17-visual-review-batch-plan'
sha=lambda b:hashlib.sha256(b).hexdigest()
enc=lambda x:json.dumps(x,ensure_ascii=True,sort_keys=True,separators=(',',':')).encode()
p=json.loads((A/'PROPOSED_BATCHES.json').read_bytes());pins=json.loads((A/'input-pins.json').read_bytes())
for rel,pin in pins.items():
 raw=(R/rel).read_bytes();assert sha(raw)==pin['sha256'] and len(raw)==pin['bytes']
ev=json.loads((R/'data/asset_evidence.json').read_bytes())
first=json.loads((R/'reviews/data-prep/2026-10-17-submission/asset-evidence/first-batch-10.v2.json').read_bytes())
assetgroups=p['asset_source_bound_batches'];qgroups=p['asset_quarantine_batches'];dgroups=p['diversity_batches']
for group in assetgroups+qgroups+dgroups:
 assert 1<=len(group['items'])<=10 and group['user_review'] is None
 for item in group['items']:assert item['user_review'] is None and item['actual_media'] is None
assets=[x for b in assetgroups for x in b['items']];quarantine=[x for b in qgroups for x in b['items']];div=[x for b in dgroups for x in b['items']]
assert len(assets)==len({x['sample_id'] for x in assets})==481
assert len(quarantine)==len({x['sample_id'] for x in quarantine})==15
assert len(div)==len({x['sample_id'] for x in div})==47
assert [x['sample_id'] for x in assetgroups[0]['items']]==[x['sample_id'] for x in first['records']]
aset={x['sample_id'] for x in assets};qset={x['sample_id'] for x in quarantine};oldset=set(p['existing_verified_claim_ids'])
assert not aset&qset and not (aset|qset)&oldset
assert aset|qset|oldset==set(ev['records']) and len(oldset)==1
assert p['counts']['asset_unverified']==len(aset|qset)==496
assert len(assetgroups)==49 and len(qgroups)==2 and len(dgroups)==5
assert p['batch_count_math']['partitioned_asset_batches']==len(assetgroups)+len(qgroups)==51
assert p['batch_count_math']['theoretical_merged_asset_batches']==(496+9)//10==50
norm_matches=0
for row in assets:
 b=row['binding'];path=R/b['path'];raw=path.read_bytes();line=raw.splitlines(keepends=True)[b['line']-1];obj=json.loads(line)
 assert sha(raw)==b['file_sha256'] and sha(line)==b['raw_line_sha256']
 assert sha(enc(obj))==b['canonical_record_sha256'] and obj['id']==row['sample_id']
 assert sha(line.decode('utf-8').strip().encode('utf-8'))==row['asset_input_sha256']
 norm_matches+=row['asset_input_sha256']==row['upstream_asset_input_sha256_claim']
 if row['diversity_cross_reference'] is not None:
  cross=row['diversity_cross_reference'];assert cross['raw_line_sha256']==b['raw_line_sha256'] and cross['canonical_record_sha256']==b['canonical_record_sha256']
for row in quarantine:
 assert row['reason']=='source_file_sha_mismatch' and row['state']=='BLOCKED_SOURCE_BINDING'
 b=row['claimed_source'];assert sha(Path(b['path']).read_bytes())!=b['sha256']
for row in div:
 b=row['binding'];path=R/b['project_source_path'];raw=path.read_bytes();line=raw.splitlines(keepends=True)[b['line_no']-1];obj=json.loads(line)
 assert sha(raw)==b['source_file_sha256'] and sha(line)==b['raw_line_sha256']
 assert sha(enc(obj))==b['canonical_record_sha256'] and obj['id']==row['sample_id']
 assert row['concept_id'] is row['variant_kind'] is row['math_review'] is row['diversity_review'] is row['leakage_review'] is None
assert p['status']=='PROPOSED_NOT_EXECUTION_OR_APPROVAL'
assert p['production']=='CLOSED' and p['global_isolation']=='NOT_ESTABLISHED'
# Reuse already-frozen source review and independently map this activity packet.
prior=R/'archives/reviews/codex-supervision/2026-10-17-content-geometry-mapping-review'
m=json.loads((prior/'delivery-manifest.json').read_bytes())
for item in m['artifacts']:
 raw=(prior/item['path']).read_bytes();assert sha(raw)==item['sha256'] and len(raw)==item['bytes']
live=json.loads((prior/'current-source-bindings.json').read_bytes())
for rel,pin in live.items():assert sha((R/rel).read_bytes())==pin['sha256']
w=R/'reviews/codex-supervision/2026-10-17-auto-start/runs/start-cbb93aaf997548419f87583d2dc455d7'
packet=json.loads((w/'signals.json').read_bytes());wanted={x['detail']['tool_id'] for x in packet['signals']}
l=Path(r'C:\Users\Jacap\.claude\projects\d--code\ee005e1f-71f1-4697-a746-054f6399acd6.jsonl')
with l.open('rb') as f:f.seek(max(0,l.stat().st_size-2*1024*1024));f.readline();lines=f.readlines()
mapped=[]
for raw in lines:
 try:obj=json.loads(raw)
 except Exception:continue
 content=obj.get('message',{}).get('content',[])
 if not isinstance(content,list):continue
 for x in content:
  if isinstance(x,dict) and x.get('id') in wanted:
   inp=x.get('input',{});entry={'tool_id':x['id'],'tool':x.get('name'),'file_path':inp.get('file_path'),
     'command_prefix':str(inp.get('command',''))[:300],'input_sha256':sha(enc(inp))}
   if x.get('name')=='Write':
    raw=inp['content'].encode('utf-8');before=(prior/'before/build_content_mapping.py').read_bytes()
    assert raw.replace(b'\r\n',b'\n')==before.replace(b'\r\n',b'\n')
    entry['write_matches_prior_before_snapshot_normalizing_CRLF_only']=True
   mapped.append(entry)
assert {x['tool_id'] for x in mapped}==wanted
(A/'activity-mapping.json').write_bytes(enc(mapped)+b'\n')
watch=json.loads((R/'reviews/codex-supervision/2026-10-04-live-watch/latest.json').read_bytes())
(A/'observer-summary.json').write_bytes(enc({k:watch.get(k) for k in ['time','head','child_jobs','core_drift']})+b'\n')
(A/'independent-verification.json').write_bytes(enc({
 'status':'PASS_PROPOSAL_COUNTS_BINDINGS_AND_PRIOR_REVIEW_REUSE_ONLY',
 'asset_bound_verified':481,'asset_quarantined_confirmed':15,'diversity_bindings_verified':47,
 'asset_normalized_input_claims_match_current':norm_matches,
 'batches':{'A':49,'Q':2,'D':5},
 'review_decisions_created':0,'actual_media_created':0,
 'prior_archive_artifacts_verified':len(m['artifacts']),'prior_live_source_pins_verified':len(live),
 'mapped_signal_ids':len(wanted),'mapped_log_records':len(mapped),
 'prior_actual_reply_id':m['actual_reply_id'],'proposed_plan_is_user_authority':False})+b'\n')
print(json.dumps({'status':'PASS','norm_matches':norm_matches,'prior_artifacts':len(m['artifacts']),'mapped_signal_ids':len(wanted),'mapped_log_records':len(mapped)}))
