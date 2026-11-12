"""Protect dated associations, immutable inputs and missing-price semantics."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock
from urllib.parse import quote

from collector.run import dump
from collector.v2_data import (
    build_daily, collect_core_prices, get_reviews, normalize_prices,
    parse_review, selected_inputs, upstream_table,
)


DAY = '2026-11-11'
URL = 'https://www.dabanke.com/index-20261111.html'
ALIASES = {'机器人': ['机器人', '减速器']}


def stock(code='000678', name='示例股份', reason='机器人+减速器 · 资料日期 · 2026-11-11',
          status='status-success'):
    market = 'SH' if code.startswith('6') else 'BJ' if code.startswith('9') else 'SZ'
    return f'''<div class="stock-line {status}" data-symbol="{code}.{market}">
      <strong class="stock-name"><a class="stock-detail-link"
      href="https://www.dabanke.com/gupiao-{code}.html?review_date={DAY}">{name}</a></strong>
      <details class="ladder-stock-reason"><summary title="{reason}">关联</summary></details>
    </div>'''


def page(stocks=None, evidence_code='000001', theme='独立题材'):
    return f'''<section id="market-concepts"><h2 id="concept-title"><strong>{DAY}</strong></h2>
      <table><tbody><tr><th><a class="concept-detail-link"
      href="https://www.dabanke.com/gn.html?name={quote(theme)}&date=20261111">{theme}</a></th>
      <td><span class="concept-stock" title="{evidence_code}.SZ"><a class="stock-detail-link"
      href="https://www.dabanke.com/gupiao-{evidence_code}.html?review_date={DAY}">示例股份</a></span>
      </td></tr></tbody></table></section>
      <section class="ladder-view-tier"><h3>2进3</h3>{stocks or stock()}</section>'''


def price(day=DAY, **changes):
    row = dict(date=day, open=10, high=11, low=9, close=10.5,
               volume=1234, amount=12345, turnover=0.0123)
    return dict(row, **changes)


class V2DataTests(unittest.TestCase):
    def test_page_and_stock_link_dates_must_match(self):
        with self.assertRaises(ValueError):
            parse_review(page(), '2026-11-10', None, URL, ALIASES)
        wrong = page().replace('gupiao-000678.html?review_date=' + DAY,
                               'gupiao-000678.html?review_date=2026-11-10')
        with self.assertRaises(ValueError):
            parse_review(wrong, DAY, None, URL, ALIASES)

    def test_future_and_undated_reasons_are_not_historical_membership(self):
        for reason in ['机器人 · 资料日期 · 2026-11-12', '机器人']:
            rows, evidence = parse_review(page(stock(reason=reason)), DAY, None, URL, ALIASES)
            self.assertEqual(rows[0]['theme_ids'], [])
            self.assertEqual(rows[0]['mapping_confidence'], 'unknown')
            self.assertFalse(rows[0]['historical_point_in_time_verified'])
            self.assertFalse(rows[0]['business_verified'])
            self.assertFalse(evidence[0]['source_price_used'])

    def test_alias_and_supplement_are_deduplicated_per_stock(self):
        rows, _ = parse_review(page(evidence_code='000678', theme='机器人'), DAY, None, URL, ALIASES)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['theme_ids'], ['机器人'])
        self.assertEqual(rows[0]['height'], 3)
        self.assertIsNone(rows[0]['all_day_one_word'])
        self.assertFalse(rows[0]['execution_verified'])
        self.assertIsNone(rows[0]['first_seal'])

    def test_duplicate_stock_is_rejected_and_ineligible_boards_are_filtered(self):
        with self.assertRaises(ValueError):
            parse_review(page(stock() + stock()), DAY, None, URL, ALIASES)
        mixed = stock() + stock('300001') + stock('688001') + stock('920001') + stock('600001', '*ST示例')
        rows, _ = parse_review(page(mixed), DAY, None, URL, ALIASES)
        self.assertEqual([r['code'] for r in rows], ['000678'])

    def test_review_cache_tampering_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            cache, output = Path(directory) / 'cache', Path(directory) / 'output'
            cache.mkdir()
            (cache / (DAY + '.html')).write_text(page(), encoding='utf-8')
            dump(cache / (DAY + '.meta.json'), {'sha256': 'invalid'})
            with self.assertRaises(ValueError):
                get_reviews([DAY], output, ALIASES, [cache], offline=True)

    def test_reused_cache_without_timestamp_keeps_timestamp_unknown(self):
        with tempfile.TemporaryDirectory() as directory:
            cache, output = Path(directory) / 'cache', Path(directory) / 'output'
            cache.mkdir()
            (cache / (DAY + '.html')).write_text(page(), encoding='utf-8')
            rows, _, coverage = get_reviews([DAY], output, ALIASES, [cache], offline=True)
            self.assertIsNone(rows[0]['fetched_at'])
            self.assertTrue(coverage[0]['original_fetched_at_unknown'])
            self.assertEqual(coverage[0]['status'], 'available')

    def test_missing_review_and_partial_counts_do_not_mean_full_constituents(self):
        rows, _ = parse_review(page(stock() + stock('000679') + stock('000680')), DAY, None, URL, ALIASES)
        old = '2026-11-10'
        daily, _ = build_daily(rows, [old, DAY], [{'date': DAY, 'status': 'available'}], [])
        missing = next(r for r in daily if r['date'] == old)
        current = next(r for r in daily if r['date'] == DAY)
        self.assertIsNone(missing['observed_limit_up_count'])
        self.assertEqual(current['observed_limit_up_count'], 3)
        self.assertIsNone(current['advancing_ratio'])
        self.assertIsNone(current['relative_return_pct'])
        self.assertIsNone(current['broken_count'])
        self.assertEqual(current['count_kind'], 'observed_lower_bound_not_full_constituents')

    def test_prices_preserve_qfq_and_fraction_turnover_and_unknown_fields(self):
        row = normalize_prices('000678', [price(volume=None, amount=None)], 'qfq')[0]
        self.assertEqual(row['adjustment'], 'qfq')
        self.assertAlmostEqual(row['turnover_rate'], .0123)
        self.assertEqual(row['turnover_unit'], 'fraction')
        self.assertIsNone(row['amount'])
        self.assertIsNone(row['volume'])
        self.assertNotEqual(row['volume_unit'], 'shares')
        with self.assertRaises(ValueError):
            normalize_prices('000678', [price()], 'hfq')

    def test_duplicate_or_invalid_dates_and_invalid_ohlc_are_not_usable(self):
        with self.assertRaises(ValueError):
            normalize_prices('000678', [price(), price()], 'qfq')
        self.assertEqual(normalize_prices('000678', [price(low=11)], 'qfq'), [])
        for date in ['not-a-date', '2026-02-30', '']:
            self.assertEqual(normalize_prices('000678', [price(date)], 'qfq'), [])

    def test_negative_optional_price_fields_do_not_survive_as_valid_amounts(self):
        rows = normalize_prices('000678', [price(volume=-1, amount=-1, turnover=-1)], 'qfq')
        for row in rows:
            for key in ['volume', 'amount', 'turnover_rate']:
                self.assertTrue(row[key] is None or row[key] >= 0, key)

    def test_price_cache_must_identify_exact_symbol_and_adjustment(self):
        for wrong in [('sz000001', 'qfq'), ('sz000678', '')]:
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                cache, output = root / 'cache', root / 'output'
                (cache / 'raw').mkdir(parents=True)
                path = cache / 'raw/qfq_000678.json'
                dump(path, [price()])
                dump(cache / 'sources.json', {'qfq_000678': {
                    'function': 'stock_zh_a_hist_tx',
                    'parameters': {'symbol': wrong[0], 'adjust': wrong[1]},
                    'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}})
                collector = Mock(root=output, calls={}, delay=0, timeout=20)
                rows, coverage = collect_core_prices(collector, ['000678'], [DAY], budget=0, caches=[cache])
                self.assertEqual(rows, [])
                self.assertEqual(coverage[0]['status'], 'missing')
                collector.call.assert_not_called()

    def test_saved_upstream_bytes_cannot_be_changed_after_snapshot(self):
        raw = '[{"code":"000678"}]'
        saved = {'files': {'clean/limit_up.json': {
            'raw_json': raw, 'sha256': hashlib.sha256(raw.encode('utf-8')).hexdigest()}}}
        self.assertEqual(upstream_table(saved, 'clean/limit_up.json')[0]['code'], '000678')
        saved['files']['clean/limit_up.json']['raw_json'] = '[]'
        with self.assertRaises(ValueError):
            upstream_table(saved, 'clean/limit_up.json')

    def test_original_manifest_detects_tampering_before_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory)
            day = data / DAY
            run = day / 'runs' / 'run1'
            dump(day / 'latest.json', {'run_id': 'run1'})
            dump(run / 'summary.json', {'trade_date': DAY, 'trading_day': True})
            dump(run / 'clean/limit_up.json', [{'code': '000678'}])
            payload = (run / 'clean/limit_up.json').read_bytes()
            dump(run / 'files.json', [{'path': 'clean/limit_up.json',
                                      'sha256': hashlib.sha256(payload).hexdigest()}])
            dump(run / 'clean/limit_up.json', [{'code': '000001'}])
            with self.assertRaises(ValueError):
                selected_inputs(data, [DAY])
