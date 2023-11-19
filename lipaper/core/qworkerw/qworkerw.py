import win32con
import win32gui


class QBaseWorkerW(object):
    def __init__(self, hwnd: int) -> None:
        self._hwnd = hwnd
        self._worker = None

    def callback(self, hwnd: int, _: list[int]) -> int:
        window = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", "")

        if window:
            self._worker = win32gui.FindWindowEx(0, hwnd, "WorkerW", "")

        return self._worker

    def createWindow(self) -> None:
        progman = win32gui.FindWindow("Progman", None)

        win32gui.SendMessageTimeout(progman, 0x052C, 0, 0, win32con.SMTO_NORMAL, 1000)
        win32gui.EnumWindows(self.callback, None)

    def setParent(self) -> None:
        win32gui.SetParent(self._hwnd, self._worker)
