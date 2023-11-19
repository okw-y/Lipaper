from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QWidget


class QBaseComboBox(QComboBox):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.view().window().setWindowFlags(
            Qt.WindowType.Popup |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.NoDropShadowWindowHint
        )
        self.view().window().setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )
