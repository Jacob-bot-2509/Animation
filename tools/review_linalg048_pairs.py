"""Prepare complete source-bound semantic review material; never infer acceptance.

Outputs a PENDING review packet, not linalg048-manual-acceptance-v2.
The prior keyword/default writer manufactured DIFFERENT_CORE_TASK verdicts;
its artifacts remain historical and require actual independent semantic review.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'src')]
from holdout_contract import Snapshot, required_text, raw_sha, object_sha, RULE_SHA, write_new_json
import admit_linalg048_v3 as render_review
from prepare_linalg048_rewrite import load_population

PACKET_SCHEMA = 'linalg048-semantic-review-packet-v1'


def make_packet(candidate, evidence, others):
    subjects = evidence.get('semantic_subjects')
    if not isinstance(subjects, list) or not subjects:
        raise ValueError('bound semantic subjects required')
    rows = {}
    for split, pid, row in others:
        if split not in ('train', 'eval', 'test') or (split, pid) in rows:
            raise ValueError('duplicate or invalid population subject')
        rows[(split, pid)] = row
    seen = set()
    material = []
    labels = []
    for subject in subjects:
        key = (required_text(subject, 'split'), required_text(subject, 'id'))
        if key in seen or key not in rows:
            raise ValueError('duplicate or missing review subject')
        seen.add(key)
        row = rows[key]
        problem = required_text(row, 'problem')
        digest = raw_sha(problem.encode('utf-8'))
        if digest != required_text(subject, 'problem_sha256'):
            raise ValueError('review subject problem binding mismatch')
        variants = row.get('_source_records', [row])
        if not isinstance(variants, list) or not variants:
            raise ValueError('full source variants required')
        for variant in variants:
            for field in ('id', 'problem', 'solution', 'answer'):
                required_text(variant, field)
            pid = variant.get('problem_id') or variant['id']
            if pid != key[1] or variant['problem'] != problem:
                raise ValueError('variant question identity mismatch')
            if not isinstance(variant.get('scene_spec'), dict):
                raise ValueError('full scene specification required')
        # Include original complete records and their hashes, never regex verdicts.
        material.append({**subject, 'source_records': variants,
                         'source_record_sha256': [object_sha(v) for v in variants],
                         'status': 'PENDING_ACTUAL_REVIEW'})
        labels.append({**subject, 'verdict': None, 'reason': ''})
    if seen != set(rows):
        raise ValueError('review packet population coverage mismatch')
    return {'schema': PACKET_SCHEMA, 'status': 'PENDING_ACTUAL_REVIEW',
            'reviewer': None, 'accepted': False,
            'candidate': candidate, 'candidate_raw_sha256': evidence['candidate_raw_sha256'],
            'scene_raw_sha256': evidence['scene']['raw_sha256'],
            'media_raw_sha256': evidence['render_result']['output']['sha256'],
            'labeling_rule_sha256': RULE_SHA,
            'visual': {'verdict': None, 'reason': ''},
            'semantic_pairs': labels, 'review_material': material,
            'review_scope': {
                'same_core_with_changed_values_is_cross_split_leakage': True,
                'same_split_variants_need_truthful_labels_and_separate_density_review': True,
                'automatic_non_alert_is_unknown': True,
                'this_packet_is_not_manual_acceptance': True,
            }, 'training_admitted': False, 'global_leakage_free_certified': False}


def publish_packet(out, evidence_path):
    snapshot = Snapshot(ROOT)
    out = Path(out).resolve()
    if not out.is_relative_to(ROOT) or out.exists():
        raise ValueError('review packet requires a new project output path')
    candidate, evidence = render_review.verify_evidence(snapshot, evidence_path)
    _, others, _, population = load_population(snapshot)
    if population != evidence['population']:
        raise ValueError('review population changed')
    packet = make_packet(candidate, evidence, others)
    snapshot.read(ROOT / 'tools/review_linalg048_pairs.py')
    packet['render_evidence_raw_sha256'] = raw_sha(snapshot.read(evidence_path))
    packet['source_bindings'] = snapshot.bindings()
    write_new_json(out, packet, snapshot)
    return packet


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render-evidence', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        packet = publish_packet(args.out, args.render_evidence)
        print('PENDING review packet published; subjects:', len(packet['semantic_pairs']))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('[FAIL]', exc)
        return 2


if __name__ == '__main__':
    sys.exit(main())
