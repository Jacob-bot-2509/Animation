"""Publish a new, exact-math shear candidate with source-bound checks.
No active dataset or manifest is modified. Automated non-alerts remain UNKNOWN;
only the two named spectral-template conflicts are independently distinguished.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from fractions import Fraction
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'src')]
from holdout_contract import Snapshot, json_object, jsonl, required_text, raw_sha, object_sha, write_new_json
from build_holdout_pairs import load_queries
from animtrain.kp_rule import kp_signature
from animtrain.near_dup import shingles
from animtrain.structural_leakage import compare
ACTIVE = ROOT/'data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl'
MANIFEST = ROOT/'data/manifest.json'
OUT = ROOT/'reviews/linalg048-rewrite-v2/linalg-048-rewrite-candidate.json'
REVIEWED_TARGET_HASHES = {'eval-linalg-015-s1':'7cf642a667f0a5f6ba93b6f87eb75d881cbf1505b723a6c45a3f89e4447a5ace',
                          'test-linalg-025':'d0889025edd38d043be6ccbaabf473ddc88a657d157cc537431e76b8887ba035'}
MATH_FIELDS = ('problem', 'solution', 'answer', 'scene_spec')
CHANGED_FIELDS = set(MATH_FIELDS) | {'function_family', 'visual_style', 'efficiency_tags'}
CANDIDATE = {'id': 'linalg-048',
 'category': '高等代数',
 'sub_category': '线性变换',
 'function_family': '线性变换',
 'visual_style': '空间几何图形',
 'efficiency_tags': ['几何意义', '剪切变换'],
 'problem': '已知矩阵 $A=\\begin{pmatrix}1&3\\\\0&1\\end{pmatrix}$，求该矩阵对应的线性变换对二维平面的几何影响。',
 'solution': '对任意点 '
             '$(x,y)$，$T(x,y)=A\\begin{pmatrix}x\\\\y\\end{pmatrix}=\\begin{pmatrix}x+3y\\\\y\\end{pmatrix}$，位移为 '
             '$(3y,0)$。故 $x$ 轴逐点固定，$\\vec e_1=(1,0)$ 不动，$\\vec e_2=(0,1)$ 映为 $(3,1)$。对于任意 $c\\in\\mathbb '
             'R$，$T(\\mathbb R\\times\\{c\\})=\\mathbb R\\times\\{c\\}$：整条水平直线作为点集保持不变，其上每个带标记点的横坐标增加 '
             '$3c$。有限线段 $[0,1]\\times\\{c\\}$ 则映为 $[3c,1+3c]\\times\\{c\\}$。竖直线 $x=c$ 的像可写为 '
             '$(X,Y)=(c+3t,t)$，$t\\in\\mathbb R$，即 $X-3Y=c$，斜率为 $\\frac13$。沿边界次序，单位正方形顶点 '
             '$(0,0),(1,0),(1,1),(0,1)$ 依次映为 $(0,0),(1,0),(4,1),(3,1)$，得到底长 $1$、高 $1$ 的平行四边形。$\\det '
             'A=1\\cdot1-3\\cdot0=1$，故面积与定向均保持。这是一种水平剪切；移动距离为 $3|y|$，纵坐标不变。长度一般不保持，例如 $\\|(0,1)\\|=1$ 而 '
             '$\\|T(0,1)\\|=\\sqrt{10}$。',
 'answer': '水平剪切 $T(x,y)=(x+3y,y)$；$x$ 轴逐点固定，水平直线作为点集不变、带标记点的位移为 $(3y,0)$；竖直线 $x=c$ 映为 '
           '$X-3Y=c$；面积和定向保持，$\\det A=1$，长度一般不保持。',
 'scene_spec': {'objects': ['带有刻度的黑色坐标轴',
                            '蓝色单位正方形，按边界次序连接 $(0,0),(1,0),(1,1),(0,1)$',
                            '橙色平行四边形，按边界次序连接 $(0,0),(1,0),(4,1),(3,1)$',
                            '青色有限线段 $[0,1]\\times\\{\\frac12\\}$ 和 '
                            '$[0,1]\\times\\{1\\}$，各自标记左端点；无限水平直线仅用作不变的参考线',
                            '白色板书 $T(x,y)=(x+3y,y)$、$\\det A=1$ 与 $X-3Y=c$'],
                'steps': ['第一步：绘制坐标轴与蓝色单位正方形，按边界次序标记四个顶点。',
                          '第二步：显示 $T(x,y)=(x+3y,y)$ 和 $\\det A=1$，说明 $x$ 轴逐点固定。',
                          '第三步：将两条有限线段分别平移 $\\frac32$ 和 $3$，终点线段为 '
                          '$[\\frac32,\\frac52]\\times\\{\\frac12\\}$ 和 '
                          '$[3,4]\\times\\{1\\}$；闪烁带标记端点，说明整条无限水平直线作为集合不变。',
                          '第四步：按原顶点对应关系变换为橙色平行四边形，依次高亮 $(0,0),(1,0),(4,1),(3,1)$，标注底 $1$、高 $1$、面积 $1$。',
                          '第五步：展示一条竖直参考线 $x=c$ 映为 $X-3Y=c$；以 $(0,1)\\mapsto(3,1)$ 说明长度由 $1$ 变为 '
                          '$\\sqrt{10}$，并重申面积保持。']},
 'source': 'self-authored',
 'license': 'Internal-Research-Use-Only'}
APPROVED_MATH_SHA256 = '343dd3027d09e6a6d9bfcb9d835b335da1dcbd7f479e63d65d201203ea3858a1'

def math_checks(candidate):
    if object_sha({k: candidate[k] for k in MATH_FIELDS}) != APPROVED_MATH_SHA256:
        raise ValueError('candidate mathematical content differs from independently reviewed template')
    match = re.search(r'\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}', candidate['problem'])
    if not match:
        raise ValueError('candidate matrix missing')
    matrix = [[Fraction(cell) for cell in row.split('&')] for row in match.group(1).split(r'\\')]
    if matrix != [[1,3],[0,1]]:
        raise ValueError('unexpected candidate matrix')
    def T(x,y):
        return (matrix[0][0]*x+matrix[0][1]*y, matrix[1][0]*x+matrix[1][1]*y)
    verts = [T(Fraction(x),Fraction(y)) for x,y in [(0,0),(1,0),(1,1),(0,1)]]
    det = matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
    area = sum(verts[i][0]*verts[(i+1)%4][1]-verts[(i+1)%4][0]*verts[i][1] for i in range(4))/2
    shifts = [T(0,Fraction(1,2))[0], T(0,1)[0]]
    slope = (T(0,1)[1]-T(0,0)[1])/(T(0,1)[0]-T(0,0)[0])
    norm2 = sum(z*z for z in T(0,1))
    if verts != [(0,0),(1,0),(4,1),(3,1)] or det != 1 or area != 1 or shifts != [Fraction(3,2),3] or slope != Fraction(1,3) or norm2 != 10:
        raise ValueError('exact geometry check failed')
    return {'matrix': [[str(x) for x in row] for row in matrix], 'det': str(det),
            'oriented_area': str(area), 'ordered_square_images': [[str(z) for z in v] for v in verts],
            'horizontal_segment_shifts': [str(z) for z in shifts], 'vertical_image_slope': str(slope),
            'e2_image_squared_norm': str(norm2), 'e2_image_norm': 'sqrt(10)',
            'horizontal_line_set': 'T(R x {c}) = R x {c}; bijective x -> x+3c',
            'reviewed_math_sha256': APPROVED_MATH_SHA256}

def load_population(snapshot):
    manifest = json_object(snapshot.read(MANIFEST)); entries = manifest.get('entries')
    if not isinstance(entries,list) or not entries:
        raise ValueError('manifest entries required')
    train, train_paths, seen = [], [], set()
    for entry in entries:
        if not isinstance(entry,dict):
            raise ValueError('manifest entry object required')
        if entry.get('split') not in ('train','eval','test'):
            continue
        path = (ROOT/'data'/entry['path']).resolve()
        if not path.is_relative_to(ROOT/'data') or path.suffix != '.jsonl' or raw_sha(snapshot.read(path)) != entry['sha256']:
            raise ValueError('manifest path/hash mismatch')
        if entry['split'] != 'train':
            continue
        if path in train_paths:
            raise ValueError('duplicate train source')
        train_paths.append(path)
        for row in jsonl(snapshot.read(path)):
            required_text(row,'id'); required_text(row,'problem')
            if row['id'] in seen:
                raise ValueError('duplicate active training ID')
            seen.add(row['id']); train.append(row)
    if ACTIVE.resolve() not in train_paths:
        raise ValueError('linalg source is not selected by active manifest')
    active = [r for r in train if r['id']=='linalg-048']
    if len(active) != 1:
        raise ValueError('exactly one active linalg-048 required')
    queries, aliases = load_queries(snapshot)
    for qid in ('eval-linalg-015-s1','test-linalg-025'):
        if qid not in aliases:
            raise ValueError('named target query missing: '+qid)
    others = [('train',r['id'],r) for r in train if r['id']!='linalg-048']
    others += [(q['_split'],q['id'],q) for q in queries]
    return active[0], others, aliases, {'active_train_records':len(train),
            'active_train_files':[p.relative_to(ROOT).as_posix() for p in train_paths],
            'unique_eval_test_questions':len(queries),
            'query_scene_records':sum(len(q['_source_records']) for q in queries)}

def j5(a,b):
    sa,sb = shingles(a),shingles(b)
    return Fraction(len(sa&sb),len(sa|sb)) if sa|sb else Fraction(0)

def check_candidate(candidate, active, others, aliases):
    if set(candidate) != set(active) or candidate['id'] != 'linalg-048' or active['id'] != 'linalg-048':
        raise ValueError('candidate identity/field schema differs from active row')
    if any(candidate[k] != active[k] for k in active if k not in CHANGED_FIELDS):
        raise ValueError('unapproved non-content field change')
    for alias,expected in REVIEWED_TARGET_HASHES.items():
        if alias not in aliases or raw_sha(aliases[alias]['problem'].encode('utf-8')) != expected:
            raise ValueError('named semantic-review target changed: '+alias)
    math = math_checks(candidate); rows = []; hits = []; sig = kp_signature(candidate)
    for split,oid,row in others:
        ratio = j5(candidate['problem'],row['problem']); same = kp_signature(row)==sig
        structural = compare(candidate['problem'],row['problem'])
        combined = same and ratio>=Fraction(2,5)
        item = {'split':split,'id':oid,'j5':str(ratio),'same_signature':same,
                'combined_candidate':combined,'structural_candidate':bool(structural['candidate']),
                'structural_coverage':structural.get('coverage','UNKNOWN')}
        rows.append(item)
        if combined or structural['candidate']:
            hits.append(item)
    if hits:
        raise ValueError('candidate screen requires review: '+json.dumps(hits,ensure_ascii=False))
    target_checks = []
    for alias in ('eval-linalg-015-s1','test-linalg-025'):
        q = aliases[alias]
        target_checks.append({'id':q['id'],'query_problem_sha256':raw_sha(q['problem'].encode('utf-8')),
            'j5':str(j5(candidate['problem'],q['problem'])),'same_signature':kp_signature(q)==sig,
            'semantic_verdict':'DIFFERENT_CORE_TASK_FOR_THIS_NAMED_PAIR',
            'basis':'Candidate is area-preserving horizontal shear [[1,3],[0,1]], with fixed x-axis and moving marked points; query computes the symmetric balanced 2x2 spectral decomposition. The shear has repeated eigenvalue 1 and one eigendirection; the named symmetric query has distinct eigenvalues 3 and -1 and orthogonal eigendirections. The requested tasks and algebraic cases differ.'})
    return {'status':'REWRITE_CANDIDATE_PENDING_FULL_SEMANTIC_AND_ASSET_REVIEW',
            'admitted':False,'render_verified':False,'active_manifest_modified':False,
            'global_leakage_free_certified':False,'non_alert_semantics':'UNKNOWN; no alert is not proof of no leakage',
            'math':math,'target_pair_checks':target_checks,'screens':rows,'automatic_candidate_count':0}

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,default=OUT)
    ap.add_argument('--checks',type=Path);args=ap.parse_args(argv)
    try:
        receipt=args.checks or args.out.with_suffix('.checks.json')
        if receipt.resolve()==args.out.resolve() or args.out.exists() or receipt.exists():
            raise ValueError('output exists or candidate/receipt collide: use new paths')
        snap=Snapshot()
        for rel in ['tools/prepare_linalg048_rewrite.py','tools/holdout_contract.py','tools/build_holdout_pairs.py',
                    'tools/draft_io.py','src/animtrain/kp_rule.py','src/animtrain/near_dup.py','src/animtrain/structural_leakage.py']:
            snap.read(ROOT/rel)
        active,others,aliases,population=load_population(snap)
        checks=check_candidate(CANDIDATE,active,others,aliases)
        checks['population']=population;checks['source_bindings']=snap.bindings()
        checks['active_record_sha256']=object_sha(active);checks['candidate_record_sha256']=object_sha(CANDIDATE)
        checks['candidate_raw_sha256']=write_new_json(args.out,CANDIDATE,snap)
        write_new_json(receipt,checks,snap)
        print(json.dumps({'candidate':str(args.out),'checks':str(receipt),'status':checks['status'],
                         'population':population,'automatic_candidate_count':0,'admitted':False},ensure_ascii=False))
        return 0
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print('[FAIL]',exc);return 2

if __name__=='__main__':sys.exit(main())
