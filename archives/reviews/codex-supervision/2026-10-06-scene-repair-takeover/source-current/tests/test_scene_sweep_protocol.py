"""Regression tests for source drift, input mutation and selector activation hazards."""
from pathlib import Path
import copy,json,os,stat,tempfile,unittest
from unittest.mock import patch
from tools import scene_sweep_protocol as p
from tools import publish_row_patches as old_publisher
from tools.draft_io import publish_jsonl

WORK=p.ROOT/'reviews/codex-supervision/2026-10-06-scene-repair-takeover/test-work'
class SceneWorkflowTests(unittest.TestCase):
    def setUp(self):
        WORK.mkdir(parents=True,exist_ok=True)
        self.tmp=tempfile.TemporaryDirectory(dir=WORK)
        self.root=Path(self.tmp.name).resolve();self.drafts=self.root/'drafts'
        self.rows=[{'id':f'q{i}','concept_id':'c1','category':'test','sub_category':'test',
                    'problem':'$1+1$','solution':'$1+1=2$','answer':'$2$',
                    'scene_spec':{'objects':['$1+1=2$'],'steps':['$1+1=2$']},
                    'admitted':True,'render_verified':True} for i in range(5)]
        self.source=self.drafts/'batch-01/old.jsonl'
        fp=publish_jsonl(self.source,self.rows)
        self.selector=self.drafts/'draft-selection.json'
        self.selector.write_text(json.dumps({'schema':2,'hash_algorithm':p.NORMALIZED_HASH,
             'entries':[{'batch':'batch-01','path':'batch-01/old.jsonl','version':'old',**fp}]}),encoding='utf-8')
        self.before=self.selector.read_bytes()
        self.inputs=self.root/'inputs'
    def tearDown(self):
        for path in self.root.rglob('*'):
            if path.is_file():
                assert path.resolve().is_relative_to(self.root)
                os.chmod(path,stat.S_IREAD|stat.S_IWRITE)
        self.tmp.cleanup()
    def build(self,chunks=3):
        return p.build_inputs(self.drafts,self.inputs,chunks=chunks,expected_count=5,root=self.root)
    def patch_packet(self):
        after=copy.deepcopy(self.rows[0]);after['scene_spec']={'objects':['$2=1+1$'],'steps':['$2=1+1$']}
        fp=p.fingerprint(self.source.read_bytes())
        packet={'records':[{'batch':'batch-01','id':'q0','expected_selected_path':'batch-01/old.jsonl',
          'expected_hash_algorithm':p.NORMALIZED_HASH,'expected_selected_sha256':fp['sha256'],
          'expected_selected_raw_sha256':fp['raw_sha256'],'expected_record_sha256':p.sorted_sha(self.rows[0]),
          'new_math_content_sha256':p.sorted_sha({k:after[k] for k in p.MATH_FIELDS}),
          'fields':{'scene_spec':after['scene_spec']}}]}
        path=self.root/'patches.json';path.write_text(json.dumps(packet),encoding='utf-8')
        return path,packet
    def stage(self,path,out=None):
        return p.stage_scene_patches(self.drafts,path,out or self.root/'staged','v1',input_dir=self.inputs,root=self.root)
    def test_balanced_nonempty_full_records(self):
        m=self.build();self.assertEqual([v['count'] for v in m['chunks'].values()],[2,2,1])
        _,rows=p.verify_inputs(self.inputs,root=self.root)
        self.assertEqual([v['record'] for v in rows],self.rows)
        self.assertTrue(all('source_line' in v['binding'] for v in rows))
    def test_excess_chunks_do_not_create_empty_packets(self):
        m=self.build(20);self.assertEqual(m['chunk_count'],5)
        self.assertTrue(all(v['count']==1 for v in m['chunks'].values()))
    def test_existing_inputs_never_overwritten(self):
        self.build();data=(self.inputs/'inputs.json').read_bytes()
        with self.assertRaises(ValueError):self.build()
        self.assertEqual((self.inputs/'inputs.json').read_bytes(),data)
    def test_output_overlap_and_escape_rejected_before_write(self):
        for out in (self.drafts/'new',self.root,self.root.parent/'escape'):
            with self.subTest(out=out),self.assertRaises(ValueError):
                p.build_inputs(self.drafts,out,root=self.root)
    def test_source_raw_change_with_same_normalized_hash_rejected(self):
        self.source.write_bytes(b'\xef\xbb\xbf'+self.source.read_bytes())
        with self.assertRaisesRegex(ValueError,'raw/normalized'):self.build()
        self.assertFalse(self.inputs.exists())
    def test_immutable_chunk_tamper_rejected(self):
        self.build();chunk=self.inputs/'chunk-01.json'
        os.chmod(chunk,stat.S_IREAD|stat.S_IWRITE);chunk.write_bytes(chunk.read_bytes()+b' ')
        with self.assertRaisesRegex(ValueError,'chunk bytes'):p.verify_inputs(self.inputs,root=self.root)
    def test_stages_fresh_records_never_activates_or_inherits_acceptance(self):
        self.build();path,packet=self.patch_packet();r=self.stage(path)
        self.assertFalse(r['production_selector_updated'])
        self.assertEqual(self.selector.read_bytes(),self.before)
        self.assertEqual(p.jsonl(self.source.read_bytes()),self.rows)
        candidate=p.json_object((self.root/'staged/draft-selection.candidate.json').read_bytes())
        rows=p.jsonl((self.root/'staged'/candidate['entries'][0]['path']).read_bytes())
        self.assertEqual(rows[0]['scene_spec'],packet['records'][0]['fields']['scene_spec'])
        self.assertTrue(all(not row['admitted'] and not row['render_verified'] for row in rows))
        self.assertTrue(all(row['strict_review']['visual_review']=='PENDING' for row in rows))
    def test_candidate_output_inside_inputs_rejected(self):
        self.build();path,_=self.patch_packet()
        with self.assertRaisesRegex(ValueError,'overlaps'):self.stage(path,self.inputs/'results')
    def test_duplicate_target_and_math_change_rejected(self):
        self.build();path,packet=self.patch_packet()
        for kind in ('duplicate','math'):
            bad=copy.deepcopy(packet)
            if kind=='duplicate':bad['records']+=copy.deepcopy(bad['records'])
            else:bad['records'][0]['fields']['answer']='$3$'
            path.write_text(json.dumps(bad),encoding='utf-8')
            with self.subTest(kind=kind),self.assertRaises(ValueError):self.stage(path)
            self.assertFalse((self.root/'staged').exists())
    def test_source_or_result_sha_mismatch_rejected(self):
        self.build();path,packet=self.patch_packet()
        for field in ('expected_selected_raw_sha256','expected_record_sha256','new_math_content_sha256'):
            bad=copy.deepcopy(packet);bad['records'][0][field]='0'*64
            path.write_text(json.dumps(bad),encoding='utf-8')
            with self.subTest(field=field),self.assertRaises(ValueError):self.stage(path)
            self.assertFalse((self.root/'staged').exists())
    def test_input_selector_drift_rejected(self):
        self.build();path,_=self.patch_packet();self.selector.write_bytes(self.before+b' ')
        with self.assertRaisesRegex(ValueError,'source binding|selector'):self.stage(path)
        self.assertFalse((self.root/'staged').exists())
    def test_existing_staged_output_not_overwritten(self):
        self.build();path,_=self.patch_packet();self.stage(path)
        receipt=(self.root/'staged/stage-receipt.json').read_bytes()
        with self.assertRaises(ValueError):self.stage(path)
        self.assertEqual((self.root/'staged/stage-receipt.json').read_bytes(),receipt)
    def test_source_change_during_stage_prevents_candidate_manifest(self):
        self.build();path,_=self.patch_packet();writer=p.publish_jsonl
        def racing_write(out,rows):
            result=writer(out,rows);self.selector.write_bytes(self.before+b' ');return result
        with patch.object(p,'publish_jsonl',racing_write):
            with self.assertRaisesRegex(ValueError,'source changed'):self.stage(path)
        self.assertFalse((self.root/'staged/draft-selection.candidate.json').exists())
    def test_legacy_auto_selector_scene_publish_retired(self):
        self.build();path,_=self.patch_packet()
        with self.assertRaisesRegex(ValueError,'scene-only'):old_publisher.publish(self.drafts,path,'v1')
        self.assertEqual(self.selector.read_bytes(),self.before)
        self.assertFalse((self.drafts/'batch-01/draft-v1.jsonl').exists())

    def test_input_change_between_verify_and_staging_rejected(self):
        self.build();path,_=self.patch_packet();verifier=p.verify_inputs
        def tamper_after_verify(*args,**kwargs):
            result=verifier(*args,**kwargs)
            chunk=self.inputs/'chunk-01.json'
            os.chmod(chunk,stat.S_IREAD|stat.S_IWRITE)
            chunk.write_bytes(chunk.read_bytes()+b' ')
            return result
        with patch.object(p,'verify_inputs',tamper_after_verify):
            with self.assertRaisesRegex(ValueError,'source changed'):self.stage(path)
        self.assertFalse((self.root/'staged').exists())

    def test_legacy_scene_with_redundant_math_field_cannot_bypass_retirement(self):
        self.build();path,packet=self.patch_packet()
        packet['records'][0]['fields']['answer']=self.rows[0]['answer']
        path.write_text(json.dumps(packet),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'scene-only'):old_publisher.publish(self.drafts,path,'v1')
        self.assertEqual(self.selector.read_bytes(),self.before)
    def test_legacy_mixed_scene_and_math_batch_cannot_bypass_retirement(self):
        self.build();path,packet=self.patch_packet()
        extra=dict(packet['records'][0]);extra['id']='q1';extra['fields']={'solution':self.rows[1]['solution']}
        packet['records'].append(extra);path.write_text(json.dumps(packet),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'scene-only'):old_publisher.publish(self.drafts,path,'v1')
        self.assertEqual(self.selector.read_bytes(),self.before)
