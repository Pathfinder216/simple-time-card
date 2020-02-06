from dataclasses import dataclass
from datetime import datetime


@dataclass
class ShiftReport:
    start: datetime
    end: datetime
