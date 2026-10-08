def token_identity(process_handle=None) -> dict:
    """Query a real process token; default is the calling process.

    A parent may pass the suspended child handle before any user code runs.
    """
    import ctypes
    from ctypes import wintypes
    result = {"api_ok": False, "is_appcontainer": None, "capability_count": None, "sid": None}
    handle = wintypes.HANDLE()
    try:
        k = ctypes.WinDLL("kernel32", use_last_error=True)
        a = ctypes.WinDLL("advapi32", use_last_error=True)
        k.GetCurrentProcess.restype = wintypes.HANDLE
        k.CloseHandle.argtypes = [wintypes.HANDLE]
        k.CloseHandle.restype = wintypes.BOOL
        a.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
        a.OpenProcessToken.restype = wintypes.BOOL
        a.GetTokenInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID,
                                         wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
        a.GetTokenInformation.restype = wintypes.BOOL
        a.ConvertSidToStringSidW.argtypes = [wintypes.LPVOID, ctypes.POINTER(wintypes.LPWSTR)]
        a.ConvertSidToStringSidW.restype = wintypes.BOOL
        k.LocalFree.argtypes = [wintypes.LPVOID]
        k.LocalFree.restype = wintypes.LPVOID
        if not a.OpenProcessToken(k.GetCurrentProcess() if process_handle is None else process_handle, 8, ctypes.byref(handle)):
            raise ctypes.WinError(ctypes.get_last_error())
        needed = wintypes.DWORD()
        value = wintypes.DWORD()
        if not a.GetTokenInformation(handle, 29, ctypes.byref(value), ctypes.sizeof(value), ctypes.byref(needed)):
            raise ctypes.WinError(ctypes.get_last_error())
        result["is_appcontainer"] = bool(value.value)
        if not a.GetTokenInformation(handle, 30, None, 0, ctypes.byref(needed)):
            error = ctypes.get_last_error()
            if error != 122:  # ERROR_INSUFFICIENT_BUFFER is expected for the size query.
                raise ctypes.WinError(error)
        if needed.value < ctypes.sizeof(wintypes.DWORD):
            raise ValueError("Invalid TokenCapabilities size")
        buffer = ctypes.create_string_buffer(needed.value)
        if not a.GetTokenInformation(handle, 30, buffer, len(buffer), ctypes.byref(needed)):
            raise ctypes.WinError(ctypes.get_last_error())
        result["capability_count"] = ctypes.cast(buffer, ctypes.POINTER(wintypes.DWORD)).contents.value
        if not a.GetTokenInformation(handle, 31, None, 0, ctypes.byref(needed)):
            error = ctypes.get_last_error()
            if error != 122:
                raise ctypes.WinError(error)
        # TokenAppContainerSid contains a pointer into the supplied information buffer.
        # Allocate the entire returned buffer and convert while it is alive.
        if needed.value < ctypes.sizeof(wintypes.LPVOID):
            raise ValueError("Invalid TokenAppContainerSid size")
        buffer31 = ctypes.create_string_buffer(needed.value)
        if not a.GetTokenInformation(handle, 31, buffer31, len(buffer31), ctypes.byref(needed)):
            raise ctypes.WinError(ctypes.get_last_error())
        sidptr = ctypes.cast(buffer31, ctypes.POINTER(wintypes.LPVOID)).contents
        if sidptr.value:
            text = wintypes.LPWSTR()
            if not a.ConvertSidToStringSidW(sidptr, ctypes.byref(text)):
                raise ctypes.WinError(ctypes.get_last_error())
            try:
                result["sid"] = text.value
            finally:
                if k.LocalFree(text):
                    raise OSError("LocalFree failed for token SID string")
            if not result["sid"]:
                raise ValueError("Empty token SID string")
        elif result["is_appcontainer"]:
            raise ValueError("AppContainer token has a null SID")
        result["api_ok"] = True
    except Exception as exc:
        result["error"] = repr(exc)
    finally:
        if handle.value:
            try:
                if not k.CloseHandle(handle):
                    raise ctypes.WinError(ctypes.get_last_error())
            except Exception as exc:
                result.update(api_ok=False, cleanup_error=repr(exc))
    return result

import json
print('TOKEN_EVIDENCE='+json.dumps(token_identity()),flush=True)

from manim.utils import tex_file_writing as _tex_writing
_original_tex_command = _tex_writing.make_tex_compilation_command
def _sandbox_tex_command(compiler, output_format, tex_file, tex_dir):
    if compiler != 'latex':
        raise ValueError('Sandbox pilot permits only the reviewed latex compiler')
    command = _original_tex_command(compiler, output_format, tex_file, tex_dir)
    command[1:1] = ['-disable-installer', '-disable-write18']
    print('TEX_COMMAND_EVIDENCE=' + json.dumps(command), flush=True)
    return command
_tex_writing.make_tex_compilation_command = _sandbox_tex_command
from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('y=2x-1', color=YELLOW)
        title = MathTex('f(x)=x^2 \\quad x=1').scale_to_fit_width(config.frame_width - 1.2)
        title.to_edge(UP)
        self.play(Write(title))
        ax = Axes(x_range=[-2, 4, 1], y_range=[-2, 6, 1],
                  x_length=7, y_length=4).shift(DOWN * 0.6)
        self.play(Create(ax))
        curve = ax.plot(lambda x: x ** 2, x_range=[-2, 3, 0.01], color=BLUE)
        self.play(Create(curve))
        p = ax.c2p(1, 1)
        tangent = ax.plot(lambda x: 2 * x - 1, x_range=[-1, 2.2, 0.01],
                          color=YELLOW)
        dot = Dot(p, color=RED)
        self.play(Create(tangent), FadeIn(dot))
        lbl = MathTex(r"f'(x)=2x").next_to(p, UR)
        self.play(Write(lbl))
        self.wait(0.4)
        s0 = Text('第一步：动态绘制带有刻度的横纵坐标轴。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：从左侧向右侧，动态绘制出蓝色抛物线 $y=x^2', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：在坐标 $(1,1)$ 的位置闪烁并显示一个黄色', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：从黄色圆点处向外延伸出一条橙色直线，表示切线 $', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        s4 = Text("第五步：在画面右下角，用白色字体依次显示导数公式 $f'", font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 4))
        self.play(FadeIn(s4))
        self.wait(0.15)
        ans = answer_math.scale_to_fit_width(config.frame_width - 2)
        ans.to_edge(DOWN)
        self.play(FadeIn(ans))
        self.wait(0.6)



if __name__ == '__main__':
    pass
