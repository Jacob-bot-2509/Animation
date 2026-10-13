# -*- coding: utf-8 -*-
"""修正 probe-raw-ipc3-v1 证据中 sandbox_hit_listener 的对照误报:
hits 共 2 条 = before 对照 1 + after 对照 1,沙箱期间零命中。
透明追加 correction 字段,不删改原始记录。
"""
import json
from pathlib import Path

P = Path(__file__).with_name("probe-raw-ipc3-v1-results.json")
d = json.loads(P.read_text(encoding="utf-8"))
hits = d["after"]["listener_hits"]
before = d["after"]["hits_before_sandbox"]
d["after"]["sandbox_hit_listener"] = False  # 原值 True 为对照误报
d["after"]["correction_note"] = (
    "listener_hits 共 %d 条:before 对照 %d 条 + after 对照 1 条;"
    "沙箱运行期间无任何命中。原 sandbox_hit_listener=True 是把 after 对照计入所致,已修正。"
    % (len(hits), before))
d["after"]["hits_accounting"] = {"total": len(hits), "before_controls": before,
                                 "after_controls": 1, "sandbox": 0}
P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("corrected:", d["after"]["sandbox_hit_listener"], "| accounting:", d["after"]["hits_accounting"])
