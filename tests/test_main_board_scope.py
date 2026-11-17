import json
import tempfile
import unittest
from pathlib import Path
from collector.market_snapshot import load_rosters, is_main_board
from collector.reconcile import ROSTERS
from collector.snapshot_public import make_files, should_promote


class MainBoardScopeTests(unittest.TestCase):
    def test_legacy_publisher_cannot_restore_all_market_latest(self):
        old = dict(trade_date='2026-11-17', universe='cn_main_board', status='complete')
        self.assertFalse(should_promote(dict(trade_date='2026-11-18', status='complete'), old))

    def test_only_official_main_rosters_and_quotes_are_used(self):
        calls = []
        class Client:
            timeout = 20
            def call(self, key, function, **kwargs):
                entry = next(x for x in ROSTERS if x[1] == function and x[2] == kwargs)
                name, _, _, code_key, date_key = entry
                calls.append(name)
                if name not in ('sh_main', 'sz'):
                    raise AssertionError('Excluded exchange must not be queried')
                codes = ['600000', '603001'] if name == 'sh_main' else ['000001', '002001', '300001', '301001']
                return [{code_key: code, date_key: '2020-01-01'} for code in codes]
        with tempfile.TemporaryDirectory() as folder:
            symbols, unavailable = load_rosters(Client(), folder, '2026-11-17')
            self.assertEqual(symbols, ['sh600000', 'sh603001', 'sz000001', 'sz002001'])
            self.assertEqual(unavailable, [])
            self.assertEqual(calls, ['sh_main', 'sz'])
            cached = json.loads((Path(folder)/'2026-11-17/rosters.json').read_text(encoding='utf-8'))
            self.assertEqual(set(cached), {'sh_main', 'sz'})
            self.assertEqual(len(cached['sz']), 2)

    def test_main_board_code_boundaries(self):
        for code in ['600000', '601001', '603001', '605001', '000001', '001001', '002001', '003001']:
            self.assertTrue(is_main_board(code))
        for code in ['300001', '301001', '688001', '689001', '920001', '830001', '900001', '200001', None]:
            self.assertFalse(is_main_board(code))

    def test_public_export_rejects_out_of_scope_rows(self):
        snapshot = dict(session='midday', status='complete', universe='cn_main_board', records=1,
                        rows=[{'代码': '300001'}])
        with self.assertRaisesRegex(ValueError, 'out-of-scope'):
            make_files(snapshot, '13292123385/a-share-market-data')
