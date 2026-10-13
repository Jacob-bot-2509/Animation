# 只读接收材料诊断

使用项目 venv 执行 inspect_receiver.py，显式提供 --sender、--receiver-log、--receiver-summary。只有取得真实证人退出码后才传 --receiver-rc；未取得时省略，由诊断记录缺失，不能填假 0。

脚本 stdout 为诊断 JSON，拒收 rc=2；无初筛问题为 READY_FOR_REGISTERED_RECONCILIATION / rc=0，只表示可进入注册对账，不代表原生验收通过。用新文件名保存 stdout；原始文件保持原字节。

当前 run 的例子（未取得证人实际 rc，因此本例省略）：

    .venv/Scripts/python.exe -X utf8 -B reviews/codex-supervision/2026-10-08-lan-receiver-review/inspect_receiver.py --sender reviews/codex-supervision/2026-10-06-all43-sandbox-repair/external-tests/remote-271e1c881c4f473fb027f5f28d4a3bd5/sender.json --receiver-log reviews/codex-supervision/2026-10-06-all43-sandbox-repair/external-tests/remote-271e1c881c4f473fb027f5f28d4a3bd5/receiver/witness_new_01.jsonl --receiver-summary reviews/codex-supervision/2026-10-06-all43-sandbox-repair/external-tests/remote-271e1c881c4f473fb027f5f28d4a3bd5/receiver/witness_new_01.jsonl.summary.json

修复方式是取得未改字节原件，或在原实验无有效对照时另起唯一新轮。不要修改旧文件字段来通过。
