"""训练后端适配器契约测试(msg_195):未批准阶段一律 NOT_APPROVED,
不下载/不安装/不训练;纯标准库零依赖。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.backend import (  # noqa: E402
    STATUS_NOT_APPROVED, BackendNotApproved, TrainingBackend, get_backend,
    register_backend)


class TestBackendContract(unittest.TestCase):
    def setUp(self):
        self.be = TrainingBackend()

    def test_load_model_not_approved(self):
        with self.assertRaises(BackendNotApproved):
            self.be.load_model({})

    def test_train_not_approved(self):
        with self.assertRaises(BackendNotApproved):
            self.be.train({}, "data/v1/manifest-train.json")

    def test_save_checkpoint_not_approved(self):
        with self.assertRaises(BackendNotApproved):
            self.be.save_checkpoint("x", "outputs/x")

    def test_evaluate_not_approved(self):
        with self.assertRaises(BackendNotApproved):
            self.be.evaluate({}, "data/v1/manifest-eval.json")

    def test_unknown_backend_returns_safe_stub(self):
        """未知后端名必须返回默认契约后端(全操作 NOT_APPROVED),不得静默假实现。"""
        stub = get_backend("some-future-backend")
        with self.assertRaises(BackendNotApproved):
            stub.train({}, "x")

    def test_registered_stub_still_not_approved(self):
        class Stub(TrainingBackend):
            name = "stub"
        register_backend("stub", Stub)
        stub = get_backend("stub")
        self.assertEqual(stub.name, "stub")
        with self.assertRaises(BackendNotApproved):
            stub.train({}, "x")

    def test_status_constant(self):
        self.assertEqual(STATUS_NOT_APPROVED, "NOT_APPROVED")


if __name__ == "__main__":
    unittest.main()
