from pathlib import Path
import hashlib,json,sys,datetime,collections
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];sys.path.insert(0,str(ROOT/'tools'))
from draft_io import NORMALIZED_HASH,RAW_HASH,fingerprint,write_utf8_lf
D=ROOT/'reviews/2026-10-05-training-diversity-drafts';SEL=D/'draft-selection.json'
base=json.loads((OUT/'before.json').read_text('utf-8'))
assert hashlib.sha256(SEL.read_bytes()).hexdigest()==base['old_selector_raw_sha256'], 'selector changed concurrently'
assert not (OUT/'historical-hash-catalog.json').exists(), 'migration already published'
def rel(p):return p.relative_to(ROOT).as_posix()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,data):write_utf8_lf(OUT/name,json.dumps(data,ensure_ascii=False,indent=2)+'\n',exclusive=True)
paths=set(p for p in D.glob('batch-*/*') if p.is_file() and p.suffix in ('.jsonl','.md'))
for name in ['2026-10-05-batch-repair-execution','2026-10-05-remaining-batch-audit']:
 paths.update((ROOT/'reviews/codex-supervision'/name/'staged').glob('*.jsonl'))
paths.add(ROOT/'reviews/codex-supervision/2026-10-05-draft-mail-reverification/training-rewrite/linalg-048-replacement.jsonl')
by_raw=collections.defaultdict(list);catalog=[]
for p in sorted(paths):
 entry={'path':rel(p),**fingerprint(p.read_bytes()),'size':p.stat().st_size}
 if p.suffix=='.jsonl':
  rows=[json.loads(x) for x in p.read_text('utf-8-sig').splitlines() if x.strip()]
  entry['count']=len(rows);entry['id_order_sha256']=hashlib.sha256(json.dumps([r['id'] for r in rows],ensure_ascii=False).encode()).hexdigest()
 catalog.append(entry);by_raw[entry['raw_sha256']].append(p)
save('historical-hash-catalog.json',{'schema':2,'hash_algorithm':NORMALIZED_HASH,'created_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'raw_bytes_preserved':True,'historical_documents_not_rewritten':True,'files':catalog})
def convert(e):
 p=D/e['path'];assert raw(p)==e['sha256'], f'old draft hash mismatch {p}'
 new={**e,**fingerprint(p.read_bytes()),'root_path':rel(p)}
 if e.get('source_sha256'):
  matches=by_raw.get(e['source_sha256'],[])
  assert matches, f'missing source mapping {e["batch"]}: {e["source_sha256"]}'
  src=next((x for x in matches if x.parent==p.parent),matches[0]);h=fingerprint(src.read_bytes())
  new.update(source_path=rel(src),source_sha256=h['sha256'],source_raw_sha256=e['source_sha256'],source_hash_algorithm=NORMALIZED_HASH)
 if e.get('report_path'):
  report=D/e['report_path'];assert raw(report)==e['report_sha256'],f'old report hash mismatch {report}'
  h=fingerprint(report.read_bytes());new.update(report_sha256=h['sha256'],report_raw_sha256=h['raw_sha256'],report_hash_algorithm=NORMALIZED_HASH,root_report_path=rel(report))
 return new
old=json.loads(SEL.read_text('utf-8-sig'))
new={**old,'schema':2,'draft_root':rel(D),'hash_algorithm':NORMALIZED_HASH,
 'raw_hash_role':'Archival original bytes; normalized sha256 is authoritative for draft content only',
 'migration':{'evidence_path':rel(OUT/'historical-hash-catalog.json'),'evidence_raw_sha256':raw(OUT/'historical-hash-catalog.json'),'previous_selector_path':rel(OUT/'before'/rel(SEL)),'previous_selector_raw_sha256':raw(SEL)},
 'entries':[convert(e) for e in old['entries']]}
# New, additive manifests for the three prior deliveries; old manifests stay byte-identical.
for label,folder in [('batch01-08','2026-10-05-batch-repair-execution'),('batch09-18','2026-10-05-remaining-batch-audit'),('v4-final','2026-10-05-draft-mail-reverification')]:
 p=ROOT/'reviews/codex-supervision'/folder/'delivery-manifest.json';d=json.loads(p.read_text('utf-8-sig'))
 files=d.get('entries',d.get('files'));converted=[convert(e) for e in files]
 save('delivery-'+label+'-normalized.json',{'schema':2,'hash_algorithm':NORMALIZED_HASH,'supersedes_hash_view_only':{'path':rel(p),'raw_sha256':raw(p),'old_fields_are_raw_hashes':True},'original_metadata':{k:v for k,v in d.items() if k not in ('entries','files')},'historical_metadata_hash_fields_remain_raw':True,'files':converted,'admission':False,'render_verified':False})
# The only active metadata change: explicitly versioned schema-2 hash interpretation.
assert raw(SEL)==base['old_selector_raw_sha256']
write_utf8_lf(SEL,json.dumps(new,ensure_ascii=False,indent=2)+'\n')
save('migration-result.json',{'schema':2,'hash_algorithm':NORMALIZED_HASH,'catalog_files':len(catalog),'selected_files':len(new['entries']),'selected_count':sum(e['count'] for e in new['entries']),'selector_before_raw_sha256':base['old_selector_raw_sha256'],'selector_after_raw_sha256':raw(SEL),'draft_content_changed':False,'math_and_record_hashes_unchanged':True,'historical_original_manifests_rewritten':False,'production_manifest_changed':False,'new_admissions':0})
print(json.dumps({'catalog_files':len(catalog),'selected':sum(e['count'] for e in new['entries']),'new_selector_sha256':raw(SEL)},ensure_ascii=False))
