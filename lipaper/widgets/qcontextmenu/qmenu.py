from lipaper.core.qlocale import QText

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMenu, QWidget


class QBaseMenu(QMenu):
    def __init__(self, title: QText | str, parent: QWidget = None) -> None:
        super().__init__(title.text() if isinstance(title, QText) else title, parent)

        if isinstance(title, QText):
            title.textChanged.connect(
                lambda: self.setTitle(title.text())
            )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.NoDropShadowWindowHint)
