def token_identity() -> dict:
    """Query classes 29/30/31 in the calling process, not its parent."""
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
        if not a.OpenProcessToken(k.GetCurrentProcess(), 8, ctypes.byref(handle)):
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
from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        title = MathTex(r'\displaystyle\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^n \quad e \quad \displaystyle\sum_{k=0}^{\infty}\frac{1}{k!}').scale_to_fit_width(config.frame_width - 1.2)
        title.to_edge(UP)
        self.play(Write(title))
        line = NumberLine(x_range=[0, 12, 1], length=9).shift(DOWN * 1.2)
        self.play(Create(line))
        dots = VGroup(*[Dot(line.n2p(n), color=TEAL)
                        for n in range(1, 9)])
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.15))
        lbl = MathTex(r'a_n', color=YELLOW).shift(UP * 1.5)
        self.play(Write(lbl))
        self.wait(0.4)
        s0 = Text('第一步：以单调有界准则为主线，建立数学分析·极限场景并呈', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：二项展开系数柱状图逐项累加。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：数列 $a_n$ 单调递增且有上界 3 的标注。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：上界 3 的水平虚线。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        s4 = Text('第五步：高亮最终结果与答案。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 4))
        self.play(FadeIn(s4))
        self.wait(0.15)
        ans = MathTex(r'e=\sum_{k=0}^{\infty}\frac{1}{k!}', color=YELLOW).scale_to_fit_width(config.frame_width - 2)
        ans.to_edge(DOWN)
        self.play(FadeIn(ans))
        self.wait(0.6)



if __name__ == '__main__':
    pass
