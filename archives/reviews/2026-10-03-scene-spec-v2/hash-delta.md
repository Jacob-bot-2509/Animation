# v1→v2 差异对照(2026-10-03)

| 文件 | v1 sha256(前16) | v2 sha256(前16) |
|---|---|---|
| data/v1/eval/dataset_eval.jsonl | 9e5b7355606dc65b | 8ff7044a0c48f348 |
| data/v1/test/dataset_test.jsonl | e1ba1eb49dd7df49 | d4de0bb6a86ff0ae |

eval 变更记录数: 300/300
test 变更记录数: 150/150

eval 变更类型:
- scene_spec 逐解法重写(300 条)
- solution 自包含修正(eval-linalg-023-s3)
- efficiency_tags 修正 Markdown 前缀残留(随场景重写一并)

test 变更类型:
- scene_spec/efficiency_tags 前缀清理
变更明细(前20条):
- eval-calc-001-s1
- eval-calc-001-s2
- eval-calc-001-s3
- eval-calc-002-s1
- eval-calc-002-s2
- eval-calc-002-s3
- eval-calc-003-s1
- eval-calc-003-s2
- eval-calc-003-s3
- eval-calc-004-s1
- eval-calc-004-s2
- eval-calc-004-s3
- eval-calc-005-s1
- eval-calc-005-s2
- eval-calc-005-s3
- eval-calc-006-s1
- eval-calc-006-s2
- eval-calc-006-s3
- eval-calc-007-s1
- eval-calc-007-s2
