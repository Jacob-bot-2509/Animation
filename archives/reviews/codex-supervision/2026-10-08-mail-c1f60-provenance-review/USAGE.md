# 当前只读诊断版本

当前脚本为本目录 inspect_receiver.py；冻结旧版本留作历史。输入参数保持 --sender、--receiver-log、--receiver-summary，真实 rc 取得后才给 --receiver-rc。

新版本修正 closed 生命周期时间语义：closed 可在 finished 后写入；payload / listening 仍须在窗口内。rc=2 表示材料拒收，rc=0 / READY_FOR_REGISTERED_RECONCILIATION 只代表可以进入既有注册对账，不是双端通过。

新版本有10项本地合成验证；当前材料仍有端点、健康对照、真实rc三项缺失。不要修改原证据以适配检查。
