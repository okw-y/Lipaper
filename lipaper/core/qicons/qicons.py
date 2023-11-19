import os

from lipaper.core.qsignal import QSignal

from PySide6.QtGui import QPixmap


class QIconsLoader(object):
    _instance = None

    themeChanged = QSignal()

    def __new__(cls, *args: object, **kwargs: object) -> type:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, directory: str, extension: str = ".png") -> None:
        self._directory = directory
        self._extension = extension

        self._icons = {}
        self._current = "light"

    @classmethod
    def instance(cls) -> "QIconsLoader":
        return cls._instance

    @classmethod
    def getIcon(cls, key: str) -> QPixmap:
        if instance := cls.instance():
            return instance._icons.get(key, {}).get(instance._current, None)

    def theme(self) -> str:
        return self._current

    def setTheme(self, theme: str) -> None:
        self._current = theme

        self.themeChanged.emit(theme)

    def load(self) -> None:
        dark = f"{self._directory}\\dark"
        light = f"{self._directory}\\light"

        for path in os.listdir(light):
            if os.path.exists(f"{dark}\\{path}"):
                self._icons[path[:-len(self._extension)]] = {
                    "dark": QPixmap(f"{dark}\\{path}"),
                    "light": QPixmap(f"{light}\\{path}")
                }


class QIcon(object):
    def __init__(self, key: str) -> None:
        self._key = key

        self.iconChanged = QSignal()

        QIconsLoader.themeChanged.connect(
            lambda _: self.iconChanged.emit(self.icon())
        )

    @classmethod
    def get(cls, key: str) -> QPixmap:
        return QIconsLoader.getIcon(key)

    def icon(self) -> QPixmap:
        return QIconsLoader.getIcon(self._key)
