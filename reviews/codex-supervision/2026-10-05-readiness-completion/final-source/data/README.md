# 数据目录与命令契约

实际数据使用独立版本目录，例如 data/v1/，其中包含 raw/、train/、eval/、test/。原始数据只读；评测集需要冻结锁（验收要求，当前尚未完整实现）。reviews/ 是合成审查证据，不参与训练。

## 登记与校验

每个文件一条 manifest entry：path、sha256、size、source、license、split、notes。path 相对清单所在目录；SHA256/size 应来自真实文件。许可证必须来自实际授权，internal-generated 只适用于有依据的内部生成数据。

make_manifest 的 --out 必须位于 --dir 根目录，默认拒绝覆盖且不提供 --force。使用新的版本目录保留历史清单。扫描按首层 raw/train/eval/test 目录推断角色，当前还会登记其他文件；应人工核对，不能把生成清单当验收通过。

以下来源和许可证文本须替换为已确认的真实值，再执行：

```powershell
python tools/make_manifest.py --dir data/v1 --out data/v1/manifest.json --name animation-data-v1 --source "填写真实来源" --license "填写已确认的许可证标识"
python tools/data_check.py --manifest data/v1/manifest.json
```

缺来源或许可证会阻断；当前许可策略见 src/animtrain/manifest.py。白名单识别并不证明实际授权成立。不要为了通过检查而填写任意标识。

## 拆分数据

split_data 的 plan 显式列出 train/eval/test ID，输出为平铺 JSONL，并自带标准 split_manifest.json。直接校验此清单；不要用 scan 重新猜平铺文件的 split，否则会标记为 raw。--license 未提供时保持空值并 quarantine，不自动推定内部生成。

```powershell
python tools/split_data.py --pool data/v1/pool.jsonl --plan data/v1/plan.json --out data/v1/split --license "填写已确认的许可证标识"
python tools/data_check.py --manifest data/v1/split/split_manifest.json
```

--force 也不能覆盖输入 pool/plan，但冻结输出锁、原子发布及空 split 策略仍待完善。来源混合时不能用单一许可证替代逐来源证据。

## 结果与后续门禁

- data_check --manifest 与 --scan、--dry-run 三选一；缺失目录和空输入失败。
- --near-dup-threshold 仅接受 [0,1] 的有限数值；统计阈值仍需实际校准。
- --dry-run 仅显示 schema 说明，没有执行数据检查。
- 数据 CLI：0=本次检查通过，1=失败，2=quarantine 或参数错误。保留具体报告才能解释退出码。
- core 字段和静态代码需分别通过 check_fields/check_code；数据门禁成功并不代表 L3–L7 全通过。
- JSONL 字段类型、合法多行 JSON、默认运行记录清单路径等剩余缺口见 reviews/2026-09-30-round2/REVIEW.md，之后修复以新审查结论为准。

当前没有已批准进入训练的数据集。


## 当前活动训练版本（2026-10-05）

以 data/manifest.json 为准。用户确认同核心结构仅换数值的题按泄漏隔离后，活动训练切换为 data/v2/train/leakage-isolated-v2-2026-10-05/，共48条；eval仍300条、test仍150条。原v1与中间版本保留归档，15条训练隔离记录及双锁绑定历史见 reviews/codex-supervision/2026-10-05-readiness-completion/READINESS_REPORT.md。数据入口 clean 不等于训练就绪，结构检测器校准和逐条资产验收仍未通过。

跨集合候选普查使用 tools/leakage_population.py，默认含不同签名，不自动赋标签或校准。可信模板沙箱试点使用 tools/sandbox_render_pilot.py，真实媒体完整解码；数学/动画语义仍需逐条独立验收。
