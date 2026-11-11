import unittest
from unittest.mock import Mock, patch
from collector.themes import collect_themes

class ThemeRetryTests(unittest.TestCase):
    def collector(self, responses):
        c = Mock(timeout=7, delay=2)
        c.calls = {}
        c.timeouts = []
        def call(key, function, **kwargs):
            rows = responses.pop(0)
            c.timeouts.append(c.timeout)
            c.calls[key] = dict(status='ok' if rows else 'error', fetched_at='2026-11-12T16:00:00+08:00')
            return rows
        c.call.side_effect = call
        return c

    def test_retry_recovers_and_keeps_failed_attempt(self):
        c = self.collector([None, [{'板块代码':'BK0001','板块名称':'测试'}], [{'代码':'600001','名称':'示例'}]])
        result = collect_themes(c,'2026-11-12','2026-11-12',300)
        self.assertEqual(result[3], 'available')
        self.assertEqual(c.calls['concept_catalog']['status'], 'error')
        self.assertEqual(c.calls['concept_catalog_retry']['status'], 'ok')
        self.assertEqual(c.timeouts, [45,45,45])
        self.assertEqual(c.timeout, 7)

    def test_retry_count_is_bounded(self):
        c = self.collector([None,None])
        self.assertEqual(collect_themes(c,'2026-11-12','2026-11-12',300)[3], 'error')
        self.assertEqual(c.call.call_count,2)
        self.assertEqual(c.timeout,7)

    def test_no_retry_outside_total_budget(self):
        c = self.collector([None])
        with patch('collector.themes.time.monotonic', side_effect=[0,0,100]):
            result = collect_themes(c,'2026-11-12','2026-11-12',30)
        self.assertEqual(c.call.call_count,1)
        self.assertEqual(c.timeouts,[28])
        self.assertEqual(result[3],'error')
        self.assertEqual(c.timeout,7)

    def test_zero_budget_makes_no_request(self):
        c = self.collector([])
        self.assertEqual(collect_themes(c,'2026-11-12','2026-11-12',0)[3], 'budget_exhausted')
        c.call.assert_not_called()
