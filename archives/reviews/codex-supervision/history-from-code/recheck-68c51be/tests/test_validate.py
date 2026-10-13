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
        _write(train, '{"id": "t1", "problem": "p1", "solution": "s1", "answer": "1"}\n'
                      '{"id": "t2", "problem": "p2", "solution": "s2", "answer": "2"}\n')
        _write(ev, '{"id": "e1", "problem": "p3", "solution": "s3", "answer": "3"}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(train),
                  size=train.stat().st_size,
                  source="x", license="internal-generated", split="train"),
            Entry(path="eval/b.jsonl", sha256=sha256_file(ev),
                  size=ev.stat().st_size,
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
        """msg_101-1 数据合约:quarantine 不默认通过。"""
        p = self.root / "train" / "a.jsonl"
        _write(p, '{"id": "t1", "problem": "p1", "solution": "s1", "answer": "1"}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(p),
                  size=p.stat().st_size,
                  source="x", license="", split="train")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("许可证未标注" in q for q in r["quarantines"]),
                        r["quarantines"])
        self.assertFalse(r["ok"], "quarantine 不得默认通过")
        self.assertEqual(r["exit_code"], 2, "quarantine exit_code 应为 2(与硬伤 1 区分)")

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
            Entry(path="train/a.jsonl", sha256=sha256_file(train),
                  size=train.stat().st_size,
                  source="x", license="internal-generated", split="train"),
            Entry(path="eval/b.jsonl", sha256=sha256_file(ev),
                  size=ev.stat().st_size,
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
            Entry(path="train/a.jsonl", sha256=sha256_file(train),
                  size=train.stat().st_size,
                  source="x", license="internal-generated", split="train"),
            Entry(path="eval/b.jsonl", sha256=sha256_file(ev),
                  size=ev.stat().st_size,
                  source="x", license="internal-generated", split="eval")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("精确重叠" in p for p in r["problems"]), r["problems"])

    def test_id_overlap_detected(self):
        """msg_101-2:样本 ID 字段重叠 = 0 —— 内容不同但 ID 相同也必须检出。"""
        train = self.root / "train" / "a.jsonl"
        ev = self.root / "eval" / "b.jsonl"
        _write(train, '{"id": "q1", "problem": "训练版题干A"}\n')
        _write(ev, '{"id": "q1", "problem": "评测版题干(内容不同)"}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(train),
                  size=train.stat().st_size,
                  source="x", license="internal-generated", split="train"),
            Entry(path="eval/b.jsonl", sha256=sha256_file(ev),
                  size=ev.stat().st_size,
                  source="x", license="internal-generated", split="eval")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("ID 重叠" in p for p in r["problems"]), r["problems"])

    def test_file_hash_overlap_detected(self):
        """msg_101-2:文件 hash 重叠 = 0 —— 两个不同路径内容相同的文件必须检出。"""
        p1 = self.root / "train" / "a.jsonl"
        p2 = self.root / "train" / "b.jsonl"
        _write(p1, '{"id": "t1"}\n')
        _write(p2, '{"id": "t1"}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(p1), size=1,
                  source="x", license="internal-generated", split="train"),
            Entry(path="train/b.jsonl", sha256=sha256_file(p2), size=1,
                  source="x", license="internal-generated", split="train")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("文件内容完全相同" in p for p in r["problems"]),
                        r["problems"])

    def test_near_dup_threshold_configurable(self):
        """msg_101-2:近重复阈值可配置(当前 0.7 只是初始值)。"""
        train = self.root / "train" / "a.jsonl"
        ev = self.root / "eval" / "b.jsonl"
        _write(train, '{"problem": "%s"}\n' % ("某工厂生产两种产品,甲每件利润3元,乙每件利润5元,"
               "生产甲需A材料2千克和B材料1千克,生产乙需A材料1千克和B材料3千克,"
               "现有A材料100千克、B材料120千克,问各生产多少件利润最大"))
        _write(ev, '{"problem": "%s"}\n' % ("某工厂生产两种产品,甲每件利润3元,乙每件利润5元,"
               "生产甲需A材料2千克和B材料1千克,生产乙需A材料1千克和B材料3千克,"
               "现有A材料100千克、B材料120千克,如何安排生产使利润达到最大"))
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(train),
                  size=train.stat().st_size,
                  source="x", license="internal-generated", split="train"),
            Entry(path="eval/b.jsonl", sha256=sha256_file(ev),
                  size=ev.stat().st_size,
                  source="x", license="internal-generated", split="eval")])
        r_loose = validate_manifest(m, self.root, near_dup_threshold=0.5)
        self.assertTrue(any("近重复" in p for p in r_loose["problems"]),
                        "阈值 0.5 应检出")
        r_strict = validate_manifest(m, self.root, near_dup_threshold=0.95)
        self.assertFalse(any("近重复" in p for p in r_strict["problems"]),
                         "阈值 0.95 不应检出")

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
