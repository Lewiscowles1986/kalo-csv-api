import unittest
from datetime import datetime

import pytz

import tzhelper


class TimeZoneHelperTest(unittest.TestCase):
    def test_get_timezones_contains_additional_items(self):
        zones_from_csv = ["PST", "CST", "EST", "GMT"]
        zones = tzhelper.get_timezones()
        for zone in zones_from_csv:
            self.assertIn(zone, zones)

    def test_get_time_returns_expected(self):
        result_table = [
            {
                "time":
                datetime(
                    year=2000,
                    month=5,
                    day=10,
                    hour=12,
                    minute=0,
                    second=0,
                    tzinfo=pytz.utc),
                "tz":
                "PST",
                "result":
                "04:00:00 PST"
            },
            {
                "time":
                datetime(
                    year=2000,
                    month=5,
                    day=10,
                    hour=12,
                    minute=0,
                    second=0,
                    tzinfo=pytz.utc),
                "tz":
                "CST",
                "result":
                "06:00:00 CST"
            },
            {
                "time":
                datetime(
                    year=2000,
                    month=5,
                    day=10,
                    hour=12,
                    minute=0,
                    second=0,
                    tzinfo=pytz.utc),
                "tz":
                "EST",
                "result":
                "07:00:00 EST"
            },
            {
                "time":
                datetime(
                    year=2000,
                    month=5,
                    day=10,
                    hour=12,
                    minute=0,
                    second=0,
                    tzinfo=pytz.utc),
                "tz":
                "GMT",
                "result":
                "12:00:00 GMT"
            },
            {
                "time":
                datetime(
                    year=2000,
                    month=5,
                    day=10,
                    hour=12,
                    minute=0,
                    second=0,
                    tzinfo=pytz.utc),
                "tz":
                "Europe/London",
                "result":
                "13:00:00 Europe/London"
            },
        ]
        for expectation in result_table:
            time = tzhelper.get_time(expectation['tz'], expectation['time'])
            result = time.strftime('%H:%M:%S') + " " + expectation['tz']
            self.assertEqual(expectation['result'], result)
