"""Verify bound rendering and manual review; publish an inactive admission proposal.

The earlier in-place writer was a one-off migration. It could mutate five live
files before failure. This entry point now creates one new, source-bound proposal.
Active data promotion uses a separate versioned publication step.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'src')]
from holdout_contract import Snapshot, json_object, required_text, raw_sha, object_sha, RULE_SHA, write_new_json
import admit_linalg048_v3 as render_review

ASSET_EVIDENCE = ROOT/'data/asset_evidence.json'
MANIFEST = ROOT/'data/manifest.json'
REVIEW_SCHEMA = 'linalg048-manual-acceptance-v2'


def require_manual_review(review, evidence, evidence_raw_sha):
    if not isinstance(review, dict) or review.get('schema') != REVIEW_SCHEMA:
        raise ValueError('bound manual acceptance v2 required')
    required_text(review, 'reviewer')
    expected = {
        'render_evidence_raw_sha256':evidence_raw_sha,
        'candidate_raw_sha256':evidence['candidate_raw_sha256'],
        'scene_raw_sha256':evidence['scene']['raw_sha256'],
        'media_raw_sha256':evidence['render_result']['output']['sha256'],
        'labeling_rule_sha256':RULE_SHA,
    }
    if any(review.get(k) != v for k,v in expected.items()):
        raise ValueError('manual review subject/rule binding mismatch')
    visual = review.get('visual')
    if not isinstance(visual, dict) or visual.get('verdict') != 'ACCEPT':
        raise ValueError('actual visual acceptance required')
    required_text(visual, 'reason')
    subjects = evidence['semantic_subjects']
    expected_keys = {(v['split'],v['id'],v['problem_sha256']) for v in subjects}
    if len(expected_keys) != len(subjects):
        raise ValueError('duplicate semantic subject')
    labels = review.get('semantic_pairs')
    if not isinstance(labels, list) or len(labels) != len(subjects):
        raise ValueError('full unique-question semantic review coverage required')
    seen = set()
    for label in labels:
        key = tuple(required_text(label,k) for k in ('split','id','problem_sha256'))
        if key not in expected_keys or key in seen:
            raise ValueError('duplicate or wrong semantic review subject')
        seen.add(key)
        if label.get('verdict') != 'DIFFERENT_CORE_TASK':
            raise ValueError('leakage or uncertain semantic pair requires revision')
        required_text(label, 'reason')
    if seen != expected_keys:
        raise ValueError('missing semantic review subject')
    return required_text(review, 'reviewer')


def publish_proposal(out, evidence_path, acceptance_path, candidate_path=render_review.CANDIDATE_PATH):
    snapshot = Snapshot(ROOT)
    out = Path(out).resolve()
    if not out.is_relative_to(ROOT) or out.exists():
        raise ValueError('proposal requires a new project output path')
    candidate, evidence = render_review.verify_evidence(snapshot, evidence_path, candidate_path)
    review = json_object(snapshot.read(acceptance_path))
    reviewer = require_manual_review(review, evidence, raw_sha(snapshot.read(evidence_path)))
    # This tool has no active-file write branch. I/O failure can only leave an
    # unselected new proposal; it cannot partially replace live data/locks.
    proposal = {
        'schema':'linalg048-admission-proposal-v2',
        'status':'MANUAL_REVIEW_VERIFIED_PENDING_VERSIONED_PROMOTION',
        'active_data_modified':False, 'training_admitted':False,
        'calibration_eligible':False, 'global_leakage_free_certified':False,
        'candidate':candidate, 'candidate_raw_sha256':render_review.CANDIDATE_SHA,
        'render_evidence_raw_sha256':raw_sha(snapshot.read(evidence_path)),
        'acceptance_raw_sha256':raw_sha(snapshot.read(acceptance_path)),
        'reviewer':reviewer, 'source_bindings':snapshot.bindings(),
        'next_step':'Publish new versioned data/assets and separately promote a consistent manifest/lock set; existing training gates still apply.',
    }
    write_new_json(out, proposal, snapshot)
    return proposal


def refresh_progress(out):
    """Rebind unchanged row identities to current raw source hashes, unselected."""
    snapshot = Snapshot(ROOT)
    out = Path(out).resolve()
    if not out.is_relative_to(ROOT) or out.exists():
        raise ValueError('progress evidence requires a new project path')
    manifest = json_object(snapshot.read(MANIFEST))
    progress = json_object(snapshot.read(ASSET_EVIDENCE))
    if progress.get('manifest_sha256') != raw_sha(snapshot.read(MANIFEST)):
        raise ValueError('asset progress manifest binding mismatch')
    records = progress.get('records')
    if not isinstance(records, dict) or not records:
        raise ValueError('asset progress records required')
    sources = {}
    for entry in manifest.get('entries', []):
        if entry.get('split') not in ('train','eval','test'):
            continue
        path = (ROOT/'data'/entry['path']).resolve()
        raw = snapshot.read(path)
        if raw_sha(raw) != entry['sha256'] or len(raw) != entry['size']:
            raise ValueError('manifest source raw binding mismatch')
        sources[path] = (raw_sha(raw), raw.decode('utf-8-sig').splitlines())
    changes = []
    for key,record in records.items():
        src = record.get('source')
        if not isinstance(src, dict):
            raise ValueError('asset source object required')
        path = Path(required_text(src,'path')).resolve()
        if path not in sources:
            raise ValueError('asset source is not in current manifest')
        digest, lines = sources[path]
        line = src.get('line')
        if type(line) is not int or not 1 <= line <= len(lines):
            raise ValueError('asset source line mismatch')
        row_raw = lines[line-1].encode('utf-8')
        row = json_object(row_raw)
        if row.get('id') != key or raw_sha(row_raw) != record.get('input_sha256'):
            raise ValueError('asset input changed; cannot retain old review: '+key)
        if src.get('sha256') != digest:
            changes.append({'id':key,'old_sha256':src.get('sha256'),'new_sha256':digest})
            src['sha256'] = digest
    # Keep all actual review statuses and counts. No new asset is admitted.
    snapshot.read(ROOT/'tools/apply_linalg048_admission.py')
    progress['binding_refresh'] = {
        'schema':'asset-progress-source-rebind-v1',
        'source_bindings':snapshot.bindings(), 'changed_source_bindings':changes,
        'active_file_modified':False, 'review_statuses_unchanged':True,
        'additional_assets_admitted':0,
    }
    write_new_json(out, progress, snapshot)
    return progress


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--render-evidence', type=Path)
    parser.add_argument('--acceptance', type=Path)
    parser.add_argument('--candidate', type=Path, default=render_review.CANDIDATE_PATH)
    parser.add_argument('--refresh-progress', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.refresh_progress:
            if args.render_evidence or args.acceptance:
                raise ValueError('progress refresh does not accept admission inputs')
            data = refresh_progress(args.out)
        else:
            if args.render_evidence is None or args.acceptance is None:
                raise ValueError('render evidence and completed manual acceptance required')
            data = publish_proposal(args.out, args.render_evidence, args.acceptance, args.candidate)
        print('published new inactive artifact:', data.get('status'))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('[FAIL]', exc)
        return 2


if __name__ == '__main__':
    sys.exit(main())
