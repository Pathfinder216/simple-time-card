import unittest
from datetime import timedelta

from simple_time_card import shift_report


class TestFormatTimeDelta(unittest.TestCase):
    def test_hours(self):
        delta = timedelta(hours=1)
        result = shift_report.format_timedelta(delta)
        self.assertEqual(result, "1:00")

    def test_minutes(self):
        delta = timedelta(minutes=2)
        result = shift_report.format_timedelta(delta)
        self.assertEqual(result, "0:02")

    def test_minutes_greater_than_10(self):
        delta = timedelta(minutes=15)
        result = shift_report.format_timedelta(delta)
        self.assertEqual(result, "0:15")

    def test_seconds(self):
        delta = timedelta(seconds=3)
        result = shift_report.format_timedelta(delta)
        self.assertEqual(result, "0:01")

    def test_zero(self):
        delta = timedelta()
        result = shift_report.format_timedelta(delta)
        self.assertEqual(result, "0:00")

    def test_seconds_negative(self):
        delta = timedelta(seconds=-2)
        with self.assertRaises(ValueError):
            shift_report.format_timedelta(delta)

    def test_wrong_type(self):
        delta = 1
        with self.assertRaises(TypeError):
            shift_report.format_timedelta(delta)


if __name__ == "__main__":
    unittest.main()
