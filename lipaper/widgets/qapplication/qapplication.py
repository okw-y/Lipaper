import datetime
import logging
import os
import typing

from lipaper.core import QIconsLoader, QLocalizationLoader

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication


class QBaseApplication(QApplication):
    _instance = None

    themeChanged = Signal()
    languageChanged = Signal()

    def __new__(cls, *args: typing.Any, **kwargs: typing.Any) -> None:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, argv: list[str], locale: str = None,
                 icons: str = None, styles: str = None, logger: bool = True) -> None:
        super().__init__(argv)

        self._path = os.path.split(argv[0])[0]

        if locale and (locale.startswith("~/") or locale.startswith("~\\")):
            locale = os.path.join(self._path, locale[2:])

        if icons and (icons.startswith("~/") or icons.startswith("~\\")):
            icons = os.path.join(self._path, icons[2:])

        if styles and (styles.startswith("~/") or styles.startswith("~\\")):
            styles = os.path.join(self._path, styles[2:])

        self._locale_loader = QLocalizationLoader(locale)
        if locale:
            self._locale_loader.load()

        self._icons_loader = QIconsLoader(icons)
        if icons:
            self._icons_loader.load()

        self._theme = "light"

        self._styles = {"dark": "", "light": ""}
        if styles:
            self._styles = {
                "dark": open(f"{styles}\\dark.qss").read(),
                "light": open(f"{styles}\\light.qss").read()
            }

        self.setStyleSheet(self._styles["light"])

        if logger:
            os.makedirs(f"{self._path}\\logs", exist_ok=True)

            logging.basicConfig(
                filename=f"{self._path}\\logs\\"
                         f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.log')}",
                filemode="w",
                encoding="utf-8",
                level=logging.INFO,
                datefmt="%Y-%m-%d %H:%M:%S",
                format="%(asctime)s.%(msecs)03d "
                       "[%(levelname)s] [%(module)s] :: "
                       "%(funcName)s() -> %(message)s",
            )

    @classmethod
    def instance(cls) -> "QBaseApplication":
        return cls._instance

    def path(self, relative: str = None) -> str:
        if relative:
            return os.path.join(self._path, relative)

        return self._path

    def localeLoader(self) -> QLocalizationLoader:
        return self._locale_loader

    def iconsLoader(self) -> QIconsLoader:
        return self._icons_loader

    def theme(self) -> str:
        return self._theme

    def language(self) -> str:
        return self._locale_loader.language()

    def setTheme(self, theme: str) -> None:
        self._theme = theme
        self._icons_loader.setTheme(theme)

        self.setStyleSheet(self._styles[theme])
        self.themeChanged.emit()

    def setLanguage(self, language: str) -> None:
        self._locale_loader.setLocale(language)

        self.languageChanged.emit()
