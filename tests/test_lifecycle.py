import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock
from collector.lifecycle import observations, collect_prices
import json
import hashlib
from unittest.mock import patch
from collector.lifecycle import main, manual_watch
from collector.lifecycle_validate import validate_run
from collector.lifecycle_public import make_files, publish
from collector.run import dump, table
from collector.themes import collect_themes

class LifecycleTests(unittest.TestCase):
    def test_missing_archive_never_confirms_break(self):
        row = dict(code='600001', name='示例', height=4)
        days = ['2026-10-09', '2026-10-12', '2026-10-13']
        watch = observations(dict(zip(days, [[row], None, []])), days, days[-1])
        self.assertIsNone(watch[0]['last_confirmed_break_date'])

    def test_twenty_sessions_and_no_lookahead(self):
        from datetime import date, timedelta
        start = date(2026, 9, 1)
        days = [(start + timedelta(days=i)).isoformat() for i in range(45)
                if (start + timedelta(days=i)).weekday() < 5]
        row = dict(code='600001', name='示例', height=4)
        pools = {d: [row] if i == 0 else [] for i, d in enumerate(days)}
        watch = observations(pools, days, days[21])
        self.assertEqual(watch[0]['sessions_after_break'], 20)
        self.assertEqual(watch[0]['last_confirmed_break_date'], days[1])
        self.assertEqual(observations(pools, days, days[0])[0]['last_confirmed_break_date'], None)
        c = Mock(delay=0)
        prices = collect_prices(c, watch, days, days[21], 0)
        self.assertEqual(len(prices), 22)
        self.assertTrue(all(r['status'] == 'missing_price' for r in prices))
        c.call.assert_not_called()

    def test_duplicate_prices_and_missing_volume(self):
        row = dict(date='2026-10-12', open=10, high=11, low=9, close=10, volume=None)
        c = Mock(delay=0)
        c.call.return_value = [row, row]
        watch = [dict(code='600001', first_observed='2026-10-12')]
        result = collect_prices(c, watch, ['2026-10-12'], '2026-10-12', 10)
        self.assertEqual(result[0]['status'], 'missing_price')
        c.call.return_value = [row]
        self.assertEqual(collect_prices(c, watch, ['2026-10-12'], '2026-10-12', 10)[0]['status'], 'missing_volume')

    def test_manual_evidence_is_required_and_not_future(self):
        with self.assertRaises(ValueError):
            manual_watch([dict(code='600001', name='示例')], ['2026-10-12'], '2026-10-12')
        row = dict(code='600001', name='示例', evidence_url='https://example.com/fixture',
                   reviewer='private-reviewer', observed_at='2026-10-13T10:00:00+08:00')
        self.assertEqual(manual_watch([row], ['2026-10-12', '2026-10-13'], '2026-10-12'), [])

    def test_themes_historical_never_calls_live_mapping(self):
        c = Mock()
        self.assertEqual(collect_themes(c, '2026-10-12', '2026-10-13', 30)[3], 'historical_membership_unavailable')
        c.call.assert_not_called()

    def test_membership_is_point_in_time_and_failures_explicit(self):
        c = Mock(delay=0, timeout=15)
        c.calls = {'concept_catalog':dict(fetched_at='2026-10-12T16:00:00+08:00')}
        c.call.side_effect = [[{'板块代码':'BK0001', '板块名称':'测试题材'}],
                              [{'代码':'600001', '名称':'示例'}]]
        catalog, members, coverage, status = collect_themes(c, '2026-10-12', '2026-10-12', 30)
        self.assertEqual(status, 'available')
        self.assertIsNone(members[0]['historical_valid_from'])
        self.assertIsNone(catalog[0]['lifecycle_stage'])
        self.assertEqual(coverage[0]['member_count'], 1)
        c.call.side_effect = [[{'板块代码':'BK0001', '板块名称':'测试题材'}],
                              [{'代码':'600001'}, {'代码':'600001'}]]
        self.assertEqual(collect_themes(c, '2026-10-12', '2026-10-12', 30)[2][0]['status'], 'schema_error')

    def test_cache_preserved_with_zero_budget(self):
        c = Mock(delay=0)
        price = dict(date='2026-10-12', open=10, high=11, low=9, close=10,
                     volume=100, amount=None, adjustment='none', source='test fixture')
        cached = [dict(code='600001', observation_date='2026-10-12', price=price,
                       status='available', execution_verified=False, entry_price=None, origin_run='fixture')]
        rows = collect_prices(c, [dict(code='600001', first_observed='2026-10-12')],
                              ['2026-10-12'], '2026-10-12', 0, cached)
        self.assertEqual(rows[0]['price'], price)
        self.assertTrue(rows[0]['reused_from_prior_run'])
        c.call.assert_not_called()

    def test_end_to_end_append_only_replay_quality_public(self):
        # Synthetic provider fixtures belong only to tests, never production archives.
        def call(c, key, function, **kwargs):
            if function == 'dated_theme_evidence':
                rows = []
            elif function == 'tool_trade_date_hist_sina':
                rows = [dict(trade_date=d) for d in ('2026-10-09','2026-10-12')]
            else:
                rows = [dict(date=d, open=10, high=11, low=9, close=10, volume=100)
                        for d in ('2026-10-09','2026-10-12')]
            table(c.root / 'raw' / key, rows)
            c.calls[key] = dict(status='ok', fetched_at='2026-10-12T16:00:00+08:00',
                                sha256=hashlib.sha256((c.root / 'raw' / (key+'.json')).read_bytes()).hexdigest())
            dump(c.root / 'sources.json', c.calls)
            return rows
        with tempfile.TemporaryDirectory() as tmp:
            data, output = Path(tmp)/'data', Path(tmp)/'lifecycle'
            day = data/'2026-10-09'
            dump(day/'latest.json', dict(run_id='fixture'))
            dump(day/'runs/fixture/summary.json', dict(trade_date='2026-10-09', trading_day=True))
            dump(day/'runs/fixture/clean/limit_up.json', [dict(code='600001',name='示例',height=4)])
            args = ['lifecycle','--date','2026-10-12','--data',str(data),'--output',str(output)]
            with patch('collector.lifecycle.Collector.call', call), patch('sys.argv', args):
                self.assertEqual(main(), 2)  # historical concept membership correctly remains missing
            root = next(output.glob('*/runs/*'))
            before = {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
            self.assertEqual(validate_run(root), [])
            files = make_files(root)
            self.assertTrue(all('/' not in name for name in files))
            self.assertNotIn('archive_inputs', str(files))
            with patch('sys.argv', ['lifecycle','--date','2026-10-12','--replay',str(root)]):
                self.assertEqual(main(), 0)
            with patch('collector.lifecycle.Collector.call', call), patch('sys.argv', args):
                self.assertEqual(main(), 2)
            self.assertEqual(len(list(output.glob('*/runs/*'))), 2)
            self.assertEqual(before, {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()})
            (root/'clean/leader_prices.json').write_text('[]', encoding='utf-8')
            self.assertTrue(validate_run(root))
            with self.assertRaises(ValueError):
                make_files(root)

    def test_public_publish_only_writes_lifecycle_namespace(self):
        session = Mock()
        session.request.side_effect = [Mock(ok=True, **{'json.return_value':{'object':{'sha':'head'}}}),
            Mock(ok=True, **{'json.return_value':{'tree':{'sha':'base'}}}),
            Mock(ok=True, **{'json.return_value':{'sha':'tree'}}),
            Mock(ok=True, **{'json.return_value':{'sha':'commit'}})]
        session.get.side_effect = [Mock(status_code=404), Mock(status_code=404)]
        session.patch.return_value.ok = True
        files = {'latest.json':json.dumps(dict(trade_date='2026-10-12',run_id='fixture',coverage=[],missing_archive_dates=[])),
                 'leader_watch.json':'[]'}
        with patch('collector.lifecycle_public.requests.Session', return_value=session):
            publish(files, 'fixture/repository', 'test-token')
        tree = session.request.call_args_list[2].kwargs['json']
        paths = [r['path'] for r in tree['tree']]
        self.assertTrue(all(p.startswith('lifecycle/') for p in paths))
        self.assertIn('lifecycle/latest.json', paths)
        self.assertIn('lifecycle/archive/2026-10-12/fixture/latest.json', paths)
        self.assertFalse(session.patch.call_args.kwargs['json']['force'])

    def test_public_partial_cannot_replace_better_same_day(self):
        import base64
        session = Mock()
        session.request.side_effect = [Mock(ok=True, **{'json.return_value':{'object':{'sha':'head'}}}),
            Mock(ok=True, **{'json.return_value':{'tree':{'sha':'base'}}}),
            Mock(ok=True, **{'json.return_value':{'sha':'tree'}}),
            Mock(ok=True, **{'json.return_value':{'sha':'commit'}})]
        old = dict(trade_date='2026-10-12', coverage=['price:600001:2026-10-12'], missing_archive_dates=[])
        session.get.side_effect = [Mock(status_code=200, **{'json.return_value':{'content':base64.b64encode(json.dumps(old).encode()).decode()}}), Mock(status_code=404)]
        session.patch.return_value.ok = True
        with patch('collector.lifecycle_public.requests.Session', return_value=session):
            publish({'latest.json':json.dumps(dict(trade_date='2026-10-12',run_id='fixture',coverage=[],missing_archive_dates=[]))}, 'fixture/repository', 'test-token')
        paths = [r['path'] for r in session.request.call_args_list[2].kwargs['json']['tree']]
        self.assertTrue(all(p.startswith('lifecycle/archive/') for p in paths))
