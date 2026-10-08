"""Check reviewed per-concept training coverage without model loading or gate release.
This validates the review ledger bindings, not an independent leakage classifier.
"""
from pathlib import Path
import json,hashlib

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def check_training_diversity(manifest:Path,policy_path:Path,evidence_path:Path)->tuple[bool,str]:
    try:
        manifest=manifest.resolve();base=manifest.parent
        policy=json.loads(policy_path.read_text(encoding='utf8'))
        if policy.get('schema')!=1:return False,'Unsupported training diversity policy'
        required=policy['concepts'];concepts={x['id']:x for x in required}
        minimum=policy['min_reviewed_samples_per_concept'];forms_min=policy['min_distinct_variant_kinds_per_concept']
        if not concepts or len(concepts)!=len(required) or type(minimum)!=int or minimum<5 or type(forms_min)!=int or forms_min<3:
            return False,'Invalid training diversity concept policy'
        if not evidence_path.is_file():return False,'Training diversity review evidence is absent'
        evidence=json.loads(evidence_path.read_text(encoding='utf8'))
        if evidence.get('schema')!=1 or evidence.get('status')!='VERIFIED':return False,'Training diversity evidence is not VERIFIED'
        if evidence.get('manifest_sha256')!=sha(manifest) or evidence.get('policy_sha256')!=sha(policy_path):
            return False,'Training diversity review bindings are stale'
        m=json.loads(manifest.read_text(encoding='utf8'));rows={};heldout_rows={}
        for entry in m['entries']:
            p=(base/entry['path']).resolve()
            if not p.is_relative_to(base) or not p.is_file() or sha(p)!=entry['sha256']:
                return False,'Manifest input is missing, escaped or hash-mismatched'
            if entry['split']!='train':
                if entry['split'] in ('eval','test'):
                    for line in p.read_bytes().splitlines(keepends=True):
                        if line.strip():
                            query=json.loads(line);qid=query['id']
                            if qid in heldout_rows:return False,'Duplicate held-out record ID'
                            heldout_rows[qid]=hashlib.sha256(line).hexdigest()
                continue
            for line in p.read_bytes().splitlines(keepends=True):
                if not line.strip():continue
                row=json.loads(line);rid=row['id']
                if rid in rows:return False,'Duplicate active training ID'
                problem=row['problem']
                if not isinstance(problem,str) or not problem.strip():return False,'Invalid active problem text'
                rows[rid]={'sha256':hashlib.sha256(line).hexdigest(),'problem':' '.join(problem.split()),'category':row['category']}
        known_cases=policy.get('known_overlap_cases',[])
        if not isinstance(known_cases,list):return False,'Invalid known overlap risk ledger'
        for case in known_cases:
            if not isinstance(case,dict) or not all(isinstance(case.get(k),str) and case[k] for k in ('train_id','query_id','query_row_sha256')):
                return False,'Invalid known overlap case binding'
            if case['train_id'] in rows and heldout_rows.get(case['query_id'])==case['query_row_sha256']:
                return False,'Known train/held-out overlap remains: '+case['train_id']+' / '+case['query_id']
        reviews=evidence['record_reviews'];seen=set();seen_problems=set();counts={x:0 for x in concepts};forms={x:set() for x in concepts}
        for review in reviews:
            rid=review['id'];cid=review['concept_id']
            if rid not in rows or rid in seen or cid not in concepts:return False,'Review ledger IDs are unknown or repeated'
            if review.get('row_sha256')!=rows[rid]['sha256']:return False,'Reviewed training row is stale'
            if rows[rid]['category']!=concepts[cid]['category']:return False,'Concept category does not match active row'
            if review.get('user_review')!='APPROVED' or review.get('independent_math_verified') is not True or review.get('independent_diversity_verified') is not True or review.get('leakage_status')!='CLEAR':
                return False,'Training record has pending user/math/diversity/leakage review'
            kind=review.get('variant_kind')
            if not isinstance(kind,str) or not kind.strip():return False,'Reviewed variant form is missing'
            fingerprint=rows[rid]['problem']
            if fingerprint in seen_problems:return False,'Repeated problem text cannot count as a new sample'
            seen.add(rid);seen_problems.add(fingerprint);counts[cid]+=1;forms[cid].add(kind)
        if seen!=set(rows):return False,'Review ledger does not cover all active training records'
        missing=[cid for cid in concepts if counts[cid]<minimum or len(forms[cid])<forms_min]
        if missing:return False,'Training diversity coverage incomplete: '+','.join(missing[:8])
        return True,'Reviewed training diversity coverage complete; other readiness gates still apply'
    except (OSError,ValueError,KeyError,TypeError,AttributeError) as exc:
        return False,'Training diversity evidence is invalid: '+type(exc).__name__
