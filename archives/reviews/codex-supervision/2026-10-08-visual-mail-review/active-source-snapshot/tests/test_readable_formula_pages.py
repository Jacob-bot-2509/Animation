import ast
from fractions import Fraction as F
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("readable_tested",ROOT/"tools/readable_formula_pages.py")
n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
class ReadablePagesTests(unittest.TestCase):
    def test_no_global_scale_or_formula_rewrite(self):
        fs=[r"x^2",r"\frac{1}{3}",r"x="+"+".join(["a"]*200)]
        tree=ast.parse(n.scene_source(fs,"sample"))
        got=next(ast.literal_eval(a.value) for a in tree.body if isinstance(a,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="FORMULAS" for t in a.targets))
        self.assertEqual(got,fs)
        for call in (x for x in ast.walk(tree) if isinstance(x,ast.Call)):
            if isinstance(call.func,ast.Name) and call.func.id=="MathTex":
                self.assertIsInstance(call.args[0],ast.Name)
                self.assertEqual(call.args[0].id,"formula")
                self.assertIn(("font_size",48),[(k.arg,ast.literal_eval(k.value)) for k in call.keywords if isinstance(k.value,ast.Constant)])
            if isinstance(call.func,ast.Attribute) and call.func.attr=="scale":
                self.assertEqual(call.func.value.id,"label")
    def test_all_many_formulas_once_in_full_pages(self):
        ps=n.plan_panels([(2,1)]*49,12,6)
        self.assertEqual([i["formula_index"] for p in ps for i in p["items"]],list(range(49)))
        self.assertTrue(all(len(p["items"])<=6 for p in ps))
    def test_full_pages_fit_without_shrink(self):
        dims=[(3,F(3,2)),(5,2),(8,1),(1,3)]
        ps=n.plan_panels(dims,12,6)
        for p in ps:
            for i in p["items"]:
                w,h=dims[i["formula_index"]]
                self.assertLessEqual(abs(i["y"])+h/2,3)
                self.assertEqual(i["x"],0)
    def test_wide_formula_views_cover_both_edges(self):
        cs=n.axis_centers(31,12)
        self.assertEqual(cs[0]-6,-F(31,2))
        self.assertEqual(cs[-1]+6,F(31,2))
        self.assertTrue(all(b-a<=12 for a,b in zip(cs,cs[1:])))
    def test_tall_and_wide_formula_two_axis_coverage(self):
        ps=n.plan_panels([(31,14)],12,6)
        self.assertEqual(len(ps),9)
        self.assertTrue(all(p["kind"]=="FORMULA_SEGMENT" for p in ps))
        self.assertTrue(all(p["tile_grid"]==[3,3] for p in ps))
    def test_exact_boundary_fits_one_view(self):
        self.assertEqual(n.axis_centers(12,12),[F(0)])
        self.assertEqual(n.plan_panels([(12,6)],12,6)[0]["kind"],"FULL_FORMULAS")
    def test_oversized_tile_limit_fails_instead_of_shrink(self):
        with self.assertRaises(ValueError):n.plan_panels([(12000,6000)],12,6)
    def test_empty_or_invalid_dimensions_rejected(self):
        for ds in ([],[(0,1)],[(1,-1)],[("nan",1)]):
            with self.assertRaises((ValueError,TypeError)):n.plan_panels(ds,12,6)
    def test_next_group_after_segment_retains_order(self):
        ps=n.plan_panels([(1,1),(40,1),(1,1)],12,6)
        self.assertEqual(ps[0]["items"][0]["formula_index"],0)
        self.assertEqual(ps[-1]["items"][0]["formula_index"],2)
        self.assertTrue(all(x["items"][0]["formula_index"]==1 for x in ps[1:-1]))
    def test_cjk_exact_template_preserved(self):
        source=n.scene_source([r"f=0,\text{其他}"],"sample")
        self.assertIn("xelatex",source)
        self.assertIn(r"\usepackage[UTF8]{ctex}",source)
        self.assertIn(r"f=0,\\text{其他}",source)
    def test_old_svg_caches_are_not_copied_into_new_render(self):
        import inspect
        source=inspect.getsource(n.render)
        self.assertNotIn("copyfile",source)
        self.assertNotIn("copytree",source)
    def test_scene_does_not_export_stale_camera_screenshots(self):
        import inspect
        source=n.scene_source(["x","y"],"sample")
        self.assertNotIn("self.renderer.get_frame",source)
        self.assertNotIn("self.renderer.update_frame",source)
        self.assertIn("decode_pages",inspect.getsource(n.render))
    def test_invalid_id_and_empty_formula_rejected(self):
        for fs,rid in [(["x"],"../escape"),([], "x"),([""],"x")]:
            with self.assertRaises(ValueError):n.scene_source(fs,rid)
if __name__=="__main__":unittest.main()
