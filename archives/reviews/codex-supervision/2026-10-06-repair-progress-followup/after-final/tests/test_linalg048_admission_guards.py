"""Synthetic regression fixtures; never real render/label/admission evidence."""
from __future__ import annotations
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'src')]
import admit_linalg048_v3 as render
import apply_linalg048_admission as apply
from holdout_contract import Snapshot, RULE_SHA, raw_sha

TMP = ROOT/'reviews/codex-supervision/2026-10-06-repair-progress-followup/test-tmp'
TMP.mkdir(exist_ok=True)

class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=TMP)
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.work = self.base/'execution-fixture'
        self.work.mkdir()
        self.scene = 'class ConceptScene:\n    pass\n'
        for name,text in [('scene.py',self.scene),('bootstrap.py','pass\n'),
                          ('stdout.txt','fixture stdout'),('stderr.txt','')]:
            (self.work/name).write_text(text,encoding='utf-8',newline='\n')
        media = self.work/'media/ConceptScene.mp4'
        media.parent.mkdir()
        media.write_bytes(b'synthetic test bytes; NOT video')
        parent = {'created_suspended':True,'job_assigned_before_resume':True,
                  'tree_stopped':True,'memory_limit_mb':2048,
                  'token':{'api_ok':True,'is_appcontainer':True,
                           'capability_count':0,'sid':'S-1-15-2-123'},
                  'private_profile':{'sid':'S-1-15-2-123','cleanup_complete':True,
                    'temporary_acl':[{'restored':True,
                      'before_sha256':'a'*64,'after_sha256':'a'*64}]}}
        command = [str((ROOT/'.venv/Scripts/python.exe').resolve()),'-I','-B',
                   str(self.work/'bootstrap.py'),'render','-ql','--format=mp4',
                   '--media_dir',str(self.work/'media'),str(self.work/'scene.py'),'ConceptScene']
        output={'path':str(media),'sha256':raw_sha(media.read_bytes()),
                'size':media.stat().st_size,'frames':2,'width':10,'height':10,'frame_rate':'15'}
        self.result = {'ok':True,'status':'rendered',
            'transport':{'rc':0,'work':str(self.work),'source_sha256':raw_sha((self.work/'scene.py').read_bytes()),
                         'command':command,'stdout':'fixture stdout','stderr':'','parent_evidence':parent},
            'isolation':{'backend':'windows_appcontainer','shell':False,'memory_limit_mb':2048,
                         'job_assigned':True,'network_isolated':True,'fs_isolation':'private_per_run',
                         'parent_evidence':parent},'output':output}
        self.scope=mock.patch.object(render.sandbox,'WORK_ROOT',self.base)
        self.scope.start();self.addCleanup(self.scope.stop)

    def verify(self,result=None,decoder=None):
        result=self.result if result is None else result
        return render.verify_result(result,self.scene,Snapshot(ROOT),
                                    decoder=decoder or (lambda p:copy.deepcopy(self.result['output'])))

    def active_hashes(self):
        paths=['data/manifest.json','data/asset_evidence.json','data/eval-v2.lock.json',
               'data/test-v2.lock.json','data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl']
        return {p:raw_sha((ROOT/p).read_bytes()) for p in paths}

    def review_fixture(self):
        evidence={'candidate_raw_sha256':'candidate-fixture',
                  'scene':{'raw_sha256':'scene-fixture'},
                  'render_result':{'output':{'sha256':'video-fixture'}},
                  'semantic_subjects':[{'split':'eval','id':'fixture-1','problem_sha256':'p1'}]}
        review={'schema':apply.REVIEW_SCHEMA,'reviewer':'synthetic regression fixture only',
                'render_evidence_raw_sha256':'receipt-fixture',
                'candidate_raw_sha256':'candidate-fixture','scene_raw_sha256':'scene-fixture',
                'media_raw_sha256':'video-fixture','labeling_rule_sha256':RULE_SHA,
                'visual':{'verdict':'ACCEPT','reason':'synthetic fixture only; not real acceptance'},
                'semantic_pairs':[{'split':'eval','id':'fixture-1','problem_sha256':'p1',
                     'verdict':'DIFFERENT_CORE_TASK','reason':'synthetic fixture only'}]}
        return evidence,review

    def test_transport_binds_actual_files(self):
        self.assertEqual(self.verify(),self.result['output'])

    def test_explicit_returncode_required(self):
        for rc in [True,False,1,None]:
            d=copy.deepcopy(self.result);d['transport']['rc']=rc
            with self.subTest(rc=rc),self.assertRaises(ValueError):self.verify(d)

    def test_render_ok_alone_is_insufficient(self):
        with self.assertRaises(ValueError):self.verify({'ok':True})

    def test_missing_cleanup_refused(self):
        d=copy.deepcopy(self.result)
        d['transport']['parent_evidence']['private_profile']['cleanup_complete']=False
        with self.assertRaises(ValueError):self.verify(d)

    def test_failed_acl_refused(self):
        d=copy.deepcopy(self.result)
        d['transport']['parent_evidence']['private_profile']['temporary_acl'][0]['restored']=False
        with self.assertRaises(ValueError):self.verify(d)

    def test_capability_token_refused(self):
        d=copy.deepcopy(self.result);d['transport']['parent_evidence']['token']['capability_count']=1
        with self.assertRaises(ValueError):self.verify(d)

    def test_parent_evidence_disagreement_refused(self):
        d=copy.deepcopy(self.result);d['isolation']['parent_evidence']={}
        with self.assertRaises(ValueError):self.verify(d)

    def test_host_command_refused(self):
        d=copy.deepcopy(self.result);d['transport']['command']=['python','scene.py']
        with self.assertRaises(ValueError):self.verify(d)

    def test_scene_tamper_refused(self):
        p=self.work/'scene.py';p.write_text('pass\n',encoding='utf-8')
        d=copy.deepcopy(self.result);d['transport']['source_sha256']=raw_sha(p.read_bytes())
        with self.assertRaises(ValueError):self.verify(d)

    def test_log_tamper_refused(self):
        (self.work/'stdout.txt').write_text('different',encoding='utf-8')
        with self.assertRaises(ValueError):self.verify()

    def test_media_tamper_refused(self):
        Path(self.result['output']['path']).write_bytes(b'changed')
        with self.assertRaises(ValueError):self.verify()

    def test_wrong_decoded_metadata_refused(self):
        changed=copy.deepcopy(self.result['output']);changed['frames']=3
        with self.assertRaises(ValueError):self.verify(decoder=lambda p:changed)

    def test_source_race_refused(self):
        def mutate(p):
            (self.work/'scene.py').write_text('changed\n',encoding='utf-8')
            return self.result['output']
        with self.assertRaises(ValueError):self.verify(decoder=mutate)

    def test_foreign_media_refused(self):
        p=self.base/'foreign.mp4';p.write_bytes(b'x')
        d=copy.deepcopy(self.result);d['output']={'path':str(p),'sha256':raw_sha(b'x'),
                                              'size':1,'frames':1,'width':1,'height':1,'frame_rate':'15'}
        with self.assertRaises(ValueError):self.verify(d)

    def test_old_unbound_receipt_refused(self):
        before=self.active_hashes()
        with self.assertRaises(ValueError):
            render.verify_evidence(Snapshot(ROOT),ROOT/'reviews/2026-10-06-linalg048-admission/render-evidence.json')
        self.assertEqual(before,self.active_hashes())

    def test_output_exists_refused_before_execution(self):
        p=self.base/'already.json';p.write_text('{}')
        renderer=mock.Mock()
        with self.assertRaises(ValueError):render.publish_render(p,renderer=renderer)
        renderer.assert_not_called()

    def test_failed_render_writes_no_receipt_or_active_data(self):
        p=self.base/'render.json';before=self.active_hashes()
        with self.assertRaises(ValueError):
            render.publish_render(p,renderer=lambda scene:{'ok':False,'status':'failed'})
        self.assertFalse(p.exists());self.assertEqual(before,self.active_hashes())

    def test_unreviewed_scene_refused_before_execution(self):
        p=self.base/'wrong-scene.py';p.write_text('pass\n');renderer=mock.Mock()
        with self.assertRaises(ValueError):render.publish_render(self.base/'out.json',scene_path=p,renderer=renderer)
        renderer.assert_not_called()

    def test_math_guard_survives_optimization(self):
        code = ("import sys;sys.path[:0]=["+repr(str(ROOT/'tools'))+","+repr(str(ROOT/'src'))+
                "];import prepare_linalg048_rewrite as p;import copy;c=copy.deepcopy(p.CANDIDATE);"
                "c['problem']=c['problem'].replace('1&3','1&9');"
                "\ntry:p.math_checks(c)\nexcept ValueError:sys.exit(0)\nsys.exit(1)")
        p=subprocess.run([sys.executable,'-O','-B','-c',code],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)

    def test_manual_binding_mismatch_refused(self):
        e,r=self.review_fixture()
        for key in ['media_raw_sha256','candidate_raw_sha256','labeling_rule_sha256']:
            bad=copy.deepcopy(r);bad[key]='wrong'
            with self.subTest(key=key),self.assertRaises(ValueError):
                apply.require_manual_review(bad,e,'receipt-fixture')

    def test_missing_full_semantic_review_refused(self):
        e,r=self.review_fixture();r['semantic_pairs']=[]
        with self.assertRaises(ValueError):apply.require_manual_review(r,e,'receipt-fixture')

    def test_duplicate_semantic_review_refused(self):
        e,r=self.review_fixture()
        e['semantic_subjects'].append({'split':'test','id':'fixture-2','problem_sha256':'p2'})
        r['semantic_pairs'].append(copy.deepcopy(r['semantic_pairs'][0]))
        with self.assertRaises(ValueError):apply.require_manual_review(r,e,'receipt-fixture')

    def test_uncertain_semantic_review_refused(self):
        e,r=self.review_fixture();r['semantic_pairs'][0]['verdict']='UNCERTAIN'
        with self.assertRaises(ValueError):apply.require_manual_review(r,e,'receipt-fixture')

    def test_visual_rejection_refused(self):
        e,r=self.review_fixture();r['visual']['verdict']='REJECT'
        with self.assertRaises(ValueError):apply.require_manual_review(r,e,'receipt-fixture')

    def test_manual_fixture_coverage_validates(self):
        e,r=self.review_fixture()
        self.assertEqual(apply.require_manual_review(r,e,'receipt-fixture'),r['reviewer'])

    def test_proposal_io_failure_cannot_change_active_data(self):
        before=self.active_hashes();p=self.base/'proposal.json'
        evidence,review=self.review_fixture()
        ep=self.base/'receipt.json';ep.write_text('{}')
        review['render_evidence_raw_sha256']=raw_sha(ep.read_bytes())
        rp=self.base/'review.json';rp.write_text(json.dumps(review))
        with mock.patch.object(render,'verify_evidence',return_value=({'id':'fixture-only'},evidence)), \
             mock.patch.object(apply,'write_new_json',side_effect=OSError('injected I/O failure')):
            with self.assertRaises(OSError):apply.publish_proposal(p,ep,rp)
        self.assertFalse(p.exists());self.assertEqual(before,self.active_hashes())

    def test_progress_rebind_preserves_all_statuses(self):
        before=self.active_hashes()
        original=json.loads((ROOT/'data/asset_evidence.json').read_text(encoding='utf-8'))
        output=apply.refresh_progress(self.base/'progress.json')
        self.assertEqual(output['n_verified_assets'],original['n_verified_assets'])
        for key,row in original['records'].items():
            for field in ['math','semantic','render']:
                self.assertEqual(output['records'][key][field],row[field])
        self.assertEqual(before,self.active_hashes())

    def test_progress_cannot_reuse_review_of_changed_input(self):
        progress=json.loads((ROOT/'data/asset_evidence.json').read_text(encoding='utf-8'))
        progress['records']['calc-derivative-001']['input_sha256']='0'*64
        p=self.base/'bad-progress.json';p.write_text(json.dumps(progress),encoding='utf-8')
        out=self.base/'refreshed.json'
        with mock.patch.object(apply,'ASSET_EVIDENCE',p),self.assertRaises(ValueError):
            apply.refresh_progress(out)
        self.assertFalse(out.exists())


    def test_parent_memory_guard_refused(self):
        d=copy.deepcopy(self.result);d['transport']['parent_evidence']['memory_limit_mb']=1
        with self.assertRaises(ValueError):self.verify(d)

    def test_boolean_media_metadata_refused(self):
        d=copy.deepcopy(self.result);d['output']['frames']=True
        with self.assertRaises(ValueError):self.verify(d)

    def test_bound_receipt_roundtrip_and_extra_bindings_refused(self):
        # Synthetic transport/decoder fixture only; no actual Manim or acceptance.
        path=self.base/'bound-fixture.json'
        def renderer(scene):
            self.scene=scene
            (self.work/'scene.py').write_text(scene,encoding='utf-8',newline='\n')
            self.result['transport']['source_sha256']=raw_sha((self.work/'scene.py').read_bytes())
            return self.result
        with mock.patch.object(render.sandbox,'decode_video',return_value=self.result['output']):
            data=render.publish_render(path,renderer=renderer)
            cand,verified=render.verify_evidence(Snapshot(ROOT),path)
            self.assertFalse(verified['accepted']);self.assertEqual(cand['id'],'linalg-048')
            data['source_bindings']['unexpected/path']={'raw_sha256':'0'*64,'bytes':1}
            bad=self.base/'bad-binding.json';bad.write_text(json.dumps(data),encoding='utf-8')
            with self.assertRaises(ValueError):render.verify_evidence(Snapshot(ROOT),bad)

    def test_valid_proposal_is_inactive(self):
        evidence,review=self.review_fixture();before=self.active_hashes()
        ep=self.base/'receipt.json';ep.write_text('{}')
        review['render_evidence_raw_sha256']=raw_sha(ep.read_bytes())
        rp=self.base/'review.json';rp.write_text(json.dumps(review))
        with mock.patch.object(render,'verify_evidence',return_value=({'id':'fixture-only'},evidence)):
            p=apply.publish_proposal(self.base/'proposal.json',ep,rp)
        self.assertFalse(p['active_data_modified']);self.assertFalse(p['training_admitted'])
        self.assertEqual(before,self.active_hashes())


if __name__ == '__main__':
    unittest.main()
