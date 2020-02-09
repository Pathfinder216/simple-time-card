import math
from dataclasses import dataclass
from datetime import datetime

from PyQt5.QtCore import QObject, pyqtProperty
from PyQt5.QtQml import qmlRegisterType


@dataclass
class ShiftReport(QObject):
    start: datetime
    end: datetime

    def __post_init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @pyqtProperty(str, constant=True)
    def date(self):
        local_start = self.start.astimezone(tz=None)
        return str(local_start.date())

    @pyqtProperty(str, constant=True)
    def length(self):
        time_delta = self.end - self.start
        hours, remainder = divmod(time_delta.seconds, 3600)
        minutes = math.ceil(remainder / 60)
        return f"{hours}:{minutes:02d}"


qmlRegisterType(ShiftReport)
