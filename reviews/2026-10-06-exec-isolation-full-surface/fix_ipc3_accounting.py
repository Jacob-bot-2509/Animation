"""Read-only analysis of old raw3; count-only logs cannot attribute sandbox traffic."""
from pathlib import Path
import hashlib,json,uuid

def main():
    source=Path(__file__).with_name('probe-raw-ipc3-v1-results.json')
    raw=source.read_bytes();record=json.loads(raw)
    analysis={'schema':'ipc3-readonly-accounting-v2','source':str(source),
              'source_raw_sha256':hashlib.sha256(raw).hexdigest(),
              'status':'UNKNOWN','production_gate':'CLOSED','original_modified':False,
              'reason':'Raw hit counts lack exact per-phase nonces; neither sandbox delivery nor zero delivery can be certified.',
              'original_after':record.get('after',{})}
    output=source.with_name('ipc3-accounting-v2-'+uuid.uuid4().hex+'.json')
    with output.open('x',encoding='utf-8',newline='\n') as stream:
        stream.write(json.dumps(analysis,ensure_ascii=False,indent=2)+'\n')
    if source.read_bytes()!=raw:raise RuntimeError('Raw source changed during analysis')
    print(output)
    return 3

if __name__=='__main__':raise SystemExit(main())
