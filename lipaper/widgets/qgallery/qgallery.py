from PySide6.QtCore import QSize, QParallelAnimationGroup, QPropertyAnimation, QPoint, QEasingCurve
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QWidget, QFrame


class QScrollableWidgetsView(QFrame):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self._widgets = []

        self._current_page = 0
        self._page_count = 0
        self._scroll_count = 0

        self._widget_size = QSize(50, 50)

        self._animation = None

    def setWidgetSize(self, size: QSize) -> None:
        self._widget_size = size

    def addWidget(self, widget: QWidget | type[QWidget]) -> None:
        if isinstance(widget, type):
            widget = widget(self)
        else:
            widget.setParent(self)

        widget.resize(self._widget_size)
        widget.show()

        self._widgets.append(widget)

    def removeWidget(self, widget: QWidget) -> None:
        widget.hide()

        if (index := self._widgets.index(widget)) != -1:
            self._widgets.pop(index)

        self.placeIcons(self.size())

    def placeIcons(self, size: QSize) -> None:
        if not self._widgets:
            return

        rows = size.height() // (self._widget_size.height() + 10)
        columns = size.width() // (self._widget_size.width() + 10)

        if columns > len(self._widgets):
            columns = len(self._widgets)

        width = size.width() // columns if columns else 0
        height = size.height() // rows if rows else 0

        if rows > round(len(self._widgets) / columns) and rows * (self._widget_size.width() + 10) <= size.height():
            height = (self._widget_size.width() + 10)

        row = 0
        column = 0
        for widget in self._widgets:
            x = (width * column) + ((width // 2) - (self._widget_size.width() // 2))
            y = (height * row) + ((height // 2) - (self._widget_size.height() // 2))

            if QPoint(x, y) != widget.pos():
                widget.move(x, y)

            if column == columns - 1:
                row += 1
                column = 0
            else:
                column += 1

        if column == 0:
            row -= 1

        self._current_page = 0
        self._page_count = row // rows
        self._scroll_count = height * rows

    def wheelEvent(self, event: QWheelEvent) -> None:
        if not self._widgets or (self._animation and self._animation.state() == QParallelAnimationGroup.State.Running):
            return

        self._animation = QParallelAnimationGroup(self)

        to = event.angleDelta().y() // abs(event.angleDelta().y())

        if (to > 0 and self._current_page == 0) or (to < 0 and self._current_page == self._page_count):
            return

        for widget in self._widgets:
            animation = QPropertyAnimation(widget, b"pos")
            animation.setStartValue(widget.pos())
            animation.setEndValue(QPoint(widget.x(), widget.y() + (to * self._scroll_count)))
            animation.setDuration(350)
            animation.setEasingCurve(QEasingCurve.Type.InOutExpo)
            animation.start()

            self._animation.addAnimation(animation)

        self._current_page -= to

        self._animation.start()
