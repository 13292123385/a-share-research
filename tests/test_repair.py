from datetime import datetime
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from collector.inventory import classify, inventory
from collector.providers import parse_tencent_quote
from collector.run import check_rows, dump, table, main, TZ
from collector.model import normalize
from collector.validate import validate


class RepairTests(unittest.TestCase):
    def test_historical_scope_is_explicit_and_limits_are_not_hidden(self):
        s = dict(verified={'mainboard_limit_up_count': 64, 'indices': [1, 2, 3, 4]},
                 missing_data=['无法恢复历史实时快照'], source_failures={}, candidate_price_quality={'missing_codes': []})
        classify(s, True)
        self.assertEqual(s['collection_status'], 'complete')
        self.assertEqual(s['status'], 'complete_with_limitations')
        self.assertEqual(s['research_status'], 'limited')
        self.assertIn('historical', s['collection_scope'])
        s['source_failures']['limit_up'] = {'status': 'error'}
        classify(s, True)
        self.assertEqual(s['collection_status'], 'partial')

    def test_empty_pool_and_invalid_ohlc_remain_unknown(self):
        class C:
            calls = {'pool': {}}
        self.assertIsNone(check_rows(C(), 'pool', [], ['代码']))
        self.assertEqual(C.calls['pool']['status'], 'empty_unverified')
        row = {'代码': '600001', '名称': '测试', '连板数': 1}
        quote = {'600001': {'今开': 0, '最高': 0, '最低': 0, '最新价': 0}}
        self.assertIsNone(normalize([row], quote)[0]['all_day_one_word'])

    def test_quote_rejects_stale_date_wrong_identity_and_intraday(self):
        fields = [''] * 38
        for i, value in {1: '九号公司', 2: '689009', 3: '36.33', 5: '36.79',
                         30: '20261026161448', 32: '-1.30', 33: '37.06', 34: '35.89', 37: '32549'}.items():
            fields[i] = value
        def payload():
            return 'v_sh689009="' + '~'.join(fields) + '";'
        r = parse_tencent_quote(payload(), 'sh689009', '2026-10-26')
        self.assertEqual(r['涨跌幅'], -1.3)
        self.assertEqual(r['成交额'], 325490000)
        with self.assertRaises(ValueError):
            parse_tencent_quote(payload(), 'sh689009', '2026-10-23')
        fields[30] = '20261026145900'
        with self.assertRaises(ValueError):
            parse_tencent_quote(payload(), 'sh689009', '2026-10-26')
        fields[30], fields[2] = '20261026161448', '600001'
        with self.assertRaises(ValueError):
            parse_tencent_quote(payload(), 'sh689009', '2026-10-26')

    def test_inventory_counts_nulls_and_detects_csv_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / '2026-10-23/runs/a'
            dump(root / 'summary.json', {'schema_version': 2, 'trade_date': '2026-10-23'})
            dump(root / 'sources.json', {})
            table(root / 'clean/sample', [{'code': '600001', 'name': '测试', 'entry_price': None}])
            manifest = inventory(root, {})
            record = next(r for r in manifest if r['path'] == 'clean/sample.json')
            self.assertEqual(record['records'], 1)
            self.assertEqual(record['missing_fields'], {'entry_price': 1})
            self.assertEqual(validate(tmp), [])
            (root / 'clean/sample.csv').write_text('code,name\n', encoding='utf-8')
            self.assertTrue(any('checksum mismatch' in s for s in validate(tmp)))
            self.assertTrue(any('record count mismatch' in s for s in validate(tmp)))
        self.assertTrue(validate('nonexistent-archive-for-test'))

    def test_calendar_lower_bound_cannot_claim_coverage(self):
        def call(c, key, function, **kwargs):
            c.calls[key] = {'status': 'ok', 'rows': 1}
            return [{'trade_date': '2026-10-23'}]
        with tempfile.TemporaryDirectory() as tmp, patch('collector.run.Collector.call', new=call), \
                patch('collector.run.datetime') as clock, \
                patch('sys.argv', ['collector', '--date', '2026-01-01', '--output', tmp]):
            clock.now.return_value = datetime(2026, 10, 26, 21, tzinfo=TZ)
            self.assertEqual(main(), 2)
            s = json.loads(next(Path(tmp).glob('*/runs/*/summary.json')).read_text())
            self.assertFalse(s['calendar_covered'])
            self.assertEqual(s['status'], 'calendar_unknown')
