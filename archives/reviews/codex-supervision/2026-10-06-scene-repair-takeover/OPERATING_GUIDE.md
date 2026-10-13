# 新场景修订入口

输入：本目录 inputs-v2/inputs.json，20 个非空只读分块、264 条完整记录。records 每项为 idx、record、binding，题目内容在 record 内。

旧 reviews/2026-10-06-scene-standard-sweep/chunks 是恢复后的只读历史输入。不要清除保护后写回或重签旧清单。后续只返回具名补丁或写新输出目录。

补丁 records 每项需含 batch、id、expected_selected_path、expected_hash_algorithm、expected_selected_sha256、expected_selected_raw_sha256、expected_record_sha256、new_math_content_sha256、fields。fields 只能为 scene_spec，数学三字段不变。期望记录及结果数学 SHA 使用 sorted JSON 默认空格算法，不可混用 compact canonical SHA。范例见 scene-candidates-corrected-v4.json。

生成新输入：tools/split_scene_sweep.py --out 新目录，默认总数 264、分块 20。已有目录拒绝。
生成新候选：tools/stage_scene_patches.py，传 --drafts 活动草稿目录、--inputs inputs-v2、--patches 具名补丁、--out 未存在新目录、--version 新版本名。来源/输入/ID/前后 SHA 失败就拒绝。命令不切换 selector、不准入；输出的 draft-selection.candidate.json 不能当活动选择器。

实际文件：

- scene-candidates-reviewed-3-v2：三条重点修订的小批版本。
- scene-candidates-53-v4：53 条合并修订的实际版本，完整数学和视觉验收未完成。
- math-corrected-v1：47 条旧训练题新版本，修订 9 条，未准入。
- math-9-corrected.md：九题完整题目、过程、答案。
- workflow-evidence-analysis.json：90 条尚无候选的 REVISE ID。

不能直接拼接多个补丁文件。同一目标以最终 v4 文件为准。旧场景 publisher 对任意 scene_spec（含混合补丁）已关闭自动 selector 激活。

正式 selector、manifest、锁、资产及隔离门禁未切换。后续仍需独立数学/视觉、密度与独立校准验收。
