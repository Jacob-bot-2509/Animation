"""Regression fixtures only: no genuine labels, calibration or gate admission."""
import copy
import json
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'src')]
import build_holdout_pairs as build
import score_holdout as scoring
import holdout_contract as contract
from draft_io import fingerprint

class HoldoutFixtures(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.drafts = self.root / 'drafts'; batch = self.drafts / 'batch-01'; batch.mkdir(parents=True)
        self.rows = [dict(id='d1', problem='问题 A', category='A', sub_category='s1', concept_id='C1', parent_training_ids=['parent']),
                     dict(id='d2', problem='问题 B', category='A', sub_category='s2', concept_id='C2', parent_training_ids=[]),
                     dict(id='d3', problem='问题 C', category='B', sub_category='s3', concept_id='C3', parent_training_ids=[])]
        self.row_path = batch / 'draft.jsonl'; self.write_jsonl(self.row_path, self.rows)
        self.entry = dict(batch='batch-01', path='batch-01/draft.jsonl', count=3, **fingerprint(self.row_path.read_bytes()))
        self.sel = self.drafts / 'draft-selection.json'; self.save_selection()
        self.eval = self.root / 'eval.jsonl'; self.test = self.root / 'test.jsonl'
        self.eval_rows = [dict(id='eval-series-001-s1', problem_id='eval-series-001', problem='问题 A', category='A', sub_category='s1', solution='method one'),
                          dict(id='eval-series-001-s2', problem_id='eval-series-001', problem='问题 A', category='A', sub_category='s1', solution='method two')]
        self.test_rows = [dict(id='test-q', problem='问题 D', category='B', sub_category='s4')]
        self.write_jsonl(self.eval, self.eval_rows); self.write_jsonl(self.test, self.test_rows)
        self.eval_lock = self.root / 'eval-lock.json'; self.test_lock = self.root / 'test-lock.json'
        self.lock(self.eval, self.eval_lock); self.lock(self.test, self.test_lock)
        self.dev_extra = self.root / 'extra.json'; self.dump(self.dev_extra, {'leakage_pairs': []})
        self.dev_pop = self.root / 'pop.json'; self.dump(self.dev_pop, {'pairs': []})
        self.dev_labels = self.root / 'dev-labels.json'; self.dump(self.dev_labels, {'annotations': [], 'counts': {}, 'additional_findings_sha256': contract.raw_sha(self.dev_extra.read_bytes())})
        self.quarantine = self.root / 'quarantine.json'; self.dump(self.quarantine, {'new_pairs': []})
        values = dict(DRAFTS=self.drafts, EVAL=self.eval, TEST=self.test, EVAL_LOCK=self.eval_lock, TEST_LOCK=self.test_lock,
                      DEV_EXTRA=self.dev_extra, DEV_POP=self.dev_pop, DEV_LABELS=self.dev_labels, QUARANTINE=self.quarantine,
                      S1B_PER_CONCEPT=1, S2_PER_CATEGORY=2, S3_TOTAL=2)
        self.patch = mock.patch.multiple(build, **values); self.patch.start()
        self.addCleanup(self.patch.stop); self.addCleanup(self.tmp.cleanup)

    @staticmethod
    def dump(path, value): path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    @staticmethod
    def write_jsonl(path, rows): path.write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n', encoding='utf-8')
    def lock(self, path, lock): self.dump(lock, {'locked': True, 'entries': [{'path': str(path), 'sha256': contract.raw_sha(path.read_bytes())}]})
    def save_selection(self, entries=None): self.dump(self.sel, {'schema': 2, 'hash_algorithm': build.NORMALIZED_HASH, 'entries': entries or [self.entry]})
    def artifacts(self):
        data, strata, drafts, queries = build.build_dataset(contract.Snapshot())
        pairs = self.root / 'pairs.json'; self.dump(pairs, data)
        labels = build.label_template(data, contract.raw_sha(pairs.read_bytes())); labels['labeler'] = 'synthetic regression fixture'
        for lab, pair in zip(labels['labels'], data['pairs']):
            lab['label'] = '泄漏' if pair['query']['problem'] == pair['train']['problem'] else '不泄漏'
            lab['reason'] = '合成回归夹具；不是实际题目标注或校准证据。'
        label_path = self.root / 'labels.json'; self.dump(label_path, labels)
        return pairs, label_path, data, strata, drafts, queries
    def run_score(self, pairs, labels):
        out = self.root / 'score.json'
        rc = scoring.main(['--pairs', str(pairs), '--labels', str(labels), '--out', str(out)])
        return rc, out
    def direct_score(self, data, strata, drafts, queries):
        labs = {p['pair_id']: {'label': '不泄漏', 'reason': 'synthetic'} for p in data['pairs']}
        return scoring.score(data['pairs'], strata, labs, {q['id']: q for q in queries}, {d['id']: d for d in drafts})

    def test_scene_rows_grouped_without_losing_source_identity(self):
        queries, aliases = build.load_queries()
        self.assertEqual(len(queries), 2); self.assertEqual(sum(len(q['_source_records']) for q in queries), 3)
        q = aliases['eval-series-001']; self.assertIs(q, aliases['eval-series-001-s2'])
        self.assertEqual(q['id'], 'eval-series-001')
    def test_scene_question_metadata_conflict_rejected(self):
        self.eval_rows[1]['sub_category'] = 'conflicting'; self.write_jsonl(self.eval, self.eval_rows); self.lock(self.eval, self.eval_lock)
        with self.assertRaises(ValueError): build.load_queries()
    def test_query_scene_duplicate_rejected(self):
        self.write_jsonl(self.eval, [self.eval_rows[0], self.eval_rows[0]]); self.lock(self.eval, self.eval_lock)
        with self.assertRaises(ValueError): build.load_queries()
    def test_freeze_lock_tamper_rejected(self):
        self.eval.write_bytes(self.eval.read_bytes() + b'\n')
        with self.assertRaises(ValueError): build.load_queries()
    def test_same_question_id_across_splits_rejected(self):
        self.test_rows[0]['id'] = 'eval-series-001'; self.write_jsonl(self.test, self.test_rows); self.lock(self.test, self.test_lock)
        with self.assertRaises(ValueError): build.load_queries()
    def test_declared_invalid_problem_id_rejected(self):
        self.eval_rows[0]['problem_id'] = 0; self.write_jsonl(self.eval,self.eval_rows); self.lock(self.eval,self.eval_lock)
        with self.assertRaises(ValueError): build.load_queries()
    def test_malformed_development_root_is_controlled(self):
        self.dump(self.dev_labels, [])
        with self.assertRaises(ValueError): build.parent_positive_queries()
    def test_sampling_or_independence_claim_tamper_rejected(self):
        for field in ('sampling','independence'):
            with self.subTest(field=field):
                p,l,data,_,_,_ = self.artifacts()
                if field == 'sampling': data[field]['seed'] = 0
                else: data[field] = {'status':'INDEPENDENT','calibration_eligible':True}
                self.dump(p,data); rc,out = self.run_score(p,l); self.assertEqual(rc,2); self.assertFalse(out.exists())
    def test_duplicate_selected_batch_rejected(self):
        self.save_selection([self.entry, self.entry])
        with self.assertRaises(ValueError): build.load_drafts()
    def test_duplicate_draft_identity_rejected(self):
        self.rows[1]['id'] = 'd1'; self.write_jsonl(self.row_path, self.rows); self.entry.update(fingerprint(self.row_path.read_bytes())); self.save_selection()
        with self.assertRaises(ValueError): build.load_drafts()
    def test_selector_count_and_hash_required(self):
        for field, value in [('count', 4), ('sha256', '0' * 64)]:
            with self.subTest(field=field):
                old = self.entry[field]; self.entry[field] = value; self.save_selection()
                with self.assertRaises(ValueError): build.load_drafts()
                self.entry[field] = old
    def test_source_snapshot_detects_late_change(self):
        snap = contract.Snapshot(); build.load_queries(snap); self.test.write_bytes(self.test.read_bytes() + b'\n')
        with self.assertRaises(ValueError): snap.check_unchanged()
    def test_cross_signature_positive_not_silently_dropped(self):
        extra = dict(query_hash='qh', train_hash='th', query_id='eval-series-001-s1', train_id='parent')
        self.dump(self.dev_extra, {'leakage_pairs': [extra]})
        self.dump(self.dev_labels, {'annotations': [dict(pair_id='extra', label='泄漏', **extra)], 'counts': {'泄漏': 1}, 'additional_findings_sha256': contract.raw_sha(self.dev_extra.read_bytes())})
        self.assertEqual(build.parent_positive_queries(), [('parent', 'eval-series-001-s1')])
    def test_development_findings_stale_binding_rejected(self):
        self.dump(self.dev_extra, {'leakage_pairs': [], 'tampered': True})
        with self.assertRaises(ValueError): build.parent_positive_queries()
    def test_parent_scene_aliases_do_not_multiply_family_quota(self):
        ds = [dict(self.rows[0], id='kid'+str(i), problem='unique '+str(i)) for i in range(6)]
        qs, aliases = build.load_queries()
        with mock.patch.multiple(build, S1A_MAX_DRAFTS_PER_PAIR=1, S1B_PER_CONCEPT=0, S2_PER_CATEGORY=0, S3_TOTAL=0):
            pairs, _ = build.build_pairs(ds, qs, aliases, __import__('random').Random(7), parent_pairs=[('parent','eval-series-001-s1'),('parent','eval-series-001-s2')])
        self.assertEqual(len(pairs), 1)
    def test_duplicate_candidates_do_not_consume_quota(self):
        qs, aliases = build.load_queries(); q = aliases['eval-series-001']; q2 = copy.deepcopy(q); q2['id'] = 'another'; q2['problem'] = 'another question'; q2['sub_category'] = 'different'; q2['_source_records'] = [{'id':'another', 'problem':'another question'}]
        q['sub_category'] = 'different'
        with mock.patch.multiple(build, S1B_PER_CONCEPT=0, S2_PER_CATEGORY=2, S3_TOTAL=0):
            pairs, strata = build.build_pairs([self.rows[0]], [q,q,q2], {q['id']:q,q2['id']:q2}, __import__('random').Random(3), parent_pairs=[])
        self.assertEqual(len(pairs), 2); self.assertEqual(Counter(strata.values())['S2_same_cat_diff_sub'], 2)
    def test_builder_creates_pending_bound_new_version(self):
        dest = self.root / 'published'
        self.assertEqual(build.main(['--out-dir', str(dest)]), 0)
        data = json.loads((dest/'holdout-pairs.json').read_text('utf-8'))
        self.assertEqual(data['schema'], contract.PAIR_SCHEMA); self.assertFalse(data['independence']['calibration_eligible']); self.assertEqual(data['labeling_status'], 'PENDING')
        self.assertEqual(contract.raw_sha((dest/'holdout-pairs.json').read_bytes()), json.loads((dest/'holdout-labels.template.json').read_text('utf-8'))['pairs_raw_sha256'])
    def test_builder_preserves_existing_output(self):
        dest = self.root / 'published'; dest.mkdir(); p = dest/'holdout-pairs.json'; p.write_bytes(b'OLD')
        self.assertEqual(build.main(['--out-dir', str(dest)]), 2); self.assertEqual(p.read_bytes(), b'OLD'); self.assertFalse((dest/'holdout-labels.template.json').exists())
    def test_valid_bound_scoring_is_diagnostic_even_if_targets_met(self):
        p,l,_,_,_,_ = self.artifacts(); rc,out = self.run_score(p,l)
        self.assertEqual(rc, 0); report = json.loads(out.read_text('utf-8')); self.assertFalse(report['calibrated']); self.assertEqual(report['screens']['combined']['recall'], '1'); self.assertFalse(report['screens']['combined']['calibrated'])
        self.assertIn('src/animtrain/validate.py', report['bindings']['inputs'])
    def test_duplicate_pairs_rejected_before_output(self):
        p,l,data,_,_,_ = self.artifacts(); data['pairs'].append(copy.deepcopy(data['pairs'][0])); self.dump(p,data)
        rc,out = self.run_score(p,l); self.assertEqual(rc,2); self.assertFalse(out.exists())
    def test_self_consistent_tampered_question_rejected(self):
        _,_,data,strata,drafts,queries = self.artifacts(); bad = data['pairs'][0]
        old = bad['pair_id']; bad['query']['problem'] = 'FAKE QUESTION'; bad['query']['problem_sha256'] = contract.raw_sha(b'FAKE QUESTION'); bad['pair_id'] = contract.object_sha({'query':bad['query'],'train':bad['train']}); strata[bad['pair_id']] = strata.pop(old)
        with self.assertRaises(ValueError): self.direct_score(data,strata,drafts,queries)
    def test_signed_pair_category_differs_from_actual_source_rejected(self):
        _,_,data,strata,drafts,queries = self.artifacts(); bad = data['pairs'][0]; old = bad['pair_id']; bad['query']['category'] = 'FAKE CATEGORY'; bad['pair_id'] = contract.object_sha({'query':bad['query'],'train':bad['train']}); strata[bad['pair_id']] = strata.pop(old)
        with self.assertRaises(ValueError): self.direct_score(data,strata,drafts,queries)
    def test_changed_source_metadata_invalidates_rebuild(self):
        p,l,_,_,_,_ = self.artifacts(); self.rows[0]['sub_category'] = 'changed'; self.write_jsonl(self.row_path,self.rows); self.entry.update(fingerprint(self.row_path.read_bytes())); self.save_selection()
        rc,out = self.run_score(p,l); self.assertEqual(rc,2); self.assertFalse(out.exists())
    def test_duplicate_labels_rejected(self):
        p,l,_,_,_,_ = self.artifacts(); data = json.loads(l.read_text('utf-8')); data['labels'].append(copy.deepcopy(data['labels'][0])); self.dump(l,data)
        rc,out = self.run_score(p,l); self.assertEqual(rc,2); self.assertFalse(out.exists())
    def test_missing_label_rejected(self):
        p,l,_,_,_,_ = self.artifacts(); data = json.loads(l.read_text('utf-8')); data['labels'].pop(); self.dump(l,data)
        rc,out = self.run_score(p,l); self.assertEqual(rc,2); self.assertFalse(out.exists())
    def test_labels_bound_to_exact_pair_file(self):
        p,l,_,_,_,_ = self.artifacts(); data = json.loads(l.read_text('utf-8')); data['pairs_raw_sha256'] = '0'*64; self.dump(l,data)
        rc,out = self.run_score(p,l); self.assertEqual(rc,2); self.assertFalse(out.exists())
    def test_label_question_hash_rejected(self):
        p,l,_,_,_,_ = self.artifacts(); data = json.loads(l.read_text('utf-8')); data['labels'][0]['query_problem_sha256'] = '0'*64; self.dump(l,data)
        rc,out = self.run_score(p,l); self.assertEqual(rc,2); self.assertFalse(out.exists())
    def test_pending_template_cannot_be_scored(self):
        p,l,data,_,_,_ = self.artifacts(); self.dump(l,build.label_template(data,contract.raw_sha(p.read_bytes())))
        rc,out = self.run_score(p,l); self.assertEqual(rc,2); self.assertFalse(out.exists())
    def test_unknown_manual_label_remains_separate(self):
        p,l,_,_,_,_ = self.artifacts(); data = json.loads(l.read_text('utf-8')); data['labels'][0]['label'] = '不确定'; self.dump(l,data)
        rc,out = self.run_score(p,l); self.assertEqual(rc,0); report = json.loads(out.read_text('utf-8')); self.assertEqual(report['screens']['union']['uncertain'],1); self.assertFalse(report['screens']['union']['empirical_targets_met'])
    def test_source_changed_during_scoring_publishes_nothing(self):
        p,l,_,_,_,_ = self.artifacts(); real = scoring.compare
        def mutate(a,b):
            self.test.write_bytes(self.test.read_bytes()+b'\n'); return real(a,b)
        with mock.patch.object(scoring,'compare',side_effect=mutate): rc,out = self.run_score(p,l)
        self.assertEqual(rc,2); self.assertFalse(out.exists())
    def test_existing_score_cannot_be_overwritten(self):
        p,l,_,_,_,_ = self.artifacts(); out = self.root/'score.json'; out.write_bytes(b'OLD'); rc,_ = self.run_score(p,l)
        self.assertEqual(rc,2); self.assertEqual(out.read_bytes(),b'OLD')
    def test_legacy_unbound_schema_fails_closed(self):
        p,l,data,_,_,_ = self.artifacts(); data['schema'] = 'holdout-pairs-v1'; self.dump(p,data)
        rc,out = self.run_score(p,l); self.assertEqual(rc,2); self.assertFalse(out.exists())
    def test_unknown_structure_not_certified_nonleak(self):
        p,l,_,_,_,_ = self.artifacts(); rc,out = self.run_score(p,l); self.assertEqual(rc,0)
        report = json.loads(out.read_text('utf-8')); self.assertTrue(all(r['structural_verdict']=='UNKNOWN' for r in report['rows'] if not r['structural']))

class StrictJsonAndRateTests(unittest.TestCase):
    def test_duplicate_keys_nan_and_overflow_rejected(self):
        for data in [b'{"x":1,"x":2}',b'{"x":NaN}',b'{"x":Infinity}',b'{"x":1e999}']:
            with self.subTest(data=data), self.assertRaises(ValueError): contract.strict_json(data)
    def test_exact_fractions_and_missing_class_are_unknown(self):
        m = scoring.metrics(Counter(tp=1,fn=1,fp=1,tn=2))
        self.assertEqual(m['recall'],'1/2'); self.assertEqual(m['fpr'],'1/3'); self.assertFalse(m['calibrated'])
        self.assertIsNone(scoring.metrics(Counter(tp=1))['fpr']); self.assertFalse(scoring.metrics(Counter(tp=1))['empirical_targets_met'])
    def test_empty_sample_cannot_certify_anything(self):
        with self.assertRaises(ValueError): scoring.score([],{}, {}, {}, {})
    def test_malformed_question_payload_rejected(self):
        with self.assertRaises(ValueError): contract.require_pairs([{'pair_id':'p','query':[],'train':{}}])

if __name__ == '__main__': unittest.main()
