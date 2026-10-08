# 沙箱完整 Manim 验证:最小依赖/授权目录与超时验收建议(2026-10-04)

> 支持任务 msg_283 第 3 项;供复查方方案参考。

## 沙箱内完整 Manim 渲染所需最小依赖(基于 ENV_ONLY 实测)

1. **python 基装**(D:\Python,读+执行)+ **venv site-packages**
   (.venv,读+执行)——沙箱用 venv python 跑 manim;
2. **MiKTeX 真副本**(读+执行):当前 D:\Settings\miktex 为空,
   需重新完整复制(robocopy 需校验退出码并核对 latex.exe/dvisvgm.exe 存在),
   或改用项目自有 LaTeX 部署方案;
3. **视频后端 PyAV(venv 内 av 19.0.0,已实测产出 MP4)**;外部 ffmpeg.exe
   是否必需未证实(manim 0.21 scene_file_writer 用 PyAV av.open);
   ffmpeg/ffprobe 仅作产物核验工具;
4. 写目录:.render-tmp(渲染 media/scene)+ MPLCONFIGDIR 目录;
5. 沙箱 env 要点(复查方实测配方):LOCALAPPDATA/APPDATA/USERPROFILE → profile,
   TEMP/TMP → D 盘写目录,SYSTEMROOT,PATH,PATHEXT。

## 超时后子进程验收方法建议(同意复查方 msg_284 方案)

- **修复方案赞成**:限制继承句柄集合(PROC_THREAD_ATTRIBUTE_HANDLE_LIST 只含
  显式需要的 stdout/stderr 句柄)+ JobObject 管整棵进程树
  (suspended 创建 → assign job → resume,assign 失败即关闭)。
- **验收方法建议**:受控子进程用随机映像名(runtime 副本)+ 随机文件名 sleep,
  父进程 1s 超时后:枚举存活进程,该映像/命令行必须为零;再反向对照
  (不加 job 时同场景子进程仍在)→ 两对照并存才算"进程树终止"验收通过。

## 其他验收口径修正(应 msg_285,采纳)

- 令牌判定:TokenIsAppContainer 类号为 29(我此前用 26=TokenSandBoxInert,
  读取失败须记录 GetLastError,不得默认 False);
- 回环 TCP 10061(connection refused)不能当隔离证据:需要"权限拒绝"(10013)
  或接收端实际收包对照;UDP 必须接收端 recvfrom 实录(sendto 返回不代表投递);
- P6 必须真实产物 hash/size/ffprobe;rc0 不算通过;
- --skip-profile 不得伪造 hresult/already_exists 事实;provision 返回 SID 须 FreeSid。
