import os

from .qworker import QBaseWorkerW

from lipaper.widgets import QVideoPlayer

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QApplication


class QWallpaperWidget(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self._worker = None
        self._path = None

        self.resize(QApplication.instance().screens()[0].size())
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnBottomHint |
            Qt.WindowType.Tool
        )

        self._video_widget = QVideoPlayer(self, repeats=9e99)
        self._video_widget.resize(self.size())

    def wallpaperPath(self) -> str:
        return self._path

    def pauseWallpaper(self) -> None:
        self._video_widget.pause()

    def unpauseWallpaper(self) -> None:
        self._video_widget.play()

    def setNewWallpaper(self, path: str) -> None:
        if os.path.exists(path):
            self.setWindowOpacity(1)

            self._video_widget.stop()
            self._video_widget.setSource(path)
            self._video_widget.play()

            self._path = path

    def show(self) -> None:
        super().show()

        self._worker = QBaseWorkerW(self.window().winId())
        self._worker.createWindow()
        self._worker.setParent()
