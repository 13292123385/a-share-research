from datetime import datetime
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from collector.followup import archived_cohorts, followup_rows, normalize_sina_spot
from collector.quality import collect_index
from collector.run import main, TZ
from collector.ci_summary import main as ci_main


class FollowupTests(unittest.TestCase):
    def test_ci_summary_does_not_present_old_archive_as_current(self):
        with patch.dict('os.environ', {'GITHUB_ACTIONS': 'true', 'COLLECT_SUMMARY_FILE': '',
                                      'GITHUB_STEP_SUMMARY': ''}), patch('builtins.print') as output:
            ci_main()
            self.assertIn('未产生采集摘要', output.call_args.args[0])
    def test_trading_sessions_skip_weekend_and_do_not_shift_missing_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            daily = Path(tmp) / '2026-10-23'
            pool = daily / 'runs' / 'a' / 'clean'
            pool.mkdir(parents=True)
            (daily / 'latest.json').write_text(json.dumps({'run_id': 'a'}))
            (pool / 'limit_up.json').write_text(json.dumps([
                dict(code='600001', name='测试', height=1, eligible_observation=True),
                dict(code='600002', name='测试二', height=2)]))
            cohorts, missing = archived_cohorts(tmp,
                ['2026-10-22', '2026-10-23', '2026-10-26', '2026-10-27'], '2026-10-27')
            self.assertEqual(missing, ['2026-10-26'])
            self.assertEqual(cohorts[0]['sessions_since_first'], 2)
            self.assertEqual(len(cohorts), 1)
            rows = followup_rows(cohorts, {}, '2026-10-27')
            self.assertEqual(rows[0]['status'], 'missing_price')
            self.assertIsNone(rows[0]['third_day_return'])
            prices = {'600001': dict(date='2026-10-27', open=10, high=11, low=9, close=10)}
            rows = followup_rows(cohorts, prices, '2026-10-27')
            self.assertEqual(rows[0]['status'], 'price_available')
            self.assertFalse(rows[0]['execution_verified'])

    def test_sina_scope_and_code_normalization(self):
        rows = normalize_sina_spot([
            {'代码': 'sh600001', '今开': 10}, {'代码': 'sz300001', '今开': 10},
            {'代码': 'bj920001', '今开': 10}, {'代码': '200001'}, {'代码': 'garbage'}])
        self.assertEqual([r['代码'] for r in rows], ['600001', '300001'])

    def test_invalid_index_date_activates_fallback(self):
        class Fake:
            def __init__(self):
                self.calls = {}
            def call(self, key, function, **kwargs):
                self.calls[key] = {'status': 'ok', 'parameters': kwargs}
                return [{'date': '2026-10-23' if function.endswith('_tx') else '2026-10-22', 'close': 10}]
        c = Fake()
        self.assertEqual(collect_index(c, 'sh000001', '2026-10-23')['date'], '2026-10-23')
        self.assertEqual(c.calls['index_sh000001']['status'], 'date_or_schema_error')
        self.assertEqual(c.calls['index_fallback_sh000001']['parameters']['end_date'], '20261023')

    def test_full_pipeline_with_spot_failure_and_historical_fallback(self):
        def call(c, key, function, **kwargs):
            if key == 'calendar':
                rows = [{'trade_date': d} for d in ['2026-10-22', '2026-10-23', '2026-10-26']]
            elif key in ('spot', 'spot_fallback'):
                rows = None
            elif key.startswith('index'):
                rows = [{'date': '2026-10-23', 'close': 10}]
            elif key.startswith('price_'):
                rows = [{'date': '2026-10-23', 'open': 10, 'high': 11, 'low': 10, 'close': 11}]
            else:
                rows = [{'代码': '600001', '名称': '测试', '连板数': 1,
                         '首次封板时间': '100000', '最后封板时间': '145000', '炸板次数': 1}]
            c.calls[key] = dict(status='ok' if rows else 'error', rows=len(rows) if rows else None)
            return rows
        with tempfile.TemporaryDirectory() as tmp:
            with patch('collector.run.Collector.call', new=call), patch('collector.run.datetime') as clock, \
                    patch('sys.argv', ['collector', '--date', '2026-10-23', '--output', tmp]):
                clock.now.return_value = datetime(2026, 10, 23, 16, tzinfo=TZ)
                self.assertEqual(main(), 2)
            pointer = json.loads((Path(tmp) / '2026-10-23/latest.json').read_text())
            run = Path(tmp) / '2026-10-23/runs' / pointer['run_id']
            summary = json.loads((run / 'summary.json').read_text(encoding='utf-8'))
            self.assertEqual(summary['candidate_price_quality']['historical_fetched'], 1)
            self.assertTrue((run / 'clean/first_board_followup.json').exists())
            clean = json.loads((run / 'clean/limit_up.json').read_text(encoding='utf-8'))
            self.assertTrue(clean[0]['eligible_observation'])
