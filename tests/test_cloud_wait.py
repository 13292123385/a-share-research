from datetime import datetime
import unittest
from collector.cloud_wait import seconds_until_capture, TZ


class CloudWaitTests(unittest.TestCase):
    def test_warmup_waits_until_each_capture_and_never_waits_after_it(self):
        self.assertEqual(seconds_until_capture(datetime(2026, 11, 16, 11, 13, tzinfo=TZ)), 17 * 60)
        self.assertEqual(seconds_until_capture(datetime(2026, 11, 16, 14, 43, tzinfo=TZ)), 17 * 60)
        for hour, minute in [(11, 30), (12, 15), (15, 0), (20, 0)]:
            self.assertEqual(seconds_until_capture(datetime(2026, 11, 16, hour, minute, tzinfo=TZ)), 0)
        self.assertEqual(seconds_until_capture(datetime(2026, 11, 21, 11, 13, tzinfo=TZ)), 0)
