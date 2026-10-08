"""Bind structural-screen diagnosis to the full current population and known labels.
The known 228 pairs are development/diagnostic data, never an independent holdout.
"""
from __future__ import annotations
import argparse,json,hashlib,sys
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'src')]
from animtrain.structural_leakage import compare,implementation_sha256,VERSION
from tools.leakage_population import census


def diagnostic(population, labels, additional):
    lookup={x['pair_id']:x for x in population['pairs']}
    for x in additional['leakage_pairs']:
        pair_id=hashlib.sha256((x['query_hash']+x['train_hash']).encode()).hexdigest()[:20]
        lookup[pair_id]={'query':{'problem':x['query_problem']},'train':{'problem':x['train_problem']}}
    outcomes=[];cm={'tp':0,'fp':0,'fn':0,'tn':0}
    for label in labels['annotations']:
        pair=lookup[label['pair_id']];prediction=compare(pair['query']['problem'],pair['train']['problem'])
        key=('tp' if prediction['candidate'] else 'fn') if label['label']=='泄漏' else ('fp' if prediction['candidate'] else 'tn')
        cm[key]+=1;outcomes.append({**label,'prediction':prediction,'result':key})
    return {'rule':VERSION,'implementation_sha256':implementation_sha256(),'counts':cm,
            'recall':str(Fraction(cm['tp'],cm['tp']+cm['fn'])) if cm['tp']+cm['fn'] else None,
            'fpr':str(Fraction(cm['fp'],cm['fp']+cm['tn'])) if cm['fp']+cm['tn'] else None,
            'calibrated':False,'usage':'DEVELOPMENT_DIAGNOSTIC; not independent held-out validation',
            'records':outcomes}


def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args(argv)
    output=a.output.resolve()
    if not output.is_relative_to(ROOT) or output.exists():p.error('Fresh output inside project required')
    old=ROOT/'reviews/codex-supervision/2026-10-05-readiness-completion'
    loads=lambda name:json.loads((old/name).read_text(encoding='utf-8'))
    diag=diagnostic(loads('leakage-population.json'),loads('independent-leakage-labels-v2.json'),loads('cross-signature-leakage-findings.json'))
    pop=census(ROOT/'data/manifest.json',ROOT/'data')
    candidates=[]
    for pair in pop['pairs']:
        result=compare(pair['query']['problem'],pair['train']['problem'])
        if result['candidate']:candidates.append({**pair,'structural_screen':result})
    report={'manifest_sha256':pop['manifest_sha256'],'source_sha256':pop['source_sha256'],
            'implementation_sha256':implementation_sha256(),'diagnostic':diag,
            'total_pairs':pop['candidate_pairs'],'candidates':candidates,'calibrated':False,
            'policy':'Candidate screen only. Unmatched pairs remain UNKNOWN. No automatic leakage labels or restoration.'}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'counts':diag['counts'],'recall':diag['recall'],'fpr':diag['fpr'],'current_candidates':len(candidates),'calibrated':False},ensure_ascii=False))
if __name__=='__main__':raise SystemExit(main())
