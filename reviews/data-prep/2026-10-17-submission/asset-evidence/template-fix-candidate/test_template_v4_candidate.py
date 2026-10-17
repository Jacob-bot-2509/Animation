"""Independent pure-logic/AST tests for the v4 candidate. No Manim import/execution."""
import ast
import copy
import unittest

import render_templates_v4_candidate as m


class TemplateV4Tests(unittest.TestCase):
    # --- v2 regression set (same expectations, v3 import) ---

    def test_mixed_content_and_whitespace(self):
        self.assertEqual(m.split_mixed(" a $x$ b "), [("text", " a "), ("math", "x"), ("text", " b ")])

    def test_newline_and_blank_line_preserved(self):
        self.assertEqual(m.split_mixed("a\n\nb"), [("text", "a"), ("break", "\n"), ("break", "\n"), ("text", "b")])

    def test_text_escaped_dollar(self):
        self.assertEqual(m.split_mixed(r"cost \$5 and $x$"), [("text", "cost $5 and "), ("math", "x")])

    def test_math_escape_retained(self):
        self.assertEqual(m.split_mixed(r"$\$$"), [("math", r"\$")])

    def test_even_backslashes_do_not_escape_delimiter(self):
        self.assertEqual(m.split_mixed("\\\\" + "$x$"), [("text", "\\\\"), ("math", "x")])

    def test_unsupported_or_empty_math_fails(self):
        for text in ("$x", "$$x$$", "$ $", r"\(x\)", "$x\ny$"):
            with self.subTest(text=text):
                with self.assertRaises(m.TemplateError):
                    m.split_mixed(text)

    def test_empty_or_nonstring_rejected(self):
        for text in ("", "  ", None, 1):
            with self.subTest(text=text):
                with self.assertRaises(m.TemplateError):
                    m.split_mixed(text)

    def test_long_step_fragments_once(self):
        source = "\n".join("unique_line_" + str(i) for i in range(12))
        code, plan = m.steps_block_v2([source])
        self.assertTrue(m.coverage_ok([source], plan))
        self.assertEqual(len(plan["rows"]), 12)
        self.assertEqual(len(plan["provisional_pages"]), 3)
        self.assertEqual(code.count("Text('unique_line_0'"), 1)

    def test_long_text_chunked_without_loss(self):
        steps = ["A" * 150 + " $x$ " + "B" * 80]
        plan = m.make_plan(steps, chunk_chars=16)
        fragments = [f for row in plan["rows"] for f in row["fragments"]]
        self.assertEqual("".join(steps[0][f["start"]:f["end"]] for f in fragments), steps[0])
        self.assertTrue(m.coverage_ok(steps, plan))

    def test_all_steps_in_order(self):
        steps = ["step" + str(i) for i in range(9)]
        plan = m.make_plan(steps)
        self.assertEqual([r["source_index"] for r in plan["rows"]], list(range(9)))
        self.assertTrue(m.coverage_ok(steps, plan))

    def test_invalid_budget_cannot_loop(self):
        for n in (0, -1, True, "5", None):
            with self.assertRaises(m.TemplateError):
                m.make_plan(["a"], per_page_lines=n)
        with self.assertRaises(m.TemplateError):
            m.paginate([0], 0, {0: 1})

    def test_empty_sources_not_proof(self):
        with self.assertRaises(m.TemplateError):
            m.make_plan([])
        self.assertFalse(m.coverage_ok([], {}))

    def test_missing_duplicate_unknown_page_fragments_rejected(self):
        for pages in ([], [[0, 0]], [[0], [99]], [[1], [0]]):
            plan = m.make_plan(["a", "b"])
            plan["provisional_pages"] = pages
            self.assertFalse(m.coverage_ok(["a", "b"], plan))

    def test_content_span_and_source_tamper_rejected(self):
        plan = m.make_plan(["a $x$"])
        for mutate in ("content", "start", "kind", "sources"):
            bad = copy.deepcopy(plan)
            if mutate == "sources":
                bad["sources"] = ["other"]
            else:
                bad["rows"][0]["fragments"][0][mutate] = "changed"
            self.assertFalse(m.coverage_ok(["a $x$"], bad))

    def test_generated_syntax_only(self):
        code, plan = m.scene_blocks_v2("Problem $x$", ["a\nb $x+1$"], "1/3")
        source = "class Candidate:\n    def construct(self):\n" + code
        ast.parse(source)
        compile(source, "<candidate-ast-only>", "exec")
        self.assertNotIn("scale_to_fit", code)
        self.assertIn("candidate_row_exceeds_measured_viewport", code)
        self.assertIn("candidate_requires_dedicated_empty_canvas", code)
        self.assertIn("candidate_page_map", code)

    def test_all_math_precedes_text(self):
        code, _ = m.scene_blocks_v2("head $h$", ["step $s$"], "tail $t$")
        self.assertLess(code.rfind("= MathTex("), code.find("= Text("))

    def test_pure_text_title_and_answer_visible(self):
        self.assertIn("Text('plain problem'", m.title_block_v2("plain problem"))
        self.assertIn("Text('1/3'", m.answer_block_v2("1/3"))

    def test_invalid_font_and_plan_rejected(self):
        with self.assertRaises(m.TemplateError):
            m.generate_block(m.make_plan(["x"]), True)
        plan = m.make_plan(["x"])
        plan["rows"] = []
        with self.assertRaises(m.TemplateError):
            m.generate_block(plan)

    def test_exact_fractions_no_estimation(self):
        self.assertEqual(m.exact_fraction_text("0.333", True), r"\frac{333}{1000}")
        self.assertEqual(m.exact_fraction_text("-0.25", True), r"-\frac{1}{4}")
        self.assertEqual(m.exact_fraction_text("2.0", True), "2")
        self.assertEqual(m.exact_fraction_text("0.333...", False), "0.333...")

    def test_fraction_requires_boolean_provenance_flag(self):
        for value in ("yes", 1, None):
            with self.assertRaises(m.TemplateError):
                m.exact_fraction_text("0.5", value)
        with self.assertRaises(m.TemplateError):
            m.exact_fraction_text("0.333...", True)

    def test_exact_measured_pagination(self):
        from fractions import Fraction
        self.assertEqual(m.measured_pages([(2, 2), (2, 2), (2, 2)], 4, Fraction(17, 4)), [[0, 1], [2]])
        with self.assertRaises(m.TemplateError):
            m.measured_pages([(5, 1)], 4, 4)

    def test_bad_or_nonfinite_dimensions_fail(self):
        for size in ((1, 0), (1, float("nan")), (True, 1), (1, float("inf"))):
            with self.assertRaises(m.TemplateError):
                m.measured_pages([size], 4, 4)
        with self.assertRaises(m.TemplateError):
            m.estimate_height([[]])

    # --- v3 additions: row breaks prefer punctuation ---

    def test_long_text_breaks_after_punctuation(self):
        source = "第一段说明，第二段说明；第三段说明。" * 4
        plan = m.make_plan([source], chunk_chars=12)
        self.assertTrue(m.coverage_ok([source], plan))
        rows = plan["rows"]
        self.assertGreater(len(rows), 1)
        for row in rows[:-1]:
            tail = [f for f in row["fragments"] if f["kind"] == "text"][-1]["content"]
            self.assertIn(tail[-1], m.ROW_END_PUNCT, msg=f"row ends mid-word: {tail[-12:]!r}")

    def test_no_punctuation_falls_back_to_hard_cut(self):
        plan = m.make_plan(["A" * 40], chunk_chars=10)
        self.assertEqual(len(plan["rows"]), 4)
        self.assertTrue(m.coverage_ok(["A" * 40], plan))

    def test_mixed_math_row_break_keeps_order_and_coverage(self):
        source = "前文很长需要断行说明，随后 $x+1$ 出现，再继续解释一部分内容。"
        plan = m.make_plan([source], chunk_chars=14)
        fragments = [f for row in plan["rows"] for f in row["fragments"]]
        self.assertEqual("".join(source[f["start"]:f["end"]] for f in fragments), source)
        kinds = [f["kind"] for f in fragments]
        self.assertIn("math", kinds)
        self.assertTrue(m.coverage_ok([source], plan))

    def test_punctuation_break_does_not_split_math(self):
        source = "$a+b$，" * 8
        plan = m.make_plan([source], chunk_chars=10)
        for row in plan["rows"]:
            for frag in row["fragments"]:
                if frag["kind"] == "math":
                    self.assertTrue(frag["content"].endswith("b"), frag["content"])

    def test_row_fragments_use_reviewed_spacing(self):
        code, _ = m.scene_blocks_v2("head $x$ tail", ["a $y$ b"], "z")
        self.assertIn(f"buff={m.ROW_BUFF}", code)
        self.assertNotIn("arrange(RIGHT, buff=0)", code)
        source = "class Candidate:\n    def construct(self):\n" + code
        ast.parse(source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
