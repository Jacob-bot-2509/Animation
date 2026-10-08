"""Build source-bound DEVELOPMENT diagnostics, not an independent calibration set.

Scene rows are grouped by question identity before metadata-stratified sampling.
No detector score is used in sampling. The labeling artifact omits strata and
parent IDs, but repository access is not a guarantee of blinded labeling.
Published v1 pairs remain immutable; v2 artifacts need fresh manual labels.
"""
from __future__ import annotations
import argparse
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from draft_io import NORMALIZED_HASH, fingerprint, selected_path
from holdout_contract import (Snapshot, INDEPENDENCE, LABEL_RULE, RULE_SHA,
    PAIR_SCHEMA, LABEL_SCHEMA, raw_sha, strict_json, json_object, jsonl, required_text,
    make_pair, require_pairs, write_new_json)

DRAFTS = ROOT / 'reviews/2026-10-05-training-diversity-drafts'
EVAL = ROOT / 'data/v2/eval/dataset_eval.jsonl'
TEST = ROOT / 'data/v2/test/dataset_test.jsonl'
EVAL_LOCK = ROOT / 'data/eval-v2.lock.json'
TEST_LOCK = ROOT / 'data/test-v2.lock.json'
DEV_LABELS = ROOT / 'reviews/codex-supervision/2026-10-05-readiness-completion/independent-leakage-labels-v2.json'
DEV_POP = ROOT / 'reviews/codex-supervision/2026-10-05-readiness-completion/leakage-population.json'
DEV_EXTRA = ROOT / 'reviews/codex-supervision/2026-10-05-readiness-completion/cross-signature-leakage-findings.json'
QUARANTINE = ROOT / 'reviews/codex-supervision/2026-10-05-math-template-followup-v2/new-overlap-before-fix.json'
OUT_DIR = ROOT / 'reviews/leakage-diagnostic-v2'
SEED = 20261006
S1A_MAX_DRAFTS_PER_PAIR = 3
S1B_PER_CONCEPT = 2
S2_PER_CATEGORY = 12
S3_TOTAL = 32

def sampling_config():
    return {'algorithm': 'unique-question-metadata-stratified-v2', 'seed': SEED,
            's1a_max_drafts_per_parent_pair': S1A_MAX_DRAFTS_PER_PAIR,
            's1b_per_concept': S1B_PER_CONCEPT, 's2_per_category': S2_PER_CATEGORY,
            's3_total': S3_TOTAL}

def load_drafts(snapshot=None):
    snap = snapshot or Snapshot()
    sel = strict_json(snap.read(DRAFTS / 'draft-selection.json'))
    if not isinstance(sel, dict) or sel.get('schema') != 2 or sel.get('hash_algorithm') != NORMALIZED_HASH:
        raise ValueError('schema2 normalized selector required')
    entries = sel.get('entries')
    if not isinstance(entries, list) or not entries:
        raise ValueError('nonempty selector entries required')
    rows, batches, ids = [], set(), set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError('selector entry object required')
        path = selected_path(DRAFTS, entry)
        if entry['batch'] in batches:
            raise ValueError('duplicate selected batch')
        batches.add(entry['batch'])
        data = snap.read(path); fp = fingerprint(data)
        if entry.get('hash_algorithm', sel['hash_algorithm']) != NORMALIZED_HASH:
            raise ValueError('selected hash algorithm mismatch')
        if fp['sha256'] != entry.get('sha256'):
            raise ValueError('selected hash mismatch')
        # Raw archives may use CRLF; canonical bytes are the portable contract.
        h = entry.get('raw_sha256')
        if not isinstance(h, str) or len(h) != 64 or any(c not in '0123456789abcdef' for c in h):
            raise ValueError('archival raw hash required')
        batch = jsonl(data)
        if type(entry.get('count')) is not int or entry['count'] != len(batch):
            raise ValueError('selected count mismatch')
        for row in batch:
            for field in ('id', 'problem', 'category', 'sub_category', 'concept_id'):
                required_text(row, field)
            if row['id'] in ids:
                raise ValueError('duplicate draft ID')
            ids.add(row['id'])
            parents = row.get('parent_training_ids', [])
            if not isinstance(parents, list) or any(not isinstance(p, str) or not p.strip() for p in parents):
                raise ValueError('invalid draft parents')
        rows.extend(batch)
    snap.check_unchanged()
    return sorted(rows, key=lambda r: r['id'])

def load_queries(snapshot=None):
    snap = snapshot or Snapshot()
    groups, ids, seen_scene_ids = {}, {}, set()
    for split, path, lock_path in [('eval', EVAL, EVAL_LOCK), ('test', TEST, TEST_LOCK)]:
        data = snap.read(path); lock = strict_json(snap.read(lock_path))
        if not isinstance(lock, dict) or not isinstance(lock.get('entries'), list) or any(not isinstance(e, dict) for e in lock['entries']):
            raise ValueError('query freeze lock shape mismatch')
        matching = [e for e in lock.get('entries', []) if Path(e['path']).resolve() == path.resolve()]
        if lock.get('locked') is not True or len(matching) != 1 or matching[0].get('sha256') != raw_sha(data):
            raise ValueError('query freeze lock mismatch: ' + split)
        for row in jsonl(data):
            for field in ('id', 'problem', 'category', 'sub_category'):
                required_text(row, field)
            if row['id'] in seen_scene_ids:
                raise ValueError('duplicate query scene ID')
            seen_scene_ids.add(row['id'])
            if 'problem_id' in row:
                required_text(row, 'problem_id')
            pid = row.get('problem_id') or row['id']
            if not isinstance(pid, str) or not pid.strip():
                raise ValueError('invalid query problem_id')
            key = (split, pid)
            if pid in ids and ids[pid] != key:
                raise ValueError('query ID collides across splits')
            ids[pid] = key
            if key not in groups:
                groups[key] = {**row, 'id': pid, '_split': split, '_source_records': []}
            rec = groups[key]
            if any(rec[field] != row[field] for field in ('problem', 'category', 'sub_category')):
                raise ValueError('conflicting metadata for query question: ' + pid)
            rec['_source_records'].append(row)
    recs = sorted(groups.values(), key=lambda r: (r['_split'], r['id']))
    aliases = {}
    for rec in recs:
        for alias in {rec['id']} | {r['id'] for r in rec['_source_records']}:
            if alias in aliases and aliases[alias] is not rec:
                raise ValueError('query alias collision')
            aliases[alias] = rec
    snap.check_unchanged()
    return recs, aliases

def parent_positive_queries(snapshot=None):
    snap = snapshot or Snapshot()
    labels = json_object(snap.read(DEV_LABELS)); pop = json_object(snap.read(DEV_POP))
    extra_bytes = snap.read(DEV_EXTRA); extra = json_object(extra_bytes)
    if labels.get('additional_findings_sha256') != raw_sha(extra_bytes):
        raise ValueError('development extra-findings binding mismatch')
    population = {p['pair_id']: p for p in pop['pairs']}
    if len(population) != len(pop['pairs']):
        raise ValueError('duplicate development population pair')
    annotations = labels['annotations']
    if len({a['pair_id'] for a in annotations}) != len(annotations):
        raise ValueError('duplicate development annotation')
    declared = labels.get('counts')
    if declared is not None and declared != dict(Counter(a['label'] for a in annotations)):
        raise ValueError('development label count mismatch')
    cross = {(a['query_hash'], a['train_hash'], a['query_id'], a['train_id'])
             for a in extra['leakage_pairs']}
    out = []
    for a in annotations:
        if a['label'] not in ('泄漏', '不泄漏', '不确定'):
            raise ValueError('invalid development label')
        if a['label'] != '泄漏':
            continue
        p = population.get(a['pair_id'])
        if p is not None:
            if (a['query_hash'], a['train_hash']) != (p['query']['hash'], p['train']['hash']):
                raise ValueError('development annotation pair/hash mismatch')
            out.extend((t['id'], q['id']) for t in p['train']['sources'] for q in p['query']['sources'])
        else:
            key = (a['query_hash'], a['train_hash'], a.get('query_id'), a.get('train_id'))
            if key not in cross:
                raise ValueError('unresolved development positive label')
            out.append((a['train_id'], a['query_id']))
    quarantine = json_object(snap.read(QUARANTINE))
    for p in quarantine.get('new_pairs', []):
        if p.get('review_label') != 'DIRECT_TEMPLATE_OVERLAP':
            raise ValueError('quarantine item is not a reviewed positive')
        out.append((p['train_id'], p['query_id']))
    snap.check_unchanged()
    return sorted(set(out))

def build_pairs(drafts, recs, by_pid, rng, *, parent_pairs=None):
    parents = parent_positive_queries() if parent_pairs is None else parent_pairs
    pairs, strata, seen_text = [], {}, set()
    def add(d, q, stratum):
        p = make_pair(d, q); pid = p['pair_id']
        key = (p['query']['problem_sha256'], p['train']['problem_sha256'])
        if pid in strata or key in seen_text:
            return False
        strata[pid] = stratum; seen_text.add(key); pairs.append(p)
        return True
    normalized_parents = set()
    for tid, qid in parents:
        if qid not in by_pid:
            raise ValueError('development query identity unresolved: ' + qid)
        normalized_parents.add((tid, by_pid[qid]['id']))
    for tid, qid in sorted(normalized_parents):
        q = by_pid[qid]
        kids = [d for d in drafts if tid in d.get('parent_training_ids', [])]
        rng.shuffle(kids)
        for d in kids[:S1A_MAX_DRAFTS_PER_PAIR]:
            add(d, q, 'S1a_parent_derived')
    by_sub, by_cat, concepts = defaultdict(list), defaultdict(list), defaultdict(list)
    for q in recs:
        by_sub[(q['category'], q['sub_category'])].append(q)
        by_cat[q['category']].append(q)
    for d in drafts:
        concepts[d['concept_id']].extend((d, q) for q in by_sub[(d['category'], d['sub_category'])])
    def sample(pool, quota, stratum):
        rng.shuffle(pool); count = 0
        for d, q in pool:
            if count == quota:
                break
            if add(d, q, stratum):
                count += 1
    for concept in sorted(concepts):
        sample(concepts[concept], S1B_PER_CONCEPT, 'S1b_same_sub')
    for cat in sorted({d['category'] for d in drafts}):
        sample([(d, q) for d in drafts if d['category'] == cat for q in by_cat[cat]
                if q['sub_category'] != d['sub_category']], S2_PER_CATEGORY, 'S2_same_cat_diff_sub')
    sample([(d, q) for d in drafts for q in recs if d['category'] != q['category']], S3_TOTAL, 'S3_cross_cat')
    require_pairs(pairs)
    return pairs, strata

def build_dataset(snapshot):
    snapshot.read(Path(__file__)); snapshot.read(ROOT / 'tools/holdout_contract.py'); snapshot.read(ROOT / 'tools/draft_io.py')
    drafts = load_drafts(snapshot); recs, aliases = load_queries(snapshot)
    parents = parent_positive_queries(snapshot)
    pairs, strata = build_pairs(drafts, recs, aliases, random.Random(SEED), parent_pairs=parents)
    snapshot.check_unchanged()
    data = {'schema': PAIR_SCHEMA, 'sampling': sampling_config(),
            'independence': INDEPENDENCE.copy(), 'labeling_rule': LABEL_RULE,
            'labeling_rule_sha256': RULE_SHA, 'labeling_status': 'PENDING',
            'source_bindings': snapshot.bindings(),
            'sampling_unit': 'unique question; all scene records retained in source identity',
            'pairs': pairs}
    return data, strata, drafts, recs

def label_template(data, pairs_sha):
    return {'schema': LABEL_SCHEMA, 'pairs_raw_sha256': pairs_sha,
            'labeling_rule_sha256': RULE_SHA, 'labeler': '',
            'labels': [{'pair_id': p['pair_id'], 'query_problem_sha256': p['query']['problem_sha256'],
                        'train_problem_sha256': p['train']['problem_sha256'],
                        'label': None, 'reason': ''} for p in data['pairs']]}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out-dir', type=Path, default=OUT_DIR); args = ap.parse_args(argv)
    try:
        pair_path = args.out_dir / 'holdout-pairs.json'; template = args.out_dir / 'holdout-labels.template.json'
        if pair_path.exists() or template.exists():
            raise ValueError('output exists: use a new directory')
        snap = Snapshot(); data, strata, drafts, recs = build_dataset(snap)
        h = write_new_json(pair_path, data, snap)
        write_new_json(template, label_template(data, h), snap)
        print(__import__('json').dumps({'pairs': len(data['pairs']), 'draft_questions': len(drafts),
            'unique_query_questions': len(recs), 'query_scene_records': sum(len(q['_source_records']) for q in recs),
            'strata': dict(Counter(strata.values())), 'independence': INDEPENDENCE,
            'labeling_status': 'PENDING', 'out': str(pair_path)}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('[FAIL]', exc); return 2

if __name__ == '__main__':
    sys.exit(main())
