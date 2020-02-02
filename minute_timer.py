from PyQt5.QtCore import QTimer, pyqtSignal, pyqtSlot

MILLISECONDS_PER_MINUTE = 60_000


class MinuteTimer(QTimer):
    total_minutes_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._total_minutes = 0
        self.setInterval(MILLISECONDS_PER_MINUTE)
        self.timeout.connect(self._tick)

    @property
    def total_minutes(self):
        return self._total_minutes

    @total_minutes.setter
    def total_minutes(self, minutes):
        if self._total_minutes != minutes:
            self._total_minutes = minutes
            self.total_minutes_changed.emit()

    @pyqtSlot()
    def start(self):
        """ Trigger once on start """
        self.timeout.emit()
        super().start()

    @pyqtSlot()
    def _tick(self):
        self.total_minutes += 1
