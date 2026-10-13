# AppContainer 是否必须提权：本机实测结果

2026-10-04，项目提交 03eb5f2；使用已修复的 AppContainer 原生启动代码。

**结论：本机创建当前用户 AppContainer 配置并启动沙箱进程，不需要管理员提权。** 这不是对所有 Windows 管理操作的概括，也不表示完整渲染隔离已经验收。

用户已明确允许 C 盘普通用户目录写入，要求不危及系统文件。本次只新建随机命名的专用用户配置；没有请求 UAC、改变管理员令牌、修改系统文件、防火墙规则或原 Python/工具链目录权限。

## 实测证据

| 项目 | 实际结果 |
|---|---|
| 父进程 TokenElevation | False，普通权限 |
| CreateAppContainerProfile | HRESULT 0，创建成功，无 UAC |
| 系统 SID 与新配置 SID | 完全一致 |
| 同样代码普通进程运行 | 退出 0，连接本机监听端口成功，读取合成私有哨兵成功 |
| AppContainer 子进程运行 | 退出 0，TokenIsAppContainer=True，TokenElevation=False |
| 底层 _socket 本机 TCP 连接 | 沙箱内未连接，服务端没有接受到连接；未使用 Python socket shim |
| 未授权合成文件读取 | 拒绝，errno 13；没有读取实际用户敏感文件 |
| DeleteAppContainerProfile | HRESULT 0 |
| 清理复核 | 两个测试的专用 Packages 目录及 HKCU 映射均不存在 |

## 为什么之前失败

已独立定位的顺序是：

1. 旧代码把 HRESULT S_OK=0 当成失败，改用了错误 SID；此前的错误 4250 不能据此归因管理员权限。
2. 修正 SID 后，尚未创建 profile，配置查询及启动返回“找不到文件”。
3. 普通权限创建 profile 成功，但极简启动环境又触发 WinError 203（环境选项缺失）。
4. 补齐标准 Windows 用户环境，并将 LOCALAPPDATA/APPDATA 指向测试容器配置后，沙箱正常启动。此次测试没有进一步单独确定哪一个环境变量消除了 203，不能宣称只有某个单一变量必要。

微软将 [CreateAppContainerProfile](https://learn.microsoft.com/en-us/windows/win32/api/userenv/nf-userenv-createappcontainerprofile) 定义为当前用户的配置创建；其[启动流程](https://learn.microsoft.com/en-us/windows/win32/secauthz/implementing-an-appcontainer)包含创建 profile 和设置对应环境。文档支持诊断方向；“本机无需提权”的结论来自上述真实普通权限运行。

## 适用范围

本轮证明普通权限可完成配置创建和真实 AppContainer 进程启动，并取得本机 TCP/合成文件访问的正反对照。未验证外网、UDP、IPv6、子进程树、Manim/LaTeX/ffmpeg 完整渲染链和超时后的进程树终止。生产 exec_isolation 门禁仍保持阻断。

所有目录 ACL 调整仅在 D:/Animation-Model-Training/reviews/codex-supervision/history-from-code 下的独立 runtime/work 副本。C 盘的临时 profile 使用系统删除 API 清理，并核对 Packages 目录与 HKCU 映射消失。

证据：[成功测试结果](/D:/Animation-Model-Training/reviews/codex-supervision/history-from-code/elevation-test-2026-10-04/new-profile-result.json)、[极简环境失败对照](/D:/Animation-Model-Training/reviews/codex-supervision/history-from-code/elevation-test-2026-10-04/result-minimal-environment.json)、[清理核验](/D:/Animation-Model-Training/reviews/codex-supervision/history-from-code/elevation-test-2026-10-04/cleanup-verification.json)、[可重放脚本](/D:/Animation-Model-Training/reviews/codex-supervision/history-from-code/elevation-test-2026-10-04/probe_new_profile.py)。
