import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from collector.run import Collector


class ArchiveTests(unittest.TestCase):
    def test_written_bytes_match_checksum(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = Collector(Path(tmp), delay=0)
            def worker(argv, **kwargs):
                Path(argv[4]).write_text('[{"代码":"600001"}]', encoding='utf-8')
                return subprocess.CompletedProcess(argv, 0, '', '')
            with patch('collector.run.subprocess.run', side_effect=worker):
                self.assertIsNotNone(c.call('sample', 'fake'))
            raw = Path(tmp) / 'raw/sample.json'
            self.assertEqual(c.calls['sample']['sha256'], hashlib.sha256(raw.read_bytes()).hexdigest())

    def test_timeout_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = Collector(Path(tmp), delay=0)
            with patch('collector.run.subprocess.run', side_effect=subprocess.TimeoutExpired('test', 1)):
                self.assertIsNone(c.call('sample', 'fake'))
            self.assertEqual(c.calls['sample']['status'], 'error')
            self.assertIsNone(c.calls['sample']['rows'])

    def test_empty_is_not_verified_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = Collector(Path(tmp), delay=0)
            def worker(argv, **kwargs):
                Path(argv[4]).write_text('[]', encoding='utf-8')
                return subprocess.CompletedProcess(argv, 0, '', '')
            with patch('collector.run.subprocess.run', side_effect=worker):
                self.assertIsNone(c.call('sample', 'fake'))
            self.assertEqual(c.calls['sample']['status'], 'empty_unverified')
