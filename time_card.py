from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot

from minute_timer import MinuteTimer


class TimeCardError(Exception):
    pass


class TimeCardManager(QObject):
    clocked_in_changed = pyqtSignal()
    current_time_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._clocked_in = False

        self.timer = MinuteTimer()
        self.timer.total_minutes_changed.connect(self.current_time_changed)

    @pyqtProperty(bool, notify=clocked_in_changed)
    def clocked_in(self):
        return self._clocked_in

    @pyqtProperty(str, notify=current_time_changed)
    def formatted_current_time(self):
        hours = self.timer.total_minutes // 60
        minutes = self.timer.total_minutes % 60
        return f"{hours}:{minutes:02d}"

    @pyqtSlot(name="clockIn")
    def clock_in(self):
        if self.clocked_in:
            raise TimeCardError("Attempted to clock in when already clocked in")

        self._clocked_in = True
        self.clocked_in_changed.emit()
        self.timer.start()

    @pyqtSlot(name="clockOut")
    def clock_out(self):
        if not self.clocked_in:
            raise TimeCardError("Attempted to clock out when already clocked out")

        self._clocked_in = False
        self.clocked_in_changed.emit()
        self.timer.stop()
        self.timer.total_minutes = 0
