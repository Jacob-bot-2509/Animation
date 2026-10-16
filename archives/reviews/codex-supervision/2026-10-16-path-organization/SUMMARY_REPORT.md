# 文件路径排查与整理报告

日期：2026-10-16（北京时间）。范围为 D:/Animation-Model-Training 及 D:/code 中关联的路径、导航和散落的 Animation 历史材料。

已完成路径整理与现行固定入口核验；这不是旧工具全部重放通过或训练验收。初始清单覆盖174095个文件、33558个目录，识别157个最外层冻结根。依赖/缓存目录记录位置后不展开，4个重解析点仅读取自身元数据、不进入目标，本轮审计输出不纳入自身目录清单。完整清单以压缩JSON保留。

## 本轮实际整理

- 无损迁移66份历史临时材料，共755452字节：D:/code/.bridge-poll 中51份审阅临时文件和1个真实保留名 NUL 文件、项目根5份临时结果、tools 中9份临时文件。全部保留大小与SHA256；NUL改为普通归档文件名 reserved-name-NUL.bin，原搜索报错已消除。
- 历史ACK共24个唯一报告绑定，原先10个旧路径缺失；从archives精确补回原字节兼容报告后，24个路径与原ACK哈希全部有效。原ACK及归档原件不改，未搬迁调度器。
- 更新现有的目录地图、环节入口、项目总览README，明确正式归档、当前运行根、固定读取兼容及MathGuide共享辅助目录的真实分工。没有批量替换历史原JSON或源码快照。
- 生成可查旧路径的PATH_INDEX.json、MOVED_FILES.md和LEGACY_PATH_REFERENCES.md；编辑前后快照与迁移映射随本报告保存。

[原 chunk13 文件的新位置](migrated/from-code-bridge-poll/_tmp_chunk13.txt) · [66件迁移清单](MOVED_FILES.md) · [机器路径索引](PATH_INDEX.json) · [ACK兼容恢复记录](ACK_REPORT_RESTORATION.json)

## 现行入口与边界

25个原具名兼容根、15个原生契约依赖、两项目Python解释器路径和数据清单的6个文件入口均核验。数据清单中的相对路径以清单所在data目录为基准，不误报为项目根缺文件。调度器、观察器源码、证人工具/配置及数据锁另有前后SHA保护记录。

可变现役Markdown的实际文件链接完成复核，cmd://等应用URI单独识别，不当成文件断链。初版扫描把历史备份、数学括号或应用协议列为候选的结果保留，但不据其直接修改档案。最终结果见[独立核验记录](FINAL_VERIFICATION.json)。

## 历史引用与资源账

静态扫描在67个工具/临时脚本里得到116处缺失字面量；110处有实际归档对应位置，已逐项建立定位索引。它们不是116次实际运行失败，其中还包括未来输出、可用备用浏览器候选及原本要求显式输入的路径。旧生成器的输入与写出位置必须区分，故本轮不将其一律替换为archives，也不为旧生成器签发可安全重放结论。已迁移的临时脚本保留原样，按历史材料查阅。

旧题源存在72处图片引用问题：30处定位到唯一现有图片，41处尚未找到同名文件，1处多候选。记录实际位置与SHA，未改原题文或生成假图片；详见[资源定位与缺口](historical-source-image-resolution.json)。未知项继续如实留账。

90条路径超过240字符，其中74条位于已声明冻结根；这是长度提示，不等于文件无法访问。4个重解析点均属冻结的历史安全测试材料，保留自身与目标说明，不删除或跟随。原件保护优先于缩短路径；清单见[长路径](long-paths.json)。

## 后续落点

业务代码与配置继续用src/tools/configs；数据与锁在data；新审查交付归archives/reviews/codex-supervision/<日期-主题>。reviews下活动运行根、冻结读取兼容及ACK报告副本有真实使用者，不整体清空。D:/code自身业务和共享协作脚本按其实际用途保留，Animation审查临时材料从本项目归档查询。

本轮没有提交或推送Git；没有运行历史生成器、实验、训练或打开门禁。文件定位与兼容入口通过不改变数学、独立盲标、全局隔离或生产资格。

## Final path verification

69 active Markdown file links: 0 broken. 73 links in new archive documents resolve. 277 named path/byte/guard checks passed; these are document and filesystem checks, not pipeline or mathematical acceptance tests. See FINAL_VERIFICATION.json.
