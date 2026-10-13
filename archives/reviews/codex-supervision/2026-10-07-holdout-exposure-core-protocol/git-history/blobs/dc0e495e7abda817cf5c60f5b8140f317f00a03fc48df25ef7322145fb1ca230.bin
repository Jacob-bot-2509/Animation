# MiKTeX 只读盘点与 D 盘目标方案(2026-10-04,应 msg_323)

只读采集:未复制、未授权、未修改任何文件。

## 1. 源安装盘点(C 盘用户目录,非系统文件)

| 项 | 值 |
|---|---|
| 位置 | C:\Users\Jacap\AppData\Local\Programs\MiKTeX |
| 总大小 | 565 MB |
| 结构 | miktex/(271M,bin+x64/config 等)、tex/(61M)、bibtex/doc/dvipdfm/dvips/fontconfig/fontname/fonts/ghostscript/hunspell/makeindex/metafont/metapost/pdftex/scripts/source/tex4ht/tpm |
| latex.exe | miktex/bin/x64/latex.exe,2,716,672 B ✓ |
| dvisvgm.exe | miktex/bin/x64/dvisvgm.exe,5,593,088 B ✓ |
| config | miktex/config 含 tcx/ini 文件 ✓ |

## 2. D 盘空间

- D: 共 500G,可用 103G —— 565MB 副本无压力(约 0.6G)。

## 3. D 盘目标方案(待复查方批准后执行)

- 目标:`D:\Settings\miktex-real\`(新建,与现存空的 D:\Settings\miktex 区分;
  旧空目录留待复查方确认后清理)。
- 复制方式:robocopy `<src> <dst> /E /COPY:DAT /DCOPY:DAT /R:2 /W:2 /NFL /NDL /NP`,
  **退出码 0-7 为成功、≥8 为失败**(此前 0 字节事故即退出码误读,本次必须记录
  robocopy 退出码并逐项核对)。
- 复制后核验(普通环境,不授权、不进沙箱):
  1. 关键文件 sha256 清单:latex.exe、dvisvgm.exe、miktex/config/*.ini 抽样;
  2. `latex.exe --version`、`dvisvgm.exe --version` 冒烟;
  3. 最小 tex 编译冒烟(x^2+y^2=1 → dvi/svg)。
- 已知风险与待核点(不阻塞清单,列为执行时验证项):
  1. MiKTeX 用户安装依赖注册表定位根目录;纯副本可能找不到 texmf 根 →
     验证 `MIKTEX_PORTABLE=1` 环境变量下的纯副本自持性(官方便携模式),
     或核对副本内 miktex/config/miktex.ini 的根路径声明;
  2. 格式文件(pdflatex.fmt)按需生成,需可写 UserData 目录 → 沙箱内须
     绑定可写目录并设 MIKTEX_USERDATA 等环境变量(接线由复查方负责);
  3. 沙箱内 dvisvgm 可能依赖 fontconfig 缓存与 ghostscript 动态库 →
     随副本整体携带(清单已含 fontconfig/ghostscript 目录)。
- 我负责:以上复制与普通环境核验(获批后);**不**新增工具链授权、
  **不**启动沙箱渲染。复查方负责:沙箱 env 接线与最终复验。

## 4. 交接结论

- 依赖齐备(两个关键可执行均在)、空间充足、可复制性方案明确;
- 待复查方批准复制方案后执行;沙箱侧接线与复验按 msg_323 归复查方。
