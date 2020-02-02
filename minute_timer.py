from PyQt5.QtCore import QTimer, pyqtSlot

MILLISECONDS_PER_MINUTE = 60_000


class MinuteTimer(QTimer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.total_minutes = 0
        self.setInterval(MILLISECONDS_PER_MINUTE)
        self.timeout.connect(self._tick)

    @pyqtSlot()
    def _tick(self):
        self.total_minutes += 1
