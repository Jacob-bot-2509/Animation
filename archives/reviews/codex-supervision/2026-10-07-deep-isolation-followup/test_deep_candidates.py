"""Adversarial exact-score, binding, coverage and decision regression checks."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

fixtures = load("signature_fixture_for_deep", ROOT / "tests/test_core_signatures.py")
deep = load("deep_candidate_tested", ROOT / "tools/deep_isolation_candidates.py")
dispose = load("deep_disposer_tested", ROOT / "tools/deep_candidates_dispositions.py")

class DeepCandidateTests(unittest.TestCase):
    def setUp(self):
        self.f = fixtures.CoreSignaturesTests()
        self.f.setUp()
        self.m = fixtures.m
        self.patchers = [mock.patch.object(deep, "core", self.m), mock.patch.object(dispose, "core", self.m), mock.patch.object(dispose, "deep", deep)]
        for p in self.patchers:
            p.start()
        for source in self.f.sources:
            path = self.f.root / source["path"]
            rows = self.m.read_rows(path.read_bytes())
            for r in rows:
                r["category"] = "family-" + source["group"]
                r["sub_category"] = "actual"
                if r["id"] in ("train-0", "eval-0"):
                    r["category"] = "collision"
            raw = b"".join(self.m.encoded(r).replace(b"\n", b"") + b"\n" for r in rows)
            path.write_bytes(raw)
            source["sha256"], source["bytes"] = self.m.digest(raw), len(raw)
            by_id = {r["id"]: r for r in rows}
            for ref in self.f.refs:
                if ref["path"] == source["path"]:
                    ref["source_sha256"] = source["sha256"]
                    ref["record_sha256"] = self.m.dense(by_id[ref["id"]])
        self.f.seal()
        self.sigs = [self.f.signature(b["id"]) for b in self.f.refs]
        by_id = {s["id"]: s for s in self.sigs}
        by_id["eval-0"]["goal"] = by_id["train-0"]["goal"]
        by_id["train-0"]["decisive_steps"] = ["a", "b"]
        by_id["eval-0"]["decisive_steps"] = ["a", "c"]
        self.input = self.f.input("complete", self.sigs)

    def tearDown(self):
        for p in reversed(self.patchers):
            p.stop()
        self.f.tearDown()

    def candidate(self):
        out = self.f.sigdir / "candidates"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(deep.generate(self.input, out), 0)
        p = out / "deep-candidates.json"
        doc = self.m.read_json(p.read_bytes())
        self.assertEqual(doc["candidate_count"], 1)
        return p, doc

    def decisions(self, cand, doc, verdict="DIFFERENT_CORE"):
        c = doc["candidates"][0]
        row = {k: c[k] for k in ("train_id", "eval_id", "train_record_sha256", "eval_record_sha256")}
        row.update(verdict=verdict, pairwise_reason="A separately reviewed mathematical distinction")
        p = self.f.sigdir / "decisions.json"
        p.write_bytes(self.m.encoded({"candidate_sha256": self.m.digest(cand.read_bytes()), "rows": [row]}))
        return p

    def call_dispose(self, cand, decisions, expected=None):
        with contextlib.redirect_stdout(io.StringIO()):
            return dispose.disposed(cand, expected or self.m.digest(cand.read_bytes()), decisions, self.f.sigdir / "disposed")

    def test_exact_fraction_set_score(self):
        self.assertEqual(str(deep.jaccard(["a", "b", "a"], ["a", "c"])), "1/3")
        self.assertEqual(str(deep.jaccard([], [])), "1")

    def test_actual_complete_binding_and_exact_coverage(self):
        _, d = self.candidate()
        self.assertEqual(d["all_record_pairs"], 139950)
        self.assertEqual(d["family_pairs_total"], 1)
        self.assertEqual(d["outside_family_pairs_not_screened"], 139949)
        self.assertEqual(d["candidates"][0]["steps_jaccard"], "1/3")
        self.assertEqual(d["filter"]["steps_jaccard_minimum"], "1/4")
        self.assertEqual(d["semantic_isolation"], "NOT_ESTABLISHED")

    def test_nonhit_never_semantically_excluded(self):
        by_id = {s["id"]: s for s in self.sigs}
        by_id["eval-0"]["goal"] = "a different label"
        by_id["eval-0"]["decisive_steps"] = ["z"]
        path = self.f.input("nohits", self.sigs)
        with contextlib.redirect_stdout(io.StringIO()):
            deep.generate(path, self.f.sigdir / "nohits")
        d = self.m.read_json((self.f.sigdir / "nohits/deep-candidates.json").read_bytes())
        self.assertEqual(d["candidate_count"], 0)
        self.assertEqual(d["family_pairs_not_flagged"], 1)
        self.assertEqual(d["nonflagged_semantic_verdict"], "NOT_REVIEWED")
        self.assertFalse(d["PASS_CORE_SCOPE_issued"])

    def test_missing_signature_rejected(self):
        with self.assertRaises(ValueError):
            deep.population(self.f.input("missing", self.sigs[:-1]))

    def test_duplicate_signature_rejected(self):
        with self.assertRaises(ValueError):
            deep.population(self.f.input("duplicate", self.sigs + [self.sigs[0]]))

    def test_stale_signature_rejected(self):
        self.sigs[0]["record_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            deep.population(self.f.input("stale", self.sigs))

    def test_frozen_binding_tampering_rejected(self):
        (self.f.core / "record-bindings.jsonl").write_bytes(b"{}\n")
        with self.assertRaises(ValueError):
            deep.population(self.input)

    def test_actual_family_tampering_rejected(self):
        p = self.f.root / self.f.sources[-1]["path"]
        p.write_bytes(p.read_bytes().replace(b'"actual"', b'"forged"'))
        with self.assertRaises(ValueError):
            deep.population(self.input)

    def test_output_overwrite_refused(self):
        cand, _ = self.candidate()
        before = cand.read_bytes()
        with self.assertRaises(FileExistsError):
            deep.generate(self.input, cand.parent)
        self.assertEqual(cand.read_bytes(), before)

    def test_any_frozen_ancestor_protected(self):
        p = self.f.root / "reviews/frozen-archive"
        p.mkdir()
        (p / "delivery-manifest.json").write_text("{}")
        with self.assertRaises(ValueError):
            self.m.publish(p / "unregistered-child", {"x": b"x"})
        self.assertFalse((p / "unregistered-child").exists())

    def test_bad_candidate_hash_rejected(self):
        cand, d = self.candidate()
        dec = self.decisions(cand, d)
        with self.assertRaises(ValueError):
            self.call_dispose(cand, dec, "0" * 64)

    def test_candidate_count_forgery_recomputed_and_rejected(self):
        cand, d = self.candidate()
        d["family_pairs_total"] += 1
        cand.write_bytes(self.m.encoded(d))
        dec = self.decisions(cand, d)
        with self.assertRaises(ValueError):
            self.call_dispose(cand, dec)

    def test_stale_decision_version_rejected(self):
        cand, d = self.candidate()
        dec = self.decisions(cand, d)
        doc = self.m.read_json(dec.read_bytes())
        doc["rows"][0]["train_record_sha256"] = "0" * 64
        dec.write_bytes(self.m.encoded(doc))
        with self.assertRaises(ValueError):
            self.call_dispose(cand, dec)

    def test_missing_decision_rejected(self):
        cand, d = self.candidate()
        dec = self.decisions(cand, d)
        doc = self.m.read_json(dec.read_bytes())
        doc["rows"] = []
        dec.write_bytes(self.m.encoded(doc))
        with self.assertRaises(ValueError):
            self.call_dispose(cand, dec)

    def test_duplicate_decision_rejected(self):
        cand, d = self.candidate()
        dec = self.decisions(cand, d)
        doc = self.m.read_json(dec.read_bytes())
        doc["rows"] *= 2
        dec.write_bytes(self.m.encoded(doc))
        with self.assertRaises(ValueError):
            self.call_dispose(cand, dec)

    def test_empty_reason_rejected(self):
        cand, d = self.candidate()
        dec = self.decisions(cand, d)
        doc = self.m.read_json(dec.read_bytes())
        doc["rows"][0]["pairwise_reason"] = ""
        dec.write_bytes(self.m.encoded(doc))
        with self.assertRaises(ValueError):
            self.call_dispose(cand, dec)

    def test_same_core_nonzero_exit_and_no_green(self):
        cand, d = self.candidate()
        dec = self.decisions(cand, d, "SAME_CORE")
        self.assertEqual(self.call_dispose(cand, dec), 3)
        report = self.m.read_json((self.f.sigdir / "disposed/deep-candidates-disposed.json").read_bytes())
        self.assertFalse(report["PASS_CORE_SCOPE_issued"])

    def test_pending_pair_nonzero_exit(self):
        cand, d = self.candidate()
        dec = self.decisions(cand, d, "NEEDS_REVIEW")
        self.assertEqual(self.call_dispose(cand, dec), 3)

    def test_all_local_distinct_is_packaging_only(self):
        cand, d = self.candidate()
        dec = self.decisions(cand, d)
        self.assertEqual(self.call_dispose(cand, dec), 0)
        report = self.m.read_json((self.f.sigdir / "disposed/deep-candidates-disposed.json").read_bytes())
        self.assertEqual(report["semantic_isolation"], "NOT_ESTABLISHED")
        self.assertEqual(report["independent_reason_correctness"], "REQUIRES_SEPARATE_REVIEW_RECEIPT")
        self.assertEqual(report["family_pairs_not_flagged"], 0)

if __name__ == "__main__":
    unittest.main()
