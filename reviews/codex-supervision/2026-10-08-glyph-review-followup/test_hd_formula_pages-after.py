import ast,json,tempfile,unittest,sys
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
import hd_formula_pages as hd
class HDTests(unittest.TestCase):
    def test_actual_resolution_and_static_fps_are_explicit(self):
        c=hd.render_command(Path("scene.py"),Path("media"))
        self.assertEqual(c[c.index("--resolution")+1],"3840,2160")
        self.assertEqual(c[c.index("--fps")+1],"1")
    def test_exact_formula_text_and_no_math_scale(self):
        fs=[r"\frac{1}{7}",r"\sqrt{2}",r"\text{??}"]
        tree=ast.parse(hd.hd_scene(fs,"sample"))
        literal=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="FORMULAS" for t in n.targets))
        self.assertEqual(literal,fs)
        for n in ast.walk(tree):
            if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ("scale","resize"):
                self.assertEqual(n.func.value.id,"label")
    def test_geometry_reports_actual_pixel_config(self):
        s=hd.hd_scene(["x"],"sample")
        self.assertIn('"pixel_width":config.pixel_width',s)
        self.assertIn('"pixel_height":config.pixel_height',s)
        self.assertNotIn("get_frame(",s)
    def test_pin_rejects_tamper(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"input";p.write_bytes(b"one");expected=hd.core.digest(p.read_bytes())
            self.assertEqual(hd.pinned(p,expected),b"one")
            p.write_bytes(b"two")
            with self.assertRaises(ValueError):hd.pinned(p,expected)
    def cache_fixture(self,d):
        root=Path(d);parent=root/"parent";work=parent/"render-id";tex=work/"media/Tex"
        tex.mkdir(parents=True);g=work/"page-geometry.json";g.write_bytes(b"{}")
        for name in ("a.svg","a.tex"):(tex/name).write_bytes(name.encode())
        row={"geometry_path":"parent/render-id/page-geometry.json","geometry_sha256":hd.core.digest(g.read_bytes())}
        artifacts={p.relative_to(parent).as_posix():{"sha256":hd.core.digest(p.read_bytes())} for p in tex.iterdir()}
        return root,parent,tex,row,artifacts
    def test_copy_only_bound_vector_sources(self):
        with tempfile.TemporaryDirectory() as d:
            root,parent,tex,row,artifacts=self.cache_fixture(d)
            with patch.object(hd.core,"ROOT",root),patch.object(hd,"PARENT",parent):
                r=hd.copy_bound_cache(row,artifacts,root/"new/Tex")
                self.assertEqual(len(r),2)
                self.assertEqual((root/"new/Tex/a.svg").read_bytes(),b"a.svg")
    def test_unlisted_cache_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root,parent,tex,row,artifacts=self.cache_fixture(d)
            (tex/"b.svg").write_bytes(b"unlisted")
            with patch.object(hd.core,"ROOT",root),patch.object(hd,"PARENT",parent):
                with self.assertRaises(ValueError):hd.copy_bound_cache(row,artifacts,root/"new/Tex")
    def test_changed_bound_svg_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root,parent,tex,row,artifacts=self.cache_fixture(d);(tex/"a.svg").write_bytes(b"changed")
            with patch.object(hd.core,"ROOT",root),patch.object(hd,"PARENT",parent):
                with self.assertRaises(ValueError):hd.copy_bound_cache(row,artifacts,root/"new/Tex")
    def test_traversal_fails(self):
        with self.assertRaises(ValueError):hd.core.checked_path(hd.PARENT/"../outside",hd.PARENT)

    def test_fraction_array_detection_is_local(self):
        self.assertTrue(hd.needs_fraction_spacing(r"\begin{pmatrix}1&\frac12\\0&\frac12\end{pmatrix}"))
        self.assertTrue(hd.needs_fraction_spacing(r"\begin{cases}\dfrac{x}{y}&x>0\\0&x=0\end{cases}"))
        self.assertFalse(hd.needs_fraction_spacing(r"\frac12+\begin{pmatrix}1&2\\3&4\end{pmatrix}"))
        self.assertFalse(hd.needs_fraction_spacing(r"\frac12"))
    def test_spacing_preserves_exact_tex_and_font(self):
        formula=r"M^{-1}=\begin{pmatrix}1&-1&-\frac12\\-1&2&\frac12\\0&0&\frac12\end{pmatrix}"
        scene=hd.hd_scene([formula],"sample")
        tree=ast.parse(scene)
        literal=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="FORMULAS" for t in n.targets))
        self.assertEqual(literal,[formula])
        self.assertIn(r"\renewcommand{\arraystretch}{2}",scene)
        for n in ast.walk(tree):
            if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="MathTex":
                self.assertTrue(any(k.arg=="font_size" and k.value.value==48 for k in n.keywords))
    def test_unaffected_scene_is_byte_identical_to_prior(self):
        fs=[r"\frac17",r"\begin{pmatrix}1&2\\3&4\end{pmatrix}"]
        old=hd.base.scene_source(fs,"sample").replace('"schema":"exact-formula-pages-v1"',
            '"schema":"exact-formula-pages-hd-v1","pixel_width":config.pixel_width,"pixel_height":config.pixel_height,"fps":str(config.frame_rate),"page_seconds":"3"')
        self.assertEqual(hd.hd_scene(fs,"sample"),old)

if __name__=="__main__":unittest.main()
