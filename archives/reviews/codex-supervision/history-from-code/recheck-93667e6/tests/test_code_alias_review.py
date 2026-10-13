"""Focused review regressions: inspect AST only; never execute sample code."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from animtrain.code_gate import check_dangerous


class TestReviewAliases(unittest.TestCase):
    def test_from_import_dangerous_functions(self):
        for code in (
            'from os import system as launch\nlaunch("never executed")',
            'from os import unlink\nunlink("never executed")',
            'from shutil import rmtree as remove_tree\nremove_tree("never executed")',
        ):
            with self.subTest(code=code):
                self.assertTrue(check_dangerous(code))

    def test_builtin_aliases(self):
        for code in (
            'from builtins import eval as evaluate\nevaluate("never executed")',
            'import builtins as b\nb.open("never executed")',
        ):
            with self.subTest(code=code):
                self.assertTrue(check_dangerous(code))

    def test_existing_module_alias(self):
        self.assertTrue(check_dangerous(
            'import os as operating\noperating.system("never executed")'))

    def test_safe_alias_is_allowed(self):
        self.assertEqual(check_dangerous(
            'from math import sqrt as root\nroot(4)'), [])

    def test_unimported_local_name_is_not_assumed_dangerous(self):
        self.assertEqual(check_dangerous(
            'def launch(value):\n    return value\nlaunch(4)'), [])


if __name__ == "__main__":
    unittest.main()
