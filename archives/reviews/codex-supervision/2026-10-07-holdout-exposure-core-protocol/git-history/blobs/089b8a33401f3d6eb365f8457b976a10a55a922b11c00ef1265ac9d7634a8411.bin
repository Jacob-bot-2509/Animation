"""数据校验器测试(标准库 unittest,零依赖;仪器纪律:校验器必须先被已知样例验证)。

覆盖:文件存在/SHA256/许可证/split/训练-评测精确重叠。
运行: python -m unittest discover tests
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.manifest import Entry, Manifest, sha256_file  # noqa: E402
from animtrain.validate import validate_manifest  # noqa: E402


def _write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


class TestValidate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_clean_manifest_passes(self):
        train = self.root / "train" / "a.jsonl"
        ev = self.root / "eval" / "b.jsonl"
        _write(train, '{"id": "t1"}\n{"id": "t2"}\n')
        _write(ev, '{"id": "e1"}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(train), size=1,
                  source="x", license="internal-generated", split="train"),
            Entry(path="eval/b.jsonl", sha256=sha256_file(ev), size=1,
                  source="x", license="internal-generated", split="eval")])
        r = validate_manifest(m, self.root)
        self.assertTrue(r["ok"], r["problems"])

    def test_missing_file_detected(self):
        m = Manifest(name="t", entries=[
            Entry(path="train/ghost.jsonl", sha256="", size=0,
                  source="x", license="internal-generated", split="train")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("不存在" in p for p in r["problems"]), r["problems"])

    def test_sha256_mismatch_detected(self):
        p = self.root / "train" / "a.jsonl"
        _write(p, '{"id": "t1"}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256="f" * 64, size=1,
                  source="x", license="internal-generated", split="train")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("SHA256 不一致" in p for p in r["problems"]), r["problems"])

    def test_missing_license_quarantined(self):
        p = self.root / "train" / "a.jsonl"
        _write(p, '{"id": "t1"}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(p), size=1,
                  source="x", license="", split="train")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("许可证未标注" in q for q in r["quarantines"]),
                        r["quarantines"])

    def test_bad_license_detected(self):
        p = self.root / "train" / "a.jsonl"
        _write(p, '{"id": "t1"}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(p), size=1,
                  source="x", license="gpl-3.0", split="train")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("不在白名单" in p for p in r["problems"]), r["problems"])

    def test_exact_overlap_detected(self):
        """前项目 20/20 污染的教训:同一行内容同时出现在训练与评测 → 必须检出。"""
        train = self.root / "train" / "a.jsonl"
        ev = self.root / "eval" / "b.jsonl"
        _write(train, '{"id": "t1"}\n{"id": "dup"}\n')
        _write(ev, '{"id": "e1"}\n{"id": "dup"}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(train), size=1,
                  source="x", license="internal-generated", split="train"),
            Entry(path="eval/b.jsonl", sha256=sha256_file(ev), size=1,
                  source="x", license="internal-generated", split="eval")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("精确重叠" in p for p in r["problems"]), r["problems"])

    def test_overlap_identical_content_detected(self):
        """重叠检测按整行内容哈希:内容相同必检出。"""
        train = self.root / "train" / "a.jsonl"
        ev = self.root / "eval" / "b.jsonl"
        _write(train, '{"id": "x", "v": 1}\n')
        _write(ev, '{"id": "x", "v": 1}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(train), size=1,
                  source="x", license="internal-generated", split="train"),
            Entry(path="eval/b.jsonl", sha256=sha256_file(ev), size=1,
                  source="x", license="internal-generated", split="eval")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("精确重叠" in p for p in r["problems"]), r["problems"])

    def test_bad_split_detected(self):
        p = self.root / "train" / "a.jsonl"
        _write(p, '{"id": "t1"}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(p), size=1,
                  source="x", license="internal-generated", split="production")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("split" in p for p in r["problems"]), r["problems"])


if __name__ == "__main__":
    unittest.main()
