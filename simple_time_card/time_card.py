import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List

from .shift_report import ShiftReport


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
