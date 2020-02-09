import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot

from .minute_timer import MinuteTimer
from .shift_report import ShiftReport


class TimeCardEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return {"__type__": datetime.__name__, "isoformat": obj.isoformat()}

        if isinstance(obj, (ShiftReport, TimeCard)):
            object_data = vars(obj)
            object_data["__type__"] = type(obj).__name__
            return object_data

        return super().default(obj)


class TimeCardDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, serialized_data):
        if "__type__" not in serialized_data:
            return serialized_data

        data_type = serialized_data["__type__"]

        if data_type == datetime.__name__:
            return datetime.fromisoformat(serialized_data["isoformat"])

        if data_type == ShiftReport.__name__:
            del serialized_data["__type__"]
            return ShiftReport(**serialized_data)

        if data_type == TimeCard.__name__:
            del serialized_data["__type__"]
            return TimeCard(**serialized_data)

        raise TypeError(f"Object of type {data_type} is not JSON deserializable")


@dataclass
class TimeCard:
    creation_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    shift_reports: List[ShiftReport] = field(default_factory=list)

    @staticmethod
    def from_file(filepath):
        with open(filepath) as f:
            return json.load(f, cls=TimeCardDecoder)

    def to_file(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w") as f:
            json.dump(self, f, cls=TimeCardEncoder)


class TimeCardError(Exception):
    pass


class TimeCardManager(QObject):
    clocked_in_changed = pyqtSignal()
    current_time_changed = pyqtSignal()
    shift_report_added = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._clocked_in = False
        self._start_time = None

        self._timer = MinuteTimer()
        self._timer.total_minutes_changed.connect(self.current_time_changed)

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

    @pyqtSlot(name="clockIn")
    def clock_in(self):
        if self.clocked_in:
            raise TimeCardError("Attempted to clock in when already clocked in")

        self._clocked_in = True
        self.clocked_in_changed.emit()
        self._timer.start()

        self._start_time = datetime.now(timezone.utc)

    @pyqtSlot(name="clockOut")
    def clock_out(self):
        if not self.clocked_in:
            raise TimeCardError("Attempted to clock out when already clocked out")

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
