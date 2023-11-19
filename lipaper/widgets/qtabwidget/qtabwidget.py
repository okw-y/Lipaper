import functools

from lipaper.core.qlocale import QText
from lipaper.widgets import QBasePushButton

from PySide6.QtCore import QPropertyAnimation, QParallelAnimationGroup, QPoint, QEasingCurve, QSize
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QWidget, QFrame


class QCheckedWidget(QFrame):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)


class QTabWidget(QFrame):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self._current = 0

        self._button_size = QSize(100, 40)

        self._widgets = []
        self._buttons = []

        self._button_frame = QFrame(self)

        self._checked_widget = QCheckedWidget(self._button_frame)
        self._checked_widget.resize(90, 4)
        self._checked_widget.move(-90, 55)

        self._animation = None

    def widgetsFrameSize(self) -> QSize:
        return QSize(self.width(), self.height() - 60)

    def setButtonSize(self, size: QSize) -> None:
        self._button_size = size

        self._checked_widget.resize(
            size.width() - 10, 4
        )

        last = 10
        for index, button in enumerate(self._buttons):
            if index == 0:
                button.move(10, 10)
                button.resize(size)
            else:
                button.move(last + size.width() + 10, 10)
                button.resize(size)

            last = button.x()

    def addWidget(self, text: QText | str, widget: QWidget) -> None:
        widget.setParent(self)
        widget.move(-self.width(), self._button_size.height() + 20)
        widget.resize(self.width(), self.height() - self._button_size.height() + 20)

        button = QBasePushButton(text, self._button_frame)
        button.clicked.connect(
            functools.partial(self.switchWidget, len(self._widgets))
        )
        button.setCheckable(True)
        button.resize(self._button_size)

        if not self._buttons:
            button.setChecked(True)
            button.move(10, 10)

            self._checked_widget.move(15, self._button_size.height() + 15)
        else:
            button.move(self._buttons[-1].x() + self._button_size.width() + 10, 10)

        widget.show()
        button.show()

        self._button_frame.adjustSize()

        self._widgets.append(widget)
        self._buttons.append(button)

        self.show()

    def switchWidget(self, index: int) -> None:
        if index == self._current:
            return

        widget = self._widgets[index]
        current = self._widgets[self._current]

        animation_first = QPropertyAnimation(widget, b"pos")
        animation_first.setStartValue(
            QPoint(self.width() if index > self._current else -self.width(), self._button_size.height() + 20)
        )
        animation_first.setEndValue(QPoint(0, self._button_size.height() + 20))
        animation_first.setDuration(350)
        animation_first.setEasingCurve(
            QEasingCurve.Type.InOutExpo
        )

        animation_second = QPropertyAnimation(current, b"pos")
        animation_second.setStartValue(QPoint(0, self._button_size.height() + 20))
        animation_second.setEndValue(
            QPoint(-self.width() if index > self._current else self.width(), self._button_size.height() + 20)
        )
        animation_second.setDuration(350)
        animation_second.setEasingCurve(
            QEasingCurve.Type.InOutExpo
        )

        animation_checked = QPropertyAnimation(self._checked_widget, b"pos")
        animation_checked.setStartValue(self._checked_widget.pos())
        animation_checked.setEndValue(QPoint(self._buttons[index].x() + 5, self._button_size.height() + 15))
        animation_checked.setDuration(350)
        animation_checked.setEasingCurve(
            QEasingCurve.Type.InOutExpo
        )

        self._animation = QParallelAnimationGroup(self)
        self._animation.addAnimation(animation_first)
        self._animation.addAnimation(animation_second)
        self._animation.addAnimation(animation_checked)
        self._animation.start(
            QPropertyAnimation.DeletionPolicy.DeleteWhenStopped
        )

        self._current = index

        for index, button in enumerate(self._buttons):
            button.setChecked(index == self._current)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._button_frame.move(
            (self.width() // 2) - (self._button_frame.width() // 2), 0
        )

        for index, widget in enumerate(self._widgets):
            widget.resize(self.width(), self.height() - self._button_size.height() + 20)
            widget.move(self.width() * (index != self._current), self._button_size.height() + 20)
