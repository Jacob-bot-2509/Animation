"""Immutable scene inputs and source-bound staged outputs; never activates a selector."""
from __future__ import annotations
import copy,hashlib,json,os,re,stat,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from holdout_contract import Snapshot,json_object,jsonl,object_sha,raw_sha
from draft_io import selected_path,fingerprint,NORMALIZED_HASH,publish_jsonl,write_utf8_lf

SCHEMA='scene-sweep-inputs-v2'
STANDARD=('Show every exact calculation; identify matrix row and column for each product; '
          'state convergence hypotheses, key bounds and limit arguments; use exact fractions and symbols.')
MATH_FIELDS=('problem','solution','answer','scene_spec')

def sorted_sha(value):
    return raw_sha(json.dumps(value,ensure_ascii=False,sort_keys=True,allow_nan=False).encode('utf-8'))

def _safe_output(output,root,protected):
    output=Path(output).resolve();root=Path(root).resolve()
    if output==root or not output.is_relative_to(root):
        raise ValueError('output must be a fresh directory inside project')
    for source in protected:
        source=Path(source).resolve()
        if output==source or output.is_relative_to(source) or source.is_relative_to(output):
            raise ValueError('output overlaps protected inputs or sources')
    if output.exists():raise ValueError('output directory already exists')
    return output

def _load(drafts,root,snapshot):
    drafts=Path(drafts).resolve()
    selection_path=drafts/'draft-selection.json'
    selection_bytes=snapshot.read(selection_path);selection=json_object(selection_bytes)
    if selection.get('schema')!=2 or selection.get('hash_algorithm')!=NORMALIZED_HASH:
        raise ValueError('schema2 normalized selector required')
    entries=selection.get('entries')
    if not isinstance(entries,list) or not entries:raise ValueError('nonempty selector entries required')
    seen_batches=set();seen_ids=set();groups=[];bound=[]
    for entry in entries:
        if entry.get('batch') in seen_batches:raise ValueError('duplicate batch')
        seen_batches.add(entry.get('batch'))
        source=selected_path(drafts,entry);data=snapshot.read(source);fp=fingerprint(data)
        if entry.get('hash_algorithm',NORMALIZED_HASH)!=NORMALIZED_HASH:
            raise ValueError('conflicting hash algorithm')
        if fp['sha256']!=entry.get('sha256') or fp['raw_sha256']!=entry.get('raw_sha256'):
            raise ValueError('selected source raw/normalized SHA mismatch')
        rows=jsonl(data)
        if type(entry.get('count')) is not int or len(rows)!=entry['count']:
            raise ValueError('selected count mismatch')
        nonblank=[(i,line) for i,line in enumerate(data.decode('utf-8-sig').splitlines(),1) if line.strip()]
        for row,(line_number,line) in zip(rows,nonblank):
            pid=row.get('id')
            if not isinstance(pid,str) or not pid or pid in seen_ids:
                raise ValueError('missing or duplicate record ID')
            seen_ids.add(pid)
            for field in ('problem','solution','answer'):
                if not isinstance(row.get(field),str) or not row[field].strip():
                    raise ValueError('missing mathematics field '+field)
            _scene(row.get('scene_spec'))
            binding={'batch':entry['batch'],'source_path':source.relative_to(root).as_posix(),
                     'source_line':line_number,'source_raw_sha256':fp['raw_sha256'],
                     'source_normalized_sha256':fp['sha256'],'hash_algorithm':NORMALIZED_HASH,
                     'raw_line_sha256':raw_sha(line.encode('utf-8')),
                     'record_canonical_sha256':object_sha(row),
                     'publisher_record_sorted_sha256':sorted_sha(row)}
            bound.append({'idx':len(bound),'record':copy.deepcopy(row),'binding':binding})
        groups.append((entry,source,data,rows))
    return selection_path,selection_bytes,selection,groups,bound

def _scene(value):
    if not isinstance(value,dict):raise ValueError('scene object required')
    for key in ('objects','steps'):
        values=value.get(key)
        if not isinstance(values,list) or not values or any(not isinstance(v,str) or not v.strip() for v in values):
            raise ValueError('nonempty scene '+key+' strings required')

def _write(path,value):
    write_utf8_lf(path,json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',exclusive=True)

def _readonly(path):
    os.chmod(path,stat.S_IREAD|stat.S_IRGRP|stat.S_IROTH)

def build_inputs(drafts,output,*,chunks=20,expected_count=None,root=ROOT):
    root=Path(root).resolve();snapshot=Snapshot(root)
    selection_path,selection_bytes,selection,groups,bound=_load(drafts,root,snapshot)
    if type(chunks) is not int or chunks<1:raise ValueError('positive chunk count required')
    if expected_count is not None and len(bound)!=expected_count:raise ValueError('unexpected record count')
    output=_safe_output(output,root,[drafts])
    snapshot.check_unchanged()
    output.mkdir(parents=True,exist_ok=False)
    count=min(chunks,len(bound));q,r=divmod(len(bound),count);start=0;chunk_bindings={}
    for i in range(count):
        size=q+(i<r);rows=bound[start:start+size]
        name=f'chunk-{i+1:02d}.json'
        _write(output/name,{'schema':'scene-sweep-chunk-v2','standard':STANDARD,'records':rows})
        data=(output/name).read_bytes()
        chunk_bindings[name]={'raw_sha256':raw_sha(data),'bytes':len(data),'count':len(rows)}
        start+=size
    assert start==len(bound)
    snapshot.check_unchanged()
    manifest={'schema':SCHEMA,'status':'IMMUTABLE_INPUT_ONLY_NOT_ACCEPTANCE',
       'record_count':len(bound),'chunk_count':count,'chunks':chunk_bindings,
       'selection_path':selection_path.relative_to(root).as_posix(),
       'selection_raw_sha256':raw_sha(selection_bytes),'source_bindings':snapshot.bindings(),
       'ordered_ids_sha256':object_sha([x['record']['id'] for x in bound]),
       'output_contract':'Write scene_spec patches to a NEW output directory. Never rewrite these files.',
       'canonical_hash_algorithm':'sha256-json-ensure_ascii_false-sort_keys_true-compact',
       'publisher_hash_algorithm':'sha256-json-ensure_ascii_false-sort_keys_true-default_spaces',
       'production_admission':False}
    _write(output/'inputs.json',manifest)
    for path in output.iterdir():_readonly(path)
    return manifest

def verify_inputs(input_dir,*,root=ROOT,snapshot=None):
    root=Path(root).resolve();input_dir=Path(input_dir).resolve()
    snapshot=Snapshot(root) if snapshot is None else snapshot
    manifest=json_object(snapshot.read(input_dir/'inputs.json'))
    if manifest.get('schema')!=SCHEMA:raise ValueError('input manifest schema mismatch')
    chunks=manifest.get('chunks')
    if not isinstance(chunks,dict) or not chunks:raise ValueError('missing chunks')
    records=[];seen=set()
    for name,item in sorted(chunks.items()):
        if not re.fullmatch(r'chunk-\d{2}\.json',name):raise ValueError('invalid chunk filename')
        data=snapshot.read(input_dir/name)
        if raw_sha(data)!=item['raw_sha256'] or len(data)!=item['bytes']:
            raise ValueError('immutable chunk bytes changed')
        packet=json_object(data)
        if packet.get('schema')!='scene-sweep-chunk-v2':raise ValueError('chunk schema mismatch')
        rows=packet.get('records')
        if not isinstance(rows,list) or not rows or len(rows)!=item['count']:raise ValueError('empty/count mismatch')
        for row in rows:
            if type(row.get('idx')) is not int or row['idx']!=len(records):raise ValueError('record ordering mismatch')
            record=row.get('record');binding=row.get('binding')
            if not isinstance(record,dict) or not isinstance(binding,dict):raise ValueError('full record/binding missing')
            pid=record.get('id')
            if not isinstance(pid,str) or pid in seen:raise ValueError('duplicate/missing ID')
            seen.add(pid)
            if object_sha(record)!=binding['record_canonical_sha256']:raise ValueError('record canonical SHA mismatch')
            if sorted_sha(record)!=binding['publisher_record_sorted_sha256']:raise ValueError('record publisher SHA mismatch')
            source=snapshot.read(root/binding['source_path'])
            if raw_sha(source)!=binding['source_raw_sha256']:raise ValueError('record source SHA changed')
            if fingerprint(source)['sha256']!=binding['source_normalized_sha256']:raise ValueError('normalized source SHA changed')
            lines=source.decode('utf-8-sig').splitlines();line_number=binding['source_line']
            if type(line_number) is not int or not 1<=line_number<=len(lines):raise ValueError('source line invalid')
            line=lines[line_number-1]
            if raw_sha(line.encode('utf-8'))!=binding['raw_line_sha256']:raise ValueError('raw line SHA mismatch')
            if json_object(line.encode('utf-8'))!=record:raise ValueError('record/source mismatch')
            records.append(row)
    if len(records)!=manifest.get('record_count') or len(chunks)!=manifest.get('chunk_count'):
        raise ValueError('manifest coverage mismatch')
    if object_sha([x['record']['id'] for x in records])!=manifest.get('ordered_ids_sha256'):
        raise ValueError('ordered ID coverage mismatch')
    for rel,item in manifest.get('source_bindings',{}).items():
        data=snapshot.read(root/rel)
        if raw_sha(data)!=item['raw_sha256'] or len(data)!=item['bytes']:
            raise ValueError('source binding changed')
    if raw_sha(snapshot.read(root/manifest['selection_path']))!=manifest['selection_raw_sha256']:
        raise ValueError('selector changed')
    snapshot.check_unchanged()
    return manifest,records

def _invalidate(row,version,source_record_sha):
    row=copy.deepcopy(row)
    for key in ('admitted','training_admitted','render_verified','animation_verified'):row[key]=False
    row['draft_status']='STAGED_NOT_ADMITTED'
    row['versioned_id']=version+'-'+row['id']
    row['strict_review']={'status':'PENDING_NEW_VERSION_REVIEW','source_record_sha256':source_record_sha,
       'math_content_sha256':sorted_sha({k:row[k] for k in MATH_FIELDS}),
       'scene_semantic_review':'PENDING','visual_review':'PENDING'}
    return row

def stage_scene_patches(drafts,patch_path,output,version,*,input_dir,root=ROOT):
    root=Path(root).resolve()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}',version):raise ValueError('invalid version')
    snapshot=Snapshot(root)
    manifest,inputs=verify_inputs(input_dir,root=root,snapshot=snapshot)
    ip=Path(input_dir).resolve()
    # Bind every input byte used by verification and recheck at the final write boundary.
    snapshot.read(ip/'inputs.json')
    for name in manifest['chunks']:snapshot.read(ip/name)
    selection_path,selection_bytes,selection,groups,bound=_load(drafts,root,snapshot)
    if raw_sha(selection_bytes)!=manifest['selection_raw_sha256']:raise ValueError('input/current selector differ')
    if [x['record']['id'] for x in inputs]!=[x['record']['id'] for x in bound]:
        raise ValueError('input/current coverage differs')
    for a,b in zip(inputs,bound):
        if a['record']!=b['record']:raise ValueError('input/current record differ')
    patch_path=Path(patch_path).resolve()
    packet=json_object(snapshot.read(patch_path));patches=packet.get('records')
    if not isinstance(patches,list) or not patches:raise ValueError('nonempty patches required')
    targets={x['record']['id']:x for x in bound};changes={};reviewed=[]
    for patch in patches:
        if not isinstance(patch,dict):raise ValueError('patch object required')
        pid=patch.get('id')
        if pid not in targets or pid in changes:raise ValueError('unknown/duplicate patch ID')
        item=targets[pid];before=item['record'];binding=item['binding']
        if patch.get('batch')!=binding['batch']:raise ValueError('patch batch mismatch')
        expected_path=selected_path(drafts,{'batch':patch['batch'],'path':patch.get('expected_selected_path')})
        if expected_path!=(root/binding['source_path']).resolve():raise ValueError('patch source/current differs')
        if patch.get('expected_hash_algorithm')!=NORMALIZED_HASH:raise ValueError('patch hash algorithm mismatch')
        if patch.get('expected_selected_sha256')!=binding['source_normalized_sha256'] or patch.get('expected_selected_raw_sha256')!=binding['source_raw_sha256']:
            raise ValueError('patch source file SHA mismatch')
        if patch.get('expected_record_sha256')!=sorted_sha(before):raise ValueError('patch record SHA mismatch')
        fields=patch.get('fields')
        if not isinstance(fields,dict) or set(fields)!={'scene_spec'}:
            raise ValueError('scene-only workflow forbids mathematics/other field changes')
        _scene(fields['scene_spec']);after=copy.deepcopy(before);after.update(copy.deepcopy(fields))
        if patch.get('new_math_content_sha256')!=sorted_sha({k:after[k] for k in MATH_FIELDS}):
            raise ValueError('patch resulting content SHA mismatch')
        changes[pid]=after
        reviewed.append({'id':pid,'before_record_canonical_sha256':object_sha(before),
          'after_scene_canonical_sha256':object_sha(after['scene_spec']),'mathematics_three_fields_unchanged':True})
    output=_safe_output(output,root,[drafts,input_dir,patch_path])
    snapshot.check_unchanged();output.mkdir(parents=True,exist_ok=False)
    candidate=copy.deepcopy(selection);candidate['entries']=[]
    candidate.update(status='UNSELECTED_NOT_ADMITTED',updated_by='scene-staging-only',
       original_selection_raw_sha256=raw_sha(selection_bytes))
    for entry,source,data,rows in groups:
        staged=[_invalidate(changes.get(row['id'],row),version,object_sha(row)) for row in rows]
        rel=Path(entry['batch'])/('draft-'+version+'.jsonl')
        fp=publish_jsonl(output/rel,staged)
        new_entry=copy.deepcopy(entry)
        for field in ('report_path','root_report_path','report_sha256','report_raw_sha256','report_hash_algorithm'):
            new_entry.pop(field,None)
        new_entry.update(path=rel.as_posix(),root_path=(output/rel).relative_to(root).as_posix(),
          version=version,**fp,source_path=source.relative_to(root).as_posix(),
          source_sha256=fingerprint(data)['sha256'],source_raw_sha256=raw_sha(data),
          source_hash_algorithm=NORMALIZED_HASH)
        candidate['entries'].append(new_entry)
    snapshot.check_unchanged()
    receipt={'schema':'scene-staging-receipt-v2','status':'STAGED_UNSELECTED_NOT_ADMITTED',
      'version':version,'patch_count':len(changes),'record_count':len(bound),
      'inputs_manifest_raw_sha256':raw_sha(snapshot.read(ip/'inputs.json')),
      'patches_raw_sha256':raw_sha(snapshot.read(patch_path)),
      'source_bindings':snapshot.bindings(),'patch_checks':reviewed,
      'production_selector_updated':False,'visual_verified':False,'training_admitted':False}
    _write(output/'draft-selection.candidate.json',candidate);_write(output/'stage-receipt.json',receipt)
    for path in output.rglob('*'):
        if path.is_file():_readonly(path)
    return receipt
