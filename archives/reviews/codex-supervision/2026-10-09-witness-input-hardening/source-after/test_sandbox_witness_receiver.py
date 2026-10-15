import concurrent.futures
import importlib.util
import json
import queue
import socket
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("witness_receiver", ROOT/"tools/sandbox_witness_receiver.py")
receiver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(receiver)


class WitnessReceiverTests(unittest.TestCase):
    def setUp(self):
        (ROOT/"reviews/codex-supervision/2026-10-09-witness-input-test-work").mkdir(parents=True,exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT/"reviews/codex-supervision/2026-10-09-witness-input-test-work")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def summary(self, log):
        return json.loads(log.with_suffix(log.suffix+".summary.json").read_text("utf-8"))

    def test_default_is_plan_without_socket_or_log(self):
        with mock.patch.object(receiver.socket, "socket") as socket_call:
            self.assertEqual(receiver.main([]), 3)
            socket_call.assert_not_called()

    def test_cli_invalid_wildcard_loopback_reserved_and_port_bind_never_opens_socket(self):
        for bind in ("0.0.0.0","::","127.0.0.1","::1","224.0.0.1","ff02::1","fe80::1","169.254.2.3","255.255.255.255"):
            with self.subTest(bind=bind), mock.patch.object(receiver.socket,"socket") as connect:
                self.assertEqual(receiver.main(["--serve","--bind",bind,"--log",str(self.root/"invalid.jsonl")]),2)
                connect.assert_not_called()
                self.assertFalse((self.root/"invalid.jsonl").exists())
        for ports in (["--udp-port","0"],["--tcp-port","49001"]):
            with mock.patch.object(receiver.socket,"socket") as connect:
                self.assertEqual(receiver.main(["--serve","--bind","192.0.2.10","--log",str(self.root/"invalid.jsonl"),*ports]),2)
                connect.assert_not_called()

    def test_cli_selftest_serve_are_mutually_exclusive(self):
        with mock.patch.object(receiver,"selftest") as selftest, self.assertRaises(SystemExit) as caught:
            receiver.main(["--selftest","--serve"])
        self.assertEqual(caught.exception.code,2)
        selftest.assert_not_called()

    def test_invalid_bind_ports_and_window(self):
        cases = [("localhost",0,0,20),("127.0.0.1",80,0,20),
                 ("127.0.0.1",True,0,20),("127.0.0.1",0,65536,20),
                 ("127.0.0.1",0,0,19),("127.0.0.1",0,0,901),
                 ("127.0.0.1",0,0,20.0)]
        for args in cases:
            with self.subTest(args=args), self.assertRaises(ValueError):
                receiver.validate(*args)

    def test_existing_log_is_preserved(self):
        log=self.root/"existing.jsonl"
        log.write_bytes(b"original\n")
        with mock.patch.object(receiver.socket,"socket") as socket_call:
            rc=receiver.main(["--serve","--bind","192.0.2.10","--log",str(log)])
            self.assertEqual(rc,2)
            socket_call.assert_not_called()
        self.assertEqual(log.read_bytes(),b"original\n")

    def test_existing_summary_is_preserved_before_listening(self):
        log=self.root/"collision.jsonl"
        summary=log.with_suffix(log.suffix+".summary.json")
        summary.write_bytes(b"original summary")
        with mock.patch.object(receiver.socket,"socket") as socket_call:
            with self.assertRaises(FileExistsError):
                receiver.run("127.0.0.1",0,0,20,log)
            socket_call.assert_not_called()
        self.assertEqual(summary.read_bytes(),b"original summary")

    def test_udp_bind_failure_is_not_success(self):
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as occupied:
            occupied.bind(("127.0.0.1",0))
            log=self.root/"udp-bind.jsonl"
            self.assertEqual(receiver.run("127.0.0.1",occupied.getsockname()[1],0,20,log),2)
        result=self.summary(log)
        self.assertFalse(result["receiver_complete"])
        self.assertFalse(result["deadline_reached"])
        self.assertTrue(result["errors"])
        self.assertTrue(result["listeners_closed"])

    def test_tcp_bind_failure_closes_partial_udp_listener(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as occupied:
            occupied.bind(("127.0.0.1",0))
            occupied.listen()
            log=self.root/"tcp-bind.jsonl"
            self.assertEqual(receiver.run("127.0.0.1",0,occupied.getsockname()[1],20,log),2)
        result=self.summary(log)
        self.assertFalse(result["receiver_complete"])
        udp_endpoint=tuple(result["endpoints"]["udp"])
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as reused:
            reused.bind(udp_endpoint)
        events=[json.loads(row) for row in log.read_text("utf-8").splitlines()]
        self.assertNotIn("listening",[row["kind"] for row in events])

    def test_early_stop_cannot_claim_complete_observation(self):
        stop=threading.Event()
        stop.set()
        log=self.root/"early.jsonl"
        self.assertEqual(receiver.run("127.0.0.1",0,0,20,log,stop=stop),2)
        result=self.summary(log)
        self.assertFalse(result["receiver_complete"])
        self.assertIn("early_stop",[e["error_kind"] for e in result["errors"]])

    def test_implementation_mutation_is_reported(self):
        owned_source=self.root/"owned-source.py"
        owned_source.write_bytes(b"original")
        identity={"kind":"python_source","path":str(owned_source),"sha256":receiver.digest(owned_source)}
        stop=threading.Event()
        def ready(_):
            owned_source.write_bytes(b"changed")
            stop.set()
        log=self.root/"changed.jsonl"
        with mock.patch.object(receiver,"implementation_identity",return_value=identity):
            self.assertEqual(receiver.run("127.0.0.1",0,0,20,log,ready=ready,stop=stop),2)
        result=self.summary(log)
        self.assertFalse(result["implementation_unchanged"])
        self.assertIn("implementation_changed",[e["error_kind"] for e in result["errors"]])

    def test_interrupt_is_not_success(self):
        selector=receiver.selectors.DefaultSelector()
        log=self.root/"interrupt.jsonl"
        with mock.patch.object(receiver.selectors,"DefaultSelector",return_value=selector):
            with mock.patch.object(selector,"select",side_effect=KeyboardInterrupt):
                self.assertEqual(receiver.run("127.0.0.1",0,0,20,log),2)
        result=self.summary(log)
        self.assertTrue(result["interrupted"])
        self.assertFalse(result["receiver_complete"])

    def test_native_v4_v6_fragmented_tcp_full_udp_and_timeout(self):
        # Three independent host-only collectors run concurrently, each 20 seconds.
        def start(bind,name,pool):
            ready=queue.Queue()
            log=self.root/(name+".jsonl")
            future=pool.submit(receiver.run,bind,0,0,20,log,ready=ready.put)
            endpoints=ready.get(timeout=5)
            return log,future,endpoints
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            runs=[]
            for bind in ("127.0.0.1","::1"):
                log,future,endpoints=start(bind,"healthy-v"+("6" if ":" in bind else "4"),pool)
                family=socket.AF_INET6 if ":" in bind else socket.AF_INET
                nonce=b"0123456789abcdef0123456789abcdef"
                with socket.socket(family,socket.SOCK_DGRAM) as sender:
                    sender.sendto(nonce,tuple(endpoints["udp"]))
                    sender.sendto(b"\xff"*5000,tuple(endpoints["udp"]))
                with socket.socket(family,socket.SOCK_STREAM) as sender:
                    sender.settimeout(3)
                    sender.connect(tuple(endpoints["tcp"]))
                    sender.sendall(nonce[:7])
                    time.sleep(1/20)
                    sender.sendall(nonce[7:])
                    sender.shutdown(socket.SHUT_WR)
                with socket.socket(family,socket.SOCK_STREAM) as sender:
                    sender.settimeout(3)
                    sender.connect(tuple(endpoints["tcp"]))
                    sender.sendall(nonce+b"extra")
                    sender.shutdown(socket.SHUT_WR)
                runs.append((log,future))
            log,timeout_future,endpoints=start("127.0.0.1","timeout",pool)
            with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as held:
                held.settimeout(3)
                held.connect(tuple(endpoints["tcp"]))
                held.sendall(b"partial")
                self.assertEqual(timeout_future.result(timeout=30),2)
            timeout_result=self.summary(log)
            self.assertIn("tcp_read_timeout",[e["error_kind"] for e in timeout_result["errors"]])
            self.assertFalse(timeout_result["receiver_complete"])
            for log,future in runs:
                self.assertEqual(future.result(timeout=30),0)
                result=self.summary(log)
                self.assertTrue(result["receiver_complete"])
                self.assertEqual(receiver.digest(log),result["log_sha256"])
                payloads=[json.loads(row) for row in log.read_text("utf-8").splitlines() if json.loads(row)["kind"]=="payload"]
                self.assertEqual(len(payloads),4)
                self.assertEqual(sum(p["exact_nonce"] for p in payloads),2)
                tcp=[p for p in payloads if p["protocol"]=="tcp"]
                self.assertIn((nonce+b"extra").hex(),[p["payload_hex"] for p in tcp])
                binary=[p for p in payloads if p["bytes"]==5000]
                self.assertEqual(binary[0]["payload_hex"],(b"\xff"*5000).hex())
                self.assertIsNone(binary[0]["nonce"])


if __name__ == "__main__":
    unittest.main()
