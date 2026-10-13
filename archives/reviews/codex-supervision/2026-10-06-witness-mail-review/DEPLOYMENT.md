# 证人机启动与正式测试要求

将release/witness_receiver_v2.exe复制到另一台获授权设备，先核对SHA256：
d6887098ccd3b1c3b9bde1180746558b78d2b2882b3cbee25d791c5f792f1cad

源码SHA256：571f4ce31465a84147395abd9778845194ac591371234737ccf2abeebc6be75e。
旧程序/EXE/日志保留，不混入新证据。默认双击仅PLAN；需要显式参数启动。下面的日志名必须是该次新建的唯一文件。

IPv4示例（在证人机自有目录，PowerShell）：

~~~powershell
$id = [guid]::NewGuid().ToString('N')
.\witness_receiver_v2.exe --serve --bind 172.30.192.202 --udp-port 49001 --tcp-port 49002 --seconds 300 --log ".\witness-v2-v4-$id.jsonl"
~~~

IPv6另开一次（地址需确实属于该证人；同/64仍是LAN路径）：

~~~powershell
$id = [guid]::NewGuid().ToString('N')
.\witness_receiver_v2.exe --serve --bind 2001:da8:2019:b282:c502:dd3f:3487:74fe --udp-port 49001 --tcp-port 49002 --seconds 300 --log ".\witness-v2-v6-$id.jsonl"
~~~

运行前须正常退出占用同端口的旧证人并保留旧日志。程序不改防火墙、账号或ACL。IPv6固定IPv6-only，IPv4/IPv6不可互相替代。

LISTENING出现后才能开始探针。每个实际登记的协议/地址族使用不同的before/sandbox/after三个32位十六进制nonce；宿主前后必须在相同端点精确收到载荷。TCP发送完整nonce后正常关闭发送端；连接通不能代替载荷健康。沙箱尝试完后至少20秒完整观察且after在该窗口内；不能提前结束程序后声称完整窗口。接收窗口不足则新增一轮唯一记录。

按本轮D9校园LAN夹具范围执行。IPv4地址/IPv6地址、TCP/UDP分别报告覆盖；原始记录中的所有payload都要归因，不能忽略nonce为null、重复或无法解释的记录。接收器rc0只代表采集完整。

回传两端主机独立身份、OS、接口/地址/掩码与路由、真实命令、源码与EXE SHA、运行前后SHA、原始stdout/stderr和实际rc；证人机JSONL及summary必须完整并核对log_sha256；训练机保留AppContainer原始传输、执行代码、父token/profile/四根ACL还原及当前15项实现绑定。收到后独立验收，D9才可更新状态。

外部IPv4/IPv6、DNS、ICMP、非Python、WinHTTP/WinINET仍按各自矩阵验证。LAN不能重复填外部缺口。F5/F6保持未验证，不访问活动用户clipboard或桌面；没有新采购/VM安装授权，生产门禁保持CLOSED。
