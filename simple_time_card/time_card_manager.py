import os
from datetime import datetime, timedelta, timezone

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot

from .minute_timer import MinuteTimer
from .shift_report import ShiftReport, format_timedelta
from .time_card import TimeCard


class TimeCardManagerError(Exception):
    pass


class TimeCardManager(QObject):
    clocked_in_changed = pyqtSignal()
    current_time_changed = pyqtSignal()
    shift_report_added = pyqtSignal()

    TIME_CARD_FILEPATH = os.path.join("timecards", "timecard.json")

    def __init__(self):
        super().__init__()

        self._clocked_in = False
        self._start_time = None

        self._timer = MinuteTimer()
        self._timer.total_minutes_changed.connect(self.current_time_changed)

        try:
            self._time_card = TimeCard.from_file(self.TIME_CARD_FILEPATH)
        except FileNotFoundError:
            self._time_card = TimeCard()

    @pyqtProperty(list, notify=shift_report_added)
    def shift_reports(self):
        return [report for report in self._time_card.shift_reports]

    @pyqtProperty(bool, notify=clocked_in_changed)
    def clocked_in(self):
        return self._clocked_in

    @pyqtProperty(str, notify=current_time_changed)
    def formatted_current_time(self):
        hours = self._timer.total_minutes // 60
        minutes = self._timer.total_minutes % 60
        return f"{hours}:{minutes:02d}"

    @pyqtProperty(str, notify=shift_report_added)
    def formatted_total_time(self):
        total_time_delta = sum(
            [report.length for report in self.shift_reports], start=timedelta()
        )
        return format_timedelta(total_time_delta)

    @pyqtSlot(name="clockIn")
    def clock_in(self):
        if self.clocked_in:
            raise TimeCardManagerError("Attempted to clock in when already clocked in")

        self._clocked_in = True
        self.clocked_in_changed.emit()
        self._timer.start()

        self._start_time = datetime.now(timezone.utc)

    @pyqtSlot(name="clockOut")
    def clock_out(self):
        if not self.clocked_in:
            raise TimeCardManagerError(
                "Attempted to clock out when already clocked out"
            )

        self._clocked_in = False
        self.clocked_in_changed.emit()
        self._timer.stop()
        self._timer.total_minutes = 0

        self._add_shift_report(datetime.now(timezone.utc))

    def _add_shift_report(self, end_time):
        report = ShiftReport(start=self._start_time, end=end_time)
        self._time_card.shift_reports.append(report)
        self._start_time = None
        self.shift_report_added.emit()
        self._time_card.to_file(self.TIME_CARD_FILEPATH)
