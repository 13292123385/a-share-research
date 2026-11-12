import copy
from datetime import date, timedelta
import unittest

from collector.v2_scoring import rank_themes, select_seats


def sessions(count=40):
    result = []
    day = date(2026, 8, 3)
    while len(result) < count:
        if day.weekday() < 5:
            result.append(day.isoformat())
        day += timedelta(days=1)
    return result


def series(ident, days, counts, complete=False):
    return [dict(date=d, theme_id=ident, theme_name=ident,
                 observed_limit_up_count=n, market_limit_up_count=100,
                 max_height=3 if n else 0, active_signal=bool(n),
                 mapping_scope='complete' if complete else 'partial_active_associations',
                 relative_return_pct=1 if complete else None,
                 advancing_ratio=.7 if complete else None,
                 turnover_share=.1 if complete else None,
                 broken_count=None)
            for d, n in zip(days, counts)]


def seat_row(ident, score, day, prior, eligible=True, new=False):
    return dict(theme_id=ident, theme_name=ident, as_of=day,
                previous_trading_date=prior, composite_score=score,
                score_kind='partial_observed_activity',
                eligible_mainline=eligible, new_hotspot=new,
                catalyst_verified=False, windows={'5': {'score': score}})


class RollingThemeTests(unittest.TestCase):
    def setUp(self):
        self.days = sessions()

    def test_one_day_burst_cannot_replace_sustained_mainline(self):
        rows = (series('sustained', self.days, [8] * 40) +
                series('content', self.days, [4] * 40) +
                series('single-day', self.days, [0] * 39 + [50]))
        rankings = rank_themes(rows, self.days)
        seats = select_seats(rankings)['seats']
        self.assertEqual(seats['A']['theme_id'], 'sustained')
        self.assertEqual(seats['B']['theme_id'], 'content')
        flash = next(r for r in rankings if r['theme_id'] == 'single-day')
        self.assertTrue(flash['new_hotspot'])
        self.assertFalse(flash['eligible_mainline'])
        self.assertIsNone(seats['C'])
        self.assertEqual(seats['A']['seat_status'], 'provisional_observation')

    def test_missing_session_is_not_zero_or_replaced_by_older_session(self):
        rows = series('a', self.days, [4] * 40)
        rows[-3]['observed_limit_up_count'] = None
        rows[-3]['active_signal'] = None
        rows[-3]['max_height'] = None
        result = rank_themes(rows, self.days)[0]
        window = result['windows']['5']
        self.assertEqual(window['start'], self.days[-5])
        self.assertEqual(window['observed_sessions'], 4)
        self.assertEqual(window['coverage'], .8)
        self.assertIsNone(window['components']['persistence'])
        self.assertIsNone(window['score'])
        self.assertIsNone(result['composite_score'])
        self.assertFalse(result['eligible_mainline'])

    def test_windows_normalize_rates_not_cumulative_stock_days(self):
        rows = (series('old-history', self.days, [80] * 20 + [5] * 20) +
                series('other', self.days, [1] * 20 + [5] * 20))
        ranked = {r['theme_id']: r for r in rank_themes(rows, self.days)}
        for size in ('5', '10', '20'):
            self.assertEqual(ranked['old-history']['windows'][size]['score'],
                             ranked['other']['windows'][size]['score'])
        self.assertEqual(ranked['old-history']['windows']['5']['components']['limit_up_share'], .05)
        self.assertGreater(ranked['old-history']['windows']['40']['score'],
                           ranked['other']['windows']['40']['score'])

    def test_large_weak_theme_tail_preserves_magnitude_gap_between_leaders(self):
        rows = (series('strong', self.days, [20] * 40) +
                series('challenger', self.days, [10] * 40))
        for index in range(300):
            rows.extend(series('weak-' + str(index), self.days, [1] + [0] * 39))
        ordinal = {r['theme_id']: r for r in rank_themes(rows, self.days,
                   {'normalization_method': 'percentile'})}
        blended = {r['theme_id']: r for r in rank_themes(rows, self.days)}
        self.assertLess(ordinal['strong']['composite_score'] - ordinal['challenger']['composite_score'], 1)
        self.assertGreater(blended['strong']['composite_score'] - blended['challenger']['composite_score'], 5)
        method = blended['strong']['windows']['5']['normalization']['limit_up_share']
        self.assertEqual(method['candidate_count'], 302)
        self.assertEqual(method['raw_max'], .2)
        self.assertEqual(method['raw_min'], 0)
        self.assertEqual(method['method'], 'percentile_minmax_blend')

    def test_short_history_does_not_invent_40_days_or_reweight_missing_windows(self):
        days = self.days[-10:]
        result = rank_themes(series('a', days, [4] * 10), days)[0]
        self.assertEqual(result['common_windows'], ['5', '10'])
        self.assertEqual(result['effective_weights'], {'5': .5, '10': .25})
        self.assertEqual(result['weight_coverage'], .75)
        self.assertEqual(result['composite_score'], 37.5)
        self.assertEqual(result['composite_interval'], [37.5, 62.5])
        self.assertEqual(result['score_kind'], 'partial_window_observed_activity')
        self.assertEqual(result['windows']['40']['coverage'], .25)
        self.assertIsNone(result['windows']['40']['score'])

    def test_common_windows_prevent_individual_missing_window_bonus(self):
        a = series('a', self.days, [3] * 40)
        b = series('b', self.days, [5] * 40)
        b[0]['observed_limit_up_count'] = None
        b[0]['active_signal'] = None
        result = rank_themes(a + b, self.days)
        self.assertEqual(result[0]['effective_weights'], result[1]['effective_weights'])
        self.assertEqual(result[0]['omitted_windows'], ['40'])
        self.assertEqual(result[0]['weight_coverage'], .95)

    def test_partial_mapping_cannot_produce_full_strength_even_with_price_values(self):
        rows = series('a', self.days, [4] * 40, complete=True)
        for row in rows:
            row['mapping_scope'] = 'partial_active_associations'
        result = rank_themes(rows, self.days)[0]
        self.assertIsNone(result['full_score'])
        self.assertEqual(result['score_kind'], 'partial_observed_activity')
        self.assertIsNone(result['windows']['5']['components']['relative_strength'])

    def test_full_strength_requires_every_component_and_dated_membership(self):
        result = rank_themes(series('a', self.days, [4] * 40, complete=True), self.days)[0]
        self.assertEqual(result['full_score'], 50)
        self.assertEqual(result['score_kind'], 'full_strength')
        self.assertEqual(result['configured_weights'], {'5': .5, '10': .25, '20': .2, '40': .05})

    def test_five_quiet_sessions_retires_old_mainline(self):
        rows = series('old', self.days, [12] * 35 + [0] * 5)
        result = rank_themes(rows, self.days)[0]
        self.assertEqual(result['recent_active_days'], 0)
        self.assertFalse(result['eligible_mainline'])
        seats = select_seats([result], previous={'target_date': self.days[-2], 'seats': {'A': 'old'}})
        self.assertIsNone(seats['seats']['A'])
        self.assertEqual(seats['changes'][0]['reason'], 'incumbent_no_longer_eligible')

    def test_theme_inactive_outside_40_day_window_is_excluded(self):
        days = sessions(41)
        rows = series('historic', days, [30] + [0] * 40)
        self.assertEqual(rank_themes(rows, days), [])

    def test_new_hotspot_needs_recent_verified_catalyst_for_C(self):
        rows = series('burst', self.days, [0] * 39 + [20])
        ranked = rank_themes(rows, self.days)
        result = select_seats(ranked)
        self.assertIsNone(result['seats']['C'])
        self.assertEqual(result['watch_new_hotspots'], ['burst'])
        rows[-1].update(catalyst_verified=True, catalyst_evidence=[
            dict(date=self.days[-1], source_url='https://example.org/dated-announcement')])
        ranked = rank_themes(rows, self.days)
        result = select_seats(ranked)
        self.assertEqual(result['seats']['C']['theme_id'], 'burst')
        self.assertIsNone(result['seats']['A'])
        rows[-1]['catalyst_evidence'][0]['date'] = self.days[-10]
        self.assertFalse(rank_themes(rows, self.days)[0]['catalyst_verified'])

    def test_future_duplicate_and_invalid_calendar_are_rejected(self):
        rows = series('a', self.days, [4] * 40)
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            rank_themes(rows + [rows[0]], self.days)
        future = dict(rows[-1], date='2026-12-01')
        with self.assertRaisesRegex(ValueError, 'future'):
            rank_themes(rows + [future], self.days)
        with self.assertRaisesRegex(ValueError, 'sorted'):
            rank_themes(rows, self.days[::-1])

    def test_configured_window_weights_are_validated(self):
        rows = series('a', self.days, [4] * 40)
        for weights in ({'5': 1}, {'5': .6, '10': .3, '20': .2, '40': .1},
                        {'5': float('nan'), '10': 0, '20': 0, '40': 0}):
            with self.assertRaises(ValueError):
                rank_themes(rows, self.days, {'window_weights': weights})
        result = rank_themes(rows, self.days, {'window_weights': {'5': 1., '10': 0., '20': 0., '40': 0.}})[0]
        self.assertEqual(result['effective_weights'], {'5': 1.})

    def test_exact_attribute_exclusion_preserves_ranking_but_not_seats(self):
        rows = (series('国企改革', self.days, [30] * 40) +
                series('产业题材', self.days, [5] * 40) +
                series('国企改革设备', self.days, [4] * 40))
        config = {'excluded_seat_themes': ['国企改革']}
        ranked = rank_themes(rows, self.days, config)
        by_id = {r['theme_id']: r for r in ranked}
        self.assertEqual(ranked[0]['theme_id'], '国企改革')
        self.assertTrue(by_id['国企改革']['seat_excluded'])
        self.assertEqual(by_id['国企改革']['theme_kind'], 'generic_attribute')
        self.assertFalse(by_id['国企改革设备']['seat_excluded'])
        selection = select_seats(ranked, config=config)
        self.assertEqual(selection['seats']['A']['theme_id'], '产业题材')
        self.assertEqual(selection['seats']['B']['theme_id'], '国企改革设备')
        self.assertIsNone(selection['seats']['C'])

    def test_excluded_new_attribute_cannot_take_C_even_with_catalyst(self):
        rows = series('业绩增长', self.days, [0] * 39 + [20])
        rows[-1].update(catalyst_verified=True, catalyst_evidence=[
            dict(date=self.days[-1], source_url='https://example.org/earnings')])
        config = {'excluded_seat_themes': ['业绩增长']}
        ranked = rank_themes(rows, self.days, config)
        self.assertTrue(ranked[0]['new_hotspot'])
        selected = select_seats(ranked, config=config)
        self.assertEqual(selected['seats'], {'A': None, 'B': None, 'C': None})


class SeatTransitionTests(unittest.TestCase):
    def setUp(self):
        self.days = sessions(45)

    def test_small_margin_holds_A_and_large_margin_requires_two_sessions(self):
        d = self.days
        initial = select_seats([seat_row('A', 90, d[39], d[38]), seat_row('B', 85, d[39], d[38])])
        small = select_seats([seat_row('B', 93, d[40], d[39]), seat_row('A', 90, d[40], d[39])], initial['state'])
        self.assertEqual(small['state']['seats']['A'], 'A')
        self.assertIsNone(small['state']['pending'])
        first = select_seats([seat_row('B', 98, d[41], d[40]), seat_row('A', 90, d[41], d[40])], small['state'])
        self.assertEqual(first['state']['pending']['sessions'], 1)
        replay = select_seats([seat_row('B', 98, d[41], d[40]), seat_row('A', 90, d[41], d[40])], first['state'])
        self.assertEqual(replay['state'], first['state'])
        second = select_seats([seat_row('B', 98, d[42], d[41]), seat_row('A', 90, d[42], d[41])], replay['state'])
        self.assertEqual(second['state']['seats'], {'A': 'B', 'B': 'A', 'C': None})
        self.assertTrue(any(x['kind'] == 'mainline_swapped' for x in second['changes']))

    def test_gap_in_daily_state_resets_confirmation(self):
        d = self.days
        initial = select_seats([seat_row('A', 90, d[39], d[38]), seat_row('B', 85, d[39], d[38])])
        first = select_seats([seat_row('B', 99, d[40], d[39]), seat_row('A', 90, d[40], d[39])], initial['state'])
        gap = select_seats([seat_row('B', 99, d[42], d[41]), seat_row('A', 90, d[42], d[41])], first['state'])
        self.assertEqual(gap['state']['seats']['A'], 'A')
        self.assertEqual(gap['state']['pending']['sessions'], 1)

    def test_expired_incumbent_is_removed_without_waiting_two_days(self):
        d = self.days
        result = select_seats([seat_row('old', 99, d[40], d[39], eligible=False),
                               seat_row('new', 60, d[40], d[39])],
                              {'target_date': d[39], 'seats': {'A': 'old'}})
        self.assertEqual(result['state']['seats']['A'], 'new')
        self.assertEqual(result['changes'][0]['reason'], 'incumbent_no_longer_eligible')

    def test_empty_selection_and_future_state(self):
        result = select_seats([], config={'as_of': self.days[-1]})
        self.assertEqual(result['seats'], {'A': None, 'B': None, 'C': None})
        self.assertEqual(result['state']['target_date'], self.days[-1])
        rows = [seat_row('a', 80, self.days[-2], self.days[-3])]
        with self.assertRaisesRegex(ValueError, 'future'):
            select_seats(rows, {'target_date': self.days[-1]})
        with self.assertRaisesRegex(ValueError, 'future'):
            select_seats(rows, {'target_date': self.days[-3], 'history': [{'date': self.days[-1]}]})

    def test_seats_are_unique_and_do_not_mutate_input(self):
        d = self.days
        rows = [seat_row('a', 90, d[40], d[39]), seat_row('b', 80, d[40], d[39]),
                seat_row('c', 70, d[40], d[39], eligible=False, new=True)]
        original = copy.deepcopy(rows)
        result = select_seats(rows)
        ids = [r['theme_id'] for r in result['seats'].values() if r]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(rows, original)
        self.assertIsNone(result['seats']['C'])

    def test_exclusion_applies_to_previously_saved_ranking(self):
        d = self.days
        rows = [seat_row('国企改革', 99, d[40], d[39]), seat_row('设备', 80, d[40], d[39])]
        result = select_seats(rows, {'target_date': d[39], 'seats': {'A': '国企改革'}},
                              {'excluded_seat_themes': ['国企改革']})
        self.assertEqual(result['state']['seats']['A'], '设备')
        self.assertTrue(result['rankings'][0]['seat_excluded'])
        self.assertNotIn('seat_excluded', rows[0])


if __name__ == '__main__':
    unittest.main()
