# 新邮件600/601审阅与证人接收器修复

ClaudeCode报告另一台校园网电脑172.30.192.202已运行证人程序，并提供IPv6地址2001:da8:2019:b282:c502:dd3f:3487:74fe；其IPv6与训练机同/64。这些是邮件报告，尚未取得该机正式双端原始证据。

邮件602已逐项回复：独立受控校园设备可以用于D9登记的LAN路径；同/64的地址不能重复当作D2/D8外部路径。外部点需要实际跨出所测LAN边界的对应地址族/协议受控接收端，不强制租云服务器。TCP连接成功或UDP发送成功都不能替代精确nonce接收。证人禁ICMP只表示D12健康通路缺失。

独立desktop不能隔离clipboard，后者属于window station。[Microsoft Window Stations](https://learn.microsoft.com/en-us/windows/win32/winstation/window-stations)明确其对象关系。独立desktop可成为隐藏窗口夹具的一部分，但窗口消息/hook的作用范围及健康对照仍需实际验证，见 [Microsoft Desktops](https://learn.microsoft.com/en-us/windows/win32/winstation/desktops)。VM是可选隔离环境，不要求必须装VirtualBox；本机CreateWindowStation三种掩码的Win5记录保持，未访问用户clipboard。

## 已直接修复

原tools/sandbox_witness_receiver.py存在TCP单次recv造成截断、UDP只收4096字节、工作线程启动失败仍总rc0、运行中仅内存日志、结束覆盖文件、吞掉异常、双栈设置失败忽略、没有实际执行源码/EXE身份及完整退出记录等缺陷。

新版本默认PLAN、不监听；显式--serve --bind --log才启动。接收窗口为20至900秒整数，默认300秒；IPv6固定IPv6-only，每个地址族另开新记录。两协议都绑定成功后才宣布LISTENING；部分启动失败关闭已开socket并返回2。TCP读取到EOF，保留分段、额外尾部和超时未完成载荷；UDP完整记录普通UDP最大载荷范围内的字节，原始十六进制保存，无UTF-8替换损失。

日志/summary以独占新建方式保留，不覆盖历史文件。逐事件记录整数UTC/monotonic时间、完整载荷、精确32位十六进制nonce和来源端点；异常、超时、提前结束、未关闭TCP或实现字节改变均不宣称完整观察。记录无效/额外载荷，后续记账不得只筛有效nonce然后宣称零命中。正常限时完成、监听器关闭且实现SHA未变，才rc0。接收器rc0只表示本次采集完整，不是沙箱隔离通过。

源程序身份绑定实际.py SHA；冻结EXE绑定实际运行EXE SHA。源码、打包过程和二进制的关系另有build-receipt.json，两端部署还需实测文件SHA一致。

## 验证与交付

10项针对性测试全部通过，完整stdout/stderr及命令见test-0dd5ef2ee903477aa32ff845866c62f7.driver.json。包括真实IPv4/IPv6的分段TCP、额外TCP尾部、5000字节非UTF-8 UDP、TCP读取超时、端口冲突及部分启动清理、提前结束、实现变更、日志/summary防覆盖和默认无监听。

新EXE已用本机现有PyInstaller生成，并在完整保留旧EXE后另存：

[release/witness_receiver_v2.exe](release/witness_receiver_v2.exe)

SHA256：d6887098ccd3b1c3b9bde1180746558b78d2b2882b3cbee25d791c5f792f1cad

当前源码SHA256：571f4ce31465a84147395abd9778845194ac591371234737ccf2abeebc6be75e

旧dist/witness_receiver.exe保持原字节，SHA256：23dce46db984e0182aa88917384893195bf99e2a1388a500b3616be5ae13cc78；另有原样副本。旧源码SHA256：2739f1daef84944c5c4ea50a08784c7f2f6d95f41b1d948562024d8aeadec76c。

新EXE默认PLAN实际rc3；EXE自测实际rc0，IPv4/IPv6 × TCP/UDP四条宿主回环路径收到精确nonce。每个采集器完整运行20秒，源EXE SHA及日志SHA独立核对，原始日志/summary保留。自测不属于LAN、外部节点或沙箱证据。

首次测试准备的命令行引号导致测试文件未写入，留下一个ImportERROR回执；该中间失败保留，不计入通过数。修正后上述10项实际测试通过，新EXE单独测试通过。

## 交给ClaudeCode的下一步

先正常结束旧证人，保存其旧日志，再把新EXE/源码复制到已获授权的证人机，核对SHA。以全新日志启动IPv4；IPv6以该机实际IPv6地址另跑，不以双栈假设替代。

[启动命令与原始证据要求](DEPLOYMENT.md)。在此具名LAN夹具、限时窗口和三个不同nonce范围内，可继续D9原生测试，不能触碰用户clipboard或签生产证书。回传完整双端记录后再独立复算；不修改当前15个生产绑定文件，不重新签署旧证据。

43点仍为30 GREEN、0 FAIL、2 PARTIAL、11 GAP，生产CLOSED。LAN设备“报告就位”不是验收通过，IPv6同网段不能填外部缺口。此前202项清单保持历史字节；本轮只读观察器源码及README是有修改前快照的两项预期变化，其余200项仍匹配，15项生产绑定不变。

观察器已纳入本目录和两个新源码文件；旧worker15492通过STOP正常结束，新隐藏worker35160有心跳。它只记录，不自动模型审查/执行/准入。详细字节清单见delivery-manifest.json，最终邮件回执和一致性检查按说明另存。
