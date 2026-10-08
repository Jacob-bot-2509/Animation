# 邮件622补交材料审阅

本轮收到224、225两封历史邮件完整摘录，核对了选择器快照与16个归一化文件绑定，并修正最新发布说明中的证据口径和网络缺口数量。历史字节缺口仍为36项；没有进一步恢复缺失原件，也没有新增题目或启动实验。

## 历史邮件及哈希补正

来信622所报摘录SHA为63446c4e638c72dd06065db045dd3d6630af6d2f1e4c78a3f8f4573f7197265e，磁盘文件实际4371字节、raw SHA为d8bf8875f7852fa248fc1ec5d2444b22ed6e7008a3a88ef9e3458b139a7ee8bc。去掉末尾恰好一个LF字节，4370字节才命中所报SHA。差异已精确定位；没有把归一化值冒充现存原始字节哈希。

已保存现存文件原字节、独立补正记录excerpt-HASH_AMENDMENT.json和来信原文，未改原文件或旧邮件。摘录还与提交556de4257aa01ec8d8ec6f4ffd004bfd58287cbe的JSON内容一致。

两封摘录均包含id/from/to/type/timestamp/read/content全部字段，发送者Codex、接收者Claude Code；时间与消息ID中的毫秒时间精确一致：

- 224：2026-10-03 14:00:09.428（北京时间），type=review。
- 225：2026-10-03 14:05:11.447（北京时间），type=review_result。

Claude声明从本机Bridge state.json仅提取这两条；本轮只读取所提交摘录，没有读取整份Bridge状态或其他会话。摘录中的提交5f4fef6、9ce2766、c88c128均存在，时间顺序与审查叙述一致。旧reviews/2026-10-03-shootout-review/results.json的head确为9ce2766，执行范围记为mock-only及本地tokenizer只读测量。

## 邮件可以证明的范围

224提出推理种子、完整输出、精确seq_len、版本覆盖和资源探针授权等待修问题；225要求正式比较前修正，并明确撤走临时组前归档完整prompt/input/output/hash、模型来源、环境与命令。

这两封是历史审查记录，不能作为实际筛选运行的输入、输出、样本清单或随后执行批准收据。225还明确当时“未加载模型权重、未推理、未训练”，所以不能以该审查复验代替之后的模型筛选运行。

Claude在622如实确认：除已有screening-cleanup-manifest.json外，没有其他原删除命令归档收据。已记录此限制，本轮没有再要求其提交同一不存在的删除收据，也没有推定具体删除操作者。缺少旧内容时继续按完整任务范围及角色访问依据判断；清理用途记录与候选资格分开。

## 选择器与归一化核对

Claude指定的harness-strict-fix/before选择器快照SHA为6cadccf0cf60ad2eca80ed3fa20ecc3b13b1f1ea016f506a21da2e7690cdfe25，与当前schema2选择器字节全同，选用264条记录。它不是缺失目标旧版本5b3ecb92dff6505d25dfc628d2448bfbc0388a281331f95bb059c0aadeb4b87a。

draft-hash-compatibility/before.json记录直接迁移前件c30e68c13eeeec8c0d9e48a5e1e7f89b39711101abaefbd64d782f12c312208b；此关系与之前已核验的迁移记录一致。旧5b3e版本、直接前件c30e版本、当前6cad版本是三个不同绑定，不能互相替代。

delivery-batch01-08-normalized.json保留旧选择器SHA引用，并提供8个后继JSONL、8个报告的raw与归一化SHA。本轮16组均验证通过。算法为UTF-8-sig解码、splitlines、LF连接、不给末行加LF；保留raw SHA与文本指纹各自用途。它说明现存后继版本的格式关系，不恢复8个旧版本或旧选择器的具体内容。

## 发布说明修正

最新提交288b4be更新NEWRELEASE.md，本轮只修正四处与当前证据有关的表述，保留修改前字节、修改后副本及逐项替换记录：

1. 391明确为候选池；初次零精确重叠限定为当时297条参照，完整历史同题/同核心隔离与逐角色曝光仍PENDING，合格数UNKNOWN。
2. 区分设计/规则预注册与尚未落实的独立人员，明确关联判定、抽样、标注、校准、最终验证尚未执行；75739文件复核仅是已捕获字节匹配，补写36项历史缺口及两项精确重建。
3. 将“全部证据SHA绑定”改为具名交付物按实际字节绑定，并保留历史缺口、失败与哈希声明差异的独立记录。
4. 根据已冻结的ipv4-joint-policy注册矩阵，网络GAP是9项：D1、D2、D7、D8、D9、D10、D11、D12、D13；加F5/F6共11个GAP。F2/F4是2个PARTIAL，总体30 GREEN、0 FAIL、2 PARTIAL、11 GAP。不是10个网络缺口。

修改后NEWRELEASE.md SHA为5845c02f417c60b0b558ee232000e0e721f306166f691cc3b2824876e0c44cb1。它仍为Pre-release，生产CLOSED。本轮没有以文档修正替代原生实验或扩大注册矩阵的通过范围；发布说明中其他逐题/视觉结果继续按原交付记录理解，本轮范围见release-corrections.json。

## 当前状态与后续依据

- 224/225摘录已收到，按实际字节SHA补正绑定。
- 历史字节缺口36项；原始38项快照及后续两项重建证据保全。
- 391候选的合格数量UNKNOWN，核心判定0，校准UNCALIBRATED。
- 沙箱实验仍安排2026-10-08北京时间，本轮未启动。
- 后续若找到精确原件或足够完整的历史内容/角色证据，按实际新增材料更新；不以邮件、用途摘要或后继快照直接标候选UNEXPOSED。

文件入口：excerpt-HASH_AMENDMENT.json、historical-mail-review.json、selector-and-normalized-binding-review.json、release-corrections.json、source-bindings.json及sources/原字节快照。
