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

- 场景:固定可信 MathTex(r'x^2 + y^2 = 1'), `-ql`;
- rc=0,产物:
  - PNG: media/images/AcceptScene/AcceptScene_ManimCE_v0.21.0.png
    (5124 B, sha256 06d4effe…b377b8)
  - Tex 中间产物: media/Tex/e044e500b9ee7c8a.{tex,svg}
    (tex 253 B / svg 5913 B,sha 见 result.json)
  - **无 MP4**:普通环境 PATH 未含 D:\Settings\ffmpeg\bin → manim 未产出视频;
    沙箱 env 必须显式把该目录加入 PATH
- 证据:env-smoke/result.json(含逐产物 sha256/size/ffprobe)
