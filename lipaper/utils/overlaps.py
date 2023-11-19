import win32gui

from pywinauto import Desktop


def overlapsApplication(size: tuple[int | float, int | float], *, deviation: int = -1) -> bool:
    if deviation == -1:
        rectangle = win32gui.GetWindowRect(
            win32gui.FindWindow("Shell_traywnd", None)
        )

        deviation = rectangle[3] - rectangle[1]

    for window in Desktop(backend="uia").windows():
        if window.is_dialog():
            x, y = window.rectangle().top, window.rectangle().left
            width, height = window.rectangle().width(), window.rectangle().height()

            if x <= 0 and y <= 0 and width >= size[0] and height >= size[1] - deviation:
                return True

    return False
