# 本机43点修复与独立复验

当前结果：**30 GREEN、0 FAIL、2 PARTIAL、11 GAP**，全43点尚未通过，生产门禁 **CLOSED**。用户已明确“暂无资源，先完成本机部分”；本轮已完成可用自有夹具下的修复、原生复验和本机资源就绪检查，余下13项保留待验证。

GREEN仅覆盖当前15项实现/runtime SHA绑定的注册夹具矩阵，不能扩为所有Windows对象、所有网络端点或未来代码。E3是边界文档验证，单独列出；没有签发生产证书，没有重新签署旧证据，没有开始训练或渲染/准入新资产。

## 已落地修复

- sandbox_execution.py 将生产证书契约升级至 production-appcontainer-v2：旧16项联合证据之外，必须重算完整43点且全部GREEN；旧v1证书或只改标签不能放行。15项绑定涵盖传输、ACL/Job、原生探针契约、当前收集器及宿主故障夹具。
- 新 full_surface_evidence.py 独立核对实际命令、执行源码、原始stdout/stderr、父token/profile、精确四个ACL授权根、stdio句柄白名单及当前实现SHA。明确将已知沙箱送达、访问宿主对象、宿主改变或异常继承判为FAIL，缺对照/协议矩阵判为PARTIAL/GAP。
- appcontainer.py 记录真实启动的stdio允许继承句柄数3。生产环境接入死代理配置及显式NETWORK_SHIM bootstrap，避免 -I 忽略sitecustomize后仍宣称Python防线已启用；渲染报告不再无条件声称network_isolated=True。Python拦截与OS隔离分别核对，非Python程序的结论需独立证据。
- 新 sandbox_surface_acceptance.py 默认仅PLAN，显式参数才执行具名自有夹具；保存新UUID原始记录、阶段检查点与源码前后绑定。补齐真实既有junction、原生Win32权限错误、TCP完整nonce接收器及存活IPC健康对照。新 host_cases.py 覆盖真实SID既有ACE冲突、跨宿主进程锁竞争、授权根及祖先junction拒绝、挂起进程的Job分配故障。
- 新 sandbox_remote_receiver.py 支持受控IPv4/IPv6 TCP、UDP、HTTP接收，不自动改防火墙；默认不监听，需显式--serve。记录完整载荷、准确nonce、来源、时间、源码SHA、日志SHA和接收器结束状态。

## 实际验证

46项相关回归通过，覆盖43点门禁、原有三门禁、AppContainer生命周期和Python网络防线。该回归在本轮已运行，独立核验记录注明控制台证据；没有伪造原始单测日志。

主验收8个真实AppContainer作业，另有真实宿主Windows故障/锁/授权夹具。父证据、每次独立profile与SID、零capability、四根临时ACL还原及profile存储清理均核对；执行源码与完整原始输出仍匹配当前15项绑定。内存压力实际返回rc17；超时案例由传输记录rc=-1，并用原进程HANDLE验证子、孙进程已结束，避免PID复用误判。

主原始记录：[surface-raw-c0ed19b0fad644a7ae76ffc4ba28e68b.json](surface-raw-c0ed19b0fad644a7ae76ffc4ba28e68b.json)。SHA256：
f399733c5ecbda4a51b537100c131d9d4c6c5da7554cdb1e86d93148fae58f4e。
[独立复验](independent-recheck.json)重算结果与原记录逐项一致。主控制器退出3表示验收未齐，不能改记为通过。

通过的注册点：A1–A9、B1–B5、C1–C7、D3–D6、E1–E3、F1、F3。其中包括当前回环TCP/UDP的IPv4/IPv6四条路径：三个不同精确nonce、宿主前后送达、沙箱nonce无送达、尝试结束后至少20秒观察。此证据不能代替外部或LAN路径。

匿名管道补测：真实自有匿名管道的读写两端保持存活，宿主同管道前后nonce读写健康；沙箱对两端HANDLE查询均得到STATUS_INVALID_HANDLE。额外原生作业完整传输绑定有效，F2仍因缺跨用户部分保持PARTIAL。见 [补测原记录](anonymous-pipe-f13bbfdb15d54ca3b74b3bd2b9e29659.json)。

接收器6项回环自测通过（TCP/UDP/HTTP × IPv4/IPv6），完整关闭且日志/源码SHA有效。发送者都是普通宿主进程，仅证明接收脚本可用，不是外部或沙箱隔离证据。

安全就绪检查：CreateWindowStationW使用三种访问掩码均返回Win5，未调用任何剪贴板API，原station/desktop保持；当前宿主token没有SeCreateGlobalPrivilege，Global mapping缺健康夹具。没有借此将F4/F5/F6标绿，也没有改UAC、账号、权限或用户当前剪贴板。

## 剩余13项

| 点 | 当前状态 | 完成所需证据/资源 |
|---|---|---|
| D1、D2 | GAP | 独立受控IPv4/IPv6 TCP端点及同协议端口的宿主前后nonce健康对照 |
| D7、D8 | GAP | 独立受控IPv4/IPv6 UDP端点及完整接收窗口；不能用TCP、DNS或另一地址族替代 |
| D9 | GAP | 另一台受控LAN主机，独立登记LAN路径/接口/子网与双端对照 |
| D10 | GAP | 新鲜随机DNS查询、缓存分离、受控DNS/完整出站采集和健康对照 |
| D11 | GAP | 实际执行的具名非Python程序网络矩阵及同协议健康接收端；缺程序/超时不算权限拒绝 |
| D12 | GAP | 受控原始socket/ICMP夹具，核对echo类型、ID、序号、完整nonce及双向健康通路 |
| D13 | GAP | WinHTTP和WinINET分别原生执行、相同协议端点健康对照及完整接收记录 |
| F2 | PARTIAL | 本地命名及匿名部分已有证据；仍需独立跨用户Windows管道健康夹具 |
| F4 | PARTIAL | Local已有证据；仍需有合法创建权限的宿主Global mapping存活健康夹具 |
| F5 | GAP | 合适的独立非交互window station/隔离Windows会话或VM，以合成剪贴板验证读、写及未改变 |
| F6 | GAP | 隔离Windows环境中隐藏窗口消息、原生全局hook各自健康夹具与权限结果 |

独立desktop不能隔离clipboard：clipboard属于window station，见 [Microsoft Window Stations](https://learn.microsoft.com/en-us/windows/win32/winstation/window-stations)。另一台校园设备可支持具名受控外部IPv6路径，但公共地址ping不能代替nonce投递；同一次跨网段IPv6实验不能重复当作独立LAN路径证明。D7需要独立IPv4 UDP对照，IPv6成功不能代替。

不存在“必须购买服务器/安装VM”的决定；用户当前选择先完成本机。资源未到位的项保留未通过。受托管父Job限制的进程不擅自breakaway或绕过限制；Windows对嵌套Job及UI限制有明确约束，见 [Microsoft Nested Jobs](https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs)。本机Win5只记录就绪不足，不推测全部根因。

## 历史、清理及监管

第一次本轮原生记录 surface-raw-e33d5765dc4645dda6aa4a8586f60198.json 保持原字节（SHA256 3a677ae7446469cc928d801383a54bb53bb1d11445c809b8f941fa2b8c1ec099）。其13项GREEN属于旧源码版本：句柄异常分类、Win32拒绝证明及TCP接收器问题已修正后重跑；旧结果不重新签署。

此前160项交付清单原字节保留。独立复验时仅检测到本轮实际修改的appcontainer、sandbox_execution，以及上轮已记载的枚举用词变化，其余157项仍匹配；net_guard按本轮START_PLAN另有修改前快照。当前状态文档和观察器随后更新，各自保存修改前版本和前后SHA。正式数据、原生历史JSON及旧清单未改写；旧20:05的CURRENT_STATUS.json仍是历史检查点。

两批C盘用户Temp自建UUID夹具已按绝对路径、直接父目录、普通文件及精确名单核验后逐文件删除，再移除空目录。没有递归删除，不跟随证据junction，不涉及系统文件；见 [清理记录](owned-temp-cleanup.json)。

只读观察器已将本目录及新核心工具加入监听，旧worker28164通过STOP正常退出，隐藏启动的新worker15492有新心跳，并拒跟随两个reparse链接。后台只记录，不自动AI审查、执行或准入。

新邮件597已通过Bridge598回复。正确UTF-8回执见 [mail-597-reply-598-utf8.json](mail-597-reply-598-utf8.json)；早期ASCII管道编码的中间落盘另保留并说明，不作为原邮件文本。完整交付及当前15项绑定见delivery-manifest.json，交接邮件回执和清单最终一致性检查按说明在清单生成后另存。
