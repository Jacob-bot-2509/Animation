"""Generated area candidate: honor CLOSED; no trusted render bypass."""
import hashlib,json,sys,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'src'))
HERE=Path(__file__).parent

def main():
    from animtrain.render_gate import render_check
    source=HERE/'scene.py';raw=source.read_bytes();code=raw.decode('utf-8')
    result=render_check(code,trusted=False)
    result['scene_source_raw_sha256']=hashlib.sha256(raw).hexdigest()
    result['full_surface_accepted']=False
    result['accepted']=False
    output=HERE/('render-v2-'+uuid.uuid4().hex+'.json')
    with output.open('x',encoding='utf-8',newline='\n') as stream:stream.write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'path':str(output),'ok':result['ok'],'status':result['status']},ensure_ascii=False))
    return 0 if result['ok'] else 3

if __name__=='__main__':raise SystemExit(main())