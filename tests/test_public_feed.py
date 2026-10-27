from datetime import datetime
import json
from pathlib import Path
import tempfile
import unittest
from collector.public_feed import make_files, TZ


class PublicFeedTests(unittest.TestCase):
    def fixture(self, folder):
        daily = Path(folder) / '2026-10-26'
        run = daily / 'runs' / 'a'
        (run / 'clean').mkdir(parents=True)
        (daily / 'latest.json').write_text(json.dumps({'run_id': 'a'}), encoding='utf-8')
        summary = dict(trade_date='2026-10-26', trading_day=True, status='complete_with_limitations',
            collection_status='complete', research_status='limited', fetched_at='2026-10-26T16:00:00+08:00',
            missing_data=['missing older archive'], private_note='PRIVATE_SENTINEL',
            verified={'mainboard_limit_up_count': 1, 'indices': [], 'secret': 'PRIVATE_SENTINEL'})
        (run / 'summary.json').write_text(json.dumps(summary), encoding='utf-8')
        for name in ('limit_up', 'first_board_candidates', 'broken', 'limit_down'):
            (run / 'clean' / (name + '.json')).write_text(json.dumps([
                dict(code='600001', name='sample', height=1, private_note='PRIVATE_SENTINEL',
                     execution_verified=False, price_date=None)]), encoding='utf-8')
        return run

    def test_public_allowlist_does_not_copy_private_fields(self):
        with tempfile.TemporaryDirectory() as folder:
            self.fixture(folder)
            files = make_files(folder, datetime(2026, 10, 27, 16, tzinfo=TZ))
            self.assertNotIn('PRIVATE_SENTINEL', ''.join(files.values()))
            payload = json.loads(files['latest.json'])
            self.assertEqual(payload['trade_date'], '2026-10-26')
            self.assertIsNone(payload['verified_tradable_rate'])
            self.assertIsNone(json.loads(files['limit_up.json'])[0]['price_date'])
            self.assertIn('2026-10-26', files['latest.md'])

    def test_failed_attempt_does_not_change_selected_market_date(self):
        with tempfile.TemporaryDirectory() as folder:
            self.fixture(folder)
            run = Path(folder) / '2026-10-27/runs/b'
            run.mkdir(parents=True)
            (run / 'summary.json').write_text(json.dumps(dict(trade_date='2026-10-27',
                fetched_at='2026-10-27T16:00:00+08:00', status='partial', collection_status='partial',
                collection_failures=['market_snapshot'])), encoding='utf-8')
            payload = json.loads(make_files(folder)['latest.json'])
            self.assertEqual(payload['trade_date'], '2026-10-26')
            self.assertEqual(payload['last_attempt']['trade_date'], '2026-10-27')
            self.assertEqual(payload['last_attempt']['collection_status'], 'partial')

    def test_empty_directory_is_not_publishable_market(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                make_files(folder)
