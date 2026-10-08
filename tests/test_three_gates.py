"""Fail-closed transport and structural-screen regression boundaries."""
import sys,json,tempfile,unittest
from pathlib import Path
from unittest import mock
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from animtrain import sandbox_execution as se
from animtrain.render_gate import render_check
from animtrain.structural_leakage import compare,normalize

class TransportTests(unittest.TestCase):
    def test_missing_acceptance_blocks_generated_code_before_launch(self):
        with mock.patch.object(se,'check_certificate',return_value=(False,"missing")), mock.patch.object(se,'render_scene') as launch:
            result=render_check('from manim import *',trusted=False)
        self.assertFalse(result['ok']);launch.assert_not_called()

    def test_self_authored_certificate_cannot_claim_private_transport(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'reviews/codex-supervision') as d:
            p=Path(d)/'e.json';p.write_text(json.dumps({'schema':'production-appcontainer-v1','fs_isolation':'private_per_run','implementation_sha256':{n:se.digest(ROOT/n) for n in se.BOUND_FILES},'cases':{}}),encoding='utf-8')
            self.assertFalse(se.check_certificate(p)[0])

    def test_no_host_fallback_on_non_windows(self):
        with mock.patch.object(sys,'platform','linux'),mock.patch('subprocess.Popen') as host:
            with self.assertRaises(OSError):se.run_code('print(1)',mode='probe')
        host.assert_not_called()

    def test_zero_exit_without_media_fails(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'reviews/codex-supervision') as d:
            result={'rc':0,'work':d,'parent_evidence':{'job_assigned_before_resume':True}}
            with mock.patch.object(se,'run_code',return_value=result):
                self.assertFalse(se.render_scene('source')['ok'])

    def test_corrupt_media_fails(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'reviews/codex-supervision') as d:
            p=Path(d)/'ConceptScene.mp4';p.write_bytes(b'not an mp4')
            with self.assertRaises(Exception):se.decode_video(p)

    def test_unreviewed_runtime_executable_is_rejected(self):
        with self.assertRaises(ValueError):se.run_code('print(1)',mode='probe',python=ROOT/'other.exe')

    def test_environment_secrets_cannot_enter_allowlist(self):
        with mock.patch.object(Path,'read_text',return_value=json.dumps({'GITHUB_TOKEN':'synthetic-token'})):
            with self.assertRaises(ValueError):se.runtime_env(ROOT)

class StructureTests(unittest.TestCase):
    def test_cross_signature_plane_distance_candidate(self):
        self.assertTrue(compare('求点 P(1,2,3) 到平面 2x-y+z=0 的距离。','求点 Q(3,2,1) 到平面 x+y-z=2 的距离及投影点。')['candidate'])

    def test_numeric_exponent_is_preserved(self):
        self.assertNotEqual(normalize('求 x^2 的导数'),normalize('求 x^3 的导数'))

    def test_different_math_objects_are_not_broad_keyword_clones(self):
        self.assertFalse(compare(r'求极限 $\sin x/x$。',r'求极限 $(1-\cos x)/x^2$。')['candidate'])

    def test_unknown_is_not_certified_negative(self):
        self.assertEqual(compare('全新数学对象','另一对象')['coverage'],'UNKNOWN')

    def test_score_is_exact_fraction(self):
        r=compare('求点P(1,2,3)到平面x+y+z=0距离。','求点Q(4,5,6)到平面x-y+z=2距离。')
        self.assertNotIn('.',r['score'])


class AssetSourceTests(unittest.TestCase):
    def test_prime_in_latex_is_not_deleted(self):
        from tools.render_templates import _math_segments, build_scene
        self.assertEqual(_math_segments("$f'(x)=2x$"), "f'(x)=2x")
        record={"problem":"求 $f'(x)$", "answer":"$y'=2x$", "scene_spec":{"steps":[]}}
        compile(build_scene(record),"scene.py","exec")

    def test_unreviewed_row_has_no_verified_scene(self):
        from tools.verified_scene_registry import build_scene
        with self.assertRaises(ValueError):build_scene({"id":"different"},"0"*64)


class LocalOutcomeTests(unittest.TestCase):
    def test_unknown_old_tcp_error_is_rejected(self):
        from animtrain.isolation_evidence import _local_outcome
        with self.assertRaises(ValueError):_local_outcome('tcp_loopback_v4',{'outcome':'error','winerror':None})

    def test_tcp_connection_or_short_timeout_does_not_prove_blocking(self):
        from animtrain.isolation_evidence import _local_outcome
        for state in ({'outcome':'sent'}, {'outcome':'error','error_type':'TimeoutError','winerror':None,'elapsed_ms':1}):
            with self.subTest(state=state), self.assertRaises(ValueError):_local_outcome('tcp_loopback_v6',state)

    def test_measured_timeout_requires_explicit_type(self):
        from animtrain.isolation_evidence import _local_outcome
        _local_outcome('tcp_loopback_v4',{'outcome':'error','error_type':'TimeoutError','winerror':None,'elapsed_ms':2000})
        with self.assertRaises(ValueError):_local_outcome('tcp_loopback_v4',{'outcome':'error','error_type':'OSError','winerror':None,'elapsed_ms':2000})

    def test_udp_unknown_error_is_rejected(self):
        from animtrain.isolation_evidence import _local_outcome
        _local_outcome('udp_loopback_v6',{'outcome':'sent'})
        with self.assertRaises(ValueError):_local_outcome('udp_loopback_v4',{'outcome':'error','winerror':None})
