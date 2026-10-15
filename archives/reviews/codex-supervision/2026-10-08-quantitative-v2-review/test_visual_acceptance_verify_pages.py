"""Adversarial evidence-contract tests: no image/glyph acceptance is simulated."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from fractions import Fraction
from unittest import mock
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"tools"))
import visual_acceptance_verify_pages as v

class EvidenceContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.image = self.root/"page.png"
        self.geometry = self.root/"geometry.json"
        self.index = self.root/"index.jsonl"
        self.output = self.root/"reviews/codex-supervision/new/evidence.json"
        self.make_image()
        self.pages = [{"page": 1, "frame": "page.png", "kind": "FULL_FORMULAS", "items": [{"formula_index": 1}]}]
        self.row = {"id": "fixture", "source_sha256": "a"*64, "record_sha256": "b"*64,
                    "math_sha256": "c"*64, "geometry_path": "geometry.json", "page_count": 1,
                    "canonical_frames": [{"path": "page.png", "sha256": v.sha256(self.image)}]}
        self.bind()

    def make_image(self, formula=True, edge=False):
        im = Image.new("RGB", v.HD_SIZE, "black")
        draw = ImageDraw.Draw(im)
        draw.rectangle((200,100,700,130), fill="white")  # header outside formula region
        if formula:
            draw.rectangle((600,600,800,720), fill="white")
        if edge:
            draw.rectangle((0,500,1,600), fill="white")
        im.save(self.image)

    def bind(self, rows=None):
        self.geometry.write_text(json.dumps({"id": "fixture", "pages": self.pages}), encoding="utf-8")
        self.row["geometry_sha256"] = v.sha256(self.geometry)
        self.row["canonical_frames"][0]["sha256"] = v.sha256(self.image)
        self.index.write_text("".join(json.dumps(r)+"\n" for r in (rows or [self.row])), encoding="utf-8")
        self.pin = v.sha256(self.index)

    def verify(self, records=1, pages=1):
        return v.verify(self.root, self.index, self.pin, records, pages)

    def cli(self):
        with mock.patch.object(v, "ROOT", self.root), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return v.main(["--index", str(self.index), "--expected-index-sha256", self.pin,
                           "--expected-records", "1", "--expected-pages", "1", "--output", str(self.output)])

    def test_exact_statistics_even_median_and_nearest_rank(self):
        self.assertEqual(v.exact_stats([Fraction(1,3), Fraction(2,3)]), {"min":"1/3", "p10_nearest_rank":"1/3", "median":"1/2"})

    def test_header_cannot_make_blank_formula_pass(self):
        self.make_image(formula=False); self.bind()
        result = self.verify()
        self.assertEqual(result["summary"]["status"], "FAIL_STRUCTURAL_CHECKS")
        self.assertEqual(result["records"][0]["page_rows"][0]["formula_ink"], 0)
        self.assertEqual(self.cli(), 1)

    def test_native_inclusive_formula_bbox_excludes_header(self):
        m = v.metrics(self.image)
        self.assertEqual(m["bbox_height"], 121)
        self.assertEqual(m["bbox_width"], 201)
        self.assertEqual(m["formula_ink"], 121*201)

    def test_source_sha_mismatch_fails_closed(self):
        self.index.write_text(self.index.read_text("utf-8")+" ", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Index SHA"): self.verify()

    def test_geometry_sha_mismatch_fails_closed(self):
        self.geometry.write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Geometry SHA"): self.verify()

    def test_frame_sha_mismatch_fails_closed(self):
        self.make_image(edge=True)
        with self.assertRaisesRegex(ValueError, "Frame SHA"): self.verify()

    def test_partial_population_not_success(self):
        with self.assertRaisesRegex(ValueError, "total page"): self.verify(pages=2)

    def test_duplicate_record_identity_rejected(self):
        self.bind(rows=[self.row,self.row])
        with self.assertRaisesRegex(ValueError, "duplicate record"): self.verify(records=2,pages=2)

    def test_unknown_page_kind_rejected(self):
        self.pages[0]["kind"]="UNRECOGNIZED"; self.bind()
        with self.assertRaisesRegex(ValueError, "Unknown page"): self.verify()

    def test_empty_item_list_not_pass(self):
        self.pages[0]["items"]=[]; self.bind()
        with self.assertRaisesRegex(ValueError, "formula items"): self.verify()

    def test_segment_excluded_from_slot_population(self):
        self.pages[0]["kind"]="FORMULA_SEGMENT"; self.bind()
        result=self.verify()
        self.assertEqual(result["summary"]["full_pages"],0)
        self.assertEqual(result["summary"]["segment_pages"],1)
        self.assertIsNone(result["records"][0]["page_rows"][0]["slot_px_proxy_exact"])
        self.assertEqual(result["summary"]["full_glyph_visual_acceptance"],"NOT_ESTABLISHED")

    def test_canvas_edge_issue_nonzero_exit(self):
        self.make_image(edge=True);self.bind()
        self.assertEqual(self.cli(),1)
        self.assertEqual(json.loads(self.output.read_text("utf-8"))["summary"]["issue_count"],1)

    def test_existing_evidence_never_overwritten(self):
        self.output.parent.mkdir(parents=True)
        self.output.write_bytes(b"ORIGINAL")
        self.assertEqual(self.cli(),1)
        self.assertEqual(self.output.read_bytes(),b"ORIGINAL")

    def test_frozen_archive_never_appended(self):
        self.output.parent.mkdir(parents=True)
        (self.output.parent/"delivery-manifest.json").write_text("{}",encoding="utf-8")
        self.assertEqual(self.cli(),1)
        self.assertFalse(self.output.exists())

    def test_out_of_root_input_rejected(self):
        with self.assertRaises(ValueError):v.input_path(self.root,"../escape.png")

    def test_actual_resolution_failure_is_nonzero(self):
        Image.new("RGB",(100,100),"white").save(self.image);self.bind()
        self.assertEqual(self.cli(),1)
        self.assertFalse(self.output.exists())

    def test_cli_success_contains_exact_pin_and_algorithm(self):
        self.assertEqual(self.cli(),0)
        d=json.loads(self.output.read_text("utf-8"))
        self.assertEqual(d["index_sha256"],self.pin)
        self.assertEqual(d["records"][0]["page_rows"][0]["slot_px_proxy_exact"],"121")
        self.assertEqual(d["summary"]["minimum_glyph_size"],"NOT_CERTIFIED_BY_SLOT_PROXY")
        self.assertIn("formula_region_zero_based_half_open",d["algorithm"])

if __name__=="__main__":unittest.main()
