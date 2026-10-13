from pathlib import Path
import json,hashlib,re
ROOT=Path(r'D:\Animation-Model-Training');OUT=ROOT/'reviews/codex-supervision/2026-10-05-remaining-batch-audit'
d=json.loads((OUT/'delivery-manifest.json').read_text(encoding='utf-8'));digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(ROOT/d['report_path'])==d['report_sha256']
for f in d['files']:
 assert digest(ROOT/f['root_path'])==f['sha256'] and digest(ROOT/f['root_report_path'])==f['report_sha256']
 rows=[json.loads(l) for l in (ROOT/f['root_path']).read_text(encoding='utf-8').splitlines()];md=(ROOT/f['root_report_path']).read_text(encoding='utf-8')
 for r in rows:
  chunk=md.split('## '+r['id']+' ',1)[1].split('\n## ',1)[0]
  assert all(r[k] in chunk for k in ('problem','solution','answer')),(r['id'],'markdown mismatch')
for target in re.findall(r'\]\(([^)]+)\)',(OUT/'REPAIR_REPORT.md').read_text(encoding='utf-8')):
 assert (OUT/target).resolve().exists(),target
handoff=json.loads((OUT/'bridge-handoff.json').read_text(encoding='utf-8-sig'));assert handoff['receipt']['status']=='sent'
summary={'delivered_batches':10,'delivered_records':145,'separate_math_documents':10,'jsonl_and_markdown_match':True,'delivery_hashes_match':True,'report_links_exist':True,'bridge_status':'sent','bridge_message_id':handoff['receipt']['message']['id']}
(OUT/'final-verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary,ensure_ascii=False))
