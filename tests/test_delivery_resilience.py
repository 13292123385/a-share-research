from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import requests
from collector.delivery_http import request, checked_download
from collector.snapshot_recover import recover


class DeliveryResilienceTests(unittest.TestCase):
    @patch('collector.delivery_http.time.sleep')
    def test_network_disconnect_and_rate_limit_retry_then_success(self, sleep):
        client = Mock()
        limited = Mock(status_code=429, headers={})
        good = Mock(status_code=200, headers={})
        client.request.side_effect = [requests.ConnectionError('secret-url'), limited, good]
        self.assertIs(request(client, 'GET', 'https://example.invalid'), good)
        self.assertEqual(client.request.call_count, 3)

    @patch('collector.delivery_http.time.sleep')
    def test_expired_credentials_not_retried_and_network_failure_is_bounded(self, sleep):
        client = Mock()
        denied = Mock(status_code=401, headers={})
        client.request.return_value = denied
        self.assertIs(request(client, 'PATCH', 'https://example.invalid'), denied)
        self.assertEqual(client.request.call_count, 1)
        client.request.side_effect = requests.exceptions.SSLError('SECRET_SENTINEL')
        with self.assertRaisesRegex(RuntimeError, 'bounded retries') as error:
            request(client, 'GET', 'https://example.invalid')
        self.assertNotIn('SECRET_SENTINEL', str(error.exception))
        self.assertEqual(client.request.call_count, 5)

    @patch('collector.delivery_http.time.sleep')
    def test_cached_old_bytes_are_retried_but_persistent_corruption_rejected(self, sleep):
        client = Mock()
        old = Mock(status_code=200, headers={}, content=b'old')
        good = Mock(status_code=200, headers={}, content=b'current')
        checksum = hashlib.sha256(b'current').hexdigest()
        client.request.side_effect = [old, good]
        self.assertIs(checked_download(client, 'https://example.invalid', checksum), good)
        client.request.side_effect = None
        client.request.return_value = old
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
            checked_download(client, 'https://example.invalid', checksum)

    def test_saved_midday_can_be_recovered_after_window_without_resampling(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / '2026-11-16/midday/runs/original'
            root.mkdir(parents=True)
            data = dict(trade_date='2026-11-16', session='midday', run_id='original', status='complete', rows=[])
            content = json.dumps(data).encode('utf-8')
            (root / 'snapshot.json').write_bytes(content)
            (root / 'manifest.json').write_text(json.dumps({'snapshot_sha256': hashlib.sha256(content).hexdigest()}), encoding='utf-8')
            (root.parents[1] / 'latest.json').write_text(json.dumps({'run_id': 'original'}), encoding='utf-8')
            with patch.dict(os.environ, {'GITHUB_OUTPUT': str(Path(folder) / 'outputs')}):
                restored = recover(folder, '2026-11-16', 'midday')
            self.assertEqual(restored['run_id'], 'original')
            self.assertEqual(restored['trade_date'], '2026-11-16')
            (root / 'snapshot.json').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                recover(folder, '2026-11-16', 'midday')
