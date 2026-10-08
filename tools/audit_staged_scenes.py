"""Read-only staged scene integrity audit; successful output is not math or visual acceptance."""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SWEEP=ROOT/'reviews/2026-10-06-scene-standard-sweep'
sys.path.insert(0,str(ROOT/'tools'))
from draft_io import fingerprint,selected_path
from holdout_contract import json_object,jsonl,raw_sha

def strings(value):
    if isinstance(value,str): yield value
    elif isinstance(value,list):
        for item in value: yield from strings(item)
    elif isinstance(value,dict):
        for key,item in value.items():
            yield str(key)
            yield from strings(item)

def audit_staged(directory:Path,*,root:Path=ROOT)->dict:
    root=Path(root).resolve();directory=Path(directory).resolve()
    if not directory.is_relative_to(root): raise ValueError('candidate outside project')
    selection_path=directory/'draft-selection.candidate.json';receipt_path=directory/'stage-receipt.json'
    selection_bytes=selection_path.read_bytes();receipt_bytes=receipt_path.read_bytes()
    selection=json_object(selection_bytes);receipt=json_object(receipt_bytes)
    if selection.get('schema')!=2 or selection.get('status')!='UNSELECTED_NOT_ADMITTED':
        raise ValueError('unselected schema2 candidate required')
    if receipt.get('schema')!='scene-staging-receipt-v2' or receipt.get('status')!='STAGED_UNSELECTED_NOT_ADMITTED':
        raise ValueError('staged receipt required')
    for key in ('production_selector_updated','training_admitted','visual_verified'):
        if receipt.get(key) is not False: raise ValueError('candidate admission state '+key)
    entries=selection.get('entries');bindings=receipt.get('source_bindings')
    if not isinstance(entries,list) or not entries:raise ValueError('nonempty entries required')
    if not isinstance(bindings,dict) or not bindings:raise ValueError('source bindings required')
    checked={selection_path:selection_bytes,receipt_path:receipt_bytes};files=[];ids=set();batches=set();bad=[]
    def read(path):
        path=path.resolve()
        if not path.is_relative_to(root):raise ValueError('source outside project')
        data=path.read_bytes();checked[path]=data;return data
    for rel,item in bindings.items():
        data=read(root/rel)
        if raw_sha(data)!=item['raw_sha256'] or len(data)!=item['bytes']:raise ValueError('bound source changed: '+rel)
    total=0
    for entry in entries:
        if entry.get('batch') in batches:raise ValueError('duplicate batch')
        batches.add(entry.get('batch'));path=selected_path(directory,entry);data=read(path);fp=fingerprint(data)
        if any(entry.get(k)!=v for k,v in fp.items()):raise ValueError('candidate raw/normalized hash mismatch')
        records=jsonl(data)
        if type(entry.get('count')) is not int or entry['count']!=len(records) or not records:raise ValueError('entry count mismatch/empty')
        files.append(str(path.relative_to(root)))
        for row in records:
            pid=row.get('id')
            if not isinstance(pid,str) or not pid or pid in ids:raise ValueError('duplicate/missing ID')
            ids.add(pid);scene=row.get('scene_spec')
            if not isinstance(scene,dict):raise ValueError('scene object missing')
            for key in ('objects','steps'):
                vals=scene.get(key)
                if not isinstance(vals,list) or not vals or any(not isinstance(v,str) or not v.strip() for v in vals):raise ValueError('invalid scene '+key)
            for value in strings(scene):
                math_ranges=[(m.start(),m.end()) for m in re.finditer(r'(?<!\\)\$(.*?)(?<!\\)\$',value,re.S)]
                for offset,ch in enumerate(value):
                    cp=ord(ch)
                    # LF between prose substeps is intentional; inside inline TeX it is rejected.
                    if cp==10 and not any(start<=offset<end for start,end in math_ranges):continue
                    if cp<32 or 127<=cp<=159 or 0xD800<=cp<=0xDFFF or cp==0xFFFD:
                        bad.append({'id':pid,'codepoint':f'U+{cp:04X}','offset':offset})
            if any(row.get(key) is not False for key in ('admitted','training_admitted','render_verified','animation_verified')):
                raise ValueError('candidate carries acceptance flag')
        total+=len(records)
    if type(receipt.get('record_count')) is not int or receipt['record_count']!=total:raise ValueError('receipt record coverage mismatch')
    for path,data in checked.items():
        if path.read_bytes()!=data:raise ValueError('source changed while auditing')
    return {'directory':str(directory.relative_to(root)),'records':total,'files':files,'control_corruption':bad,
            'passed':not bad,'scope':'candidate/source byte integrity and scene control characters only',
            'math_verified':False,'visual_verified':False,'training_admitted':False}

def main(argv=None)->int:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--staged',type=Path,action='append');args=ap.parse_args(argv)
    targets=args.staged or [SWEEP/f'batch{n}-staged-v1' for n in range(1,11)]
    results=[];failed=False
    for target in targets:
        try:
            result=audit_staged(target);failed |= not result['passed'];results.append(result)
        except (OSError,ValueError,KeyError,TypeError) as exc:
            failed=True;results.append({'directory':str(target),'passed':False,'error':str(exc)})
    print(json.dumps({'results':results,'passed':not failed,'math_verified':False,'visual_verified':False},ensure_ascii=False,indent=2))
    return int(failed)
if __name__=='__main__':sys.exit(main())