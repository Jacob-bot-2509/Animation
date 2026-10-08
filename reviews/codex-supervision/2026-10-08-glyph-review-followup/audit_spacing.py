"""Independent verification of the nine spacing repair candidates and inherited versions."""
from pathlib import Path
import json,hashlib,importlib.util,sys,ast
ROOT=Path(__file__).resolve().parents[3]; OWNER=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
import core_signatures as core
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(x,msg):
    if not x:raise ValueError(msg)
PARENT=ROOT/'reviews/codex-supervision/2026-10-08-hd-formula-mail-review'
PARENT_SHA='12d50e59e50ee53c219be17d080c83a615523c7305ae5c659bec3b7fbacf902b'
def verify_manifest():
    require(sha(PARENT/'delivery-manifest.json')==PARENT_SHA,'4K parent manifest changed')
    m=json.loads((PARENT/'delivery-manifest.json').read_text('utf-8'))
    for a in m['artifacts']:
        p=core.checked_path(PARENT/a['path'],PARENT)
        require(sha(p)==a['sha256'] and p.stat().st_size==a['bytes'],'Parent artifact changed')
    return {r['id']:r for r in map(json.loads,(PARENT/'DELIVERY_INDEX.jsonl').read_text('utf-8').splitlines())}
def main():
    parents=verify_manifest()
    file=PARENT/'audit_hd.py'
    require(sha(file)==sha(OWNER/'auditor-before.py'),'Named frozen auditor changed')
    spec=importlib.util.spec_from_file_location('bound_hd_independent',file)
    prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior);prior.OWNER=OWNER
    old=json.loads((prior.PARENT/'delivery-manifest.json').read_text('utf-8'))
    prior.ARTIFACTS={a['path']:a for a in old['artifacts']}
    bindings={r['id']:r for r in core.load_record_bindings()}
    scan=json.loads((OWNER/'fraction-array-scan-final.json').read_text('utf-8'))
    expected={r['id'] for r in scan['records']}
    receipts=[]
    for folder in ('spacing-probe','spacing-rest'):
        data=json.loads((OWNER/folder/'receipt.json').read_text('utf-8'))
        require(data['summary']['failed']==0,'Failed candidate shard')
        require(sha(OWNER/folder/'generator-snapshot.py')==sha(ROOT/'tools/hd_formula_pages.py'),'Generator snapshot mismatch')
        receipts+=data['results']
    require(len(receipts)==len(expected)==len({r['id']for r in receipts}),'Duplicate or missing repair')
    require({r['id']for r in receipts}==expected,'Repair ID mismatch')
    repaired=[]
    for r in receipts:
        checked=prior.verify_one(r,parents[r['id']],bindings[r['id']])
        scene=core.checked_path(ROOT/r['mp4_path'],OWNER).parents[3].parent/'scene.py'
        text=scene.read_text('utf-8')
        require(r'\renewcommand{\arraystretch}{2}' in text,'Missing fraction spacing template')
        # No formula rewriting: verify_one compares the literal to frozen source inventory.
        checked['spacing_repair']='EXACT_TEX_UNCHANGED_ARRAYSTRETCH_2'
        repaired.append(checked)
        print('Independently verified '+r['id'],flush=True)
    byid={r['id']:r for r in repaired}
    combined=[byid.get(rid,row)for rid,row in parents.items()]
    require(len(combined)==165 and len({r['id']for r in combined})==165,'Combined delivery lost ID')
    (OWNER/'REPAIRED_INDEX.jsonl').write_bytes(b''.join((json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n').encode('utf-8')for r in repaired))
    (OWNER/'DELIVERY_INDEX.jsonl').write_bytes(b''.join((json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n').encode('utf-8')for r in combined))
    metrics=[p for r in combined for p in r['page_metrics']]
    summary={'records':165,'repaired_records':len(repaired),'inherited_unchanged_records':165-len(repaired),
             'affected_formula_items':scan['formula_count'],'pages':sum(r['page_count']for r in combined),
             'repaired_pages':sum(r['page_count']for r in repaired),
             'segment_pages':sum(r['segment_pages']for r in combined),
             'parent_manifest_sha256':PARENT_SHA,'parent_index_sha256':sha(PARENT/'DELIVERY_INDEX.jsonl'),
             'combined_index_sha256':sha(OWNER/'DELIVERY_INDEX.jsonl'),
             'generator_sha256':sha(ROOT/'tools/hd_formula_pages.py'),
             'minimum_slot_proxy_at_1080p_exact':str(min(prior.F(p['slot_proxy_at_1080p_exact']) for p in metrics)),
             'minimum_glyph_size':'NOT_CERTIFIED_BY_BBOX_PROXY',
             'full_glyph_review':'NOT_ESTABLISHED','all_record_math_and_scene_text':'UNCHANGED',
             'production':'CLOSED','semantic_isolation':'NOT_ESTABLISHED','native_sandbox':'UNVERIFIED'}
    (OWNER/'independent-spacing-summary.json').write_bytes(core.encoded(summary))
    print(json.dumps(summary))
if __name__=='__main__':main()
