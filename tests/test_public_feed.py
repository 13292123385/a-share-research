from datetime import datetime
import base64
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, Mock
from collector.public_feed import make_files, publish, publish_repository, MARKET_FIELDS, TZ


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

    def test_all_market_rows_are_exported_without_private_fields_or_zero_fill(self):
        with tempfile.TemporaryDirectory() as folder:
            run = self.fixture(folder)
            rows = [dict(代码=f'{600000 + i:06d}', 名称='sample', 最新价=12.5,
                         成交量=None, 私人字段='PRIVATE_SENTINEL') for i in range(251)]
            (run / 'clean/market_quotes.json').write_text(json.dumps(rows), encoding='utf-8')
            files = make_files(folder)
            full = json.loads(files['market_snapshot.json'])
            manifest = json.loads(files['market_snapshot/manifest.json'])
            self.assertEqual(full['records'], 251)
            exported = [row for part in manifest['parts']
                        for row in json.loads(files[part['file']])['rows']]
            self.assertEqual(exported, full['rows'])
            self.assertEqual(sum(part['records'] for part in manifest['parts']), 251)
            self.assertEqual([row['代码'] for row in exported], [row['代码'] for row in rows])
            self.assertEqual(set(exported[0]), set(MARKET_FIELDS))
            self.assertIsNone(exported[0]['成交量'])
            self.assertIsNone(exported[0]['quote_timestamp'])
            self.assertNotIn('PRIVATE_SENTINEL', ''.join(files.values()))
            self.assertFalse(full['all_market_verified'])
            self.assertEqual(json.loads(files['latest.json'])['market_snapshot']['records'], 251)
            self.assertIn('market/index.md', files['START_HERE.md'])

    def test_missing_market_archive_is_explicit_not_empty_complete(self):
        with tempfile.TemporaryDirectory() as folder:
            self.fixture(folder)
            files = make_files(folder)
            snapshot = json.loads(files['market_snapshot.json'])
            self.assertEqual(snapshot['status'], 'missing')
            self.assertIsNone(snapshot['records'])
            self.assertIsNone(snapshot['rows'])
            self.assertEqual(json.loads(files['market_snapshot/manifest.json'])['parts'], [])

    @patch.dict('os.environ', {'PUBLIC_FEED_REPOSITORY': 'owner/public-market'})
    @patch('collector.public_feed.requests.patch')
    def test_gist_is_small_summary_mirror_with_public_market_link(self, request):
        request.return_value = Mock(status_code=200)
        request.return_value.json.return_value = {'html_url': 'https://gist.github.com/example'}
        publish({'latest.json': '{}', 'market_snapshot.json': 'LARGE',
                 'market_snapshot/part-001.json': 'LARGE',
                 'market_snapshot/manifest.json': '{}'}, 'id', 'test-token')
        sent = request.call_args.kwargs['json']['files']
        self.assertIn('latest.json', sent)
        self.assertNotIn('market_snapshot.json', sent)
        self.assertFalse(any('/' in name for name in sent))
        self.assertIn('owner/public-market/main/market_snapshot/manifest.json',
                      sent['FULL_MARKET.md']['content'])

    @patch('collector.public_feed.requests.Session')
    def test_repository_retries_new_head_and_deduplicates_large_blobs(self, session_factory):
        client = session_factory.return_value
        trees, commits, patches, blob_bodies = [], [], [], []
        heads = iter(('old-head', 'concurrent-head'))
        def response(status, payload):
            result = Mock(status_code=status, ok=200 <= status < 300)
            result.json.return_value = payload
            return result
        def request(method, url, json=None, timeout=None):
            if method == 'GET' and url.endswith('/git/ref/heads/main'):
                return response(200, {'object': {'sha': next(heads)}})
            if method == 'GET' and '/git/commits/' in url:
                return response(200, {'tree': {'sha': url.rsplit('/', 1)[1] + '-tree'}})
            if method == 'POST' and url.endswith('/git/blobs'):
                blob_bodies.append(json)
                return response(201, {'sha': 'large-blob'})
            if method == 'POST' and url.endswith('/git/trees'):
                trees.append(json)
                return response(201, {'sha': 'new-tree'})
            if method == 'POST' and url.endswith('/git/commits'):
                commits.append(json)
                return response(201, {'sha': 'commit-' + str(len(commits))})
            if method == 'PATCH' and url.endswith('/git/refs/heads/main'):
                patches.append(json)
                return response(422 if len(patches) == 1 else 200, {})
            self.fail('unexpected request: ' + method + ' ' + url)
        client.request.side_effect = request
        # A concurrent writer promotes a newer day between our two attempts.
        newer = dict(trade_date='2026-10-28', status='complete', missing_data=[])
        client.get.side_effect = [response(404, {}), response(200, {
            'content': base64.b64encode(json.dumps(newer).encode()).decode()})]
        payload = dict(trade_date='2026-10-27', published_at='2026-10-27T16:00:00+08:00',
                       status='complete', missing_data=[])
        large = '沪' * 18000  # UTF-8 bytes exceed threshold, characters do not.
        files = {'latest.json': json.dumps(payload), 'latest.md': 'report', 'market_snapshot.json': large}
        self.assertFalse(publish_repository(files, 'owner/repo', 'test-token'))
        self.assertEqual(len(blob_bodies), 1)
        self.assertEqual(blob_bodies[0], {'content': large, 'encoding': 'utf-8'})
        self.assertEqual([tree['base_tree'] for tree in trees], ['old-head-tree', 'concurrent-head-tree'])
        self.assertEqual([commit['parents'] for commit in commits], [['old-head'], ['concurrent-head']])
        first = {row['path']: row for row in trees[0]['tree']}
        second = {row['path']: row for row in trees[1]['tree']}
        self.assertEqual(first['market_snapshot.json']['sha'], 'large-blob')
        self.assertNotIn('content', first['market_snapshot.json'])
        self.assertNotIn('market_snapshot.json', second)
        self.assertNotIn('README.md', second)
        self.assertTrue(all(path.startswith('archive/') for path in second))
        self.assertTrue(all(patch['force'] is False for patch in patches))

    @patch('collector.public_feed.requests.Session')
    def test_repository_conflicts_stop_after_three_non_force_attempts(self, session_factory):
        client = session_factory.return_value
        ref_updates = []
        def response(status, payload):
            result = Mock(status_code=status, ok=200 <= status < 300)
            result.json.return_value = payload
            return result
        def request(method, url, json=None, timeout=None):
            if method == 'GET' and url.endswith('/git/ref/heads/main'):
                return response(200, {'object': {'sha': 'head'}})
            if method == 'GET':
                return response(200, {'tree': {'sha': 'base'}})
            if method == 'POST':
                return response(201, {'sha': 'created'})
            if method == 'PATCH':
                ref_updates.append(json)
                return response(409, {})
            self.fail('unexpected request')
        client.request.side_effect = request
        client.get.return_value = response(404, {})
        payload = dict(trade_date='2026-10-27', published_at='2026-10-27T16:00:00+08:00')
        with self.assertRaisesRegex(RuntimeError, 'PATCH HTTP 409'):
            publish_repository({'latest.json': json.dumps(payload), 'latest.md': 'report'},
                               'owner/repo', 'test-token')
        self.assertEqual(len(ref_updates), 3)
        self.assertTrue(all(update['force'] is False for update in ref_updates))
