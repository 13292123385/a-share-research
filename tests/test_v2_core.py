import unittest
from datetime import date, timedelta

from collector.v2_core import select_cores, trade_filter, render_report


class CoreSelectionTests(unittest.TestCase):
    def setUp(self):
        self.days = [(date(2026, 10, 1) + timedelta(days=i)).isoformat() for i in range(12)]
        self.theme = 'test:robot'

    def prices(self, closes=None, code='600001', adjustment='qfq'):
        closes = closes or [10 * 1.06 ** i for i in range(len(self.days))]
        return [dict(code=code, date=d, open=v, high=v * 1.01, low=v * .99,
                     close=v, volume=100, amount=None, adjustment=adjustment,
                     source='fixture') for d, v in zip(self.days, closes)]

    def observations(self, code='600001', name='样例', signals=None):
        if signals is None:
            signals = set(self.days)
        return [dict(date=d, code=code, name=name, theme_ids=[self.theme],
                     closed_limit_up=d in signals, height=2 if d in signals else None,
                     first_seal='09:30:00', all_day_one_word=False)
                for d in self.days]

    def test_duplicate_roles_merge_and_daily_order_does_not_prove_influence(self):
        cores = select_cores(self.theme, self.observations(), self.prices(), self.days)
        self.assertEqual(len(cores), 1)
        self.assertEqual(cores[0]['roles'], ['爆发王'])  # first-day start has no prior baseline
        self.assertIsNone(cores[0]['round_return_pct'])
        self.assertEqual(cores[0]['leadership_status'], 'pending_confirmation')
        self.assertNotIn('带动王', cores[0]['roles'])
        self.assertIsNone(cores[0]['relative_strength_5d_pct'])
        self.assertFalse(cores[0]['execution_verified'])

    def test_explicit_calendar_baseline_enables_round_return_without_backfill(self):
        baseline = '2026-09-30'
        prices = self.prices() + [dict(code='600001', date=baseline, open=9,
                                     high=9, low=9, close=9, adjustment='qfq')]
        cores = select_cores(self.theme, self.observations(), prices, self.days,
                             {'baseline_date': baseline})
        row = cores[0]
        self.assertEqual(row['roles'], ['涨幅王', '爆发王'])
        self.assertEqual(row['round_baseline_date'], baseline)
        self.assertAlmostEqual(row['round_return_pct'], (10 * 1.06 ** 11 / 9 - 1) * 100, places=3)
        self.assertTrue(row['round_start_left_censored'])
        self.assertTrue(all(day in self.days for day in row['recent_strong_signal_dates']))

    def test_today_association_is_not_filled_into_history(self):
        observations = self.observations()
        for row in observations[:-1]:
            row['theme_ids'] = []
        cores = select_cores(self.theme, observations, self.prices(), self.days)
        row = cores[0]
        self.assertEqual(row['round_start'], self.days[-1])
        self.assertEqual(row['round_baseline_date'], self.days[-2])
        self.assertAlmostEqual(row['round_return_pct'], 6)

    def test_current_roster_exclusion_overrides_older_non_st_observation(self):
        self.assertEqual(select_cores(self.theme, self.observations(), self.prices(), self.days,
                                     {'current_ineligible_codes': ['600001']}), [])

    def test_future_and_unpermitted_names_never_enter(self):
        observations, prices = self.observations(), self.prices()
        for code, name in [('300001', '创业'), ('688001', '科创'), ('920001', '北交'), ('600003', '*ST样例')]:
            observations += self.observations(code, name)
            prices += self.prices(code=code)
        future = dict(self.observations('600002')[-1], date='2027-01-01')
        observations.append(future)
        prices.append(dict(self.prices(code='600002')[-1], date='2027-01-01', close=1000000))
        cores = select_cores(self.theme, observations, prices, self.days)
        self.assertEqual([r['code'] for r in cores], ['600001'])
        # An earlier non-ST name must not retain a now-ST security.
        observations[-2]['name'] = '无关'
        current = self.observations()[-1]
        current['name'] = 'ST样例'
        observations = self.observations()[:-1] + [current]
        self.assertEqual(select_cores(self.theme, observations, self.prices(), self.days), [])

    def test_missing_day_cannot_be_skipped_to_compute_five_day_return(self):
        prices = [r for r in self.prices() if r['date'] != self.days[-3]]
        row = select_cores(self.theme, self.observations(), prices, self.days)[0]
        self.assertIsNone(row['return_5d_pct'])
        self.assertIsNone(row['round_return_pct'])
        self.assertIsNone(row['drawdown_pct'])
        self.assertAlmostEqual(row['return_1d_pct'], 6)

    def test_raw_price_changes_do_not_become_adjusted_returns_or_roles(self):
        self.assertEqual(select_cores(self.theme, self.observations(),
                                     self.prices(adjustment='none'), self.days), [])

    def test_conflicting_price_and_observation_fail_visibly(self):
        prices = self.prices()
        prices += [dict(prices[-1], close=prices[-1]['close'] * 1.001)]
        with self.assertRaises(ValueError):
            select_cores(self.theme, self.observations(), prices, self.days)
        observations = self.observations()
        observations += [dict(observations[-1], height=4)]
        with self.assertRaises(ValueError):
            select_cores(self.theme, observations, self.prices(), self.days)

    def test_continuously_weak_former_high_board_is_removed(self):
        observations = self.observations()
        prices = self.prices([10, 11, 12, 13, 14, 15, 16, 17, 18, 17, 16, 15])
        self.assertEqual(select_cores(self.theme, observations, prices, self.days), [])

    def test_confirmed_break_resets_observed_round_without_historical_honour(self):
        observations = self.observations()
        observations[-2]['closed_limit_up'] = False
        observations[-2]['height'] = None
        prices = self.prices([10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 19, 20.9])
        row = select_cores(self.theme, observations, prices, self.days)[0]
        self.assertEqual(row['round_start'], self.days[-1])
        self.assertEqual(row['round_baseline_date'], self.days[-2])
        self.assertAlmostEqual(row['round_return_pct'], 10)
        self.assertEqual(row['round_segment_evidence']['confirmed_break_date'], self.days[-2])
        self.assertEqual(row['round_start_kind'], 'observed_signal_segment')
        self.assertFalse(row['round_identity_verified'])
        # An absent row cannot create that same reset.
        observations = [r for r in observations if r['date'] != self.days[-2]]
        row = select_cores(self.theme, observations, prices, self.days)[0]
        self.assertEqual(row['round_start'], self.days[0])
        self.assertTrue(row['round_start_left_censored'])
        self.assertIsNone(row['round_return_pct'])

    def test_unconfirmed_missing_observation_does_not_create_break(self):
        observations = self.observations()
        observations[-1]['closed_limit_up'] = False
        observations[-1]['height'] = None
        observations = [r for r in observations if r['date'] != self.days[-2]]
        row = select_cores(self.theme, observations, self.prices(), self.days)[0]
        self.assertEqual(row['lifecycle_stage'], '未知')
        observations = self.observations()
        observations[-1]['closed_limit_up'] = False
        row = select_cores(self.theme, observations, self.prices(), self.days)[0]
        self.assertEqual(row['lifecycle_stage'], '断板')

    def test_reviewed_response_evidence_requires_later_independent_followers(self):
        evidence = dict(code='600001', independently_reviewed=True,
                        causal_status='externally_reviewed_directional_evidence',
                        source_url='https://example.com/review',
                        leader_seal_at=self.days[-1] + 'T09:35:00+08:00', followers=[
                            dict(code='600002', confirmed_response=True,
                                 response_at=self.days[-1] + 'T09:36:00+08:00', source_url='https://example.com/a'),
                            dict(code='600003', confirmed_response=True,
                                 response_at=self.days[-1] + 'T09:37:00+08:00', source_url='https://example.com/b')])
        row = select_cores(self.theme, self.observations(), self.prices(), self.days,
                           {'leadership_evidence': [evidence]})[0]
        self.assertIn('带动王', row['roles'])
        evidence['followers'][0]['response_at'] = self.days[-1] + 'T09:34:00+08:00'
        row = select_cores(self.theme, self.observations(), self.prices(), self.days,
                           {'leadership_evidence': [evidence]})[0]
        self.assertNotIn('带动王', row['roles'])

    def test_partial_market_benchmark_stays_unknown(self):
        observations = self.observations()
        for row in observations:
            row['market_return_pct'] = 1
        row = select_cores(self.theme, observations, self.prices(), self.days)[0]
        self.assertAlmostEqual(row['relative_strength_5d_pct'], (1.06 ** 5 - 1.01 ** 5) * 100, places=3)
        observations[-1]['market_return_pct'] = None
        row = select_cores(self.theme, observations, self.prices(), self.days)[0]
        self.assertIsNone(row['relative_strength_5d_pct'])


class TradeFilterTests(unittest.TestCase):
    def core(self, code='600001'):
        return dict(code=code, name='样例', roles=['爆发王'], current_height=2,
                    lifecycle_stage='连板', current_limit_up=True, all_day_one_word=False,
                    seat='A', observation_date='2026-11-11')

    def plan(self):
        return dict(estimated_adverse_move_pct=3, liquidity_verified=True,
                    execution_evidence_verified=True, t_plus_one_exit_risk_assessed=True,
                    acceleration_risk_assessed=True, entry_condition='verified condition',
                    invalidation_condition='verified invalidation',
                    evidence_url='https://example.com/plan', quote_asof='2026-11-12T09:35:00+08:00')

    def test_daily_only_report_has_zero_candidates_and_no_fake_entry(self):
        result = trade_filter([self.core()])
        self.assertEqual(result['candidates'], [])
        self.assertEqual(len(result['research_setups']), 1)
        self.assertIsNone(result['research_setups'][0]['entry_price'])
        self.assertIsNone(result['actual_positions'])
        self.assertIsNone(result['actual_return'])

    def test_risk_gate_and_one_word_block_even_verified_plan(self):
        core = dict(self.core(), execution_plan=self.plan())
        market = dict(trade_date='2026-11-12', short_term_relay_suitable=True,
                      risk_assessment_verified=True)
        self.assertEqual(len(trade_filter([core], market, 5)['candidates']), 1)
        self.assertEqual(trade_filter([core], market, 2)['candidates'], [])
        core['all_day_one_word'] = True
        self.assertEqual(trade_filter([core], market, 5)['candidates'], [])
        core['all_day_one_word'] = None
        self.assertEqual(trade_filter([core], market, 5)['candidates'], [])

    def test_candidate_limit_four_deduplicated_and_bad_plan_date_blocked(self):
        cores = [dict(self.core('60000' + str(i)), execution_plan=self.plan()) for i in range(1, 10)]
        market = dict(trade_date='2026-11-12', short_term_relay_suitable=True,
                      risk_assessment_verified=True)
        result = trade_filter(cores + cores, market, 5)
        self.assertEqual(len(result['candidates']), 4)
        self.assertEqual(result['observation_count'], 9)
        bad = dict(self.core(), execution_plan=dict(self.plan(), quote_asof='2026-11-11T15:01:00+08:00'))
        self.assertEqual(trade_filter([bad], market, 5)['candidates'], [])

    def test_report_keeps_empty_seats_and_missingness_visible(self):
        report = render_report(dict(trade_date='2026-11-11', selection={'seats': {}},
                                    rankings=[], core_by_theme={}, missing_data=['historical_members'],
                                    coverage={'observed_sessions': 40}, trading={'candidates': []}))
        self.assertIn('已核验活跃股样本', report)
        self.assertEqual(report.count('空缺：'), 3)
        self.assertIn('**0只**', report)
        self.assertIn('historical_members', report)


if __name__ == '__main__':
    unittest.main()
