"""Independent regression cases for evidence mistakes and grant-root validation."""
import ast
import contextlib
import ctypes
import io
import json
import socket
import sys
import tempfile
import types
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[3]
PROBES=ROOT/'reviews/2026-10-06-exec-isolation-full-surface'
sys.path[:0]=[str(PROBES),str(ROOT/'src')]
import surface_probe_contract as contract
import surface_probe_suite as suite
import animtrain.private_profile as profile

class EvidenceTests(unittest.TestCase):
    def setUp(self):self.n={'before':'before-exact','sandbox':'sandbox-exact','after':'after-exact'}
    def verdict(self,state,packets=None,complete=True,ns=20_000_000_000):
        return contract.classify_delivery(state,packets if packets is not None else [self.n['before'],self.n['after']],self.n,complete,ns)
    def test_substring_is_not_before_control(self):
        self.assertEqual(self.verdict({'outcome':'sent'},['probe-lan-before-exact','after-exact']),'UNKNOWN')
    def test_after_control_is_not_sandbox_hit(self):
        self.assertEqual(self.verdict({'outcome':'sent'}),'BOUNDED_NO_DELIVERY')
    def test_exact_sandbox_packet_fails(self):
        self.assertEqual(self.verdict({'outcome':'sent'},list(self.n.values())),'FAIL')
    def test_missing_before_unknown(self):self.assertEqual(self.verdict({'outcome':'sent'},['after-exact']),'UNKNOWN')
    def test_duplicate_control_unknown(self):self.assertEqual(self.verdict({'outcome':'sent'},['before-exact','before-exact','after-exact']),'UNKNOWN')
    def test_incomplete_receiver_unknown(self):self.assertEqual(self.verdict({'outcome':'sent'},complete=False),'UNKNOWN')
    def test_short_window_unknown(self):self.assertEqual(self.verdict({'outcome':'sent'},ns=19_999_999_999),'UNKNOWN')
    def test_unexplained_error_unknown(self):self.assertEqual(self.verdict({'outcome':'error','winerror':None}),'UNKNOWN')
    def test_permission_error_needs_exact_code(self):
        self.assertEqual(self.verdict({'outcome':'os_denied','winerror':10013}),'SCOPED_PASS')
        self.assertEqual(self.verdict({'outcome':'os_denied','winerror':10051}),'UNKNOWN')
    def test_file_not_found_not_access_denied(self):
        self.assertEqual(contract.classify_permission({'outcome':'error','winerror':2},True),'UNKNOWN')
    def test_permission_requires_live_control(self):
        self.assertEqual(contract.classify_permission({'outcome':'os_denied','winerror':5},False),'UNKNOWN')
        self.assertEqual(contract.classify_permission({'outcome':'os_denied','winerror':5},True),'SCOPED_PASS')
    def test_entire_output_must_parse(self):
        with self.assertRaises(ValueError):contract.parse_observations({'rc':0,'stdout':'log\n{}'})
    def test_nonzero_rc_not_pass(self):
        with self.assertRaises(ValueError):contract.parse_observations({'rc':2,'stdout':'{}'})
    def test_exclusive_save_preserves_existing_bytes(self):
        f=PROBES/('exclusive-test-'+uuid.uuid4().hex+'.json')
        contract.save_exclusive(f,{'sentinel':'first'})
        before=f.read_bytes()
        with self.assertRaises(FileExistsError):contract.save_exclusive(f,{'sentinel':'overwrite'})
        self.assertEqual(f.read_bytes(),before)
    def test_save_cannot_escape_directory(self):
        with self.assertRaises(ValueError):contract.save_exclusive(ROOT/'escaped.json',{})
    def test_udp_v4_healthy_fixture_and_stop(self):
        r=contract.Receiver('udp',socket.AF_INET)
        try:self.assertTrue(contract.host_control(r,'owned-nonce')['received_exactly_once'])
        finally:r.close()
        self.assertEqual(r.packets,['owned-nonce']);self.assertTrue(r.complete);self.assertFalse(r.thread.is_alive())
    def test_udp_v6_healthy_fixture_and_stop(self):
        r=contract.Receiver('udp',socket.AF_INET6)
        try:self.assertTrue(contract.host_control(r,'owned-v6')['received_exactly_once'])
        finally:r.close()
        self.assertEqual(r.packets,['owned-v6']);self.assertTrue(r.complete)
    def test_http_nonce_path_and_stop(self):
        r=contract.Receiver('http')
        try:self.assertTrue(contract.host_control(r,'http-owned-nonce')['received_exactly_once'])
        finally:r.close()
        self.assertEqual(r.packets,['http-owned-nonce']);self.assertTrue(r.complete)
    def test_real_socket_enum_is_serialized_as_int(self):
        code=suite.build_udp_code({'v4':{'family':socket.AF_INET,'endpoint':('127.0.0.1',1234),'nonce':'x'}})
        compile(code,'<enum-source>','exec')
        self.assertNotIn('<AddressFamily',code)
    def test_all_generated_sources_compile(self):
        inputs=[suite.build_udp_code({'v4':{'family':2,'endpoint':('127.0.0.1',1234),'nonce':'x'}}),
                suite.build_exe_code({'commands':{},'victim':'x','cmd':'cmd','fixture':'x','nonce':'x','registry_key':'x'}),
                suite.build_ipc_code({'mapping':'Global\\owned'})]
        for code in inputs:compile(code,'<reviewed-generated-source>','exec')
    def test_generated_sources_never_access_clipboard(self):
        code=suite.build_ipc_code({'pipe':'owned'})
        calls=[node.func.attr for node in ast.walk(ast.parse(code)) if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute)]
        for name in ('OpenClipboard','EmptyClipboard','GetClipboardData','SetClipboardData'):self.assertNotIn(name,calls)
    def test_api_handle_results_are_pointer_sized(self):
        env={};exec(contract.WIN32_SOURCE,env)
        dll=env['bind_kernel32']()
        for name in ('CreateFileW','CreateNamedPipeW','CreateMailslotW','CreateFileMappingW','OpenFileMappingW'):
            self.assertEqual(getattr(dll,name).restype,ctypes.wintypes.HANDLE)
        self.assertTrue(env['invalid_handle'](-1));self.assertTrue(env['invalid_handle'](ctypes.c_void_p(-1).value))
        self.assertFalse(env['invalid_handle'](0x1234567887654321))
    def test_window_class_is_explicit_and_callback_pointer_sized(self):
        env={};exec(contract.WIN32_SOURCE,env)
        self.assertTrue(issubclass(env['WNDCLASSW'],ctypes.Structure))
        self.assertEqual(ctypes.sizeof(env['LRESULT']),ctypes.sizeof(ctypes.c_void_p))
    def test_default_plan_does_not_run_native(self):
        for mode in ('udp','exe','ipc','ipc4'):
            with patch.object(suite,'source_bindings',side_effect=AssertionError('native path entered')):
                output=io.StringIO()
                with contextlib.redirect_stdout(output):self.assertEqual(suite.main(mode,[]),3)
                record=json.loads(output.getvalue());self.assertFalse(record['native_executed']);self.assertEqual(record['production_gate'],'CLOSED')
                self.assertEqual(set(record['safety_points'].values()),{'UNKNOWN'})
    def test_grant_reparse_root_rejected_before_resolve(self):
        original=Path.lstat
        def lstat(path,*args,**kwargs):
            if path==ROOT:return types.SimpleNamespace(st_mode=0o040755,st_file_attributes=0x400)
            return original(path,*args,**kwargs)
        with patch.object(Path,'lstat',lstat),patch.object(Path,'resolve',side_effect=AssertionError('resolved before reject')):
            with self.assertRaises(ValueError):profile._validated_grant_path(ROOT)
    def test_grant_reparse_ancestor_rejected(self):
        target=PROBES;original=Path.lstat
        def lstat(path,*args,**kwargs):
            if path==ROOT/'reviews':return types.SimpleNamespace(st_mode=0o040755,st_file_attributes=0x400)
            return original(path,*args,**kwargs)
        with patch.object(Path,'lstat',lstat):
            with self.assertRaises(ValueError):profile._validated_grant_path(target)
    def test_grant_regular_roots_allowed(self):
        self.assertEqual(profile._validated_grant_path(ROOT),ROOT.resolve())
        self.assertEqual(profile._validated_grant_path(Path(r'D:\Python')),Path(r'D:\Python').resolve())
    def test_grant_unreviewed_root_rejected(self):
        with self.assertRaises(ValueError):profile._validated_grant_path(Path(r'D:\code'))

if __name__=='__main__':unittest.main(verbosity=2)