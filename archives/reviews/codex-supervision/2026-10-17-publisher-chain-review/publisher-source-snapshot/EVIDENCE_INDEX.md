# OneDrive 通道验证证据索引(wjw-2026-10-17)

时间线(北京时间 2026-10-17 凌晨):
- 00:49 WJW 端 witness_pack.py --execute 成功(LOCAL_PUBLISHED)
- 00:50 交付包经 OneDrive 跨端同步到达本机 C:\Users\Jacap\OneDrive\witness
- 00:52 本机 witness_consumer.py --execute 消费回执 REGISTERED_RECONCILIATION_COMPLETE
- 01:10 WJW 侧实跑配置与打包回执经 OneDrive 回传归档

通道判定:按 Codex 口径(实际跨端 OneDrive 同步 + 消费回执)通道 PASS。
本轮为 lan-2026-10-13-a 旧轮回放,仅验证传输通道,不计新沙箱实验证据。

## 本目录证据(WJW 侧原件回传)

| 文件 | SHA-256 | 大小 |
|---|---|---|
| wjw-run-config.json | 22bc005e43edca687c9ea77e3b5e6d5703b5f0a17def905200e44828964c6e8a | 2014B |
| wjw-pack/publish-receipt.json | acb6480a279dded4b8f90ba866df8eb386461fed9b409389a72033620591b8f9 | 963B |
| wjw-pack/7d25d860…zip | 7d25d860a9cffb497f99e4e016c4228eab5b7aa5144e3c9ffac631b015efca6f | 4844B |

配置要点(实跑):kit 根=C:\witness\wjw-witness-kit,active=true,
sync_root=C:\Users\WJW\OneDrive\witness,sender_registry=[],production=CLOSED。

## 本机消费侧证据(主要)

job: reviews/witness-automation/jobs/job-e652263c33094648a5113e70dfa5adab
- SUMMARY.json / REPORT.md / PRECHECK.json / ADAPTER_INTENT.json /
  ADAPTER_RECEIPT.json / reconciled-1340170d…json / delivery-manifest.json / package.zip
- 状态:REGISTERED_RECONCILIATION_COMPLETE
- 身份:round=lan-2026-10-13-a,capture_id=e605e0ee…,receiver_run_id=f801046c…
- adapter:tcp/udp D9 记录,输入绑定 SHA 全匹配

交付包(OneDrive 传输原件,仍在同步目录):
7d25d860….zip / 7d25d860….ready.json

生产状态:production=CLOSED,full_surface_accepted=false,probe_emitted=false,
training_started=false,ipv6_D2_D8=GAP_DEFERRED_NONBLOCKING_PREPARATION。
