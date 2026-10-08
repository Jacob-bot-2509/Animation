from pathlib import Path
import json,hashlib,collections
R=Path(r'D:\Animation-Model-Training');O=R/'reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
rows=[json.loads(x) for x in (O/'reference-closure-final.jsonl').read_text(encoding='utf-8').splitlines()]
pending={r['expected_sha256'] for r in rows if r['status']=='EXPECTED_HASH_UNRESOLVED'}
fs=[json.loads(x) for x in (O/'filesystem-inventory.jsonl').read_text(encoding='utf-8').splitlines()]
git=[json.loads(x) for x in (O/'git-history-inventory.jsonl').read_text(encoding='utf-8').splitlines()]
fingerprints=collections.defaultdict(list);seen=set()
for row in fs+git:
 if row['sha256'] in seen:continue
 if 'path' in row and row['path'].startswith('holdout-sources/'):continue
 names=[row['path']] if 'path' in row else row['logical_paths']
 if not any(Path(n).suffix.lower() in {'.jsonl','.md','.json','.ini','.html','.txt'} for n in names):continue
 seen.add(row['sha256'])
 p=R/row['actual_bound_path'];b=p.read_bytes()
 try:text=b.decode('utf-8-sig')
 except UnicodeError:continue
 normalized=sha('\n'.join(text.splitlines()).encode('utf-8'))
 if normalized in pending:fingerprints[normalized].append({'path':row['actual_bound_path'],'raw_sha256':row['sha256'],'normalized_sha256':normalized,
  'algorithm':'sha256-utf8-sig-splitlines-lf-v1','original_bytes_preserved':True})
for row in rows:
 if row['status']!='EXPECTED_HASH_UNRESOLVED':continue
 matches=fingerprints.get(row['expected_sha256'],[])
 if matches:
  row['content_fingerprint_bindings']=matches
  row['status']='LEGACY_CONTENT_FINGERPRINT_MATCH_RAW_BOUND_SEPARATE' if row['expected_hash_role']=='DECLARED_GENERIC' else 'RAW_HASH_CLAIM_MATCHES_ONLY_CONTENT_FINGERPRINT'
  row['archival_expected_raw_bytes_recovered']=False
with (O/'reference-closure-authoritative.jsonl').open('x',encoding='utf-8',newline='\n') as f:
 for row in rows:f.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
counts=dict(collections.Counter(r['status'] for r in rows))
remaining=[r for r in rows if r['status'] in {'EXPECTED_HASH_UNRESOLVED','RAW_HASH_CLAIM_MATCHES_ONLY_CONTENT_FINGERPRINT'}]
summary={'schema':'history-evidence-reference-resolution-authoritative-v1','reference_count':len(rows),'statuses':counts,
 'unresolved_archival_raw_claims':remaining,'unresolved_archival_raw_claim_count':len(remaining),
 'complete_available_material_inventory':True,'complete_human_model_exposure_proof':False,
 'normalization_never_replaces_archival_raw_sha256':True,'role_exposure_default':'UNKNOWN','qualified_count':None}
with (O/'REFERENCE_STATUS.json').open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'states':counts,'unresolved_archival_raw_claims':len(remaining),
 'remaining_referrers':dict(collections.Counter(r['referring_path'] for r in remaining))},ensure_ascii=False))
