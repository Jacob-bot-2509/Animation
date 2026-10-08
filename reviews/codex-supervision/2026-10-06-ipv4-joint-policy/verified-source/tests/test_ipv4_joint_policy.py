"""Policy unit fixtures are simulated; these tests are not network acceptance."""
import copy,json,sys,tempfile,unittest,uuid
from pathlib import Path
from unittest import mock
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"src"))
from animtrain import full_surface_evidence as fe,isolation_evidence as ie,sandbox_execution as se

class IPv4JointPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="joint-policy-test-",dir=fe.REVIEW_ROOT)
        self.directory=Path(self.temp.name).resolve()
        self.assertTrue(self.directory.is_relative_to(fe.REVIEW_ROOT.resolve()))
        self.capture=self.directory/"interfaces.json"
        self.capture.write_text(json.dumps([{"IPAddress":"2001:4860:1000::1","PrefixLength":64}]),encoding="utf-8")
        self.topology=self.directory/"topology.json"
        self.topology_data={"schema":"ipv4-joint-topology-v1","sender_host_id":"sender-test",
            "receiver_host_id":"controlled-external-test","controlled_receiver":True,
            "sender_ipv6":"2001:4860:1000::1","receiver_ipv6":"2606:4700:2000::2",
            "sender_interfaces":{"path":str(self.capture),"sha256":fe.digest(self.capture),"rc":0,"stderr":"",
                "command":"Get-NetIPAddress -AddressFamily IPv6 | Select-Object IPAddress,PrefixLength | ConvertTo-Json -Compress"}}
        self.write_topology()
    def tearDown(self):
        self.assertTrue(self.directory.is_relative_to(fe.REVIEW_ROOT.resolve()))
        self.temp.cleanup()
    def write_topology(self):
        self.topology.write_text(json.dumps(self.topology_data),encoding="utf-8")
    def case(self,point="D1"):
        tcp=point=="D1"
        def leg(operation,endpoint):
            nonces={p:uuid.uuid4().hex for p in ("before","sandbox","after")}
            return {"operation":operation,"endpoint":endpoint,"nonces":nonces,
                "packets":[nonces["before"],nonces["after"]],"receiver_complete":True,
                "receiver_errors":[],"post_attempt_observation_ns":20_000_000_000,
                "observation_key":"attempt","state":{"outcome":"os_denied","winerror":10013},
                "transport":{"rc":0}}
        lan=leg("lan_peer",["172.30.192.202",49002 if tcp else 49001])
        lan.update(wire_protocol="tcp" if tcp else "udp",independent_lan_peer=True)
        external=leg("external_tcp_v6" if tcp else "external_udp_v6",["2606:4700:2000::2",49002 if tcp else 49001])
        external["controlled_remote_peer"]=True
        local=leg("loopback_tcp_v4" if tcp else "loopback_udp_v4",["127.0.0.1",49101])
        return {"operation":fe.NETWORKS[point],"acceptance_basis":fe.IPV4_JOINT_POLICY,
            "components":{"lan_ipv4":lan,"external_ipv6":external,"local_ipv4":local},
            "topology_evidence":{"path":str(self.topology),"sha256":fe.digest(self.topology)}}
    def verify(self,case,point="D1"):
        with mock.patch.object(fe,"transport",side_effect=lambda row:(row["transport"],{"attempt":row["state"]})):
            fe.network(point,case)
    def external(self,include_v4=False,outcome="error"):
        names=["tcp_external_v6"]
        if include_v4:names.insert(0,"tcp_external_v4")
        return {"external_network":{"transport":{"rc":0,"stdout":json.dumps({n:{"outcome":outcome,"winerror":10013} for n in names})},
            "before":{n:"connected" for n in names},"after":{n:"connected" for n in names},
            "endpoints":[[n,0,[]] for n in names]}}
    def legacy(self,records,case=None):
        with mock.patch.object(ie,"_transport"),mock.patch.object(fe,"transport",side_effect=lambda row:(row["transport"],{"attempt":row["state"]})):
            return ie._external_network(records,se.digest,case)
    def test_tcp_and_udp_each_require_their_own_three_legs(self):
        for point in ("D1","D7"):
            with self.subTest(point=point):self.verify(self.case(point),point)
    def test_missing_each_component_is_rejected(self):
        for leg in ("lan_ipv4","external_ipv6","local_ipv4"):
            case=self.case();del case["components"][leg]
            with self.subTest(leg=leg),self.assertRaises(ValueError):self.verify(case)
    def test_tcp_cannot_borrow_udp_lan(self):
        case=self.case();case["components"]["lan_ipv4"]["wire_protocol"]="udp"
        with self.assertRaises(ValueError):self.verify(case)
    def test_udp_cannot_borrow_tcp_external(self):
        case=self.case("D7");case["components"]["external_ipv6"]["operation"]="external_tcp_v6"
        with self.assertRaises(ValueError):self.verify(case,"D7")
    def test_lan_must_be_ipv4_on_a_distinct_host(self):
        for addr,independent in (("::1",True),("127.0.0.1",True),("172.30.192.202",False)):
            case=self.case();case["components"]["lan_ipv4"].update(endpoint=[addr,49002],independent_lan_peer=independent)
            with self.subTest(addr=addr),self.assertRaises(ValueError):self.verify(case)
    def test_local_component_must_be_ipv4_loopback(self):
        case=self.case();case["components"]["local_ipv4"]["endpoint"][0]="172.30.192.202"
        with self.assertRaises(ValueError):self.verify(case)
    def test_external_ipv6_cannot_be_the_campus_same_64(self):
        case=self.case();case["components"]["external_ipv6"]["endpoint"][0]="2001:4860:1000::abcd"
        self.topology_data["receiver_ipv6"]="2001:4860:1000::abcd"
        self.write_topology();case["topology_evidence"]["sha256"]=fe.digest(self.topology)
        with self.assertRaisesRegex(ValueError,"inside the sender LAN"):self.verify(case)
    def test_larger_registered_lan_prefix_also_rejected(self):
        self.capture.write_text(json.dumps([{"IPAddress":"2001:4860:1000::1","PrefixLength":32}]),encoding="utf-8")
        self.topology_data["sender_interfaces"]["sha256"]=fe.digest(self.capture)
        self.topology_data["receiver_ipv6"]="2001:4860:2000::2";self.write_topology()
        case=self.case();case["components"]["external_ipv6"]["endpoint"][0]="2001:4860:2000::2"
        with self.assertRaisesRegex(ValueError,"inside the sender LAN"):self.verify(case)
    def test_interfaces_and_topology_hashes_are_bound(self):
        case=self.case();self.capture.write_text("[]",encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"capture missing/changed"):self.verify(case)
        self.write_topology();case=self.case();self.topology.write_text("{}",encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"Topology evidence changed"):self.verify(case)
    def test_topology_cannot_escape_registered_evidence_root(self):
        case=self.case();case["topology_evidence"]["path"]=str(ROOT/"AGENTS.md")
        with self.assertRaisesRegex(ValueError,"outside registered"):self.verify(case)
    def test_external_receiver_must_be_controlled(self):
        case=self.case();case["components"]["external_ipv6"]["controlled_remote_peer"]=False
        with self.assertRaises(ValueError):self.verify(case)
    def test_phase_nonces_cannot_be_reused_across_legs(self):
        case=self.case();a=case["components"]["lan_ipv4"];b=case["components"]["local_ipv4"]
        b["nonces"]=copy.deepcopy(a["nonces"]);b["packets"]=list(a["packets"])
        with self.assertRaisesRegex(ValueError,"reuses phase nonces"):self.verify(case)
    def test_every_component_requires_full_twenty_second_window(self):
        for leg in ("lan_ipv4","external_ipv6","local_ipv4"):
            case=self.case();case["components"][leg]["post_attempt_observation_ns"]=19_999_999_999
            with self.subTest(leg=leg),self.assertRaises(ValueError):self.verify(case)
    def test_any_actual_sandbox_delivery_is_failure(self):
        for leg in ("lan_ipv4","external_ipv6","local_ipv4"):
            case=self.case();row=case["components"][leg];row["packets"].append(row["nonces"]["sandbox"])
            with self.subTest(leg=leg),self.assertRaises(fe.BoundaryFailure):self.verify(case)
    def test_incomplete_other_leg_does_not_mask_actual_delivery(self):
        case=self.case();case["components"]["lan_ipv4"]["receiver_complete"]=False
        row=case["components"]["local_ipv4"];row["packets"].append(row["nonces"]["sandbox"])
        with self.assertRaises(fe.BoundaryFailure):self.verify(case)
    def test_labels_alone_still_cannot_be_green(self):
        raw={"schema":"sandbox-surface-native-v1","initial_bindings":{n:se.digest(ROOT/n) for n in se.BOUND_FILES},
             "cases":{"D1":{"operation":fe.NETWORKS["D1"],"acceptance_basis":fe.IPV4_JOINT_POLICY,"status":"GREEN"}}}
        self.assertEqual(fe.recompute(raw)["D1"]["status"],"PARTIAL")
    def test_joint_result_is_explicitly_inference(self):
        case=self.case();raw={"schema":"sandbox-surface-native-v1","initial_bindings":{n:se.digest(ROOT/n) for n in se.BOUND_FILES},"cases":{"D1":case}}
        with mock.patch.object(fe,"transport",side_effect=lambda row:(row["transport"],{"attempt":row["state"]})):
            result=fe.recompute(raw)["D1"]
        self.assertEqual(result["status"],"GREEN")
        self.assertEqual(result["acceptance_basis"],fe.IPV4_JOINT_POLICY)
        self.assertIn("no direct public IPv4 measurement",result["scope"])
    def test_direct_public_ipv4_route_remains_available(self):
        case=self.case()["components"]["external_ipv6"]
        case.update(operation="external_tcp_v4",endpoint=["8.8.8.8",49002])
        self.verify(case)
    def test_unknown_policy_id_is_rejected(self):
        case=self.case();case["acceptance_basis"]="just-trust-me"
        with self.assertRaises(ValueError):self.verify(case)
    def test_legacy_tcp_accepts_joint_without_public_ipv4_endpoint(self):
        self.assertEqual(self.legacy(self.external(),self.case()),{"tcp_external_v4":"PASS","tcp_external_v6":"PASS"})
    def test_legacy_default_still_requires_direct_ipv4(self):
        with self.assertRaisesRegex(ValueError,"incomplete"):self.legacy(self.external())
        self.assertEqual(len(self.legacy(self.external(True))),2)
    def test_legacy_joint_is_independently_checked(self):
        case=self.case();del case["components"]["external_ipv6"]
        with self.assertRaises(ValueError):self.legacy(self.external(),case)
    def test_legacy_joint_cannot_hide_ipv4_delivery_even_if_endpoint_omitted(self):
        for include in (True,False):
            records=self.external(include)
            observed=json.loads(records["external_network"]["transport"]["stdout"])
            observed["tcp_external_v4"]={"outcome":"connected"}
            records["external_network"]["transport"]["stdout"]=json.dumps(observed)
            with self.subTest(include=include),self.assertRaisesRegex(ValueError,"cannot be masked"):
                self.legacy(records,self.case())
    def test_joint_cannot_waive_legacy_ipv6_controls(self):
        records=self.external();records["external_network"]["before"]["tcp_external_v6"]="failed"
        with self.assertRaises(ValueError):self.legacy(records,self.case())
    def test_joint_boolean_is_not_accepted(self):
        with self.assertRaises((ValueError,AttributeError)):self.legacy(self.external(),True)
    def test_duplicate_legacy_endpoint_is_rejected(self):
        records=self.external();records["external_network"]["endpoints"]*=2
        with self.assertRaises(ValueError):self.legacy(records,self.case())

if __name__=="__main__":unittest.main()
