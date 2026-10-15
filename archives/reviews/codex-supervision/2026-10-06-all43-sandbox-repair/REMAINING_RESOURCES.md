# 外部资源接入与验收准备

当前用户安排：暂无资源，先完成本机部分。13项未通过保持原状态，具体矩阵见FIX_REPORT.md。

受控接收端须由使用方合法控制并允许此次测试。独立接收机保存原始JSONL、summary、stdout/stderr、运行命令、OS/地址/接口/路由信息与接收脚本SHA，不仅返回“零命中”汇总。

脚本默认PLAN，不开放监听。明确接收机实际本地地址、高端口、时长、自有输出目录后，才运行：
python -B tools/sandbox_remote_receiver.py --serve --bind <接收机实际地址> --protocol udp --port 39443 --seconds 300 --output <接收机自有输出目录>

每个地址族、协议、端口分别登记。使用三个各不相同的32位十六进制nonce区分before/sandbox/after；宿主在相同协议端点前后必须精确送达，沙箱尝试之后至少20秒完整观察，不能有无法归因的接收数据。外部节点及LAN节点条件不同，同一设备可以承载两套夹具，但须独立验证两条登记路径。

F2需要独立跨用户原生管道夹具，F4需要Global mapping合法创建权限及存活健康对照；不创建新用户或提权绕过政策。F5/F6需要合适的独立Windows隔离上下文；不触碰活动用户clipboard或桌面。资源到位后新增原始记录，按新源码绑定重新验证；旧证据不得重签。

接收器仅覆盖TCP/UDP/HTTP载荷。DNS、ICMP、WinHTTP/WinINET、非Python程序与UI/IPC仍需各自的具名夹具和原生对照；接收脚本可用不等于这些点已验收。
