"""Independent scanner, publication and source validation regressions. No rendering."""
import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
from unittest import mock
HERE=Path(__file__).absolute().parent
spec=importlib.util.spec_from_file_location("review_math_scanner",HERE/"build_math_correspondence.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
SCRATCH=m.ROOT/"reviews/codex-supervision/2026-10-17-math-correspondence-tests";SCRATCH.mkdir(exist_ok=True)
class Tests(unittest.TestCase):
 def test_decimal_forms(self):
  items=[x for x in m.scan(" .5 -1.25 2.50e2 1e-3 3. ")["items"] if x["kind"]=="decimal_literal"]
  self.assertEqual([x["literal_fraction_candidate"] for x in items],["1/2","-5/4","250","1/1000","3"])
 def test_no_float_rounding_guess(self):
  self.assertEqual(m.scan("0.333")["items"][0]["literal_fraction_candidate"],"333/1000")
 def test_large_exponent_not_converted(self):
  self.assertIsNone(m.scan("1e99999")["items"][0]["literal_fraction_candidate"])
 def test_no_number_inside_identifier(self):
  self.assertEqual(m.scan("foo0.5 v1.2.3")["items"],[])
 def test_negative_denominator(self):
  self.assertEqual(m.scan("1/-2")["items"][0]["literal_fraction_candidate"],"-1/2")
 def test_zero_denominator_not_exact(self):
  x=m.scan("1/0")["items"][0];self.assertEqual(x["meaning"],"UNDEFINED_ZERO_DENOMINATOR");self.assertIsNone(x["literal_fraction_candidate"])
 def test_decimal_slash_not_integer_fraction(self):
  self.assertFalse(any(x["kind"]=="text_fraction_syntax" for x in m.scan("0.5/2")["items"]))
 def test_nested_dfrac_tfrac(self):
  text=r"$\dfrac{1+\frac{1}{2}}{\sqrt{n}}+\tfrac{2}{4}$"
  xs=[x for x in m.scan(text)["items"] if x["kind"]=="latex_fraction_syntax"]
  self.assertEqual([x["value"] for x in xs],[r"\dfrac{1+\frac{1}{2}}{\sqrt{n}}",r"\frac{1}{2}",r"\tfrac{2}{4}"])
  self.assertIsNone(xs[0]["literal_fraction_candidate"]);self.assertEqual(xs[2]["literal_fraction_candidate"],"1/2")
 def test_latex_zero_denominator(self):
  self.assertEqual(m.scan(r"\frac{1}{0}")["items"][0]["meaning"],"UNDEFINED_ZERO_DENOMINATOR")
 def test_unparsed_fraction_explicit(self):
  self.assertEqual(m.scan(r"\frac12")["items"][0]["meaning"],"UNPARSED_FRACTION_COMMAND_REQUIRES_REVIEW")
 def test_symbolic_arcsin(self):
  self.assertEqual(m.scan(r"\arcsin x")["items"][0]["value"],r"\arcsin")
 def test_math_semicolon_not_sentence_split(self):
  text="\u7532\u3002"+r"$x\;y$"+"\uff1b\u4e59;"
  parts=m.sentences(text);self.assertEqual(len(parts),3);self.assertEqual("".join(x["text"] for x in parts),text)
 def test_formula_unmatched_explicit(self):
  self.assertEqual(m.formulas("bad $x")[0]["meaning"],"UNMATCHED_DELIMITER_REQUIRES_REVIEW")
 def test_every_field_and_span(self):
  obj={"problem":"P","solution":r"$\frac{1}{2}$?","answer":"A","scene_spec":{"objects":["0.5"],"steps":["1/2"]}}
  f=m.fields(obj);self.assertEqual(set(f),{"problem","solution","answer","scene_spec.objects[0]","scene_spec.steps[0]"})
  for scanned in f.values():
   for item in scanned["items"]:self.assertEqual(scanned["text"][item["start"]:item["end"]],item["value"])
 def test_missing_solution_rejected(self):
  with self.assertRaises(ValueError):m.fields({"problem":"P","answer":"A"})
 def test_real_ten_source_bound(self):
  result=m.build();self.assertEqual(len(result["records"]),10)
  self.assertTrue(all(x["math_verdict"]=="PENDING_REVIEW" for x in result["records"]))
  first=result["records"][0];self.assertIn("scene_spec.steps[6]",first["fields"])
 def test_source_replaced_after_binding_rejected(self):
  bound=m.core.build();bound["records"][0]["source"]["canonical_record_sha256"]="0"*64
  with mock.patch.object(m.core,"build",return_value=bound):
   with self.assertRaisesRegex(ValueError,"source_identity_changed"):m.build()
 def test_new_generation_does_not_overwrite(self):
  d=Path(tempfile.mkdtemp(prefix="case-",dir=SCRATCH))
  try:
   historical=d/"math-correspondence.jsonl";historical.write_bytes(b"KEEP")
   result={"records":[{"sample_id":"test"}],"input_pins":{},"schema":"test","qualification":"TEST_ONLY"}
   a=m.publish(result,base=d);b=m.publish(result,base=d);self.assertNotEqual(a,b)
   self.assertEqual(historical.read_bytes(),b"KEEP")
   complete=json.loads((a/"COMPLETE.json").read_bytes())
   for pin in complete["artifacts"]:
    raw=(a/pin["path"]).read_bytes();self.assertEqual(m.sha(raw),pin["sha256"]);self.assertEqual(len(raw),pin["bytes"])
  finally:
   assert d.resolve().is_relative_to(SCRATCH.resolve()) and d.resolve()!=SCRATCH.resolve();shutil.rmtree(d)
 def test_frozen_parent_rejected(self):
  d=Path(tempfile.mkdtemp(prefix="case-",dir=SCRATCH))
  try:
   (d/"delivery-manifest.json").write_bytes(b"{}");child=d/"child";child.mkdir()
   with self.assertRaisesRegex(ValueError,"frozen_output"):m.publish({},base=child)
  finally:
   assert d.resolve().is_relative_to(SCRATCH.resolve()) and d.resolve()!=SCRATCH.resolve();shutil.rmtree(d)
 def test_outside_output_rejected(self):
  with self.assertRaises(ValueError):m.publish({},base=m.ROOT.parent)
 def test_pins_changed_before_publish_rejected(self):
  d=Path(tempfile.mkdtemp(prefix="case-",dir=SCRATCH))
  try:
   p=d/"pin.txt";p.write_bytes(b"actual")
   result={"input_pins":{p.relative_to(m.ROOT).as_posix():{"sha256":"0"*64}}}
   with self.assertRaisesRegex(ValueError,"input_changed_before_publish"):m.publish(result,base=d)
  finally:
   assert d.resolve().is_relative_to(SCRATCH.resolve()) and d.resolve()!=SCRATCH.resolve();shutil.rmtree(d)
if __name__=="__main__":unittest.main(verbosity=2)
