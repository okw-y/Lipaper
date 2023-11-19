from lipaper.core.qlocale import QText

from PySide6.QtWidgets import QLabel, QWidget


class QBaseLabel(QLabel):
    def __init__(self, text: QText | str, parent: QWidget = None) -> None:
        super().__init__(text.text() if isinstance(text, QText) else text, parent)

        if isinstance(text, QText):
            text.textChanged.connect(
                lambda: self.setText(text.text())
            )
