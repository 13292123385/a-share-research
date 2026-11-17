from datetime import datetime
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from collector.market_snapshot import (TZ, archive_snapshot, capture, parse_batch, parse_quote,
                                       session_for, validate_snapshot)


def quote_fields(code='600000', stamp='20261116113000'):
    fields = [''] * 47
    for index, value in {1: '样本股票', 2: code, 3: '10.2', 4: '10', 5: '10.1',
                         6: '100', 30: stamp, 31: '.2', 32: '2', 33: '10.5',
                         34: '9.9', 37: '10.2', 38: '1', 39: '12', 44: '50',
                         45: '100', 46: '1.1'}.items():
        fields[index] = value
    return fields


class MarketSnapshotTests(unittest.TestCase):
    def test_missed_capture_window_is_not_a_successful_cli_run(self):
        from collector.market_snapshot import main
        with patch('sys.argv', ['market_snapshot', '--session', 'midday']), \
                patch('collector.market_snapshot.capture', return_value=None), \
                self.assertRaises(SystemExit) as result:
            main()
        self.assertEqual(result.exception.code, 2)

    def test_midday_has_strict_capture_and_quote_window(self):
        for hour, minute, requested, expected in [(11, 29, 'midday', None),
                (11, 30, 'midday', 'midday'), (12, 59, 'auto', 'midday'),
                (13, 0, 'midday', None), (14, 59, 'close', None),
                (15, 0, 'auto', 'close'), (15, 1, 'midday', None)]:
            self.assertEqual(session_for(datetime(2026, 11, 16, hour, minute, tzinfo=TZ), requested), expected)
        afternoon = parse_quote('sh600000', quote_fields(stamp='20261116130000'), '2026-11-16', 'midday')
        self.assertEqual(afternoon['quote_status'], 'stale')

    def test_parser_identity_units_time_and_no_synthetic_missing(self):
        row = parse_quote('sh600000', quote_fields(), '2026-11-16', 'midday')
        self.assertEqual(row['quote_status'], 'fresh')
        self.assertEqual(row['成交量'], 10000)
        self.assertEqual(row['成交额'], 102000)
        self.assertEqual(row['总市值'], 10000000000)
        self.assertEqual(row['quote_timestamp'], '2026-11-16T11:30:00+08:00')
        fields = quote_fields()
        fields[39] = ''
        missing = parse_quote('sh600000', fields, '2026-11-16', 'midday')
        self.assertIsNone(missing['市盈率'])
        self.assertIn('市盈率', missing['missing_fields'])
        with self.assertRaises(ValueError):
            parse_quote('sh600001', fields, '2026-11-16', 'midday')

    def test_stale_suspended_and_inconsistent_ohlc_are_explicit(self):
        old = parse_quote('sh600000', quote_fields(stamp='20261113150000'), '2026-11-16', 'close')
        self.assertEqual(old['quote_status'], 'stale')
        fields = quote_fields(stamp='20261116150000')
        for index in (5, 6, 33, 34, 37):
            fields[index] = '0'
        suspended = parse_quote('sh600000', fields, '2026-11-16', 'close')
        self.assertEqual(suspended['quote_status'], 'suspended_or_no_trade')
        self.assertFalse(suspended['suspension_verified'])
        fields[6] = '100'
        bad = parse_quote('sh600000', fields, '2026-11-16', 'close')
        self.assertIn('ohlc_order', bad['validation_errors'])

    def test_coverage_exact_set_duplicates_and_stale_required(self):
        row = parse_quote('sh600000', quote_fields(), '2026-11-16', 'midday')
        self.assertEqual(validate_snapshot([row], {'600000'})[0], 'complete')
        for rows, expected, unavailable in [([row], {'600000', '600001'}, []),
                ([row, row], {'600000'}, []), ([row], {'600000'}, ['bj']),
                ([row], {'600001'}, [])]:
            self.assertEqual(validate_snapshot(rows, expected, unavailable)[0], 'partial')
        stale = parse_quote('sh600000', quote_fields(stamp='20261113150000'), '2026-11-16', 'close')
        self.assertEqual(validate_snapshot([stale], {'600000'})[0], 'partial')

    def test_batch_retains_duplicates_and_reports_omitted_symbol(self):
        text = 'v_sh600000="' + '~'.join(quote_fields()) + '";'
        rows, errors = parse_batch(text + text, ['sh600000', 'sz000001'], '2026-11-16', 'midday')
        self.assertEqual(len(rows), 2)
        self.assertEqual(errors['sz000001'], 'missing_quote')
        self.assertEqual(validate_snapshot(rows, {'600000', '000001'})[0], 'partial')

    def test_complete_pointer_survives_partial_later_attempt(self):
        with tempfile.TemporaryDirectory() as folder:
            snapshot = dict(trade_date='2026-11-16', session='midday', run_id='a',
                            status='complete', records=1, rows=[{'代码': '600000'}])
            root, promoted = archive_snapshot(folder, snapshot)
            self.assertTrue(promoted)
            snapshot.update(run_id='b', status='partial', records=0, rows=[])
            _, promoted = archive_snapshot(folder, snapshot)
            self.assertFalse(promoted)
            daily = Path(folder) / '2026-11-16/midday'
            self.assertEqual(json.loads((daily / 'latest.json').read_text(encoding='utf-8'))['run_id'], 'a')
            self.assertEqual(json.loads((daily / 'last_attempt.json').read_text(encoding='utf-8'))['run_id'], 'b')
            self.assertTrue((root / 'snapshot.json').exists())
            snapshot.update(session='close', run_id='c', status='complete')
            archive_snapshot(folder, snapshot)
            self.assertEqual(json.loads((daily / 'latest.json').read_text(encoding='utf-8'))['run_id'], 'a')

    def test_missing_or_holiday_calendar_does_not_request_quotes_or_promote(self):
        class FakeCollector:
            calendar = None

            def __init__(self, root, **kwargs):
                pass

            def call(self, key, function, **kwargs):
                if function != 'tool_trade_date_hist_sina':
                    raise AssertionError('Calendar failure must prevent quote collection')
                return self.calendar

        now = datetime(2026, 11, 16, 11, 40, tzinfo=TZ)
        with tempfile.TemporaryDirectory() as folder:
            result = capture(folder, 'midday', now, FakeCollector, now_fn=lambda: now)
            self.assertEqual(result['status'], 'calendar_unknown')
            self.assertFalse((Path(folder) / '2026-11-16/midday/latest.json').exists())
            FakeCollector.calendar = [{'trade_date': '2026-11-13'}, {'trade_date': '2026-11-17'}]
            result = capture(folder, 'midday', now, FakeCollector, now_fn=lambda: now)
            self.assertEqual(result['status'], 'skipped')
            self.assertEqual(result['reason'], 'non_trading_day')


if __name__ == '__main__':
    unittest.main()
