"""REVIEW_BACKLOG A 组反例测试(A1 校验漏洞 / A2 top20 截断漏检)。"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.manifest import Entry, Manifest, sha256_file  # noqa: E402
from animtrain.validate import validate_manifest  # noqa: E402
from animtrain.fields import check_fields  # noqa: E402
from animtrain.near_dup import ShingleIndex  # noqa: E402


def _mk(d: Path, rel: str, text: str) -> Path:
    p = d / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


class TestA1Validate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_empty_manifest_fails(self):
        """A1: entries=[] 函数直调也必须失败,不靠 CLI 拦。"""
        r = validate_manifest(Manifest(name="t", entries=[]), self.root)
        self.assertFalse(r["ok"], "空清单不得 ok=true")
        self.assertTrue(any("条目" in p or "空清单" in p for p in r["problems"]),
                        r["problems"])

    def test_blank_source_quarantined(self):
        """A1: source=' '(仅空白)也算未标注。"""
        p = _mk(self.root, "train/a.jsonl", '{"id": "t1"}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(p), size=1,
                  source="   ", license="internal-generated", split="train")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("来源" in q for q in r["quarantines"]), r["quarantines"])

    def test_wrong_size_detected(self):
        """A1: size 与实际不符必须报问题。"""
        p = _mk(self.root, "train/a.jsonl", '{"id": "t1"}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(p), size=999999,
                  source="x", license="internal-generated", split="train")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("size" in x for x in r["problems"]), r["problems"])

    def test_null_line_reported(self):
        """A1: JSONL 里的 null 行必须形成问题报告(不只内部标记)。"""
        p = _mk(self.root, "train/a.jsonl", '{"id": "t1"}\nnull\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(p), size=p.stat().st_size,
                  source="x", license="internal-generated", split="train")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("不是 JSON 对象" in x for x in r["problems"]),
                        r["problems"])


class TestA1Fields(unittest.TestCase):
    def test_empty_containers_missing(self):
        """A1: problem=[]/solution={} 空容器算缺失。"""
        bad = check_fields([{"id": "a", "problem": [], "solution": {},
                             "answer": "42"}],
                           required=["problem", "solution", "answer"])
        self.assertEqual(len(bad), 1)
        self.assertEqual(set(bad[0]["missing"]), {"problem", "solution"})


class TestA2NearDup(unittest.TestCase):
    def test_self_query_returns_one(self):
        """A2: 池子里的文本查自身必须返回 1.0(top20 截断曾致 0.042)。"""
        texts = [f"第 {i} 个几乎相同的长文本,主体内容一致,只是序号不同。"
                 "某工厂生产两种产品,甲产品每件利润3元,乙产品每件利润5元,"
                 "生产甲产品需要A材料2千克和B材料1千克,生产乙产品需要A材料"
                 "1千克和B材料3千克。现有A材料100千克、B材料120千克,"
                 "问两种产品各生产多少件利润最大。" for i in range(25)]
        idx = ShingleIndex()
        for i, t in enumerate(texts):
            idx.add(t, {"id": i})
        sim, hit = idx.max_sim(texts[21])
        self.assertAlmostEqual(sim, 1.0, places=6,
                               msg=f"第 21 个候选自身相似度 {sim} 而非 1.0")
        self.assertEqual(hit, {"id": 21})

    def test_exact_duplicate_among_many_found(self):
        """A2: 25 个候选里第 21 个与 query 完全相同时必须命中它。"""
        base = ("长文本题目:已知函数 f(x)=x^3-3x^2+2x+1,求函数在区间[-1,2]"
                "上的最大值与最小值,并说明在哪些点处取得,给出完整推理过程。")
        texts = [f"{base} 变体{i}。" for i in range(20)]
        dup = base + " 变体X。"
        texts.append(dup)
        idx = ShingleIndex()
        for i, t in enumerate(texts):
            idx.add(t, {"id": i})
        sim, hit = idx.max_sim(dup)
        self.assertAlmostEqual(sim, 1.0, places=6)
        self.assertEqual(hit["id"], 20)


if __name__ == "__main__":
    unittest.main()


class TestA1IdAndSource(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_source_none_quarantined(self):
        """A1 补:source=None(JSON null)不得经 str() 蒙混为非空。"""
        p = _mk(self.root, "train/a.jsonl", '{"id": "t1"}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(p),
                  size=p.stat().st_size, source=None,
                  license="internal-generated", split="train")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("来源" in q for q in r["quarantines"]), r)

    def test_blank_id_reported(self):
        """A1 补:id=' '(仅空白)必须形成问题报告。"""
        p = _mk(self.root, "train/a.jsonl", '{"id": "  "}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(p),
                  size=p.stat().st_size, source="x",
                  license="internal-generated", split="train")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("ID 非法" in x for x in r["problems"]), r["problems"])

    def test_nonscalar_id_no_typeerror(self):
        """A1 补:id=['x'] 或 dict 不得抛 TypeError,须可定位报告。"""
        p = _mk(self.root, "train/a.jsonl",
                '{"id": ["x"]}\n{"sample_id": {"v": 1}}\n{"id": true}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(p),
                  size=p.stat().st_size, source="x",
                  license="internal-generated", split="train")])
        r = validate_manifest(m, self.root)  # 不抛异常
        self.assertTrue(any("ID 非法" in x for x in r["problems"]), r["problems"])
        self.assertTrue(any("bool" in x for x in r["problems"]), r["problems"])
