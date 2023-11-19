from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QResizeEvent, QPixmap, QMouseEvent
from PySide6.QtWidgets import QWidget, QLabel, QPushButton


class QImagePreview(QWidget):
    pressed = Signal(object)

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self._wallpaper = None
        self._button_size = QSize(30, 30)

        self._buttons = []

        self._image = QLabel(self)
        self._image.resize(self.size())

    def wallpaper(self) -> str:
        return self._wallpaper

    def pixmap(self) -> QPixmap:
        return self._image.pixmap()

    def addButton(self, button: QPushButton) -> None:
        button.setParent(self)
        button.resize(self._button_size)

        if not self._buttons:
            button.move(5, self._image.y() + 5)
        else:
            button.move(
                self._buttons[-1].x() + self._button_size.width() + 5, self._image.y() + 5
            )

        button.show()

        self._buttons.append(button)

    def setWallpaper(self, path: str) -> None:
        self._wallpaper = f"{path}/wallpaper.mp4"

        self.setPixmap(
            QPixmap(f"{path}/thumbnail.png")
        )

    def setPixmap(self, pixmap: QPixmap) -> None:
        self._image.setPixmap(
            pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio,
                          Qt.TransformationMode.SmoothTransformation)
        )

        self._image.resize(self._image.pixmap().size())
        self._image.move(
            (self.width() // 2) - (self._image.pixmap().width() // 2),
            (self.height() // 2) - (self._image.pixmap().height() // 2)
        )

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.pressed.emit(self._wallpaper)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._image.resize(self.size())

        if pixmap := self._image.pixmap():
            self._image.setPixmap(
                pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio,
                              Qt.TransformationMode.SmoothTransformation)
            )

            self._image.resize(self._image.pixmap().size())
            self._image.move(
                (self.width() // 2) - (self._image.pixmap().width() // 2),
                (self.height() // 2) - (self._image.pixmap().height() // 2)
            )

            last = 5
            for index, button in enumerate(self._buttons):
                if index == 0:
                    button.move(5, self._image.y() + 5)
                else:
                    button.move(
                        last + self._button_size.width() + 5, self._image.y() + 5
                    )

                last = button.x()
