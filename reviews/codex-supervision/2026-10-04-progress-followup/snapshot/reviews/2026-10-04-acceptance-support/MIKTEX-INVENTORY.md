# MiKTeX 只读盘点与 D 盘目标方案 v3(2026-10-04,应 msg_323/330/342)

只读采集:未复制、未授权、未修改任何文件。v3 修正(应 msg_342):
复制命令显式加 /XJ(官方默认**包含** junction,先前"不复制 junction"表述
与官方口径冲突);SHA 核验改为**全量文件**(非关键文件+抽样);目标改项目内
具名目录。

## 1. 源安装盘点(C 盘用户目录,非系统文件)

| 项 | 值 |
|---|---|
| 位置 | C:\Users\Jacap\AppData\Local\Programs\MiKTeX |
| 总大小 | 565 MB |
| 结构 | miktex/(271M,bin/x64+config)、tex/(61M)、bibtex/doc/dvipdfm/dvips/fontconfig/fontname/fonts/ghostscript/hunspell/makeindex/metafont/metapost/pdftex/scripts/source/tex4ht/tpm |
| latex.exe | miktex/bin/x64/latex.exe,2,716,672 B ✓ |
| dvisvgm.exe | miktex/bin/x64/dvisvgm.exe,5,593,088 B ✓ |

## 2. D 盘空间

- 复查方实测 109,618,438,144 B(约 102.1 GiB)可用 —— 空间不是卡点。

## 3. D 盘目标方案(待复查方批准后执行)

- 目标:`D:\Animation-Model-Training\.sandbox-runtime\miktex-real\`(项目内
  具名目录,新建;旧 D:\Settings\miktex 空目录留待复查方确认后清理)。
- 复制:robocopy `<src> <dst> /E /COPY:DAT /DCOPY:DAT /R:2 /W:2 /NFL /NDL /NP /XJ`。
  **/XJ 说明(修正)**:官方文档规定 junction 默认**包含**在复制中,
  必须显式 /XJ 排除;目标目录不得含任何 reparse/junction 逃逸链接。
  **退出码口径**:退出码 <8 仅表示未报告复制失败;**5/6/7 仍可能含
  不匹配/额外项**(5=部分文件不匹配、6=存在额外文件/目录、7=不匹配+额外),
  不得仅凭退出码宣称复制成功或自持。
- **复制验收清单(必须逐项落证据)**:
  1. 源/目标完整相对路径清单 + 文件数 + 总字节数,源目标逐项一致;
  2. **全量文件 sha256 清单**(源与目标逐文件比对,非抽样);
  3. 重解析点处理:/XJ 排除后源内 junction 清单单独记录并核对
     目标确无重解析点;空目录保留规则记录;
  4. 普通环境冒烟:latex.exe --version、dvisvgm.exe --version、
     最小 tex 编译(x^2+y^2=1 → dvi/svg),输出与缓存目录**限定 D 盘**,
     **禁止自动拉包**(禁联网自动安装缺失宏包,所需宏包须在源安装内已存在,
     或列为缺项上报);
  5. 以上全部通过才称"普通环境副本可用";沙箱侧接线与复验按分工归复查方。

## 4. 自持性依据(修正:一律未验证,待实测)

- 之前把 MIKTEX_PORTABLE=1 标为"官方便携模式"**无依据,已撤回**:
  MiKTeX 官方便携版说明(https://miktex.org/howto/portable-edition)描述的是
  便携安装器/启动脚本;官方环境变量手册(https://docs.miktex.org/manual/envvars.html)
  **未列出** MIKTEX_PORTABLE,亦未列出 MIKTEX_USERDATA。
- 普通用户安装目录纯复制后是否自持(不依赖注册表/用户配置定位 texmf 根、
  格式文件与字体缓存来源)**未验证**;执行时需以本机安装版本支持的参数/配置
  实测为准(source install / user-config / user-data / package roots、
  fmt/font/ghostscript 依赖边界逐项核实),并记录依据。
- 结论:依赖齐备、空间充足、复制方案与验收清单明确;自持性一律待实测,
  不凭两个 exe+抽样 ini+退出码宣称。

## 5. 交接结论

- 待复查方批准复制方案后,我执行复制 + 上述清单核验(普通环境,输出限定
  D 盘,禁自动拉包);沙箱 env 接线与最终复验按 msg_323 归复查方。
