import typing

from lipaper.core.qlocale import QText

from PySide6.QtCore import QObject
from PySide6.QtGui import QAction


class QBaseAction(QAction):
    def __init__(self, text: QText | str, shortcut: str = None,
                 function: typing.Callable = None, parent: QObject = None) -> None:
        super().__init__(text.text() if isinstance(text, QText) else text, parent)

        if shortcut:
            self.setShortcut(shortcut)
        if function:
            self.triggered.connect(function)

        if isinstance(text, QText):
            text.textChanged.connect(
                lambda: self.setText(text.text())
            )
