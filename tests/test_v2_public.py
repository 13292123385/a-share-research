import base64
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from collector.run import dump
from collector.v2_public import FILENAMES, blob_sha, make_files, publish, _coverage, _not_worse


DAY = '2026-11-11'


def encoded(value):
    return Mock(status_code=200, **{'json.return_value': {
        'content': base64.b64encode(json.dumps(value).encode()).decode()}})


def files(day=DAY, run_id='run1', keys=None, valid_rows=41):
    coverage = dict(summary={'dated_review_days': 40, 'core_price_valid_rows': valid_rows},
                    coverage_keys=keys if keys is not None else ['review:' + DAY, 'price:000678:' + DAY])
    result = {name: '{}' for name in FILENAMES}
    result['latest.json'] = json.dumps(dict(trade_date=day, run_id=run_id, status='partial_research'))
    result['coverage.json'] = json.dumps(coverage)
    result['latest.md'] = 'public research'
    return result


def remote_session(prior=None, prior_coverage=None, archive=None, ref_failures=0):
    session = Mock()
    attempts = []

    def request(method, url, json=None, timeout=None):
        if method == 'GET' and '/git/ref/heads/main' in url:
            attempts.append(len(attempts) + 1)
            value = {'object': {'sha': 'head' + str(len(attempts))}}
        elif method == 'GET' and '/git/commits/' in url:
            value = {'tree': {'sha': 'base' + str(len(attempts))}}
        elif method == 'POST' and url.endswith('/git/trees'):
            value = {'sha': 'tree' + str(len(attempts))}
        elif method == 'POST' and url.endswith('/git/commits'):
            value = {'sha': 'commit' + str(len(attempts))}
        else:
            raise AssertionError('unexpected API operation: ' + method + url)
        return Mock(ok=True, **{'json.return_value': value})

    def get(url, params=None, timeout=None):
        path = url.split('/contents/')[1]
        if '/archive/' in path:
            return Mock(status_code=404) if archive is None else Mock(status_code=200, **{'json.return_value': archive})
        if path == 'research-v2/latest.json':
            return Mock(status_code=404) if prior is None else encoded(prior)
        if path == 'research-v2/coverage.json':
            return Mock(status_code=404) if prior_coverage is None else encoded(prior_coverage)
        raise AssertionError('unexpected public path: ' + path)

    session.request.side_effect = request
    session.get.side_effect = get
    session.patch.side_effect = [Mock(ok=False, status_code=422) for _ in range(ref_failures)] + [Mock(ok=True)]
    return session


def tree_calls(session):
    return [r.kwargs['json'] for r in session.request.call_args_list
            if r.args[0] == 'POST' and r.args[1].endswith('/git/trees')]


class V2PublicTests(unittest.TestCase):
    def test_same_day_amount_and_association_loss_cannot_promote(self):
        report = dict(coverage={'core_price_valid_rows': 1})
        inputs = dict(review_coverage=[], selected_inputs=[], market_coverage=[], price_coverage=[],
                      prices=[dict(code='600001', date=DAY, adjustment='qfq', amount=100, volume=10, turnover_rate=.1)],
                      observations=[dict(code='600001', date=DAY, theme_ids=['样例'])])
        prior = _coverage(report, inputs)
        inputs['prices'][0]['amount'] = None
        current = _coverage(report, inputs)
        self.assertFalse(_not_worse(current, prior))
        inputs['prices'][0]['amount'] = 100
        inputs['observations'][0]['theme_ids'] = []
        self.assertFalse(_not_worse(_coverage(report, inputs), prior))

    def fixture(self, folder):
        run = Path(folder) / DAY / 'runs' / 'run1'
        seat = dict(theme_id='机器人', theme_name='机器人', as_of=DAY, rank=1, composite_score=80,
            private_note='PRIVATE_SENTINEL', windows={'5': {'score': 90, 'private': 'PRIVATE_SENTINEL'}})
        core = dict(code='000678', name='示例', theme_id='机器人', roles=['涨幅王'],
            role_evidence={'涨幅王': {'basis': '日期证据', 'private': 'PRIVATE_SENTINEL'}},
            private_path='PRIVATE_SENTINEL', execution_verified=False, entry_price=None)
        state = dict(target_date=DAY, seats={'A': '机器人', 'B': None, 'C': None}, pending=None,
            history=['PRIVATE_SENTINEL'], private_path='PRIVATE_SENTINEL', policy={'swap_margin': 5})
        report = dict(trade_date=DAY, status='partial_research', ranking_scope='dated_partial_active_associations',
            coverage={'dated_review_days': 40, 'private_note': 'PRIVATE_SENTINEL'},
            selection={'seats': {'A': seat, 'B': None, 'C': None}, 'state': state,
                       'rankings': ['PRIVATE_SENTINEL']},
            core_by_theme={'机器人': [core]}, rankings=['PRIVATE_SENTINEL'], state_history=['PRIVATE_SENTINEL'],
            private_path='PRIVATE_SENTINEL', changes=[], missing_data=['完整历史成分未知'],
            trading={'candidates': [], 'private_plan': 'PRIVATE_SENTINEL'})
        inputs = dict(review_coverage=[{'date': DAY, 'status': 'available', 'private_path': 'PRIVATE_SENTINEL'}],
            selected_inputs=[{'date': DAY, 'private_path': 'PRIVATE_SENTINEL'}],
            market_coverage=[], price_coverage=[], prices=[])
        dump(run / 'report.json', report)
        dump(run / 'summary.json', {'trade_date': DAY, 'run_id': run.name})
        dump(run / 'analysis_inputs.json', inputs)
        return run

    def test_validation_precedes_any_public_export(self):
        with patch('collector.v2_public.validate_run', return_value=['checksum_mismatch']), \
                patch('collector.v2_public.read') as reader:
            with self.assertRaises(ValueError):
                make_files('missing')
            reader.assert_not_called()

    def test_allowlist_removes_private_fields_and_rankings_in_every_file(self):
        with tempfile.TemporaryDirectory() as folder:
            run = self.fixture(folder)
            with patch('collector.v2_public.validate_run', return_value=[]):
                result = make_files(run)
            self.assertEqual(set(result), FILENAMES)
            self.assertNotIn('PRIVATE_SENTINEL', ''.join(result.values()))
            payload = json.loads(result['latest.json'])
            self.assertNotIn('rankings', payload)
            self.assertNotIn('history', json.loads(result['state.json']))
            self.assertEqual(payload['status'], 'partial_research')
            self.assertIn('完整历史成分未知', result['latest.md'])

    def test_publisher_only_adds_isolated_namespace_and_preserves_remote_tree(self):
        session = remote_session()
        with patch('collector.v2_public.requests.Session', return_value=session):
            result = publish(files(), 'fixture/repository', 'test-token')
        body = tree_calls(session)[0]
        self.assertEqual(body['base_tree'], 'base1')
        paths = {r['path'] for r in body['tree']}
        self.assertTrue(all(p.startswith('research-v2/') for p in paths))
        self.assertIn('research-v2/latest.json', paths)
        self.assertIn('research-v2/archive/' + DAY + '/run1/latest.json', paths)
        self.assertTrue(all(r['type'] == 'blob' and r.get('sha', 'non-null') is not None for r in body['tree']))
        self.assertFalse(session.patch.call_args.kwargs['json']['force'])
        self.assertTrue(result['promoted'])

    def test_same_day_lost_price_identity_cannot_replace_latest(self):
        previous_files = files(keys=['review:' + DAY, 'price:000678:' + DAY])
        previous = json.loads(previous_files['latest.json'])
        session = remote_session(previous, json.loads(previous_files['coverage.json']))
        with patch('collector.v2_public.requests.Session', return_value=session):
            result = publish(files(run_id='run2', keys=['review:' + DAY], valid_rows=42),
                             'fixture/repository', 'test-token')
        self.assertFalse(result['promoted'])
        self.assertTrue(all('/archive/' in r['path'] for r in tree_calls(session)[0]['tree']))

    def test_same_day_numeric_quality_regression_also_blocks_promotion(self):
        old = files(valid_rows=41)
        session = remote_session(json.loads(old['latest.json']), json.loads(old['coverage.json']))
        with patch('collector.v2_public.requests.Session', return_value=session):
            result = publish(files(run_id='run2', valid_rows=40), 'fixture/repository', 'test-token')
        self.assertFalse(result['promoted'])

    def test_large_prior_coverage_uses_same_repository_blob_api(self):
        old = files()
        prior = json.loads(old['latest.json'])
        coverage = json.loads(old['coverage.json'])
        session = remote_session(prior, coverage)
        original_get, original_request = session.get.side_effect, session.request.side_effect
        def get(url, params=None, timeout=None):
            if '/contents/research-v2/coverage.json' in url:
                return Mock(status_code=200, **{'json.return_value': {'encoding': 'none', 'content': '', 'sha': 'large-coverage-blob', 'git_url': 'https://untrusted.invalid/'}})
            return original_get(url, params=params, timeout=timeout)
        def request(method, url, json=None, timeout=None):
            if method == 'GET' and url.endswith('/git/blobs/large-coverage-blob'):
                encoded_blob = base64.b64encode(__import__('json').dumps(coverage).encode()).decode()
                return Mock(ok=True, **{'json.return_value': {'encoding': 'base64', 'content': encoded_blob}})
            return original_request(method, url, json=json, timeout=timeout)
        session.get.side_effect, session.request.side_effect = get, request
        with patch('collector.v2_public.requests.Session', return_value=session):
            result = publish(files(run_id='new-run'), 'fixture/repository', 'test-token')
        self.assertTrue(result['promoted'])
        self.assertTrue(any('/git/blobs/large-coverage-blob' in r.args[1] for r in session.request.call_args_list))
        self.assertFalse(any('untrusted.invalid' in str(r) for r in session.request.call_args_list))

    def test_old_day_backfill_is_archived_without_changing_latest(self):
        session = remote_session({'trade_date': '2026-11-12'})
        with patch('collector.v2_public.requests.Session', return_value=session):
            result = publish(files(), 'fixture/repository', 'test-token')
        self.assertFalse(result['promoted'])
        self.assertTrue(all('/archive/' in r['path'] for r in tree_calls(session)[0]['tree']))

    def test_exact_archive_is_idempotent_and_all_files_are_compared(self):
        payload = files()
        archive = [dict(name=name, type='file', sha=blob_sha(value)) for name, value in payload.items()]
        session = remote_session(archive=archive)
        with patch('collector.v2_public.requests.Session', return_value=session):
            result = publish(payload, 'fixture/repository', 'test-token')
        self.assertTrue(result['already_archived'])
        self.assertEqual(tree_calls(session), [])
        session.patch.assert_not_called()
        archive[-1]['sha'] = 'changed_non_latest_file'
        with patch('collector.v2_public.requests.Session', return_value=remote_session(archive=archive)):
            with self.assertRaisesRegex(ValueError, 'immutable'):
                publish(payload, 'fixture/repository', 'test-token')

    def test_cas_race_rebuilds_on_latest_remote_tree(self):
        session = remote_session(ref_failures=1)
        with patch('collector.v2_public.requests.Session', return_value=session):
            publish(files(), 'fixture/repository', 'test-token')
        self.assertEqual([r['base_tree'] for r in tree_calls(session)], ['base1', 'base2'])
        self.assertEqual(session.patch.call_count, 2)

    def test_three_ref_races_stop_without_forcing_remote_head(self):
        session = remote_session(ref_failures=3)
        with patch('collector.v2_public.requests.Session', return_value=session):
            with self.assertRaisesRegex(RuntimeError, 'three V2 publish attempts'):
                publish(files(), 'fixture/repository', 'test-token')
        self.assertEqual(session.patch.call_count, 3)
        self.assertTrue(all(r.kwargs['json']['force'] is False for r in session.patch.call_args_list))

    def test_unsafe_paths_and_nonallowlisted_exports_are_rejected(self):
        extra = files()
        extra['../latest.json'] = '{}'
        for bad_files, repository in [(extra, 'fixture/repository'), (files(run_id='../bad'), 'fixture/repository'),
                                      (files(), '../repository')]:
            with self.assertRaises(ValueError):
                publish(bad_files, repository, 'test-token')
