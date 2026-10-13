# 验收尝试期 ACL 变更盘点与恢复方案(2026-10-04)

> 应 msg_285 要求盘点;本文件只盘点与给方案,**不盲目改回**。
> 生产 profile(animtrain-render-sandbox,已获用户允许写 C 盘普通用户目录)
> 不在本方案的恢复范围。

## 变更来源

`tools/isolation_acceptance.py` 的 run_sandbox/allowed_dirs 在每次沙箱启动前对
下列目录调用 grant_dir_access(追加 AppContainer SID 的 ACE,继承传播):

| 目录 | 授予权限 | 状态 |
|---|---|---|
| D:\Python | 读+执行 | 原工具链目录,**本次被追加 ACE** |
| D:\Animation-Model-Training\.venv | 读+执行 | 原工具链目录,**被追加 ACE** |
| D:\Settings\ffmpeg\bin | 读+执行 | 原工具链目录,**被追加 ACE** |
| D:\Settings\miktex\miktex\bin | 读+执行 | 原目录(空副本),被追加 ACE |
| D:\Animation-Model-Training\.render-tmp | 读+写 | 本项目自建临时目录,可保留或随恢复一并移除 |

## 恢复方案(待复查方确认后执行)

1. 对上述前四个目录,用 SetEntriesInAclW 以 **REVOKE_ACCESS(mode 4)**
   移除 AppContainer SID 的 ACE(仅移除该 SID 的项,不动其他 ACE);
2. .render-tmp 属本项目临时目录:建议保留(沙箱渲染工作目录),或整体删除;
3. 执行前先对每个目录导出当前 DACL 快照(GetNamedSecurityInfo → SDDL)存档,
   恢复后再导出一次,两者对比为证据。

**当前状态:验收脚本已停止运行(不再触碰任何目录);恢复动作等复查方确认。**
