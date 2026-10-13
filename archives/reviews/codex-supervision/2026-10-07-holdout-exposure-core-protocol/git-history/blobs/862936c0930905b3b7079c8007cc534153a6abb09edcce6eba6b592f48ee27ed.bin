"""Create a new bound area candidate by ID; never overwrite an earlier candidate."""
import copy,hashlib,json,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).parent
SOURCE=ROOT/'data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl'
STEPS=['第一步：画出两条边界曲线','第二步：标出两个交点','第三步：填充封闭区域','第四步：展示面积微元','第五步：计算定积分面积']

def main():
    raw=SOURCE.read_bytes()
    rows=[json.loads(line) for line in raw.decode('utf-8').splitlines() if line.strip()]
    matches=[row for row in rows if row.get('id')=='calc-area-007']
    if len(matches)!=1:raise ValueError('Source ID missing or duplicated')
    original=matches[0];candidate=copy.deepcopy(original)
    candidate['scene_spec']['steps']=STEPS
    if len(STEPS)!=5 or any(len(step)>28 for step in STEPS):raise ValueError('Navigation layout invalid')
    for field in ('problem','solution','answer'):
        if candidate[field].encode('utf-8')!=original[field].encode('utf-8'):raise ValueError('Math field drift: '+field)
    out=HERE/('calc-area-007.corrected-v2-'+uuid.uuid4().hex+'.candidate.jsonl')
    receipt=out.with_suffix('.receipt.json')
    if SOURCE.read_bytes()!=raw:raise ValueError('Source changed during preparation')
    with out.open('x',encoding='utf-8',newline='\n') as stream:stream.write(json.dumps(candidate,ensure_ascii=False)+'\n')
    proof={'status':'DRAFT_UNSELECTED_NOT_ADMITTED','source':str(SOURCE),'source_raw_sha256':hashlib.sha256(raw).hexdigest(),
           'candidate':str(out),'candidate_raw_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
           'math_three_fields_byte_equal':True,'scene_source_raw_sha256':hashlib.sha256((HERE/'scene.py').read_bytes()).hexdigest(),
           'full_surface_accepted':False,'rendered':False,'accepted':False}
    with receipt.open('x',encoding='utf-8',newline='\n') as stream:stream.write(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(proof,ensure_ascii=False))
    return 0

if __name__=='__main__':raise SystemExit(main())