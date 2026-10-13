"""Guard actual delimiter commands without misclassifying TeX arrows."""
import unittest
from tools.dataset_audit import Audit,check_latex

class LatexDelimiterTests(unittest.TestCase):
    def issues(self,text):
        audit=Audit()
        check_latex(audit,{'path':'fixture'}, {'locator':'row1','record':{'problem':text}},'fixture')
        return audit.issues

    def test_arrows_are_not_delimiters(self):
        for command in (r'\leftarrow',r'\leftrightarrow',r'\rightarrow',r'\rightleftharpoons'):
            with self.subTest(command=command):
                self.assertFalse(any(x['code']=='L006' for x in self.issues('$a'+command+'b$')))

    def test_paired_real_delimiters_with_arrows(self):
        text=r'$\left(a\leftarrow b\right)$'
        self.assertFalse(any(x['code']=='L006' for x in self.issues(text)))

    def test_missing_delimiters_still_detected(self):
        for text in (r'$\left(a$',r'$a\right)$',r'$\left(a\rightarrow b$'):
            with self.subTest(text=text):
                self.assertTrue(any(x['code']=='L006' for x in self.issues(text)))

    def test_cjk_hard_guard_unchanged(self):
        self.assertTrue(any(x['code']=='L002' and x['severity']=='hard'
                            for x in self.issues('$P('+chr(0x4e2d)+')$')))
