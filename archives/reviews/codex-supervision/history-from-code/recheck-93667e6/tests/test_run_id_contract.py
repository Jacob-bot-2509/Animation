"""Run identifiers must match the entire input, including its final character."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from animtrain.fs_guard import valid_run_id

class TestRunIdContract(unittest.TestCase):
    def test_valid_identifiers(self):
        for value in ("run-1_a","x"*64):
            with self.subTest(value=value):
                self.assertTrue(valid_run_id(value))

    def test_invalid_identifiers(self):
        for value in ("run\n","run\r\n","","x"*65,"../run"," run","run/1"):
            with self.subTest(value=value):
                self.assertFalse(valid_run_id(value))
