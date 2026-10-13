"""Mocked diagnostics regression tests. No external sockets or native acceptance."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("host_pretest", ROOT / "tools/host_pretest_witness.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


class HostPretestTests(unittest.TestCase):
    def socket_case(self, code=0, error=None):
        sock = mock.MagicMock()
        sock.__enter__.return_value = sock
        sock.connect_ex.return_value = code
        sock.connect_ex.side_effect = error
        sock.sendto.return_value = 7
        return sock

    def tcp(self, sock, ticks=(100, 22_497_600)):
        with mock.patch.object(p.socket, "socket", return_value=sock), mock.patch.object(
                p.time, "monotonic_ns", side_effect=ticks):
            result = p.tcp_probe()
        sock.__exit__.assert_called_once()
        return result

    def test_timeout_code_never_claims_live_path(self):
        r = self.tcp(self.socket_case(10060))
        self.assertEqual(r["outcome"], "TIMEOUT_UNCONFIRMED")
        self.assertFalse(r["receiver_delivery_verified"])

    def test_refusal_does_not_authenticate_witness(self):
        r = self.tcp(self.socket_case(10061))
        self.assertEqual(r["outcome"], "CONNECTION_REFUSED")
        self.assertFalse(r["receiver_delivery_verified"])

    def test_success_is_local_completion_without_delivery_claim(self):
        r = self.tcp(self.socket_case())
        self.assertEqual(r["outcome"], "LOCAL_CONNECT_COMPLETED")
        self.assertFalse(r["receiver_delivery_verified"])

    def test_elapsed_nanoseconds_and_fraction_keep_all_precision(self):
        r = self.tcp(self.socket_case())
        self.assertEqual(r["elapsed_ns"], 22_497_500)
        self.assertEqual(r["elapsed_ms_exact"], "8999/400")
        self.assertNotIn("elapsed_ms", r)

    def test_typed_timeout_closes_socket(self):
        r = self.tcp(self.socket_case(error=TimeoutError("timeout")))
        self.assertEqual(r["outcome"], "TIMEOUT_UNCONFIRMED")
        self.assertIsNone(r["errno"])

    def test_unknown_socket_error_does_not_become_timeout_or_live_path(self):
        r = self.tcp(self.socket_case(error=OSError(10013, "denied")))
        self.assertEqual(r["outcome"], "SOCKET_ERROR")
        self.assertEqual(r["error"]["errno"], 10013)

    def test_socket_setup_error_still_closes_socket(self):
        s = self.socket_case()
        s.settimeout.side_effect = OSError("setup")
        r = self.tcp(s)
        self.assertEqual(r["outcome"], "SOCKET_ERROR")
        s.connect_ex.assert_not_called()

    def test_udp_short_send_is_not_sent(self):
        s = self.socket_case()
        s.sendto.return_value = 3
        with mock.patch.object(p.socket, "socket", return_value=s), mock.patch.object(
                p.time, "monotonic_ns", side_effect=(0, 15)):
            r = p.udp_probe()
        self.assertFalse(r["sent"])
        self.assertEqual(r["outcome"], "SHORT_SEND")
        s.__exit__.assert_called_once()

    def test_udp_os_error_preserved_and_socket_closed(self):
        s = self.socket_case()
        s.sendto.side_effect = OSError(10013, "denied")
        with mock.patch.object(p.socket, "socket", return_value=s), mock.patch.object(
                p.time, "monotonic_ns", side_effect=(0, 15)):
            r = p.udp_probe()
        self.assertFalse(r["sent"])
        self.assertEqual(r["error"]["errno"], 10013)
        s.__exit__.assert_called_once()

    def test_main_emits_parseable_json_without_timeout_qualification(self):
        s = self.socket_case(10060)
        out = io.StringIO()
        with mock.patch.object(p.socket, "socket", return_value=s), mock.patch.object(
                p.time, "monotonic_ns", side_effect=(0, 1, 2, 3)), contextlib.redirect_stdout(out):
            self.assertEqual(p.main(), 0)
        r = json.loads(out.getvalue())
        self.assertEqual(r["verdict"], "TIMEOUT_UNCONFIRMED")
        self.assertEqual(r["qualification"], "NOT_ESTABLISHED")
        self.assertFalse(r["full_surface_accepted"])
        self.assertEqual(r["production_gate"], "CLOSED")

    def test_socket_creation_failure_is_a_diagnostic_error(self):
        with mock.patch.object(p.socket, "socket", side_effect=OSError("create")), mock.patch.object(
                p.time, "monotonic_ns", side_effect=(0, 2)):
            r = p.tcp_probe()
        self.assertEqual(r["outcome"], "SOCKET_ERROR")


if __name__ == "__main__":
    unittest.main()
