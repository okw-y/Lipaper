import ctypes


def setTileBarDarkTheme(hwnd: int) -> None:
    ctypes.windll.dwmapi.DwmSetWindowAttribute(
        hwnd, 20, ctypes.byref(ctypes.c_int(2)), ctypes.sizeof(ctypes.c_int(2))
    )
