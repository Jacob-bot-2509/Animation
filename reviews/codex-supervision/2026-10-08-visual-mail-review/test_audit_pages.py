import importlib.util
from pathlib import Path
import copy, unittest
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location("page_audited",Path(__file__).with_name("audit_pages.py"))
n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
class CoverageAdversarialTests(unittest.TestCase):
    def valid(self):
        return {"font_size":48,"formula_scale":"1","viewport_width":"12","viewport_height":"6","dimensions":[["2","1"],["2","1"]],
                "pages":[{"page":1,"kind":"FULL_FORMULAS","items":[{"formula_index":0,"x":"0","y":"1"},{"formula_index":1,"x":"0","y":"-1"}],"frame":"a.png"}]}
    def bad(self,g):
        with self.assertRaises(ValueError):n.verify_geometry(g,2)
    def test_valid_geometry(self):self.assertEqual(n.verify_geometry(self.valid(),2),1)
    def test_drop_formula(self):
        g=self.valid();g["pages"][0]["items"].pop();self.bad(g)
    def test_small_font(self):
        g=self.valid();g["font_size"]=12;self.bad(g)
    def test_global_shrink(self):
        g=self.valid();g["formula_scale"]="1/5";self.bad(g)
    def test_clipped_full_formula(self):
        g=self.valid();g["pages"][0]["items"][0]["x"]="6";self.bad(g)
    def test_overlap(self):
        g=self.valid();g["pages"][0]["items"][1]["y"]="1";self.bad(g)
    def test_duplicate_page(self):
        g=self.valid();g["pages"].append(copy.deepcopy(g["pages"][0]));self.bad(g)
    def test_missing_start_of_long_formula(self):
        with self.assertRaises(ValueError):n.cover_axis(["0"],n.F(30),n.F(12))
    def test_internal_segment_gap(self):
        with self.assertRaises(ValueError):n.cover_axis(["-9","9"],n.F(30),n.F(12))
    def test_complete_long_formula_overlaps(self):
        n.cover_axis(["-9","0","9"],n.F(30),n.F(12))
if __name__=="__main__":unittest.main()
