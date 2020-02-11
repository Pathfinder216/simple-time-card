import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, PropertyMock, patch

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


class TestShiftReport(unittest.TestCase):
    def setUp(self):
        self.report = shift_report.ShiftReport(start=None, end=None)

    def test_length_one_day(self):
        self.report.start = datetime(2000, 1, 1)
        self.report.end = datetime(2000, 1, 2)
        self.assertEqual(self.report.length, timedelta(days=1))

    def test_length_seconds(self):
        self.report.start = datetime(2000, 1, 1)
        self.report.end = datetime(2000, 1, 1, second=1)
        self.assertEqual(self.report.length, timedelta(seconds=1))

    def test_length_negative(self):
        self.report.start = datetime(2000, 1, 2)
        self.report.end = datetime(2000, 1, 1)
        self.assertEqual(self.report.length, timedelta(days=-1))

    def test_length_int(self):
        self.report.start = 0
        self.report.end = 1
        self.assertEqual(self.report.length, 1)

    def test_date(self):
        self.report.start = datetime(2000, 1, 2)
        self.assertEqual(self.report.date, "2000-01-02")

    def test_date_with_seconds(self):
        self.report.start = datetime(2000, 1, 2, second=10)
        self.assertEqual(self.report.date, "2000-01-02")

    def test_date_timezone_change(self):
        class MockableDatetime(datetime):
            pass

        self.report.start = MockableDatetime(2000, 1, 3, tzinfo=timezone.utc)
        self.report.start.astimezone = Mock(return_value=datetime(2000, 1, 2, hour=1))

        result = self.report.date

        self.assertEqual(result, "2000-01-02")
        self.report.start.astimezone.assert_called_once_with(tz=None)

    @patch(
        "simple_time_card.shift_report.ShiftReport.length", new_callable=PropertyMock
    )
    @patch("simple_time_card.shift_report.format_timedelta")
    def test_formatted_length(self, format_mock, length_mock):
        length_mock.return_value = 2
        format_mock.return_value = "01:02"

        result = self.report.formatted_length

        self.assertEqual(result, format_mock.return_value)
        length_mock.assert_called_once()
        format_mock.assert_called_once_with(2)


if __name__ == "__main__":
    unittest.main()
