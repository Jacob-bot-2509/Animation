# Metadata/hash-only run archive; does not judge mathematical cores.

from pathlib import Path
import json,hashlib,collections
R=Path(r'D:\Animation-Model-Training')
H=R/'reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol'
g=json.loads((H/'EXPECTED_VERSION_GAPS.json').read_text(encoding='utf-8-sig'))['versions']
targets={v['expected_sha256']:v for v in g}
wanted={Path(p.replace('\\','/')).name.casefold() for v in g for p in v['claimed_paths']}
sources={}
for name in ['filesystem-inventory.jsonl','extra-filesystem-inventory.jsonl','git-history-inventory.jsonl','git-all-material-supplement.jsonl']:
 p=H/name
 for line in p.read_text(encoding='utf-8-sig').splitlines():
  d=json.loads(line)
  logical=[d.get('path','')]+d.get('logical_paths',[])
  if not any(Path(p.replace('\\','/')).name.casefold() in wanted for p in logical):continue
  rel=d.get('actual_bound_path',d.get('path'))
  if rel and d.get('sha256'):sources.setdefault(d['sha256'],rel)
hits=[];errors=[];trials=0
for digest,rel in sources.items():
 p=R/rel
 raw=p.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=digest:
  errors.append({'path':rel,'expected_source_sha':digest});continue
 try:raw.decode('utf-8-sig','strict')
 except UnicodeError:continue
 if b'\x00' in raw:continue
 lf=raw.replace(b'\r\n',b'\n')
 candidates={'LF':lf,'CRLF':lf.replace(b'\n',b'\r\n'),'NO_FINAL_LF':lf[:-1] if lf.endswith(b'\n') else lf,'FINAL_LF':lf if lf.endswith(b'\n') else lf+b'\n'}
 for label,data in list(candidates.items()):
  candidates[label+'_UTF8_BOM']=b'\xef\xbb\xbf'+data.removeprefix(b'\xef\xbb\xbf')
 for label,data in candidates.items():
  trials+=1;h=hashlib.sha256(data).hexdigest()
  if h in targets:hits.append({'expected_sha256':h,'source_path':rel,'source_sha256':digest,'transformation':label,'result_bytes':len(data)})
print(json.dumps({'unique_sources':len(sources),'transform_trials':trials,'hits':hits,'source_errors':errors},ensure_ascii=False))
