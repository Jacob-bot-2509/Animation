"""Independent negative contracts for configured and observed local isolation."""
from __future__ import annotations
import copy
import ctypes
import inspect
import socket
import sys
import time
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
    def test_known_sandbox_delivery_survives_malformed_sibling_fields(self):
        r=valid();r["nonces"]["before"]=None;r["packets"].append(None)
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
        self.assertTrue(text.startswith(inspect.getsource(net.token_identity)))
    def test_wsa_access_denied_supported_for_tcp_and_udp(self):
        for transport in ("tcp", "udp"):
            r=valid(); r["transport"]=transport
            for c in r["clients"].values(): c["data"]["transport"]=transport
            r["clients"]["sandbox"]["data"].update(outcome="net_error",winerror=10013)
            self.assertEqual(net.judge_loopback_evidence(r)["verdict"], "PASS_LOCAL_LOOPBACK")
    def test_review_malformed_fields_are_unknown_not_exceptions(self):
        for field,value in [("expected_sid",None),("policy_before",None),("nonce",b"b"*32),
                            ("client",[]),("data","bad"),("token",[]),("clients",None),
                            ("server_errors",None),("server_errors",False),("server_errors",{}),
                            ("server_errors",""),("expected_sid","S-1-15-2-x-1")]:
            with self.subTest(field=field,value=value):
                r=valid()
                if field=="nonce": r["nonces"]["sandbox"]=value
                elif field=="client": r["clients"]["sandbox"]=value
                elif field in ("data","token"):
                    if field=="data": r["clients"]["sandbox"]["data"]=value
                    else: r["clients"]["sandbox"]["data"]["token"]=value
                else: r[field]=value
                self.assertUnverified(r)
        for value in (None,[],"record",False): self.assertUnverified(value)
    def test_packet_timestamp_required_finite_in_lifetime_and_after_client_start(self):
        for value in (None, -1, 30, float("nan"), float("inf"), True, "2", 0):
            with self.subTest(value=value):
                r=valid(); r["packets"][0]["at"]=value; self.assertUnverified(r)
        r=valid(); del r["packets"][0]["at"]; self.assertUnverified(r)
    def test_listener_and_client_unknown_or_nonfinite_timestamps(self):
        for value in (None,float("nan"),float("inf"),True,"0"):
            r=valid(); r["server_started"]=value; self.assertUnverified(r)
            r=valid(); r["clients"]["sandbox"]["data"]["finished"]=value; self.assertUnverified(r)
    def test_structural_unknowns_cannot_be_coerced_to_success(self):
        for mode in ("cap_bool","rc_bool","api_code_bool","port_bool","sid_items","nonce_unicode"):
            r=valid()
            if mode=="cap_bool": r["clients"]["sandbox"]["data"]["token"]["capability_count"]=False
            if mode=="rc_bool": r["clients"]["sandbox"]["rc"]=False
            if mode=="api_code_bool": r["policy_before"]["return_code"]=False
            if mode=="port_bool": r["port"]=True
            if mode=="sid_items": r["policy_before"]["sids"]=[None]
            if mode=="nonce_unicode": r["nonces"]["sandbox"]="\u03bb"*32
            self.assertUnverified(r)

@unittest.skipUnless(sys.platform == "win32", "Windows ctypes prototypes")
class TestReadOnlyConfigOwnership(unittest.TestCase):
    def check_config(self, conversion_failure=False, free_failure=False, api_error=0, local_free_failure=False):
        keep = []
        k = mock.MagicMock(); a = mock.MagicMock(); fw = mock.MagicMock()
        k.GetProcessHeap.return_value = 1
        k.HeapFree.return_value = not free_failure
        k.LocalFree.return_value = 1 if local_free_failure else None
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
        result=self.check_config()
        self.assertTrue(result["api_ok"])
        self.assertEqual(result["sids"],["S-1-15-2-1001","S-1-15-2-1002"])
    def test_conversion_failure_frees_all_and_is_unknown(self):
        self.assertFalse(self.check_config(conversion_failure=True)["api_ok"])
    def test_free_failure_cannot_be_success(self):
        self.assertFalse(self.check_config(free_failure=True)["api_ok"])
    def test_string_free_failure_still_frees_array_and_sids(self):
        self.assertFalse(self.check_config(local_free_failure=True)["api_ok"])
    def test_api_error_preserves_code_and_frees_owned_output(self):
        result=self.check_config(api_error=5)
        self.assertEqual(result["return_code"],5)
        self.assertFalse(result["api_ok"])

    def test_null_array_positive_count_is_unknown_but_empty_list_is_valid(self):
        for count in (0,1):
            k=mock.MagicMock(); a=mock.MagicMock(); fw=mock.MagicMock()
            def config(count_arg, pointer_arg):
                ctypes.cast(count_arg,ctypes.POINTER(net.wintypes.DWORD)).contents.value=count
                return 0
            fw.NetworkIsolationGetAppContainerConfig.side_effect=config
            with mock.patch.object(ctypes,"WinDLL",side_effect=lambda name,**kw:{"kernel32":k,"advapi32":a,"Firewallapi":fw}[name]):
                result=net.read_loopback_exemptions()
            self.assertEqual(result["api_ok"],count==0)
            self.assertEqual(result["sids"],[] if count==0 else None)
            k.HeapFree.assert_not_called()


@unittest.skipUnless(sys.platform == "win32", "Windows ctypes token APIs")
class TestTokenAPI(unittest.TestCase):
    def query(self, *, open_ok=True, is_ac=True, null_sid=False, size_error=122,
              bad_size=False, conversion_ok=True, close_ok=True, local_free_ok=True,
              size_error_class=None, buffer_failure_class=None):
        k=mock.MagicMock(); a=mock.MagicMock(); keep=[]
        k.GetCurrentProcess.return_value=-1
        k.LocalFree.return_value=None if local_free_ok else 7
        def close(handle):
            # Cleanup must not overwrite the captured query/conversion error.
            ctypes.set_last_error(0 if close_ok else 6)
            return close_ok
        k.CloseHandle.side_effect=close
        def open_token(process, access, out):
            self.assertEqual(access,8)
            if not open_ok:
                ctypes.set_last_error(5); return False
            ctypes.cast(out,ctypes.POINTER(net.wintypes.HANDLE)).contents.value=99
            return True
        a.OpenProcessToken.side_effect=open_token
        def info(handle, cls, buffer, size, needed):
            self.assertEqual(handle.value,99)
            need=ctypes.cast(needed,ctypes.POINTER(net.wintypes.DWORD))
            if cls==29:
                if buffer_failure_class==29:
                    ctypes.set_last_error(87);return False
                ctypes.cast(buffer,ctypes.POINTER(net.wintypes.DWORD)).contents.value=int(is_ac)
                need.contents.value=ctypes.sizeof(net.wintypes.DWORD)
                return True
            self.assertIn(cls,(30,31))
            if buffer is None:
                need.contents.value=1 if bad_size else 64
                ctypes.set_last_error(size_error if size_error_class in (None,cls) else 122); return False
            self.assertEqual(size,64)
            if cls==buffer_failure_class:
                ctypes.set_last_error(87);return False
            if cls==30: ctypes.cast(buffer,ctypes.POINTER(net.wintypes.DWORD)).contents.value=0
            else: ctypes.cast(buffer,ctypes.POINTER(net.wintypes.LPVOID)).contents.value=None if null_sid else 1234
            return True
        a.GetTokenInformation.side_effect=info
        def convert(sid, output):
            if not conversion_ok:
                ctypes.set_last_error(5); return False
            self.assertEqual(sid.value,1234)
            buf=ctypes.create_unicode_buffer("S-1-15-2-123-456");keep.append(buf)
            ctypes.cast(output,ctypes.POINTER(net.wintypes.LPWSTR))[0]=ctypes.cast(buf,net.wintypes.LPWSTR)
            return True
        a.ConvertSidToStringSidW.side_effect=convert
        with mock.patch.object(ctypes,"WinDLL",side_effect=lambda name,**kw:{"kernel32":k,"advapi32":a}[name]):
            result=net.token_identity()
        if open_ok:
            k.CloseHandle.assert_called_once()
            self.assertEqual(k.CloseHandle.call_args.args[0].value,99)
        else: k.CloseHandle.assert_not_called()
        return result,k,a
    def test_class_29_30_31_size_queries_and_sid_copy(self):
        r,k,a=self.query()
        self.assertEqual(r,dict(api_ok=True,is_appcontainer=True,capability_count=0,sid="S-1-15-2-123-456"))
        self.assertEqual([call.args[1] for call in a.GetTokenInformation.call_args_list],[29,30,30,31,31])
        k.LocalFree.assert_called_once()
    def test_open_failure_has_no_handle_to_close(self):
        r,k,a=self.query(open_ok=False)
        self.assertFalse(r["api_ok"]); self.assertIn("5",r["error"])
        a.GetTokenInformation.assert_not_called()
    def test_only_error_122_is_accepted_for_size_query(self):
        for cls in (30,31):
            r,k,a=self.query(size_error=5,size_error_class=cls)
            self.assertFalse(r["api_ok"]); self.assertIn("5",r["error"])
    def test_information_buffer_failures_never_report_success(self):
        for cls in (29,30,31):
            r,k,a=self.query(buffer_failure_class=cls)
            self.assertFalse(r["api_ok"]);self.assertIn("87",r["error"])
    def test_undersized_buffer_is_unknown(self):
        self.assertFalse(self.query(bad_size=True)[0]["api_ok"])
    def test_null_sid_is_valid_only_for_ordinary_token(self):
        for is_ac in (True,False):
            r,k,a=self.query(is_ac=is_ac,null_sid=True)
            self.assertEqual(r["api_ok"],not is_ac); self.assertIsNone(r["sid"])
            a.ConvertSidToStringSidW.assert_not_called(); k.LocalFree.assert_not_called()
    def test_conversion_error_survives_close_last_error_reset(self):
        r,k,a=self.query(conversion_ok=False)
        self.assertFalse(r["api_ok"]); self.assertIn("5",r["error"])
        k.LocalFree.assert_not_called()
    def test_close_or_string_free_failure_cannot_report_api_success(self):
        self.assertFalse(self.query(close_ok=False)[0]["api_ok"])
        self.assertFalse(self.query(local_free_ok=False)[0]["api_ok"])
    def test_dll_setup_type_error_returns_unknown(self):
        with mock.patch.object(ctypes,"WinDLL",side_effect=TypeError("DLL wiring")):
            self.assertFalse(net.token_identity()["api_ok"])
            self.assertFalse(net.read_loopback_exemptions()["api_ok"])


class TestReceiver(unittest.TestCase):
    def test_native_ordinary_tcp_and_udp_receiver_records_and_closes(self):
        for transport in ("tcp","udp"):
            receiver=net.LoopbackReceiver(transport,"127.0.0.1")
            try:
                nonce=b"d"*32
                with socket.socket(socket.AF_INET,socket.SOCK_STREAM if transport=="tcp" else socket.SOCK_DGRAM) as client:
                    client.settimeout(2)
                    if transport=="tcp": client.connect(("127.0.0.1",receiver.port)); client.sendall(nonce)
                    else: client.sendto(nonce,("127.0.0.1",receiver.port))
                deadline=time.monotonic()+2
                while not receiver.snapshot() and time.monotonic()<deadline: time.sleep(0.01)
            finally: receiver.close()
            packets=receiver.snapshot()
            self.assertEqual(len(packets),1); self.assertEqual(packets[0]["hex"],nonce.hex())
            self.assertLessEqual(receiver.started,packets[0]["at"]);self.assertLessEqual(packets[0]["at"],receiver.closed)
            self.assertFalse(receiver.errors);self.assertFalse(receiver.thread.is_alive())
    def test_bind_or_thread_start_failure_closes_socket(self):
        for phase in ("bind","thread"):
            sock=mock.MagicMock();sock.getsockname.return_value=("127.0.0.1",1234)
            if phase=="bind": sock.bind.side_effect=OSError("bind failed")
            with mock.patch.object(net.socket,"socket",return_value=sock), mock.patch.object(net.threading,"Thread") as thread:
                if phase=="thread": thread.return_value.start.side_effect=RuntimeError("start failed")
                with self.assertRaises((OSError,RuntimeError)): net.LoopbackReceiver("udp","127.0.0.1")
            sock.close.assert_called_once()

if __name__ == "__main__": unittest.main()
