"""Source-bound leakage-screen diagnostics, never independent calibration.

Use v2 pairs and fresh, explicitly hash-bound manual labels. Unknown structures
are unreviewed candidates/UNKNOWN, not certified non-leaks. Empirical ratios are
exact fractions on this stratified sample, not estimates of production rates.
"""
from __future__ import annotations
import argparse
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'src')]
from animtrain.near_dup import shingles
from animtrain.kp_rule import kp_signature
from animtrain.structural_leakage import compare
from build_holdout_pairs import build_dataset
from holdout_contract import (Snapshot, PAIR_SCHEMA, LABEL_SCHEMA, SCORE_SCHEMA,
    INDEPENDENCE, RULE_SHA, raw_sha, strict_json, required_text, require_pairs,
    make_pair, write_new_json)
MIN_RECALL = Fraction(19, 20)
MAX_FPR = Fraction(1, 100)
J5_THRESHOLD = Fraction(2, 5)

def load_labels(path, pairs_data, pairs_sha, snapshot):
    data = strict_json(snapshot.read(path))
    if not isinstance(data, dict) or data.get('schema') != LABEL_SCHEMA or data.get('pairs_raw_sha256') != pairs_sha or data.get('labeling_rule_sha256') != RULE_SHA:
        raise ValueError('label schema/subject/rule binding mismatch; v2 labels required')
    required_text(data, 'labeler')
    labs = data.get('labels')
    if not isinstance(labs, list):
        raise ValueError('label list required')
    expected = {p['pair_id']: p for p in pairs_data['pairs']}; out = {}
    for lab in labs:
        if not isinstance(lab, dict):
            raise ValueError('label object required')
        pid = required_text(lab, 'pair_id')
        if pid in out or pid not in expected:
            raise ValueError('duplicate or extra label: ' + pid)
        pair = expected[pid]
        if any(lab.get(side + '_problem_sha256') != pair[side]['problem_sha256'] for side in ('query', 'train')):
            raise ValueError('label problem binding mismatch: ' + pid)
        if lab.get('label') not in ('泄漏', '不泄漏', '不确定'):
            raise ValueError('missing or invalid manual label: ' + pid)
        required_text(lab, 'reason'); out[pid] = lab
    if set(out) != set(expected):
        raise ValueError('labels do not cover pairs 1:1')
    return out, data['labeler']

def sig_of(rec):
    try:
        return kp_signature(rec)
    except ValueError:
        return None

def j5_fraction(a, b):
    sa, sb = shingles(a), shingles(b)
    return Fraction(len(sa & sb), len(sa | sb)) if sa | sb else Fraction(0)

def metrics(c):
    tp, fp, fn, tn = (c[k] for k in ('tp', 'fp', 'fn', 'tn'))
    recall = Fraction(tp, tp + fn) if tp + fn else None
    fpr = Fraction(fp, fp + tn) if fp + tn else None
    return {'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn, 'uncertain': c['uncertain'],
            'recall': str(recall) if recall is not None else None,
            'fpr': str(fpr) if fpr is not None else None,
            'empirical_targets_met': bool(c['uncertain'] == 0 and recall is not None and fpr is not None
                                         and recall >= MIN_RECALL and fpr <= MAX_FPR),
            'calibrated': False}

def score(pairs, strata, labels, query_lookup, draft_lookup):
    ids = require_pairs(pairs)
    if set(strata) != ids or set(labels) != ids:
        raise ValueError('pair/stratum/label identities mismatch')
    rows = []; cm = {k: Counter() for k in ('combined', 'structural', 'union')}
    per = defaultdict(lambda: {k: Counter() for k in cm})
    for p in pairs:
        pid = p['pair_id']; lab = labels[pid]; label = lab.get('label')
        if label not in ('泄漏', '不泄漏', '不确定'):
            raise ValueError('invalid label')
        q = query_lookup[p['query']['id']]; t = draft_lookup[p['train']['id']]
        if make_pair(t, q) != p:
            raise ValueError('pair differs from actual source question/metadata: ' + pid)
        sq, st = sig_of(q), sig_of(t); same = sq is not None and sq == st
        j5 = j5_fraction(q['problem'], t['problem']); combined = same and j5 >= J5_THRESHOLD
        structural_result = compare(q['problem'], t['problem']); structural = bool(structural_result['candidate'])
        preds = {'combined': combined, 'structural': structural, 'union': combined or structural}
        for screen, pred in preds.items():
            key = 'uncertain' if label == '不确定' else (('tp' if pred else 'fn') if label == '泄漏' else ('fp' if pred else 'tn'))
            cm[screen][key] += 1; per[strata[pid]][screen][key] += 1
        rows.append({'pair_id': pid, 'label': label, 'sig_equal': same, 'j5': str(j5),
                     **preds, 'structural_coverage': structural_result.get('coverage', 'UNKNOWN'),
                     'structural_verdict': 'CANDIDATE_REQUIRES_REVIEW' if structural else 'UNKNOWN',
                     'reason': lab.get('reason', '')})
    return {'schema': SCORE_SCHEMA, 'status': 'DEVELOPMENT_DIAGNOSTIC',
            'independence': INDEPENDENCE.copy(), 'calibrated': False,
            'targets': {'min_recall': str(MIN_RECALL), 'max_fpr': str(MAX_FPR), 'j5_threshold': str(J5_THRESHOLD)},
            'denominator_scope': 'manually labeled finite stratified sample; no production-rate estimate; uncertain labels counted separately',
            'pair_count': len(rows), 'label_counts': dict(Counter(r['label'] for r in rows)),
            'screens': {k: metrics(v) for k, v in cm.items()},
            'per_stratum': {s: {k: metrics(c) for k, c in cs.items()} for s, cs in sorted(per.items())},
            'rows': rows}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    for flag in ('pairs', 'labels', 'out'):
        ap.add_argument('--' + flag, type=Path, required=True)
    args = ap.parse_args(argv)
    try:
        if args.out.exists():
            raise ValueError('output exists: use a new path')
        snap = Snapshot(); pairs_bytes = snap.read(args.pairs); data = strict_json(pairs_bytes)
        if not isinstance(data, dict) or data.get('schema') != PAIR_SCHEMA:
            raise ValueError('v1 is unbound development data; rebuild a new v2 diagnostic and label it')
        rebuilt, strata, drafts, queries = build_dataset(snap)
        # build_dataset binding excludes submitted pairs: compare only captured source files.
        source_bindings = {k: v for k, v in rebuilt['source_bindings'].items()
                           if k != args.pairs.resolve().relative_to(ROOT).as_posix()}
        rebuilt['source_bindings'] = source_bindings
        if data != rebuilt:
            raise ValueError('pairs, sampling protocol or source bindings differ from frozen rebuild')
        labels, labeler = load_labels(args.labels, data, raw_sha(pairs_bytes), snap)
        for rel in ['tools/score_holdout.py', 'src/animtrain/structural_leakage.py',
                    'src/animtrain/kp_rule.py', 'src/animtrain/near_dup.py', 'src/animtrain/validate.py']:
            snap.read(ROOT / rel)
        report = score(data['pairs'], strata, labels, {q['id']: q for q in queries}, {d['id']: d for d in drafts})
        report['bindings'] = {'inputs': snap.bindings(), 'pairs_sha256': raw_sha(pairs_bytes),
                              'labels_sha256': raw_sha(snap.read(args.labels)), 'labeler': labeler,
                              'labeling_rule_sha256': RULE_SHA}
        write_new_json(args.out, report, snap)
        print(__import__('json').dumps({'status': report['status'], 'calibrated': False,
              'pair_count': report['pair_count'], 'screens': report['screens']}, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('[FAIL]', exc); return 2

if __name__ == '__main__':
    sys.exit(main())
