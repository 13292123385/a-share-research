import unittest
from collector.quality import collect_index
from collector.reconcile import reconcile_market, collect_reconciliation


class ReconcileTests(unittest.TestCase):
    def fixtures(self):
        rosters = {
            'sh_main': [{'证券代码': '600001', '上市日期': '2000-01-01'}],
            'sh_star': [{'证券代码': '688001', '上市日期': '2020-01-01'}],
            'sz': [{'A股代码': '000001', 'A股上市日期': '2000-01-01'},
                   {'A股代码': '300001', 'A股上市日期': '2020-01-01'}],
            'bj': [{'证券代码': '920001', '上市日期': '2020-01-01'}]}
        spot = [{'代码': c, '成交额': 10} for c in ['600001', '688001', '000001', '300001', '920001']]
        official = [{'证券类别': k, '成交金额': 10} for k in ['主板A股', '创业板A股']]
        return spot, rosters, official

    def test_matching_codes_and_turnover_do_not_prove_timestamps(self):
        spot, rosters, official = self.fixtures()
        result = reconcile_market(spot, rosters, '2026-10-23', official)
        self.assertEqual(result['status'], 'code_coverage_matched')
        self.assertEqual(result['szse_turnover_check']['status'], 'within_tolerance')
        self.assertFalse(result['all_market_verified'])

    def test_missing_stock_and_roster_are_not_zero(self):
        spot, rosters, official = self.fixtures()
        result = reconcile_market(spot[:-1], rosters, '2026-10-23', official)
        self.assertEqual(result['missing_codes'], ['920001'])
        rosters['bj'] = None
        result = reconcile_market(spot, rosters, '2026-10-23', official)
        self.assertIsNone(result['expected_count'])
        self.assertEqual(result['status'], 'unavailable')

    def test_official_roster_retry_preserves_first_failure(self):
        spot, rosters, official = self.fixtures()
        class Fake:
            timeout = 45
            def __init__(self):
                self.calls = {}
            def call(self, key, function, **kwargs):
                self.calls[key] = {'status': 'ok'}
                if key == 'official_roster_sz':
                    self.calls[key]['status'] = 'error'
                    return None
                if key.startswith('official_roster_'):
                    name = key.removeprefix('official_roster_').split('_retry')[0]
                    return rosters[name]
                return official
        c = Fake()
        result = collect_reconciliation(c, spot, '2026-10-23')
        self.assertEqual(result['status'], 'code_coverage_matched')
        self.assertEqual(c.calls['official_roster_sz']['status'], 'error')
        self.assertEqual(c.calls['official_roster_sz_retry1']['status'], 'ok')

    def test_duplicates_and_missing_amount_are_not_verified(self):
        spot, rosters, official = self.fixtures()
        result = reconcile_market(spot + [spot[0]], rosters, '2026-10-23', official)
        self.assertEqual(result['duplicate_codes'], ['600001'])
        self.assertEqual(result['szse_turnover_check']['status'], 'not_comparable')
        spot[2]['成交额'] = None
        result = reconcile_market(spot, rosters, '2026-10-23', official)
        self.assertEqual(result['szse_turnover_check']['status'], 'not_comparable')

    def test_csi_official_fallback_checks_symbol_and_date(self):
        class Fake:
            def __init__(self):
                self.calls = {}
                self.code = '932000'
            def call(self, key, function, **kwargs):
                self.calls[key] = {'status': 'error'}
                if function.endswith('_csindex'):
                    self.calls[key] = {'status': 'ok', 'parameters': kwargs}
                    return [{'日期': '2026-10-23', '指数代码': self.code, '收盘': 2856.27}]
                return None
        c = Fake()
        self.assertEqual(collect_index(c, 'csi932000', '2026-10-23')['close'], 2856.27)
        self.assertEqual(c.calls['index_official_csi932000']['parameters']['symbol'], '932000')
        c.code = '000001'
        self.assertIsNone(collect_index(c, 'csi932000', '2026-10-23'))
        self.assertEqual(c.calls['index_official_csi932000']['status'], 'date_or_schema_error')

    def test_daily_supplement_fills_code_but_leaves_direction_unknown(self):
        spot, rosters, official = self.fixtures()
        spot = [r for r in spot if r['代码'] != '688001']
        class Fake:
            timeout, calls = 45, {}
            def call(self, key, function, **kwargs):
                if key.startswith('official_roster_'):
                    return rosters[key.removeprefix('official_roster_')]
                if key == 'official_szse_summary':
                    return official
                return [dict(date='2026-10-23', open=10, high=11, low=9, close=10, amount=100)]
        c = Fake()
        result = collect_reconciliation(c, spot, '2026-10-23')
        self.assertEqual(result['status'], 'code_coverage_matched')
        self.assertEqual(result['daily_supplement_codes'], ['688001'])
        self.assertIsNone(spot[-1]['涨跌幅'])
        self.assertFalse(result['all_market_verified'])
        self.assertEqual(c.timeout, 45)
