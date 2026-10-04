# MiKTeX 只读盘点与 D 盘目标方案 v2(2026-10-04,应 msg_323/330)

只读采集:未复制、未授权、未修改任何文件。v2 修正(应 msg_330):
撤回"MikTeX_PORTABLE=1 为官方便携模式"的无依据表述;修正 robocopy 退出码
口径;复制验收补完整清单要求。

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

- 目标:`D:\Settings\miktex-real\`(新建)。
- 复制:robocopy `<src> <dst> /E /COPY:DAT /DCOPY:DAT /R:2 /W:2 /NFL /NDL /NP`。
  **退出码口径(修正)**:退出码 <8 仅表示未报告复制失败;**5/6/7 仍可能含
  不匹配/额外项**(5=部分文件不匹配、6=存在额外文件/目录、7=不匹配+额外),
  不得仅凭退出码宣称复制成功或自持。
- **复制验收清单(必须逐项落证据)**:
  1. 源/目标完整相对路径清单 + 文件数 + 总字节数,源目标逐项一致;
  2. 关键文件 sha256 清单(latex.exe、dvisvgm.exe 及 texmf 抽样),源目标一致;
  3. 空目录与重解析点处理规则明确(robocopy 不复制 junction/reparse,
     目标不得含逃逸链接;空目录保留规则记录);
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
