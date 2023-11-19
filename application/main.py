import sys
import typing

from application.core.gallery import QGalleryWidget
from application.core.settings import QSettingsWidget
from lipaper.core.qaction import QBaseAction

from lipaper.utils import titlebar, overlaps
from lipaper.core import QText, QIcon, QBaseWorkerW
from lipaper.widgets import QTabWidget, QBaseApplication, QVideoPlayer, QControlPanel, QBasePushButton, QBaseMenu

from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QResizeEvent, QPixmap, QCloseEvent
from PySide6.QtWidgets import QWidget, QSystemTrayIcon


class QWallpaper(QWidget):
    _instance = None

    def __new__(cls, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self._app = QBaseApplication.instance()

        self.resize(QBaseApplication.instance().screens()[0].size())
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnBottomHint |
            Qt.WindowType.Tool
        )

        self._worker = None

        self._settings = QSettingsWidget()
        self._settings.restoreSettings()

        # self._settings.setAudioEnabledHandler(self.setAudioEnabled)
        # self._settings.setSavingEnabledHandler(self.setEffectiveModeEnabled)

        self._player = QVideoPlayer(self, repeats=9e99)
        self._player.resize(self.size())

        self._context = QBaseMenu("")
        self._context.addAction(QBaseAction(QText("menu.settings"), function=self.settings))
        self._context.addSeparator()
        self._context.addAction(QBaseAction(QText("menu.play"), function=self.play))
        self._context.addAction(QBaseAction(QText("menu.pause"), function=self.pause))
        self._context.addSeparator()
        self._context.addAction(QBaseAction(QText("menu.exit"), function=sys.exit))

        self._tray = QSystemTrayIcon(self)
        self._tray.setIcon(QPixmap(self._app.path("resources/lipaper.png")))
        self._tray.setToolTip("Lipaper")
        self._tray.setContextMenu(self._context)
        self._tray.show()

        # self._timer = QTimer(self)
        # self._timer.timeout.connect(self.effectiveMode)

        self.restoreWallpaper()

    @classmethod
    def play(cls) -> None:
        cls._instance.player().play()

    @classmethod
    def pause(cls) -> None:
        cls._instance.player().pause()

    @classmethod
    def setVideo(cls, path: str) -> None:
        cls._instance.player().setSource(path)
        cls._instance.player().play()

    @classmethod
    def setAudioEnabled(cls, state: bool) -> None:
        cls._instance.player().setAudioEnabled(state)

    @classmethod
    def setEffectiveModeEnabled(cls, state: bool) -> None:
        # if state:
        #     cls._instance.timer().start(2500)
        # else:
        #     cls._instance.timer().stop()
        ...

    def settings(self) -> None:
        self._settings = QMain()
        self._settings.show()

    def player(self) -> QVideoPlayer:
        return self._player

    def effectiveMode(self) -> None:
        if overlaps.overlapsApplication(self.size().toTuple()):
            self.pause()
        else:
            self.play()

    def restoreWallpaper(self) -> None:
        with open(self._app.path("resources/settings/current"), mode="r", encoding="utf-8") as file:
            self.setVideo(file.read())

    def show(self) -> None:
        super().show()

        self._worker = QBaseWorkerW(self.window().winId())
        self._worker.createWindow()
        self._worker.setParent()


class QMain(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self._app = QBaseApplication.instance()

        self._wallpaper_gallery = QGalleryWidget()

        self._wallpaper_gallery.setChangeWallpaperHandler(self.changeWallpaper)
        self._wallpaper_gallery.setAddWallpaperHandler(self.addWallpaper)

        self._wallpaper_gallery.setWidgetSize(QSize(320, 240))
        self._wallpaper_gallery.loadWallpapers()

        self._settings_widget = QSettingsWidget()

        # self._settings_widget.setAudioEnabledHandler(QWallpaper.setAudioEnabled)
        # self._settings_widget.setSavingEnabledHandler(QWallpaper.setEffectiveModeEnabled)

        self._tab_widget = QTabWidget(self)
        self._tab_widget.setButtonSize(QSize(120, 30))
        self._tab_widget.addWidget(QText("tabs.gallery"), self._wallpaper_gallery)
        self._tab_widget.addWidget(QText("tabs.settings"), self._settings_widget)

        self._add_wallpaper = QBasePushButton(QText("tabs.add"), self)
        self._add_wallpaper.setThemedIcon(QIcon("add"))
        self._add_wallpaper.clicked.connect(self._wallpaper_gallery.addWallpaper)
        self._add_wallpaper.resize(150, 40)
        self._add_wallpaper.move(5, 5)

        self._base_control = QControlPanel(self)
        self._base_control.addLeftButton(QIcon("play"), QWallpaper.play)
        self._base_control.addLeftButton(QIcon("pause"), QWallpaper.pause)

        self._settings_widget.restoreSettings()

        self.setWindowTitle("Lipaper")
        self.setWindowIcon(QPixmap(self._app.path("resources/lipaper.png")))
        self.resize(800, 610)
        self.setMinimumSize(800, 610)

        titlebar.setTileBarDarkTheme(self.window().winId())

    def changeWallpaper(self, path: str, update: bool = True) -> None:
        QWallpaper.setVideo(path)

        if not update:
            return

        with open(self._app.path("resources/settings/current"), mode="w", encoding="utf-8") as file:
            file.write(path.replace("\\", "/"))

    def addWallpaper(self) -> None:
        self._tab_widget.switchWidget(0)

        self._wallpaper_gallery.placeIcons(
            self._tab_widget.widgetsFrameSize()
        )

    def closeEvent(self, event: QCloseEvent) -> None:
        self.destroy()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._tab_widget.resize(
            self.width(), self.height() - 50
        )

        self._base_control.move(10, self.height() - 50)

        self._wallpaper_gallery.placeIcons(
            self._tab_widget.widgetsFrameSize()
        )


if __name__ == "__main__":
    app = QBaseApplication(
        sys.argv, icons="~/resources/icons", locale="~/resources/locale", styles="~/resources/styles"
    )
    app.setQuitOnLastWindowClosed(False)

    wallpaper = QWallpaper()
    wallpaper.show()

    sys.exit(app.exec())
