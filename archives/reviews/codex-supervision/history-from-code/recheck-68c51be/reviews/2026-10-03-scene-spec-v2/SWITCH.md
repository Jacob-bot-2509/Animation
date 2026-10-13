# v1→v2 切换记录(2026-10-03,用户批准)

- 活动清单位置:data/manifest.json(覆盖 v1aw 与 v2\{eval,test},6 条目)
- 活动清单 sha256: b11def7be9027162f95a43726c403f81b7f0d54b25ce408418061896b63bf866
- v2 锁 data/{eval,test}-v2.lock.json 绑定活动清单(freeze_gate PASS)
- v1 数据/清单(data/v1/manifest.json,sha b4b61618…)/锁 data/*-v1.lock.json 全部保留归档,不作废
- data_check 活动清单 6 条目 0 问题;preflight data_manifest/freeze_gate PASS;全量 361+29 绿
- 此后 harness 审计活动版本:--base data/v2,活动清单 data/manifest.json(替代 data/v1/manifest.json)
