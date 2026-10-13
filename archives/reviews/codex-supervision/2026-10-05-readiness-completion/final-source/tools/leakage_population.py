"""Source-bound cross-split population; exact fractions, no automatic labels.
By default include DIFFERENT signatures too: they may conceal structural leaks.
This census does not calibrate the text detector or enable a training gate.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from animtrain.kp_rule import kp_signature
from animtrain.manifest import canonical_problem_hash
from animtrain.near_dup import shingles
BOUNDS = [Fraction(0), Fraction(1,5), Fraction(3,10), Fraction(2,5), Fraction(3,5), Fraction(1)]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def census(manifest, data_root, same_signature_only=False):
    groups = {}
    sources = {}
    counts = Counter()
    missing = []
    for entry in json.loads(manifest.read_text(encoding='utf-8'))['entries']:
        if entry['split'] not in ('train','eval','test'):
            continue
        path = (data_root / entry['path']).resolve()
        if not path.is_relative_to(ROOT) or digest(path) != entry['sha256']:
            raise ValueError('Source path/hash mismatch: ' + str(path))
        sources[entry['path']] = digest(path)
        for i,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
            if not line.strip():
                continue
            rec = json.loads(line)
            if not isinstance(rec,dict) or not isinstance(rec.get('problem'),str) or not rec['problem'].strip():
                raise ValueError('Missing complete problem: ' + str(path))
            counts[entry['split']] += 1
            h = canonical_problem_hash(line)
            try:
                signature = kp_signature(rec)
            except ValueError:
                signature = None
                missing.append({'path':entry['path'],'line':i,'id':rec.get('id')})
            key = (entry['split'],h)
            group = groups.setdefault(key,{'split':entry['split'],'hash':h,'problem':rec['problem'],'signature':signature,'sources':[],'shingles':shingles(rec['problem'])})
            if group['signature'] != signature:
                raise ValueError('Same problem has conflicting signatures: ' + h)
            group['sources'].append({'id':rec['id'],'path':entry['path'],'line':i,'row_sha256':hashlib.sha256(line.strip().encode()).hexdigest()})
    train = [g for g in groups.values() if g['split']=='train']
    queries = [g for g in groups.values() if g['split'] in ('eval','test')]
    pairs = []
    strata = Counter()
    for query in queries:
        for example in train:
            same = query['signature'] is not None and query['signature']==example['signature']
            if same_signature_only and not same:
                continue
            a,b = query['shingles'],example['shingles']
            score = Fraction(len(a&b),len(a|b)) if a|b else Fraction(0)
            band = next(i for i in range(5) if BOUNDS[i]<=score and (score<BOUNDS[i+1] or i==4))
            strata[query['split']+'|same_signature='+str(same)+'|'+str(BOUNDS[band])+'..'+str(BOUNDS[band+1])] += 1
            pairs.append({'pair_id':hashlib.sha256((query['hash']+example['hash']).encode()).hexdigest()[:20],'split':query['split'],'same_signature':same,'j5':str(score),'intersection':len(a&b),'union':len(a|b),'band':band,'query':{k:query[k] for k in ('hash','problem','signature','sources')},'train':{k:example[k] for k in ('hash','problem','signature','sources')}})
    return {'manifest_sha256':digest(manifest),'implementation_sha256':digest(Path(__file__)),'source_sha256':sources,'raw_record_counts':dict(counts),'unique_problem_counts':dict(Counter(g['split'] for g in groups.values())),'candidate_pairs':len(pairs),'same_signature_pairs':sum(p['same_signature'] for p in pairs),'missing_signatures':missing,'strata':dict(sorted(strata.items())),'pairs':pairs,'automatically_labeled':False,'calibrated':False}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,default=ROOT/'data/manifest.json')
    parser.add_argument('--data-root',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--same-signature-only',action='store_true')
    args=parser.parse_args(argv)
    manifest=args.manifest.resolve()
    data_root=(args.data_root or manifest.parent).resolve()
    output=args.output.resolve()
    if not all(p.is_relative_to(ROOT) for p in (manifest,data_root,output)):
        parser.error('All paths must be in this project')
    if output.exists():
        parser.error('Output already exists; preserve historical evidence')
    result=census(manifest,data_root,args.same_signature_only)
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x',encoding='utf-8') as stream:
        json.dump(result,stream,ensure_ascii=False,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('pairs','source_sha256','strata')},ensure_ascii=False))
    return 0
if __name__=='__main__':
    raise SystemExit(main())
