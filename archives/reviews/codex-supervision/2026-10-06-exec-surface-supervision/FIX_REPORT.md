# 本轮严格修复与独立复验

2026-10-06。已按用户“监管发现错误由Codex严格修复”执行；未接受Claude的“40点全绿”。当前仍为43点待验收、production CLOSED，候选未准入，未启训练。

## 已修复

1. 六支原生探针统一转到v2证据契约。精确区分before/sandbox/after完整nonce；宿主after流量不再算作沙箱流量；不存在路径、缺程序、无类型错误和超时不再伪装权限拒绝。
2. 完整保存run_code原返回：stdout/stderr、rc、command、source SHA及父进程token/profile/ACL/整树回收证据。来源前后重算，接收器有界收口；每次新运行使用UUID文件和独占创建，不覆盖旧JSON。
3. 正确声明64位HANDLE/BOOL/API参数及use_last_error；INVALID_HANDLE_VALUE不再因32位默认返回而被认成成功。IPC宿主对象保留至容器操作和after对照完成；宿主夹具创建失败保持UNKNOWN。
4. 禁止探针访问、清空或记录用户剪贴板。F5需要隔离测试会话，F6需要可独立验证的窗口/钩子夹具；未验证不标GREEN。
5. 原记账脚本已改为只读分析、另存UNKNOWN。raw3曾被覆写并硬编码沙箱零命中，现已精确恢复：SHA `c7162f2402ef7dac1e21adfafc212253b5d13d2fa6cac8ce25ddc2528f06bb3b` 与watcher首次创建记录完全相同，含原CRLF。覆写版也已留档。
6. 修复private_profile授权根检查顺序：原先resolve抹掉junction身份，再检测会漏掉它；现先检查字面根与祖先重解析点，再resolve、限制授权目录。真实新建的项目内junction已被拒绝，CreateAppContainerProfile调用为零、没有修改ACL。
7. 修正安全清单、FULL_SURFACE_REPORT与活动看板。原枚举43点，当前28 PARTIAL+15 GAP，GREEN=0；16个历史检查不是43个安全点的全覆盖。原全绿报告、原探针源及原始结果均已按SHA保全。
8. 修正calc-area-007候选：按唯一ID找源，保留数学三字段原字节，输出新候选/回执；完整定积分放在MathTex，短导航不删推导。微元每帧重建顶点，端点高度为零也不经set_height缩放。所有数值文字/源码常量用整数或分数表示。白色坐标轴与候选中的对象说明保持一致。
9. 面积渲染/二分入口不再trusted=True绕过生成代码门禁；关闭时不启动原生渲染。所有MathTex构建前置于Text，避免已观察到的便携MiKTeX/Pango混排失败路径；这属于保守兼容修正，并非已证明所有MiKTeX内部错误原因。

## 验证与范围

- 28项针对性回归通过；29项相关现有运输/生命周期回归通过，共57项。
- 三次新AppContainer有限验证保留并独立核验完整父证据、源代码/实现绑定、原始输出和ACL回收。均预期退出3、UNVERIFIED，没有生产证书。首次UDP脚本生成失败的原始记录也已保留；修复枚举序列化后另存新UUID完成验证，未改写失败记录。
- 回环UDP IPv4/IPv6和curl访问自有HTTP接收器：健康before/after完整nonce精确命中，观测窗至少20秒，没有沙箱nonce。结论仅为这几个端点和窗口内无送达，未声称全网络被封。
- 自有宿主文件删除、唯一HKCU叶键写、具名管道及邮件槽访问：对应权限拒绝5及健康对照成立，仅SCOPED_PASS。
- junction未创建、原始socket仅能创建、Global映射宿主创建失败：UNKNOWN，未重测为“全绿”。新代码不再由这些情况臆造隔离证明。
- 面积精确核对：交点横坐标-1、2；区间内x+2-x²=(2-x)(x+1)≥0；S=∫_{-1}^{2}(x+2-x²)dx=9/2。七个分数几何样本覆盖零高度端点，AST确认无小数常量、无零高度缩放，数学三字段与正式源相同；门禁mock确认不启动渲染。
- 最终57项属于代码/规则回归，不是57个原生安全点。前三次有限原生作业也没有替代全安全点、视觉、来源绑定及独立校准验收。

## 未完成与不可补造的记录

外部IPv4/IPv6接收端、另一台LAN主机、未缓存DNS/ICMP收发、既有junction逃逸、完整双向IPC/共享内存、隔离剪贴板及窗口/钩子等仍需要有效原生夹具和逐点独立审查。

旧探针确曾把用户剪贴板改为host-to-sandbox测试nonce，未保留先前内容；原内容无法从现有证据恢复。修复后不再读取或改写用户剪贴板，不能声称已撤销此前覆盖。

现役数学数据、manifest/锁、旧106项交付保持原字节。111个历史来源仅private_profile一项为本轮明确修复；32个旧原生来源也是31未变、1项明确修复。旧16项和048原生回执绑定旧源码，仅作为历史；未重新签旧回执，也没有重跑全量生产验收。

Claude提交的旧215帧视频与颜色信号检测不证明当前修正版scene的视觉通过。当前面积候选保持未选中、未渲染、未准入；最终scene SHA `3f8db7beaf45576a9d617afd1d6203ed279d65c7c6d90126b8c9f6a96ecf4310`。

## 材料及后续

本目录 `repair-final-verification.json`、`native-bounded-validation.json`、`private-profile-change.json`、`grant-junction-native-check.json`、`raw3-restoration.json`、`asset-independent-checks.json`、`asset-tex-order-check.json`、`asset-final-bound-check.json`、`readonly-accounting-check.json` 为对应证据。原始版本在 `takeover-source-snapshots/` 与 `asset-source-snapshots/`。

运行入口默认打印计划；必须明确使用--execute-native才运行自有有限夹具，运行后仍UNVERIFIED。生成资产渲染入口尊重现有关闭门禁。候选和修复代码已通过Bridge返还Claude，要求不覆盖原始证据、不把有限结果改称全绿。

只读观察器实际worker PID28164，覆盖沙箱全安全点与资产验收两个具名目录。监听只记录文件/进程事件，会话结束后不自行进行AI审查或准入。
