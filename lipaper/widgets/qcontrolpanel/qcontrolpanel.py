import typing

from lipaper.core.qicons import QIcon
from lipaper.widgets.qpushbutton import QBasePushButton

from PySide6.QtCore import QSize
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QWidget, QFrame


class QControlPanel(QFrame):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self._left_buttons = []
        self._right_buttons = []

        self._button_size = QSize(30, 30)

    def addLeftButton(self, icon: QIcon, triggered: typing.Callable) -> None:
        button = QBasePushButton("", self)
        button.setThemedIcon(icon)
        button.clicked.connect(triggered)

        if not self._left_buttons:
            button.move(5, 5)
            button.resize(self._button_size)
        else:
            button.move(
                self._left_buttons[-1].x() + self._button_size.width() + 5, 5
            )
            button.resize(self._button_size)

        button.show()

        self._left_buttons.append(button)

    def addRightButton(self, icon: QIcon, triggered: typing.Callable) -> None:
        button = QBasePushButton("", self)
        button.setIcon(icon)
        button.clicked.connect(triggered)

        if not self._right_buttons:
            button.move(self.width() - self._button_size.width() - 5, 5)
            button.resize(self._button_size)
        else:
            button.move(
                self._right_buttons[-1].x() - self._button_size.width() - 5, 5
            )
            button.resize(self._button_size)

        button.show()

        self._right_buttons.append(button)

    def resizeEvent(self, event: QResizeEvent) -> None:
        for index, button in enumerate(self._right_buttons):
            if index == 0:
                button.move(self.width() - self._button_size.width() - 5, 5)
            else:
                button.move(
                    self._right_buttons[-1].x() - self._button_size.width() - 5, 5
                )
