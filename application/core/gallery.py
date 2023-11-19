import functools
import os
import shutil
import typing

from lipaper.utils import hash, thumbnail
from lipaper.core import QIcon, QText
from lipaper.widgets import QScrollableWidgetsView, QImagePreview, QBasePushButton, QBaseApplication

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QFileDialog


class QGalleryWidget(QScrollableWidgetsView):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self._app = QBaseApplication.instance()

        self._change_wallpaper = None
        self._delete_wallpaper = None
        self._add_wallpaper = None

        self.setWidgetSize(QSize(320, 240))

    def setChangeWallpaperHandler(self, function: typing.Callable) -> None:
        self._change_wallpaper = function

    def setDeleteWallpaperHandler(self, function: typing.Callable) -> None:
        self._delete_wallpaper = function

    def setAddWallpaperHandler(self, function: typing.Callable) -> None:
        self._add_wallpaper = function

    def appendWallpaper(self, path: str) -> None:
        wallpaper = QImagePreview()

        set_button = QBasePushButton("")
        set_button.setThemedIcon(QIcon("play"))
        set_button.clicked.connect(
            functools.partial(
                self.changeWallpaper, self._app.path(f"resources/wallpapers/{path}/wallpaper.mp4")
            )
        )

        remove_button = QBasePushButton("")
        remove_button.setThemedIcon(QIcon("delete"))
        remove_button.clicked.connect(
            functools.partial(self.deleteWallpaper, wallpaper)
        )

        wallpaper.addButton(set_button)
        wallpaper.addButton(remove_button)
        wallpaper.setWallpaper(self._app.path(f"resources/wallpapers/{path}"))

        self.addWidget(wallpaper)

    def loadWallpapers(self) -> None:
        for path in os.listdir(self._app.path("resources/wallpapers")):
            self.appendWallpaper(path)

    def changeWallpaper(self, path: str) -> None:
        if self._change_wallpaper:
            self._change_wallpaper(path)

    def deleteWallpaper(self, wallpaper: QImagePreview) -> None:
        path = self._app.path(os.path.split(wallpaper.wallpaper())[0])

        self.removeWidget(wallpaper)
        if self._delete_wallpaper:
            self._delete_wallpaper(path)

        shutil.rmtree(path)

    def addWallpaper(self) -> None:
        path = QFileDialog.getOpenFileName(
            self, QText.get("dialog.choose"), "", QText.get("dialog.filters"), ""
        )[0]

        if not path:
            return

        file_hash = hash.getFileHash(path)

        os.makedirs(self._app.path(f"resources/wallpapers/{file_hash}"), exist_ok=True)
        shutil.copy(path, self._app.path(f"resources/wallpapers/{file_hash}/wallpaper.mp4"))

        thumbnail.getVideoThumbnail(
            self._app.path(f"resources/wallpapers/{file_hash}/wallpaper.mp4"),
            self._app.path(f"resources/wallpapers/{file_hash}/thumbnail.png")
        )

        self.appendWallpaper(file_hash)

        if self._add_wallpaper:
            self._add_wallpaper()
