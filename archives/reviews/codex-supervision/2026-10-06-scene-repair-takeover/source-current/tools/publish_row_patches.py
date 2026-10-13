"""Publish a new exact row-patch version only after every batch passes binding checks."""
from pathlib import Path
import argparse,copy,hashlib,json,re,sys,os,uuid
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from draft_io import selected_path,verify_entry,fingerprint,publish_jsonl,write_utf8_lf,NORMALIZED_HASH
from build_review_pdf import report_body
MATH_FIELDS=('problem','solution','answer','scene_spec')
def sorted_sha(obj):return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,allow_nan=False).encode()).hexdigest()
def rows_at(path):
 rows=[json.loads(x) for x in path.read_text('utf-8-sig').splitlines() if x.strip()];ids=[r['id'] for r in rows]
 if not rows or any(not isinstance(i,str) or not i for i in ids) or len(ids)!=len(set(ids)):raise ValueError('invalid or duplicate IDs')
 return rows

def publish(drafts,patch_path,version):
 if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}',version):raise ValueError('invalid version')
 sel_path=drafts/'draft-selection.json';original=sel_path.read_bytes();sel=json.loads(original.decode('utf-8-sig'))
 if sel.get('schema')!=2 or sel.get('hash_algorithm')!=NORMALIZED_HASH:raise ValueError('schema2 normalized selector required')
 entries={e['batch']:e for e in sel['entries']}
 if len(entries)!=len(sel['entries']):raise ValueError('duplicate selector batches')
 patches=json.loads(patch_path.read_text('utf-8-sig'))['records'];plans={};seen=set()
 if isinstance(patches,list) and any(isinstance(p,dict) and isinstance(p.get('fields'),dict) and 'scene_spec' in p['fields'] for p in patches):
  raise ValueError('scene-only or mixed scene auto-selector publication retired; use stage_scene_patches.py with immutable inputs and fresh output')
 if not patches:raise ValueError('empty patches')
 for patch in patches:
  batch=patch['batch'];identity=(batch,patch['id'])
  if identity in seen:raise ValueError('duplicate patch target')
  seen.add(identity);entry=entries[batch];current=selected_path(drafts,entry);verify_entry(current,entry,NORMALIZED_HASH)
  source=selected_path(drafts,{'batch':batch,'path':patch['expected_selected_path']});fp=fingerprint(source.read_bytes())
  if patch['expected_hash_algorithm']!=NORMALIZED_HASH or fp['sha256']!=patch['expected_selected_sha256'] or fp['raw_sha256']!=patch['expected_selected_raw_sha256']:raise ValueError('patch source file binding mismatch')
  originals=rows_at(source);before=next((row for row in originals if row['id']==patch['id']),None)
  if before is None or sorted_sha(before)!=patch['expected_record_sha256']:raise ValueError('original record SHA mismatch')
  fields=patch['fields']
  if not isinstance(fields,dict) or not fields or set(fields)-set(MATH_FIELDS):raise ValueError('non-mathematical patch fields')
  after=copy.deepcopy(before);after.update(fields)
  if sorted_sha({k:after[k] for k in MATH_FIELDS})!=patch['new_math_content_sha256']:raise ValueError('new mathematical SHA mismatch')
  if batch not in plans:
   rows=rows_at(current)
   if [row['id'] for row in rows]!=[row['id'] for row in originals] or entry['count']!=len(rows):raise ValueError('source/current ID order or count mismatch')
   plans[batch]={'rows':rows,'entry':entry,'source':current,'fp':fingerprint(current.read_bytes()),'patched':[]}
  plan=plans[batch];row=next(row for row in plan['rows'] if row['id']==patch['id']);updated=copy.deepcopy(row);updated.update(fields)
  if sorted_sha({k:updated[k] for k in MATH_FIELDS})!=patch['new_math_content_sha256']:raise ValueError('current mathematics differs from patch result')
  old_vid=row.get('versioned_id');row.update(copy.deepcopy(fields));row['versioned_id']=f'{version}-{batch}-{row["id"]}'
  lin=copy.deepcopy(row.get('revision_lineage') or {});lin.update(version=version,previous_selected_version={'version':entry['version'],'path':current.relative_to(ROOT).as_posix() if current.is_relative_to(ROOT) else current.as_posix(),'sha256':plan['fp']['sha256'],'raw_sha256':plan['fp']['raw_sha256'],'hash_algorithm':NORMALIZED_HASH,'versioned_id':old_vid})
  notes=lin.get('math_correction_notes',[])
  if isinstance(notes,str):notes=[notes]
  if not isinstance(notes,list):raise ValueError('invalid correction notes')
  lin['math_correction_notes']=notes+['Original record and resulting mathematical SHA verified before publication'];row['revision_lineage']=lin
  sr=copy.deepcopy(row.get('strict_review') or {});sr.update(math_content_sha256=patch['new_math_content_sha256'],math_review_evidence=patch_path.as_posix());row['strict_review']=sr
  row['draft_status']=version.upper()+'-NOT-ADMITTED';plan['patched'].append(patch['id'])
 summary=drafts/f'repair-{version}-summary.json'
 for batch,plan in plans.items():
  plan['out']=drafts/batch/f'draft-{version}.jsonl';plan['report']=drafts/batch/f'DRAFT_REPORT-{version}.md'
  if any(p.exists() for p in (plan['out'],plan['report'],summary)):raise ValueError('versioned output exists')
  json.dumps(plan['rows'],ensure_ascii=False,allow_nan=False)
 lock=drafts/'.row-publish.lock';receipts={}
 with lock.open('x') as stream:stream.write(version)
 try:
  if sel_path.read_bytes()!=original:raise ValueError('selection changed before publication')
  for batch,plan in sorted(plans.items()):
   fp=publish_jsonl(plan['out'],plan['rows']);md=f'# {batch} 精确数学修订文档\n\n版本：{version}。未正式准入；动画未验收。\n\n'
   md+='\n\n'.join(f'## {row["id"]} · {row.get("concept_id","")}\n\n'+report_body(row) for row in plan['rows'])+'\n'
   write_utf8_lf(plan['report'],md,exclusive=True);rfp=fingerprint(plan['report'].read_bytes());e=plan['entry']
   e.update(path=plan['out'].relative_to(drafts).as_posix(),version=version,**fp)
   root=lambda p:p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix()
   e.update(root_path=root(plan['out']),report_path=plan['report'].relative_to(drafts).as_posix(),root_report_path=root(plan['report']),source_path=root(plan['source']),source_sha256=plan['fp']['sha256'],source_raw_sha256=plan['fp']['raw_sha256'],source_hash_algorithm=NORMALIZED_HASH,report_sha256=rfp['sha256'],report_raw_sha256=rfp['raw_sha256'],report_hash_algorithm=NORMALIZED_HASH)
   receipts[batch]={'source':plan['fp'],'published':fp,'report':rfp,'patched_ids':plan['patched']}
  write_utf8_lf(summary,json.dumps(receipts,ensure_ascii=False,indent=2)+'\n',exclusive=True)
  if sel_path.read_bytes()!=original:raise ValueError('selection changed; published outputs remain unselected')
  sel['updated_by']='strict-row-publisher';tmp=sel_path.with_name('.selection-'+uuid.uuid4().hex+'.json')
  try:write_utf8_lf(tmp,json.dumps(sel,ensure_ascii=False,indent=2)+'\n',exclusive=True);os.replace(tmp,sel_path)
  finally:
   if tmp.exists():tmp.unlink()
 finally:lock.unlink()
 return receipts

def main(argv=None):
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--drafts',type=Path,required=True);ap.add_argument('--patches',type=Path,required=True);ap.add_argument('--version',required=True);a=ap.parse_args(argv)
 try:print(json.dumps(publish(a.drafts,a.patches,a.version),ensure_ascii=False,indent=2));return 0
 except (OSError,ValueError,KeyError,TypeError,StopIteration) as exc:print('[FAIL]',exc);return 1
if __name__=='__main__':sys.exit(main())
