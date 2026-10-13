# OS 级网络隔离(AppContainer)尝试记录

> 2026-10-03。结论:**本机被系统拒绝,机制未启用**;网络隔离保持
> UNVERIFIED,exec_isolation 门禁保持阻断(如实,不假绿)。

## 尝试内容

1. 机制层 `src/animtrain/appcontainer.py`(完整实现):
   - SID 派生:优先 `DeriveAppContainerSidFromAppContainerName`
     (userenv 导出,本机调用返回 FALSE 且不设错误 → Home 版 stub);
     回退哈希派生 `S-1-15-2-{SHA256(名称 UTF-16LE)[0:16] 四个小端 DWORD}`;
   - ACL 授权:`SetEntriesInAclW`(TRUSTEE_IS_SID 需二进制 SID 指针,
     实测修正)+ `SetNamedSecurityInfoW` 在自有 D 盘目录追加 ACE;
   - 启动:`STARTUPINFOEX` + `PROC_THREAD_ATTRIBUTE_SECURITY_CAPABILITIES`。
2. 工具链准备:MiKTeX 复制至 `D:\Settings\miktex`(ffmpeg 已在 D 盘、
   python 基装在 D:\Python,均无需动 C 盘)。
3. 探针测试 `tests/test_appcontainer.py`(原版,现改为如实 SKIP):
   - 沙箱内 python 运行/读授权目录;
   - 沙箱内底层 `_socket.connect` 到本机监听端口必须被 OS 拒绝;
   - 未授权路径不可读。

## 实测结果

- `CreateProcessW` 携带 AppContainer 属性,**固定低盒 SID 与哈希派生
  SID 均返回错误 4250**:"此操作仅在应用容器上下文有效";
- 无管理员条件下,本机(Windows 11 Home 26200)拒绝创建 AppContainer
  子进程。

## 结论与出路

- OS 级网络隔离在本机**需要管理员路线**:一次性防火墙出站规则
  (netsh advfirewall,按沙箱 python 程序阻断)或 AppContainer profile
  创建(需提权)。机制层代码保留,管理员授权后即可启用并复跑探针。
- 在此之前:network_isolation=False、python_socket_guard(best-effort,
  msg_259 实测可绕过)、exec_isolation 门禁如实阻断、不可信代码执行拒绝。
