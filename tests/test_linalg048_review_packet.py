"""Semantic preparation must never manufacture an acceptance verdict."""
import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'src')]
import review_linalg048_pairs as packet
import apply_linalg048_admission as apply
from holdout_contract import raw_sha


class ReviewPacketTests(unittest.TestCase):
    def inputs(self):
        problem = '将平面上点的横坐标改为 x+3y，纵坐标不动，说明单位正方形的像和面积。'
        row = {'id': 'test-example-s1', 'problem_id': 'test-example',
               'problem': problem, 'solution': 'T(x,y)=(x+3y,y)，面积为1。',
               'answer': '面积1', 'scene_spec': {'objects': ['单位正方形'], 'steps': ['剪切']}}
        variants = [dict(row, id='test-example-s'+str(i)) for i in range(1,4)]
        grouped = {**row, 'id':'test-example', '_source_records': variants}
        subject = {'split':'test', 'id':'test-example', 'problem_sha256':raw_sha(problem.encode())}
        evidence = {'semantic_subjects':[subject], 'candidate_raw_sha256':'a'*64,
                    'scene':{'raw_sha256':'b'*64},
                    'render_result':{'output':{'sha256':'c'*64}}}
        return {'problem':problem}, evidence, [('test','test-example',grouped)]

    def test_same_core_example_is_pending_not_automatically_cleared(self):
        p=packet.make_packet(*self.inputs())
        self.assertIsNone(p['reviewer'])
        self.assertIsNone(p['semantic_pairs'][0]['verdict'])
        self.assertEqual(p['semantic_pairs'][0]['reason'],'')
        self.assertIsNone(p['visual']['verdict'])
        self.assertFalse(p['accepted'])
        self.assertFalse(p['training_admitted'])

    def test_all_scene_variants_and_solutions_are_present(self):
        p=packet.make_packet(*self.inputs())
        rows=p['review_material'][0]['source_records']
        self.assertEqual(len(rows),3)
        self.assertEqual([r['id'] for r in rows],['test-example-s1','test-example-s2','test-example-s3'])
        self.assertEqual(rows[2]['solution'],'T(x,y)=(x+3y,y)，面积为1。')

    def test_problem_hash_mismatch_refused(self):
        c,e,o=self.inputs();e['semantic_subjects'][0]['problem_sha256']='f'*64
        with self.assertRaisesRegex(ValueError,'binding mismatch'):packet.make_packet(c,e,o)

    def test_missing_subject_refused(self):
        c,e,o=self.inputs()
        with self.assertRaisesRegex(ValueError,'missing review subject'):packet.make_packet(c,e,[])

    def test_duplicate_subject_refused(self):
        c,e,o=self.inputs();e['semantic_subjects'].append(copy.deepcopy(e['semantic_subjects'][0]))
        with self.assertRaisesRegex(ValueError,'duplicate'):packet.make_packet(c,e,o)

    def test_unreviewed_extra_population_refused(self):
        c,e,o=self.inputs();o.append(('train','other',{'problem':'other'}))
        with self.assertRaisesRegex(ValueError,'coverage'):packet.make_packet(c,e,o)

    def test_variant_identity_mismatch_refused(self):
        c,e,o=self.inputs();o[0][2]['_source_records'][2]['problem_id']='different'
        with self.assertRaisesRegex(ValueError,'identity'):packet.make_packet(c,e,o)

    def test_variant_solution_missing_refused(self):
        c,e,o=self.inputs();del o[0][2]['_source_records'][1]['solution']
        with self.assertRaises(ValueError):packet.make_packet(c,e,o)

    def test_packet_is_rejected_by_acceptance_protocol(self):
        p=packet.make_packet(*self.inputs())
        with self.assertRaisesRegex(ValueError,'manual acceptance'):apply.require_manual_review(p,{},'a'*64)

    def test_existing_output_refused_before_media_validation(self):
        with patch.object(packet.render_review,'verify_evidence') as verify:
            with self.assertRaisesRegex(ValueError,'new project output'):packet.publish_packet(Path(__file__),ROOT/'missing.json')
            verify.assert_not_called()

    def test_outside_output_refused_before_media_validation(self):
        with patch.object(packet.render_review,'verify_evidence') as verify:
            with self.assertRaisesRegex(ValueError,'new project output'):packet.publish_packet(ROOT.parent/'outside.json',ROOT/'missing.json')
            verify.assert_not_called()

    def test_compatibility_render_entry_uses_bound_pipeline(self):
        import render_shear_scene_v2 as shim
        import admit_linalg048_v3 as bound
        self.assertIs(shim.main,bound.main)

    def test_compatibility_entry_requires_fresh_output_before_rendering(self):
        import render_shear_scene_v2 as shim
        with patch.object(packet.render_review.sandbox,'render_scene') as render:
            self.assertEqual(shim.main(['--out',str(Path(__file__))]),2)
            render.assert_not_called()

    def test_no_argument_does_not_write_legacy_acceptance(self):
        with self.assertRaises(SystemExit) as caught:packet.main([])
        self.assertEqual(caught.exception.code,2)


if __name__ == '__main__':
    unittest.main()
