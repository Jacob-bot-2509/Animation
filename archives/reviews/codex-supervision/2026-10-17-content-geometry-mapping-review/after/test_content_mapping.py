"""Independent safety and content-binding regression tests; no generated scene execution."""
import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).absolute().parent
ROOT = HERE.parents[4]
spec = importlib.util.spec_from_file_location("reviewed_content_mapping", HERE/"build_content_mapping.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
SCRATCH = ROOT / "reviews/codex-supervision/2026-10-17-content-geometry-tests"
SCRATCH.mkdir(exist_ok=True)

class MappingTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="case-", dir=SCRATCH))
        self.base = self.root / HERE.relative_to(ROOT)
        self.base.mkdir(parents=True)
        self.batch = json.loads((HERE.parent/"first-batch-10.v2.json").read_bytes())
        self.ev = json.loads((ROOT/"data/asset_evidence.json").read_bytes())
        for rel in {x["source"]["path"] for x in self.batch["records"]} | {"tools/render_templates.py"}:
            p = self.root/rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((ROOT/rel).read_bytes())
        for rec in self.batch["records"]:
            self.ev["records"][rec["sample_id"]]["source"]["path"] = str(self.root / rec["source"]["path"])
        self.write()

    def tearDown(self):
        resolved = self.root.resolve()
        assert resolved.is_relative_to(SCRATCH.resolve()) and resolved != SCRATCH.resolve()
        shutil.rmtree(resolved)

    def write(self):
        ep = self.root/"data/asset_evidence.json"
        ep.write_bytes(m.encoded(self.ev))
        self.batch["evidence_sha256"] = m.sha(ep.read_bytes())
        (self.base.parent/"first-batch-10.v2.json").write_bytes(m.encoded(self.batch))

    def build(self):
        return m.build(root=self.root)

    def test_all_ten_full_content_and_original_unchanged(self):
        r = self.build()
        self.assertEqual(len(r["records"]), 10)
        for out, rec in zip(r["records"], self.batch["records"]):
            raw = (self.root/rec["source"]["path"]).read_bytes().splitlines(keepends=True)[rec["source"]["line"]-1]
            obj = json.loads(raw)
            texts = [obj["problem"], *obj["scene_spec"]["steps"], obj["answer"]]
            self.assertEqual(out["full_content_plan"]["sources"], texts)
            self.assertTrue(m.candidate.coverage_ok(texts, out["full_content_plan"]))
            self.assertEqual(out["source"]["raw_line_sha256"], m.sha(raw))
            self.assertEqual(out["math_verdict"], "PENDING_REVIEW")
            self.assertIsNone(out["user_review"])
        self.assertEqual(r["records"][0]["provisional_step_rows"], 12)
        self.assertEqual(r["records"][0]["provisional_step_pages"], 3)
        self.assertTrue(r["records"][1]["legacy_geometry_checklist"])

    def test_empty_batch_rejected(self):
        self.batch["records"] = []
        self.write()
        with self.assertRaises(ValueError): self.build()

    def test_duplicate_id_rejected(self):
        self.batch["records"][1] = copy.deepcopy(self.batch["records"][0])
        self.write()
        with self.assertRaises(ValueError): self.build()

    def test_nested_source_hash_rejected(self):
        self.batch["records"][0]["source"]["raw_line_sha256"] = "0"*64
        self.write()
        with self.assertRaises(ValueError): self.build()

    def test_nested_source_line_rejected(self):
        self.batch["records"][0]["source"]["line"] = 1
        self.write()
        with self.assertRaises(ValueError): self.build()

    def test_changed_dataset_rejected(self):
        p = self.root/self.batch["records"][0]["source"]["path"]
        p.write_bytes(p.read_bytes()+b"\n")
        with self.assertRaises(ValueError): self.build()

    def test_source_id_mismatch_rejected(self):
        sid = self.batch["records"][0]["sample_id"]
        self.ev["records"][sid]["source"]["line"] = 1
        self.write()
        with self.assertRaises(ValueError): self.build()

    def test_bool_line_rejected(self):
        sid = self.batch["records"][0]["sample_id"]
        self.ev["records"][sid]["source"]["line"] = True
        self.write()
        with self.assertRaises(ValueError): self.build()

    def test_outside_source_rejected(self):
        sid = self.batch["records"][0]["sample_id"]
        self.ev["records"][sid]["source"]["path"] = str(self.root.parent/"outside.jsonl")
        self.write()
        with self.assertRaises(ValueError): self.build()

    def test_stale_evidence_rejected(self):
        self.ev["extra"] = True
        (self.root/"data/asset_evidence.json").write_bytes(m.encoded(self.ev))
        with self.assertRaises(ValueError): self.build()

    def test_stale_legacy_template_rejected(self):
        (self.root/"tools/render_templates.py").write_bytes(b"changed")
        with self.assertRaises(ValueError): self.build()

    def test_stale_selector_pin_rejected(self):
        self.batch["selector_sha256"] = "0"*64
        self.write()
        with self.assertRaises(ValueError): self.build()

    def test_unknown_template_rejected(self):
        sid = self.batch["records"][0]["sample_id"]
        self.ev["records"][sid]["scene_source"]["template"] = "invented"
        self.write()
        with self.assertRaises(ValueError): self.build()

    def test_false_coverage_rejected(self):
        with mock.patch.object(m.candidate, "coverage_ok", return_value=False):
            with self.assertRaises(ValueError): self.build()

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(ValueError): m.strict_json(b'{"x":1,"x":2}')
        with self.assertRaises(ValueError): m.strict_json(b'{"x":NaN}')

    def test_generation_new_only_and_completion_hashes(self):
        r = self.build()
        historical = self.base/"content-geometry-mapping.jsonl"
        historical.write_bytes(b"KEEP")
        out = m.publish(r, base=self.base, root=self.root)
        c = json.loads((out/"COMPLETE.json").read_bytes())
        for name, pin in c["files"].items():
            raw = (out/name).read_bytes()
            self.assertEqual(pin, {"sha256":m.sha(raw),"bytes":len(raw)})
        self.assertEqual(historical.read_bytes(),b"KEEP")
        again = m.publish(r, base=self.base, root=self.root)
        self.assertNotEqual(out, again)

    def test_frozen_ancestor_rejected(self):
        (self.root/"delivery-manifest.json").write_bytes(b"{}")
        with self.assertRaises(ValueError): m.publish({},base=self.base,root=self.root)

    def test_outside_output_rejected(self):
        with self.assertRaises(ValueError): m.publish({},base=self.root.parent,root=self.root)

    def test_collision_preserves_existing(self):
        out = self.base/("generation-"+"a"*32)
        out.mkdir()
        (out/"KEEP").write_bytes(b"KEEP")
        with mock.patch.object(m.uuid,"uuid4",return_value=type("U",(),{"hex":"a"*32})()):
            with self.assertRaises(FileExistsError): m.publish(self.build(),base=self.base,root=self.root)
        self.assertEqual((out/"KEEP").read_bytes(),b"KEEP")


    def test_batch_bool_line_rejected(self):
        self.batch["records"][0]["source"]["line"] = True
        self.write()
        with self.assertRaisesRegex(ValueError, "batch_source_shape"): self.build()

    def test_mutation_during_plan_rejected(self):
        original = m.candidate.make_plan
        p = self.root/"tools/render_templates.py"
        called = False
        def mutate(*args, **kwargs):
            nonlocal called
            if not called:
                p.write_bytes(p.read_bytes()+b"\n")
                called = True
            return original(*args, **kwargs)
        with mock.patch.object(m.candidate,"make_plan",side_effect=mutate):
            with self.assertRaisesRegex(ValueError,"input_changed"): self.build()

    def test_self_consistent_but_unreviewed_legacy_rejected(self):
        p = self.root/"tools/render_templates.py"
        p.write_bytes(p.read_bytes()+b"\n")
        new_sha = m.sha(p.read_bytes())
        self.batch["template_sha256"] = new_sha
        self.ev["template_sha256"] = new_sha
        self.write()
        with self.assertRaisesRegex(ValueError,"unreviewed_legacy_geometry_inventory"): self.build()

    def test_all_legacy_template_kinds_have_inventory(self):
        self.assertEqual(set(m.INVENTORY),{"unit_circle","graph_limit","sequence","matrix","derivative","geometry","statistics","fallback"})

if __name__ == "__main__":
    unittest.main(verbosity=2)
