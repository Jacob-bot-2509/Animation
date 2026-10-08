"""Independent negative contracts for configured and observed local isolation."""
from __future__ import annotations
import copy
import ctypes
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from animtrain import network_isolation as net

def valid():
    sid = "S-1-15-2-123-456"
    nonces = dict(before="a" * 32, sandbox="b" * 32, after="c" * 32)
    clients = {}
    for side, start, end in [("before", 1, 2), ("sandbox", 3, 6), ("after", 27, 28)]:
        clients[side] = dict(rc=0, timed_out=False, data=dict(host="127.0.0.1", port=12345,
            transport="udp", nonce=nonces[side], started=start, finished=end,
            token=dict(api_ok=True, is_appcontainer=side == "sandbox", capability_count=0,
                       sid=sid if side == "sandbox" else None),
            outcome="sent_ok", winerror=None))
    return dict(host="127.0.0.1", port=12345, transport="udp", expected_sid=sid, nonces=nonces,
                clients=clients, packets=[dict(hex=nonces[s].encode().hex(), at=t) for s,t in [("before",2),("after",28)]],
                policy_before=dict(api_ok=True, return_code=0, cleanup_ok=True, sids=[]),
                policy_after=dict(api_ok=True, return_code=0, cleanup_ok=True, sids=[]),
                runtime_integrity=True, server_started=0, server_closed=29,
                server_complete=True, server_errors=[])

class TestLoopbackJudgment(unittest.TestCase):
    def assertUnverified(self, r):
        self.assertEqual(net.judge_loopback_evidence(r)["verdict"], "UNVERIFIED")
    def test_udp_configured_observed_scope(self):
        self.assertEqual(net.judge_loopback_evidence(valid())["verdict"], "PASS_LOCAL_LOOPBACK")
    def test_tcp_timeout_supported_without_inventing_wsa_error(self):
        r=valid(); r["transport"]="tcp"
        for c in r["clients"].values(): c["data"]["transport"]="tcp"
        r["clients"]["sandbox"]["data"]["outcome"]="net_timeout"
        self.assertEqual(net.judge_loopback_evidence(r)["verdict"], "PASS_LOCAL_LOOPBACK")
    def test_delivery_wins_over_other_bad_evidence(self):
        r=valid(); r["runtime_integrity"]=False; r["clients"]["before"]["rc"]=1
        r["packets"].append(dict(hex=r["nonces"]["sandbox"].encode().hex(),at=5))
        self.assertEqual(net.judge_loopback_evidence(r)["verdict"],"FAIL")
    def test_silent_drop_alone_never_passes(self):
        r=valid(); del r["policy_before"]; self.assertUnverified(r)
    def test_api_failure_unknown_or_exempt_profile(self):
        for mode in ["api", "unknown", "exempt", "cleanup", "changed"]:
            with self.subTest(mode=mode):
                r=valid()
                if mode=="api": r["policy_before"].update(api_ok=False,return_code=5)
                if mode=="unknown": r["policy_before"]["sids"]=None
                if mode=="exempt": r["policy_before"]["sids"]=[r["expected_sid"]]
                if mode=="cleanup": r["policy_before"]["cleanup_ok"]=False
                if mode=="changed": r["policy_after"]["sids"]=["S-1-15-2-999"]
                self.assertUnverified(r)
    def test_receiver_failure_or_missing_control(self):
        for mode in ["error","unfinished","no_before","no_after","duplicate","foreign","partial"]:
            with self.subTest(mode=mode):
                r=valid()
                if mode=="error": r["server_errors"]=["receiver failed"]
                if mode=="unfinished": r["server_complete"]=False
                if mode=="no_before": r["packets"]=r["packets"][1:]
                if mode=="no_after": r["packets"]=r["packets"][:1]
                if mode=="duplicate": r["packets"].append(r["packets"][0])
                if mode=="foreign": r["packets"].append(dict(hex="00",at=5))
                if mode=="partial": r["packets"].append(dict(hex=r["nonces"]["sandbox"][:3].encode().hex(),at=5))
                self.assertUnverified(r)
    def test_token_identity_capability_and_exit_failures(self):
        for mode in ["api","sid","not_ac","cap","rc","timeout","data","runtime"]:
            with self.subTest(mode=mode):
                r=valid(); c=r["clients"]["sandbox"]; t=c["data"]["token"]
                if mode=="api": t["api_ok"]=False
                if mode=="sid": t["sid"]="S-1-15-2-other"
                if mode=="not_ac": t["is_appcontainer"]=False
                if mode=="cap": t["capability_count"]=1
                if mode=="rc": c["rc"]=7
                if mode=="timeout": c["timed_out"]=True
                if mode=="data": c["data"]=None
                if mode=="runtime": r["runtime_integrity"]=False
                self.assertUnverified(r)
    def test_external_endpoint_invalid_order_or_short_window(self):
        for mode in ["external","other_port","same_nonce","old_listener","short","reordered"]:
            with self.subTest(mode=mode):
                r=valid()
                if mode=="external": r["host"]="8.8.8.8"
                if mode=="other_port": r["clients"]["sandbox"]["data"]["port"]=999
                if mode=="same_nonce": r["nonces"]["after"]=r["nonces"]["before"]
                if mode=="old_listener": r["server_closed"]=1
                if mode=="short": r["clients"]["after"]["data"]["started"]=7
                if mode=="reordered": r["clients"]["before"]["data"]["finished"]=5
                self.assertUnverified(r)
    def test_refused_or_unknown_error_not_pass(self):
        for code in [10061,None,123]:
            r=valid(); r["clients"]["sandbox"]["data"].update(outcome="net_error",winerror=code)
            self.assertUnverified(r)
    def test_tcp_sent_without_receipt_not_pass(self):
        r=valid(); r["transport"]="tcp"
        for c in r["clients"].values(): c["data"]["transport"]="tcp"
        self.assertUnverified(r)
    def test_standalone_client_compiles_without_project_import(self):
        text=net.client_source(); compile(text,"<client>","exec")
        self.assertNotIn("from animtrain",text)

@unittest.skipUnless(sys.platform == "win32", "Windows ctypes prototypes")
class TestReadOnlyConfigOwnership(unittest.TestCase):
    def check_config(self, conversion_failure=False, free_failure=False, api_error=0):
        keep = []
        k = mock.MagicMock(); a = mock.MagicMock(); fw = mock.MagicMock()
        k.GetProcessHeap.return_value = 1
        k.HeapFree.return_value = not free_failure
        def config(count_arg, pointer_arg):
            struct = type(pointer_arg._obj)._type_
            array = (struct * 2)()
            array[0].Sid = 1001; array[1].Sid = 1002
            keep.append(array)
            ctypes.cast(count_arg,ctypes.POINTER(net.wintypes.DWORD)).contents.value=2
            ctypes.cast(pointer_arg,ctypes.POINTER(ctypes.POINTER(struct)))[0]=array
            return api_error
        fw.NetworkIsolationGetAppContainerConfig.side_effect=config
        def convert(sid, text_arg):
            if conversion_failure:
                ctypes.set_last_error(5)
                return False
            buf=ctypes.create_unicode_buffer("S-1-15-2-"+str(sid))
            keep.append(buf)
            ctypes.cast(text_arg,ctypes.POINTER(net.wintypes.LPWSTR))[0]=ctypes.cast(buf,net.wintypes.LPWSTR)
            return True
        a.ConvertSidToStringSidW.side_effect=convert
        dlls={"kernel32":k,"advapi32":a,"Firewallapi":fw}
        with mock.patch.object(ctypes,"WinDLL",side_effect=lambda name,**kw:dlls[name]):
            result=net.read_loopback_exemptions()
        self.assertEqual(k.HeapFree.call_count,3)  # Each SID and the API-owned array.
        self.assertEqual(k.HeapFree.call_args_list[0].args[2],1001)
        self.assertEqual(k.HeapFree.call_args_list[1].args[2],1002)
        return result
    def test_success_copies_then_frees(self):
        self.assertTrue(self.check_config()["api_ok"])
    def test_conversion_failure_frees_all_and_is_unknown(self):
        self.assertFalse(self.check_config(conversion_failure=True)["api_ok"])
    def test_free_failure_cannot_be_success(self):
        self.assertFalse(self.check_config(free_failure=True)["api_ok"])
    def test_api_error_preserves_code_and_frees_owned_output(self):
        result=self.check_config(api_error=5)
        self.assertEqual(result["return_code"],5)
        self.assertFalse(result["api_ok"])

if __name__ == "__main__": unittest.main()
