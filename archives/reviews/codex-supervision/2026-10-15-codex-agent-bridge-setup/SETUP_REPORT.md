# codex-agent-bridge 接入记录

已安装 npm 包 codex-agent-bridge@1.1.0，MCP 服务名为 agent-bridge。Codex CLI 已确认 enabled=true；使用配置中的真实 command、args、cwd、env 完成 MCP initialize、tools/list 与 bridge_doctor 调用。

本次发现并处理了安装兼容问题：通过 npm exec 启动时，外层 npm 注入的脚本许可参数被内部 project-scoped install 拒绝（EALLOWSCRIPTS）。改用已下载同版本包的官方 Node 入口执行 setup 后成功；未修改第三方源码或放宽脚本许可设置。第一次失败日志和成功日志均保留。

安装位置：
- 运行时：C:/Users/Jacap/.agent-bridge/node_modules/codex-agent-bridge
- MCP 配置：C:/Users/Jacap/.codex/config.toml 中的 mcp_servers.agent-bridge
- Skill：C:/Users/Jacap/.codex/skills/agent-bridge/SKILL.md
- 安装包 registry integrity：sha512-27CBXvhsyUL5ujoDsi4arf9J3APA8FWJnqJIKU9MB07yMDBZ73teImNqHdJwrH1aONXubawQK2v+6QVy6I1D8Q==

验证结论：
- 原有配置项与两个既有 MCP 的解析后内容均保留。
- 配置使用本机 Node 和稳定安装路径，未指向 npm 缓存。
- 握手通过，16 个工具定义齐全。
- doctor 的 Node、Git、tsx、Windows Job Object 创建关闭、MCP 配置、Skill、worker-ready、项目 Git、孤立 worktree 检查通过。
- Claude ACP 适配器与凭据文件被检测到；本次未调用 Claude 模型，因此未验证实际登录或任务执行。
- DeepSeek Harness 未安装，不影响本次 Claude 接入。
- 项目没有 .agent-bridge/verify.json，后续任务的项目级独立验证规则尚未配置；安装自检通过不能替代任务代码验收。
- MCP initialize 的 serverInfo.version 被上游写死为 1.0.0；实际安装包和 doctor 版本均为 1.1.0，原样记录，不伪称二者一致。
- 当前已运行的 Codex 会话没有热加载新工具；需要重载 Codex 或新开会话，使原生 bridge_* 工具进入会话。当前实际握手使用独立 stdio 客户端完成。

本次仅执行安装与接入检查，启动工作任务数为 0。没有改动项目业务源码、旧邮箱调度器、训练或生产门禁。后续 apply/approve 具有 Git 副作用，应按用户当前任务权限执行。

上游：https://github.com/JaylanJerry/codex-agent-bridge
官方 Codex MCP 配置说明：https://learn.chatgpt.com/docs/extend/mcp?surface=cli
