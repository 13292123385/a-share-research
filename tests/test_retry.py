import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from collector.retry import pending_date

class RetryTests(unittest.TestCase):
    def test_midnight_retries_previous_closed_day(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / '2026-10-30').mkdir()
            self.assertEqual(pending_date(['2026-10-30','2026-11-02','2026-11-03'], datetime(2026,11,3,2), root), '2026-10-30')
    def test_today_gets_live_snapshot_before_backlog(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / '2026-10-30').mkdir()
            self.assertEqual(pending_date(['2026-10-30','2026-11-02'], datetime(2026,11,2,15,5), root), '2026-11-02')
    def test_complete_day_is_not_recollected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            daily = root / '2026-11-02'
            run = daily / 'runs' / 'test'
            run.mkdir(parents=True)
            (daily / 'latest.json').write_text(json.dumps({'run_id':'test'}))
            (run / 'summary.json').write_text(json.dumps({'trade_date':'2026-11-02','status':'complete'}))
            self.assertIsNone(pending_date(['2026-11-02','2026-11-03'], datetime(2026,11,3,2), root))
