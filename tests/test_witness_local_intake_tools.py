"""Local material/tool regressions only. No dual-endpoint execution or acceptance."""
import base64,contextlib,hashlib,importlib.util,io,json,socket,tempfile,unittest
from pathlib import Path
from unittest import mock
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/"reviews/codex-supervision/2026-10-13-tool-test-work"
SOURCE=ROOT/"reviews/codex-supervision/2026-10-06-all43-sandbox-repair/external-tests/remote-3a28dfd9dc96430a8ed0edb1989c3e76/captures/lan-2026-10-13-a-e605e0ee3a8b4388aa72271d56f473cd"
def load(name,relative):
    spec=importlib.util.spec_from_file_location(name,ROOT/relative)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
decoder=load("decoder_local_regressions","tools/decode_lan_1013_capture.py")
diagnostic=load("tcp_local_regressions","tools/witness_tcp_diagnostics.py")

class DecoderTests(unittest.TestCase):
    def setUp(self):
        WORK.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=WORK)
        self.base=Path(self.temp.name).resolve()
        self.input=self.base/"input";self.input.mkdir()
        self.registered=self.base/"registered"
        self.patch=mock.patch.object(decoder,"REGISTERED_ROOT",self.registered);self.patch.start()
        self.original={name:(SOURCE/name).read_bytes() for name in decoder.NAMES}
        self.input_snapshot={}
        for name,raw in self.original.items():
            p=self.input/(name+".b64");p.write_bytes(base64.b64encode(raw));self.input_snapshot[p.name]=p.read_bytes()
        proof=json.loads(self.original["process-exit.json"])
        self.capture_name=proof["round"]+"-"+proof["capture_id"]
    def tearDown(self):
        self.patch.stop()
        self.assertTrue(self.base.is_relative_to(WORK.resolve()))
        self.temp.cleanup()
    def result(self):
        result=decoder.decode_capture(self.input,self.registered)
        self.assertFalse(result["native_acceptance"]);self.assertEqual(result["production"],"CLOSED")
        return result
    def test_default_plan_reads_no_inputs_and_writes_nothing(self):
        with mock.patch.object(decoder,"decode_capture") as decode,contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(decoder.main([]),3)
        decode.assert_not_called();self.assertFalse(self.registered.exists())
    def test_import_has_no_io_side_effect(self):
        with mock.patch.object(Path,"write_bytes") as write, mock.patch.object(Path,"mkdir") as mkdir:
            load("decoder_import_guard","tools/decode_lan_1013_capture.py")
        write.assert_not_called();mkdir.assert_not_called()
    def test_real_originals_losslessly_roundtrip_without_modifying_inputs(self):
        result=self.result();target=Path(result["path"])
        self.assertEqual(target.name,self.capture_name)
        for name,raw in self.original.items():self.assertEqual((target/name).read_bytes(),raw)
        self.assertEqual(self.input_snapshot,{p.name:p.read_bytes() for p in self.input.iterdir()})
    def test_wrapped_transport_and_explicit_empty_stderr_are_valid(self):
        for p in self.input.iterdir():
            b=p.read_bytes();p.write_bytes(b"\r\n".join(b[i:i+64] for i in range(0,len(b),64)))
        self.result()
    def test_existing_capture_is_never_overwritten(self):
        target=self.registered/self.capture_name;target.mkdir(parents=True);sentinel=target/"original";sentinel.write_bytes(b"unchanged")
        with self.assertRaises(FileExistsError):self.result()
        self.assertEqual(sentinel.read_bytes(),b"unchanged");self.assertEqual(list(target.iterdir()),[sentinel])
    def test_corrupted_base64_fails_before_any_output(self):
        p=self.input/"stdout.bin.b64";p.write_bytes(p.read_bytes()+b"!")
        with self.assertRaises(Exception):self.result()
        self.assertFalse(self.registered.exists())
    def test_hash_mismatch_cannot_be_repaired_by_decoder(self):
        p=self.input/"receiver.jsonl.summary.json.b64";p.write_bytes(base64.b64encode(self.original["receiver.jsonl.summary.json"]+b" "))
        with self.assertRaisesRegex(ValueError,"parent-process hashes"):self.result()
        self.assertFalse(self.registered.exists())
    def test_missing_stderr_is_not_silently_fabricated(self):
        (self.input/"stderr.bin.b64").unlink()
        with self.assertRaisesRegex(ValueError,"Base64 source required"):self.result()
        self.assertFalse(self.registered.exists())
    def test_duplicate_alias_is_rejected(self):
        (self.input/"stdout.b64").write_bytes((self.input/"stdout.bin.b64").read_bytes())
        with self.assertRaisesRegex(ValueError,"Exactly one"):self.result()
    def test_output_escape_and_traversal_are_rejected(self):
        for target in (self.base/"outside",self.registered/"../escape"):
            with self.subTest(target=target),self.assertRaises(ValueError):decoder.decode_capture(self.input,target)
        self.assertFalse((self.base/"outside").exists())
    def test_reparse_input_is_rejected_before_read(self):
        with mock.patch.object(Path,"is_symlink",return_value=True),self.assertRaisesRegex(ValueError,"Reparse"):
            self.result()
    def test_io_failure_never_publishes_partial_capture(self):
        with mock.patch.object(decoder.json,"dump",side_effect=OSError("controlled write failure")),self.assertRaises(OSError):
            self.result()
        self.assertFalse((self.registered/self.capture_name).exists())
        self.assertEqual(len(list(self.registered.glob(".decode-stage-*"))),1)
    def test_invalid_cli_is_failed_without_network(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(decoder.main(["--execute"]),2)
        self.assertFalse(self.registered.exists())

class DiagnosticTests(unittest.TestCase):
    def sock(self):
        s=mock.MagicMock();s.__enter__.return_value=s;return s
    def test_plan_never_creates_socket(self):
        with mock.patch.object(diagnostic.socket,"socket") as sockets,contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(diagnostic.main(["192.0.2.1","49002"]),3)
        sockets.assert_not_called()
    def test_import_of_wrappers_never_connects(self):
        with mock.patch.object(diagnostic.socket,"socket") as sockets:
            load("tcp_check_import","tools/oneoff_tcp_check.py")
            load("tcp_banner_import","tools/oneoff_tcp_banner.py")
        sockets.assert_not_called()
    def test_time_is_exact_fraction_not_rounded_decimal(self):
        s=self.sock();s.connect_ex.return_value=0
        with mock.patch.object(diagnostic.socket,"socket",return_value=s),mock.patch.object(diagnostic.time,"monotonic_ns",side_effect=[1,333334]):
            result=diagnostic.probe("192.0.2.1",49002)
        self.assertEqual(result["elapsed_ns"],333333);self.assertEqual(result["elapsed_ms_exact"],"333333/1000000")
        self.assertNotIn("elapsed_ms",result);self.assertFalse(result["receiver_delivery_verified"]);s.__exit__.assert_called_once()
    def test_refusal_and_timeout_never_imply_healthy_witness_or_blocking_cause(self):
        for code,outcome in ((10061,"CONNECTION_REFUSED"),(10060,"TIMEOUT_UNCONFIRMED"),(10013,"OS_ACCESS_DENIED")):
            s=self.sock();s.connect_ex.return_value=code
            with mock.patch.object(diagnostic.socket,"socket",return_value=s):
                result=diagnostic.probe("192.0.2.1",49002)
            self.assertEqual(result["outcome"],outcome);self.assertEqual(result["qualification"],"NOT_ESTABLISHED")
    def test_connect_and_timeout_setup_errors_close_socket(self):
        for method in ("settimeout","connect_ex"):
            s=self.sock();getattr(s,method).side_effect=OSError("controlled error")
            with mock.patch.object(diagnostic.socket,"socket",return_value=s):
                result=diagnostic.probe("192.0.2.1",49002)
            self.assertEqual(result["outcome"],"SOCKET_ERROR");s.__exit__.assert_called_once()
    def test_constructor_failure_is_structured(self):
        with mock.patch.object(diagnostic.socket,"socket",side_effect=OSError("constructor")):
            result=diagnostic.probe("192.0.2.1",49002)
        self.assertEqual(result["outcome"],"SOCKET_ERROR")
    def test_banner_bytes_are_lossless_and_timeout_distinct_from_eof(self):
        for payload,expected in ((b"\xff\x00","DATA"),(b"","EOF"),(TimeoutError("deadline"),"TIMEOUT_UNCONFIRMED")):
            s=self.sock();s.connect_ex.return_value=0
            if isinstance(payload,Exception):s.recv.side_effect=payload
            else:s.recv.return_value=payload
            with mock.patch.object(diagnostic.socket,"socket",return_value=s):
                result=diagnostic.probe("192.0.2.1",49002,banner=True)
            self.assertEqual(result["read_outcome"],expected)
            if isinstance(payload,bytes):self.assertEqual(result["first_bytes_hex"],payload.hex())
            s.__exit__.assert_called_once()
    def test_ipv6_literal_uses_v6_socket(self):
        s=self.sock();s.connect_ex.return_value=0
        with mock.patch.object(diagnostic.socket,"socket",return_value=s) as factory:
            diagnostic.probe("2001:db8::1",49002)
        factory.assert_called_once_with(socket.AF_INET6,socket.SOCK_STREAM)
    def test_invalid_target_never_opens_socket(self):
        for host,port in (("example.com",49002),("0.0.0.0",49002),("ff02::1",49002),("192.0.2.1",0),("192.0.2.1",True)):
            with self.subTest(host=host,port=port),mock.patch.object(diagnostic.socket,"socket") as sockets,self.assertRaises(ValueError):
                diagnostic.probe(host,port)
            sockets.assert_not_called()

if __name__=="__main__":unittest.main()
