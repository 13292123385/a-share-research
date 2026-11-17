import csv
import io
import json
import unittest

from collector.snapshot_public import make_files, should_promote, digest


class SnapshotPublicTests(unittest.TestCase):
    def fixture(self, count=201):
        return dict(schema_version=1, trade_date='2026-11-16', session='midday', run_id='sample',
                    fetched_at='2026-11-16T11:31:00+08:00', finished_at='2026-11-16T11:32:00+08:00',
                    status='complete', records=count, expected_count=count,
                    coverage={'private_path': 'PRIVATE_SENTINEL'}, quality={'secret': 'PRIVATE_SENTINEL'}, units={},
                    rows=[{'代码': str(i).zfill(6), '名称': 'sample', '最新价': 3, 'secret': 'PRIVATE_SENTINEL'} for i in range(count)])

    def test_all_rows_exported_once_across_shards_and_checksums_match(self):
        files, manifest = make_files(self.fixture(), '13292123385/a-share-market-data')
        counts = []
        for chunk in manifest['chunks']:
            path = chunk['url'].split('/main/')[1]
            content = files[path]
            self.assertEqual(chunk['sha256'], digest(content))
            counts.append(len(list(csv.DictReader(io.StringIO(content)))))
        self.assertEqual(counts, [100, 100, 1])
        self.assertEqual(sum(counts), 201)
        self.assertNotIn('PRIVATE_SENTINEL', ''.join(files.values()))
        self.assertEqual(len(json.loads(files['market/midday/snapshot.json'])['rows']), 201)
        archive = 'market/archive/2026-11-16/midday/sample/'
        archived = json.loads(files[archive + 'manifest.json'])
        for entry in list(archived['files'].values()) + archived['chunks']:
            path = entry['url'].split('/main/')[1]
            self.assertTrue(path.startswith(archive))
            self.assertEqual(digest(files[path]), entry['sha256'])

    def test_partial_cannot_replace_complete_same_day_but_new_date_remains_visible(self):
        old = self.fixture(2)
        new = dict(old, status='partial', fetched_at='2026-11-16T11:40:00+08:00')
        self.assertFalse(should_promote(new, old))
        self.assertTrue(should_promote(dict(new, trade_date='2026-11-17'), old))
        self.assertFalse(should_promote(dict(new, trade_date='2026-11-13'), old))

    def test_inconsistent_count_and_unpublishable_run_rejected(self):
        with self.assertRaises(ValueError):
            make_files(dict(self.fixture(2), records=1), '13292123385/a-share-market-data')
        with self.assertRaises(ValueError):
            make_files(dict(self.fixture(2), status='skipped'), '13292123385/a-share-market-data')

    def test_first_real_snapshot_replaces_missing_date_placeholder(self):
        self.assertTrue(should_promote(self.fixture(2), {'trade_date': None, 'status': 'missing'}))


if __name__ == '__main__':
    unittest.main()
