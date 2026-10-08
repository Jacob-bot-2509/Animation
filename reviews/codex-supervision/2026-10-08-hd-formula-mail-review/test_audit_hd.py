import importlib.util,json,sys,tempfile,unittest
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from PIL import Image
OWNER=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("hd_auditor_tested",OWNER/"audit_hd.py")
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
class AuditorTests(unittest.TestCase):
    def test_wrong_png_resolution_fails(self):
        with tempfile.TemporaryDirectory()as d:
            p=Path(d)/"frame.png";Image.new("RGB",(854,480)).save(p)
            with self.assertRaises(ValueError):a.page_density(p,1)
    def test_empty_formula_viewport_fails(self):
        with tempfile.TemporaryDirectory()as d:
            p=Path(d)/"frame.png";Image.new("RGB",(3840,2160)).save(p)
            with self.assertRaises(ValueError):a.page_density(p,1)
    def test_page_count_and_exact_fraction_not_record_total(self):
        with tempfile.TemporaryDirectory()as d:
            p=Path(d)/"frame.png";arr=np.zeros((2160,3840,3),dtype=np.uint8)
            arr[500:541,600:680]=255;Image.fromarray(arr).save(p)
            r=a.page_density(p,6)
            self.assertEqual(r["bbox_height_per_displayed_item_px_exact"],"41/6")
            self.assertEqual(r["slot_proxy_at_1080p_exact"],"41/12")
    def test_invalid_page_item_count_fails(self):
        for count in (0,-1,True,"6"):
            with self.assertRaises(ValueError):a.page_density(Path("unused"),count)
if __name__=="__main__":unittest.main()
