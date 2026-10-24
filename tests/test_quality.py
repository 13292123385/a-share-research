import json
from pathlib import Path
import tempfile
import unittest
from collector.quality import candidate_prices, daily_price, select_snapshot


class QualityTests(unittest.TestCase):
    def test_price_rejects_wrong_date_duplicates_and_invalid_ohlc(self):
        r = dict(date='2026-10-23', open=10, high=11, low=9, close=11)
        self.assertIsNotNone(daily_price([r], '2026-10-23'))
        self.assertIsNone(daily_price([r], '2026-10-22'))
        self.assertIsNone(daily_price([r, r], '2026-10-23'))
        self.assertIsNone(daily_price([dict(r, high=8)], '2026-10-23'))

    def test_fallback_dates_and_budget_missing(self):
        class Fake:
            timeout, delay = 45, 0
            calls = {}
            def call(self, key, function, **kwargs):
                self.request = kwargs
                return [dict(date='2026-10-23', open=10, high=11, low=10, close=11)]
        pool = [{'代码': '600001', '名称': '测试', '连板数': 1}]
        c, quotes = Fake(), {}
        prices, missing = candidate_prices(c, pool, quotes, '2026-10-23', 10)
        self.assertEqual(c.request['start_date'], '20261023')
        self.assertEqual(c.request['adjust'], '')
        self.assertEqual(len(prices), 1)
        self.assertFalse(missing)
        self.assertEqual(quotes['600001']['最高'], 11)
        self.assertEqual(c.timeout, 45)
        _, missing = candidate_prices(c, pool, {}, '2026-10-23', 0)
        self.assertEqual(missing, ['600001'])
        prices, missing = candidate_prices(c, pool, {}, '2026-10-23', 0, prices)
        self.assertFalse(missing)
        self.assertTrue(prices[0]['reused_from_prior_run'])
        _, missing = candidate_prices(c, pool, {}, '2026-10-22', 0, prices)
        self.assertEqual(missing, ['600001'])

    def test_snapshot_never_replaces_better_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            daily = Path(tmp)
            def snapshot(run, codes):
                s = dict(run_id=run, status='partial', verified={'mainboard_limit_up_count': 2},
                         price_coverage=codes)
                p = daily / 'runs' / run
                p.mkdir(parents=True)
                (p / 'summary.json').write_text(json.dumps(s), encoding='utf-8')
                return s
            self.assertTrue(select_snapshot(daily, snapshot('a', ['600001'])))
            self.assertTrue(select_snapshot(daily, snapshot('b', ['600001', '600002'])))
            self.assertFalse(select_snapshot(daily, snapshot('c', ['600001'])))
            self.assertEqual(json.loads((daily / 'latest.json').read_text())['run_id'], 'b')
