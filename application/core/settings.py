import json
import os
import typing

from PySide6.QtCore import Qt
from PySide6.QtGui import QResizeEvent, QFont

from lipaper.utils import locales
from lipaper.core import QText
from lipaper.widgets import QBaseLabel, QBaseComboBox, QBaseApplication

from PySide6.QtWidgets import QWidget, QFrame, QCheckBox


class QSettingsFrame(QFrame):
    def __init__(self, title: QText | str, parent: QWidget = None) -> None:
        super().__init__(parent)

        self._label = QBaseLabel(title, self)
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._font = self._label.font()
        self._font.setPointSize(13)
        self._font.setBold(True)
        self._font.setHintingPreference(
            QFont.HintingPreference.PreferFullHinting
        )

        self._label.setFont(self._font)

        self._labels = []
        self._widgets = []

    def addParameter(self, title: QText | str, widget: QWidget) -> None:
        label = QBaseLabel(title, self)
        label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        label.resize(150, 35)
        if not self._labels:
            label.move(20, 50)
        else:
            label.move(
                20, self._labels[-1].y() + self._labels[-1].height() + 10
            )

        widget.setParent(self)
        if not self._widgets:
            widget.move(self.width() - widget.width() - 20, 50)
        else:
            widget.move(
                self.width() - widget.width() - 20,
                self._labels[-1].y() + self._labels[-1].height() + 10
            )

        label.show()
        widget.show()

        self._labels.append(label)
        self._widgets.append(widget)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._label.resize(self.width(), 35)


class QSettingsWidget(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self._app = QBaseApplication.instance()

        self._audio_enabled = None
        self._saving_enabled = None

        self._frame = QWidget(self)
        self._frame.resize(300, self.height())

        self._general = QSettingsFrame(QText("settings.general"), self._frame)
        self._general.move(0, 10)
        self._general.resize(300, 150)

        self._theme = QBaseComboBox()
        self._theme.insertItems(
            2, [QText.get("settings.general.theme.dark"),
                QText.get("settings.general.theme.light")]
        )
        self._theme.currentIndexChanged.connect(self.themeChanged)
        self._theme.resize(120, 35)

        self._language = QBaseComboBox()
        self._language.insertItems(
            len(self._app.localeLoader().languages()),
            [locales.locales[code].capitalize() for code in self._app.localeLoader().languages()]
        )
        self._language.currentIndexChanged.connect(self.languageChanged)
        self._language.resize(120, 35)

        self._general.addParameter(QText("settings.general.theme"), self._theme)
        self._general.addParameter(QText("settings.general.language"), self._language)

        self._audio = QCheckBox()
        self._audio.clicked.connect(self.audioChanged)
        self._audio.resize(25, 25)

        self._saving = QCheckBox()
        self._saving.clicked.connect(self.savingChanged)
        self._saving.resize(25, 25)

        self._additional = QSettingsFrame(QText("settings.additional"), self._frame)
        self._additional.move(0, 170)
        self._additional.resize(300, 150)

        self._additional.addParameter(QText("settings.additional.audio"), self._audio)
        self._additional.addParameter(QText("settings.additional.saving"), self._saving)

    def setAudioEnabledHandler(self, function: typing.Callable) -> None:
        self._audio_enabled = function

    def setSavingEnabledHandler(self, function: typing.Callable) -> None:
        self._saving_enabled = function

    def restoreSettings(self) -> None:
        if not os.path.exists(self._app.path("resources/settings/propertys")):
            return

        with open(self._app.path("resources/settings/propertys"), mode="r", encoding="utf-8") as file:
            data = json.loads(file.read())

        self._app.setTheme(data["general"]["theme"])
        self._app.setLanguage(data["general"]["language"])

        self._theme.setCurrentIndex(int(data["general"]["theme"] == "light"))
        self._language.setCurrentText(locales.locales[data["general"]["language"]].capitalize())

        self._audio.setChecked(data["additional"]["audio"])
        self._saving.setChecked(data["additional"]["saving"])

        self.audioChanged(data["additional"]["audio"])
        self.savingChanged(data["additional"]["saving"])

    def updateSettings(self) -> None:
        data = {
            "general": {
                "theme": self._app.theme(),
                "language": self._app.language()
            },
            "additional": {
                "audio": self._audio.isChecked(),
                "saving": self._saving.isChecked()
            }
        }

        with open(self._app.path("resources/settings/propertys"), mode="w", encoding="utf-8") as file:
            file.write(json.dumps(data))

    def themeChanged(self, index: int) -> None:
        self._app.setTheme("light" if index else "dark")

        self.updateSettings()

    def languageChanged(self, index: int) -> None:
        self._app.setLanguage(
            self._app.localeLoader().languages()[index]
        )

        self._theme.clear()
        self._theme.insertItems(
            2, [QText.get("settings.general.theme.dark"),
                QText.get("settings.general.theme.light")]
        )

        self.updateSettings()

    def audioChanged(self, enabled: bool) -> None:
        if self._audio_enabled:
            self._audio_enabled(enabled)

        self.updateSettings()

    def savingChanged(self, enabled: bool) -> None:
        if self._saving_enabled:
            self._saving_enabled(enabled)

        self.updateSettings()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._frame.resize(300, self.height())
        self._frame.move(
            (self.width() // 2) - (self._frame.width() // 2), 0
        )
