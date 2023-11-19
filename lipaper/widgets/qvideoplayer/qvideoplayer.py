import vlc

from PySide6.QtWidgets import QWidget


class QVideoPlayer(QWidget):
    def __init__(self, parent: QWidget = None, repeats: int | float = 1) -> None:
        super().__init__(parent)

        self._instance = vlc.Instance(f"--input-repeat={int(repeats)}")

        self._player = self._instance.media_player_new()
        self._player.set_hwnd(self.winId())

        self._timer = None

    def play(self) -> None:
        self._player.play()

    def stop(self) -> None:
        self._player.stop()

    def pause(self) -> None:
        self._player.pause()

    def setSource(self, path: str) -> None:
        self._player.set_media(
            self._instance.media_new(path)
        )

    def setAudioEnabled(self, state: bool) -> None:
        self._player.audio_set_volume(100 * state)
