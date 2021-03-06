import math
from dataclasses import dataclass
from datetime import datetime, timedelta

from PyQt5.QtCore import QObject, pyqtProperty
from PyQt5.QtQml import qmlRegisterType


def format_timedelta(delta: timedelta):
    if delta < timedelta():
        raise ValueError("Cannot format negative time deltas")

    hours, remainder = divmod(delta.seconds, 3600)
    minutes = math.ceil(remainder / 60)
    return f"{hours}:{minutes:02d}"


@dataclass
class ShiftReport(QObject):
    start: datetime
    end: datetime

    def __post_init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def length(self):
        return self.end - self.start

    @pyqtProperty(str, constant=True)
    def date(self):
        local_start = self.start.astimezone(tz=None)
        return str(local_start.date())

    @pyqtProperty(str, constant=True)
    def formatted_length(self):
        return format_timedelta(self.length)


qmlRegisterType(ShiftReport)
