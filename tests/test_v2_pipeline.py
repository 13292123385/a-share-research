"""Integration contracts: preserved upstream, exact replay, honest partial output."""
import hashlib
import json
from datetime import date, timedelta
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from collector.run import dump
from collector.inventory import inventory
from collector.v2 import main, read, selection_trace
from collector.v2_data import build_daily
from collector.v2_validate import validate_run


class V2PipelineTests(unittest.TestCase):
    def test_future_stock_cannot_change_topic_qualification(self):
        with self.assertRaisesRegex(ValueError, 'future_stock'):
            build_daily([dict(date='2026-11-12', code='600001', theme_ids=['样例'])],
                        ['2026-11-11'], [], [])

    def test_prefix_qualification_does_not_know_future_constituents(self):
        days = ['2026-10-01', '2026-10-02', '2026-10-05']
        rows = [dict(date=d, code=c, theme_ids=['样例主题'], closed_limit_up=True,
                     height=1, broken_at_close=False)
                for d, c in zip(days, ('600001', '600002', '600003'))]
        coverage = [dict(date=d, status='available') for d in days]
        _, _, _, _, history = selection_trace(rows, days, coverage, [], {})
        self.assertEqual(history[0]['state']['target_date'], days[0])
        self.assertTrue(all(v is None for v in history[0]['state']['seats'].values()))
        first, _ = build_daily(rows[:1], days[:1], coverage[:1], [])
        self.assertEqual(first, [])

    def test_offline_run_is_append_only_replayable_and_leaves_old_data_untouched(self):
        start = date(2026, 8, 24)
        calendar = [(start + timedelta(days=i)).isoformat() for i in range(65)
                    if (start + timedelta(days=i)).weekday() < 5][:41]
        days = calendar[-40:]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cache, data = root / 'cache', root / 'old-data'
            cache.mkdir()
            data.mkdir()
            sentinel = data / 'original.txt'
            sentinel.write_bytes(b'unchanged prior research')
            before = hashlib.sha256(sentinel.read_bytes()).hexdigest()
            cal = root / 'calendar.json'
            dump(cal, [dict(trade_date=d) for d in calendar])
            for day in days:
                compact = day.replace('-', '')
                stock = lambda code: f'<span class="concept-stock" title="{code}.SH"><a class="stock-detail-link" href="gupiao-{code}.html?review_date={day}">样例股</a></span>'
                line = lambda code: f'<div class="stock-line status-success" data-symbol="{code}.SH"><strong class="stock-name"><a class="stock-detail-link" href="gupiao-{code}.html?review_date={day}">样例股</a></strong><details class="ladder-stock-reason"><summary title="样例题材 ｜ 资料日期 {day}">样例题材</summary></details></div>'
                html = f'<section id="market-concepts"><h2 id="concept-title"><strong>{day}</strong></h2><table><tbody><tr><th><a class="concept-detail-link" href="gn.html?name=样例题材&date={compact}">样例题材</a></th><td>{stock("600001")}</td></tr></tbody></table></section><div class="ladder-view-tier"><h3>首板</h3>{line("600001")}{line("600002")}{line("600003")}</div>'
                (cache / (day + '.html')).write_text(html, encoding='utf-8')
            output = root / 'v2'
            argv = ['--date', days[-1], '--data', str(data), '--lifecycle-data', str(root / 'no-lifecycle'),
                    '--output', str(output), '--calendar', str(cal), '--history-cache', str(cache),
                    '--offline', '--allow-partial']
            with patch('builtins.print'):
                self.assertEqual(main(argv), 0)
                self.assertEqual(main(argv), 0)
            runs = sorted(output.glob('*/runs/*'))
            self.assertEqual(len(runs), 2)
            first = runs[0]
            self.assertEqual(validate_run(first), [])
            report = read(first / 'report.json')
            self.assertEqual(report['coverage']['complete_historical_membership_days'], 0)
            self.assertEqual(report['trading']['candidates'], [])
            self.assertEqual(report['coverage']['dated_review_days'], 40)
            self.assertTrue(all(r['full_score'] is None for r in report['rankings']))
            self.assertFalse((data / days[-1]).exists())
            self.assertEqual(hashlib.sha256(sentinel.read_bytes()).hexdigest(), before)
            with patch('builtins.print'):
                self.assertEqual(main(['--date', days[-1], '--replay', str(first)]), 0)
            original = read(first / 'report.json')
            changed = read(first / 'report.json')
            changed['trading']['actual_positions'] = ['600999']
            changed['trading']['candidates'] = [dict(code='600999', execution_verified=True, entry_price=10, actual_return=.1)]
            dump(first / 'report.json', changed)
            inventory(first, read(first / 'sources.json'))
            errors = validate_run(first)
            self.assertIn('fabricated_positions_or_trading_return', errors)
            self.assertIn('trading_code_outside_observation_pool', errors)
            self.assertIn('fabricated_candidate_execution', errors)
            dump(first / 'report.json', original)
            inventory(first, read(first / 'sources.json'))
            (first / 'report.md').write_text('tampered', encoding='utf-8')
            self.assertTrue(any('checksum' in e for e in validate_run(first)))
