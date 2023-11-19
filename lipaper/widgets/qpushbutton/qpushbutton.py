import functools

from PySide6.QtGui import QPixmap

from lipaper.core.qicons import QIcon
from lipaper.core.qlocale import QText

from PySide6.QtWidgets import QPushButton, QWidget


class QBasePushButton(QPushButton):
    def __init__(self, text: QText | str, parent: QWidget = None) -> None:
        super().__init__(text.text() if isinstance(text, QText) else text, parent)

        if isinstance(text, QText):
            text.textChanged.connect(
                lambda: self.setText(text.text())
            )

    def setIcon(self, icon: QPixmap) -> None:
        super().setIcon(icon)

    def setThemedIcon(self, icon: QIcon) -> None:
        self.setIcon(icon.icon())

        icon.iconChanged.connect(
            self.setIcon
        )
