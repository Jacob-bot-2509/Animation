# 环境只读清点(2026-10-04,支持任务 msg_283 第 1 项)

只读采集,未修改任何 ACL/文件(除支持目录自身产物)。

| 项 | 值 |
|---|---|
| OS | Windows 11 Home 10.0.26200(本机) |
| Python(venv) | 3.13.13, D:\Animation-Model-Training\.venv |
| Python 基装 | D:\Python |
| manim | 0.21.0 |
| numpy / sympy | 2.5.3 / 1.14.0 |
| matplotlib | **缺失**(venv 内未安装;manim 基础渲染目前未用到) |
| ffmpeg / ffprobe | 9.0.2-essentials, D:\Settings\ffmpeg\bin(在 D 盘 ✓) |
| latex / dvisvgm | C 盘原装 MiKTeX(C:\Users\Jacap\AppData\Local\Programs\MiKTeX) |
| MiKTeX D 盘副本 | **不存在(空目录,0 字节)**——此前后台 robocopy 的"完成"报告有误,robocopy 退出码被误读;沙箱渲染链需要真正的 D 盘副本或明确依赖方案 |

## ENV_ONLY 冒烟(普通环境,标注 ENV_ONLY,不构成沙箱渲染通过)

- 场景 v1:固定可信 MathTex(r'x^2 + y^2 = 1') 仅 self.add(无 play/wait);
  rc=0,产物:PNG(5124 B, sha256 06d4effe…b377b8)+ Tex 中间产物
  (tex 253 B / svg 5913 B)。**无 MP4 的归因更正(应 msg_288)**:
  manim 0.21 对无动画场景按设计只出 PNG(cairo_renderer),与 ffmpeg PATH 无关;
  此前"无 MP4=PATH 无 ffmpeg"的因果断言错误,已撤回。
- 场景 v2(补证):加 self.play(Write(eq)) + self.wait(1), `-ql`;
  rc=0,**产出 MP4**:media2/videos/AcceptScene/480p15/AcceptScene.mp4
  (10916 B, sha256 f34242e7…,时长 2.000s,h264 854x480,30 帧,
  完整 ffprobe JSON 见 result-mp4.json)。
  视频后端为 **PyAV(venv 内 av 19.0.0)**,未证明需要外部 ffmpeg.exe。
- 证据:env-smoke/result.json、result-mp4.json(逐产物 sha256/size+完整 ffprobe)
