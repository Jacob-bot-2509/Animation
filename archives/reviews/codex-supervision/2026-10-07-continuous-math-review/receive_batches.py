from pathlib import Path
import json,hashlib,importlib.util
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
def sha(x):return hashlib.sha256(x).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def snapshot(path,data):
 path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists() and path.read_bytes()!=data:raise ValueError('immutable snapshot mismatch '+str(path))
 path.write_bytes(data)
def main():
 sp=importlib.util.spec_from_file_location('batch_v3',ROOT/'tools/math_review_batch.py')
 m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
 ledger=json.loads((OUT/'REVIEW_LEDGER.json').read_text(encoding='utf-8'))
 refs={r['id']:r for r in m.load_bound_refs(ROOT)}
 existing={r['batch'] for r in ledger['batches']};added=[]
 for d in sorted((ROOT/'reviews/2026-10-07-math-review').iterdir()):
  if not d.is_dir() or not (d/'batch-receipt.json').exists():continue
  receipt=json.loads((d/'batch-receipt.json').read_text(encoding='utf-8-sig'))
  if receipt.get('schema')!='math-review-batch-receipt-v3':continue
  batch=receipt['batch']
  if batch in existing:continue
  number=int(batch.split('-')[0][5:])
  if number<17:continue
  result=m.verify_bundle(d,ROOT)
  spec=json.loads((d/'batch-spec.json').read_text(encoding='utf-8-sig'))
  authored={r['id']:r for r in m.jsonl_bytes((d/'review-input-verdicts.jsonl').read_bytes())}
  bound=[]
  for rid in spec['ids']:
   ref=refs[rid];raw=(ROOT/ref['source_path']).read_bytes()
   r=json.loads(raw.splitlines()[ref['source_line']-1].decode('utf-8-sig'))
   assert sha(raw)==ref['source_raw_sha256'] and sha(canon(r))==ref['record_version_sha256'] and r['id']==rid
   bound.append({'source':ref,'record':r,'author_review':authored[rid]})
  for file in d.iterdir():snapshot(OUT/'received'/file.relative_to(ROOT),file.read_bytes())
  for suffix in ('.json','-verdicts.jsonl'):
   f=ROOT/'tools/review-batches'/(batch+suffix)
   snapshot(OUT/'received'/f.relative_to(ROOT),f.read_bytes())
  dest=OUT/'bound-records'/batch/'records.jsonl'
  snapshot(dest,b''.join(canon(r)+b'\n' for r in bound))
  snapshot(dest.parent/'binding-verification.json',(json.dumps(result,indent=2)+'\n').encode())
  ledger['batches'].append({'batch':batch,'count':len(bound),'groups':sorted({x['source']['group'] for x in bound}),
    'author_claim':'MATH_PASS','binding_verdict':'PASS','independent_math':'PENDING','revision':'PENDING',
    'record_snapshot':str(dest.relative_to(OUT)).replace('\\','/')})
  existing.add(batch);added.append({'batch':batch,'count':len(bound)})
 (OUT/'REVIEW_LEDGER.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'added':added,'received_batches':len(ledger['batches']),'received_records':sum(b['count'] for b in ledger['batches'])},indent=2))
if __name__=='__main__':main()
