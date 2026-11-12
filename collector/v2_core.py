"""Evidence-constrained core roles and a separate conditional trade research gate.

These functions read saved observations. They neither collect prices nor infer
executions, causal influence, or historical memberships from today's members.
"""
from datetime import date, datetime
import math
from zoneinfo import ZoneInfo

from .model import number, ordinary

TZ = ZoneInfo('Asia/Shanghai')


def _days(days):
    result = sorted(set(str(d) for d in days))[-40:]
    for day in result:
        if date.fromisoformat(day).isoformat() != day:
            raise ValueError('invalid trading date')
    return result


def _valid_bar(row):
    values = [number(row.get(k)) for k in ('open', 'high', 'low', 'close')]
    if None in values:
        return False
    o, h, low, close = values
    return 0 < low <= min(o, close) <= max(o, close) <= h


def _bars(prices, code, days):
    """Use a single basis throughout; reject contradictory same-basis bars."""
    result = {'qfq': {}, 'none': {}}
    for row in prices:
        if row.get('code') != code or row.get('date') not in days:
            continue
        basis = row.get('adjustment')
        if basis not in result or not _valid_bar(row):
            continue
        day = row['date']
        normalized = {k: number(row.get(k)) for k in ('open', 'high', 'low', 'close')}
        if day in result[basis] and any(normalized[k] != number(result[basis][day].get(k)) for k in normalized):
            raise ValueError('conflicting daily price: ' + code + ':' + day + ':' + basis)
        result[basis][day] = row
    # QFQ is preferred, but a sparse QFQ series cannot be combined with raw bars.
    basis = 'qfq' if result['qfq'] else 'none'
    return basis, result[basis]


def _change(bars, days, start, end):
    span = days[days.index(start):days.index(end) + 1]
    if not span or any(d not in bars for d in span):
        return None
    return (number(bars[end]['close']) / number(bars[start]['close']) - 1) * 100


def _one_day(bars, days, index):
    if index <= 0 or days[index] not in bars or days[index - 1] not in bars:
        return None
    return (number(bars[days[index]]['close']) / number(bars[days[index - 1]]['close']) - 1) * 100


def _observations(rows, days):
    result = {}
    for row in rows:
        day, code = row.get('date'), row.get('code')
        if day not in days or not ordinary(code, row.get('name')):
            continue
        key = (code, day)
        if key in result and result[key] != row:
            raise ValueError('conflicting daily stock observation: ' + code + ':' + day)
        result[key] = row
    return result


def _directional_evidence(code, evidence, days):
    """Daily sealing order alone is insufficient. An independently reviewed,
    timestamped response study may support an observed leading role, not proof
    of causality. This hook is empty for the current daily-only collector.
    """
    valid = []
    for item in evidence or []:
        if item.get('code') != code or item.get('independently_reviewed') is not True:
            continue
        if item.get('causal_status') != 'externally_reviewed_directional_evidence':
            continue
        if not str(item.get('source_url', '')).startswith('https://'):
            continue
        try:
            lead = datetime.fromisoformat(item['leader_seal_at'])
            if lead.tzinfo is None or lead.astimezone(TZ).date().isoformat() not in days[-5:]:
                continue
            followers = set()
            for row in item.get('followers', []):
                response = datetime.fromisoformat(row['response_at'])
                if (response.tzinfo is not None and response.astimezone(TZ).date() == lead.astimezone(TZ).date() and response > lead
                        and (response - lead).total_seconds() <= 30 * 60
                        and ordinary(row.get('code'), row.get('name') or 'observed_security')
                        and row.get('code') != code and row.get('confirmed_response') is True
                        and str(row.get('source_url', '')).startswith('https://')):
                    followers.add(row.get('code'))
            if len(followers) >= 2:
                valid.append(item)
        except (KeyError, TypeError, ValueError):
            continue
    return valid


def _lifecycle(stock, bars, days):
    target = days[-1]
    current = stock.get(target)
    up = current.get('closed_limit_up') if current else None
    height = number(current.get('height')) if up is True else None
    prior = stock.get(days[-2]) if len(days) > 1 else None
    evidence = []
    if up is True and height is not None and height >= 2:
        return '连板', [dict(date=target, kind='dated_limit_up_height', height=height)]
    known_breaks = []
    for previous, day in zip(days, days[1:]):
        a, b = stock.get(previous), stock.get(day)
        if a and b and a.get('closed_limit_up') is True and b.get('closed_limit_up') is False:
            known_breaks.append(day)
    last_break = known_breaks[-1] if known_breaks else None
    if up is False and prior and prior.get('closed_limit_up') is True:
        return '断板', [dict(date=target, kind='adjacent_confirmed_limit_up_then_not')]
    if up is True:
        past_ups = [d for d in days[:-1] if stock.get(d, {}).get('closed_limit_up') is True]
        if last_break and past_ups:
            last_up = past_ups[-1]
            previous = days[-2] if len(days) > 1 else None
            if (last_up in bars and target in bars and previous in bars
                    and number(bars[previous]['close']) < number(bars[last_up]['close'])
                    and number(bars[target]['close']) >= number(bars[last_up]['high'])):
                return '反包', [dict(date=target, kind='confirmed_return_to_limit_up_above_prior_up_high',
                                    prior_limit_up_date=last_up, confirmed_break_date=last_break)]
            return '二次走强', [dict(date=target, kind='return_to_limit_up_after_confirmed_break',
                                  confirmed_break_date=last_break)]
        return '启动观察', [dict(date=target, kind='dated_limit_up_no_confirmed_previous_break')]
    today_return = _one_day(bars, days, len(days) - 1)
    if last_break and today_return is not None and today_return > 0:
        return '修复观察', [dict(date=target, kind='price_rise_after_confirmed_break',
                              confirmed_break_date=last_break, daily_price_change_pct=round(today_return, 4))]
    if today_return is not None and today_return < 0:
        return '回撤观察', [dict(date=target, kind='negative_daily_price_change')]
    return '未知', evidence


def _stock_metrics(code, stock, prices, days, theme_id, config):
    baseline_day = config.get('baseline_date')
    if baseline_day is not None:
        if date.fromisoformat(baseline_day).isoformat() != baseline_day or baseline_day >= days[0]:
            raise ValueError('invalid calendar baseline date')
    price_days = ([baseline_day] if baseline_day else []) + days
    basis, bars = _bars(prices, code, price_days)
    target = days[-1]
    if target not in bars:
        return None
    name = stock[max(stock)]['name']
    five = _change(bars, days, days[-6], target) if len(days) >= 6 else None
    day_return = _one_day(bars, days, len(days) - 1)
    # A startup requires a dated association and strength signal. The first
    # calendar row is never silently used as the startup/return denominator.
    signals = []
    quiet = 0
    starts = []
    start_events = {}
    pending_break = None
    for index, day in enumerate(days):
        row = stock.get(day, {})
        previous = stock.get(days[index - 1], {}) if index > 0 else {}
        if previous.get('closed_limit_up') is True and row.get('closed_limit_up') is False:
            pending_break = day
        daily = _one_day(bars, price_days, price_days.index(day))
        linked = theme_id in (row.get('theme_ids') or [])
        strong = linked and (row.get('closed_limit_up') is True or
                             (daily is not None and daily >= config['strong_day_pct']))
        if strong:
            signals.append(day)
            if not starts or pending_break or quiet >= config['round_reset_quiet_sessions']:
                starts.append(day)
                start_events[day] = dict(basis='dated_strength_signal_after_confirmed_break' if pending_break else
                                        'dated_strength_signal_after_observed_quiet_sessions' if starts[:-1] else
                                        'first_dated_strength_signal_in_window',
                                        confirmed_break_date=pending_break)
                pending_break = None
            quiet = 0
        elif daily is not None and daily < config['strong_day_pct']:
            quiet += 1
        else:
            quiet = 0  # missing is not evidence of an inactive trading session
    start = starts[-1] if starts else None
    baseline = price_days[price_days.index(start) - 1] if start and price_days.index(start) > 0 else None
    round_change = _change(bars, price_days, baseline, target) if baseline else None
    start_index = days.index(start) if start else None
    segment_event = start_events.get(start, {})
    left_censored = ((start_index is None or start_index < config['round_reset_quiet_sessions'] + 1)
                     and not segment_event.get('confirmed_break_date'))
    segment = days[start_index:] if start else []
    complete_segment = bool(segment) and all(d in bars for d in segment)
    peak = max(number(bars[d]['close']) for d in segment) if complete_segment else None
    drawdown = (number(bars[target]['close']) / peak - 1) * 100 if peak else None
    recent_daily = [_one_day(bars, days, i) for i in range(max(1, len(days) - 3), len(days))]
    continuously_weak = len(recent_daily) == 3 and all(v is not None and v < 0 for v in recent_daily)
    recent_signal = any(d in days[-3:] for d in signals)
    # Actual inactivity, rather than historical height, retires an old core.
    if continuously_weak or not recent_signal:
        return None
    stage, stage_evidence = _lifecycle(stock, bars, days)
    current = stock.get(target, {})
    heights = [number(r.get('height')) for r in stock.values() if r.get('closed_limit_up') is True]
    heights = [v for v in heights if v is not None]
    market_returns = dict(config.get('market_returns', {}))
    for day, row in stock.items():
        if number(row.get('market_return_pct')) is not None:
            market_returns.setdefault(day, number(row['market_return_pct']))
    benchmark_days = days[-5:] if len(days) >= 6 else []
    benchmark = None
    if benchmark_days and all(number(market_returns.get(d)) is not None for d in benchmark_days):
        benchmark = (math.prod(1 + number(market_returns[d]) / 100 for d in benchmark_days) - 1) * 100
    formal = basis == 'qfq'
    one_word = current.get('all_day_one_word')
    if one_word is None and current.get('closed_limit_up') is True:
        raw_today = [r for r in prices if r.get('code') == code and r.get('date') == target
                     and r.get('adjustment') == 'none' and _valid_bar(r)]
        if len(raw_today) == 1:
            one_word = len({number(raw_today[0][k]) for k in ('open', 'high', 'low', 'close')}) == 1
    risks = ['观察身份不保证成交；次日条件需盘中确认', 'T+1下当天买入不能当天退出']
    if one_word is True:
        risks.append('当日全天一字板：排队成交不可验证')
    if one_word is None:
        risks.append('全天一字板状态未知')
    if day_return is not None and day_return >= config['acceleration_day_pct']:
        risks.append('当日涨幅较大，次日加速与回撤需重新评估')
    if not formal:
        risks.append('仅有不复权价格，正式累计涨幅与角色比较缺失')
    if left_censored:
        risks.append('启动前观察不足：所列启动是窗口内首次有效信号')
    return dict(code=code, name=name, theme_id=theme_id, observation_date=target,
                roles=[], role_evidence={}, role_status='provisional_active_stock_sample',
                selection_scope='dated_active_stock_sample_not_all_constituents',
                mapping_confidence=current.get('mapping_confidence', 'dated_secondary_association'),
                round_start=start, round_baseline_date=baseline,
                round_start_basis=segment_event.get('basis'), round_start_kind='observed_signal_segment',
                round_identity_verified=False, round_segment_evidence=segment_event,
                round_start_left_censored=left_censored,
                round_return_pct=round(round_change, 4) if formal and round_change is not None else None,
                return_5d_pct=round(five, 4) if formal and five is not None else None,
                return_1d_pct=round(day_return, 4) if formal and day_return is not None else None,
                raw_round_price_change_pct=round(round_change, 4) if not formal and round_change is not None else None,
                raw_price_change_5d_pct=round(five, 4) if not formal and five is not None else None,
                adjustment=basis, return_kind='qfq_price_change_not_strategy_return' if formal else 'unadjusted_price_change_only',
                drawdown_pct=round(drawdown, 4) if drawdown is not None else None,
                drawdown_kind='close_from_observed_round_peak',
                lifecycle_stage=stage, lifecycle_evidence=stage_evidence,
                current_height=number(current.get('height')) if current.get('closed_limit_up') is True else None,
                max_height=max(heights) if heights else None,
                relative_strength_5d_pct=round(five - benchmark, 4) if formal and five is not None and benchmark is not None else None,
                relative_strength_unit='percentage_points_above_compounded_market_return',
                leadership_status='pending_confirmation', leadership_evidence=[],
                recent_strong_signal_dates=[d for d in signals if d in days[-5:]],
                current_limit_up=current.get('closed_limit_up'), all_day_one_word=one_word,
                first_seal=current.get('first_seal'), last_close=number(bars[target]['close']),
                status_lost_conditions=['连续3个已知交易日收盘下跌', '最近3个交易日无有效强势信号',
                                       '最近3个交易日无可验证的本题材关联', '同角色出现证据更充分的新核心'],
                risks=risks, execution_verified=False, entry_price=None,
                actual_return=None)


def select_cores(theme_id, observations, prices, days, config=None):
    """Select at most one winner for each evidenced role; combine repeats.

    A role means the leader within the verified active-stock sample. It does
    not assert that an unobserved constituent has a lower return. No price or
    insufficient evidence can correctly result in an empty list.
    """
    settings = dict(strong_day_pct=5.0, round_reset_quiet_sessions=3,
                    explosion_min_pct=5.0, acceleration_day_pct=9.0)
    settings.update(config or {})
    if any(number(settings[k]) is None or settings[k] < 0 for k in
           ('strong_day_pct', 'round_reset_quiet_sessions', 'explosion_min_pct', 'acceleration_day_pct')):
        raise ValueError('invalid core selection settings')
    days = _days(days)
    if not days:
        return []
    saved = _observations(observations, days)
    latest_identity = {}
    for row in observations:
        if row.get('date') in days:
            code = row.get('code')
            if code not in latest_identity or row['date'] >= latest_identity[code]['date']:
                latest_identity[code] = row
    identities = {code for (code, day), row in saved.items()
                  if day in days[-3:] and theme_id in (row.get('theme_ids') or [])
                  and ordinary(code, latest_identity[code].get('name'))}
    candidates = []
    for code in sorted(identities):
        stock = {day: row for (c, day), row in saved.items() if c == code}
        row = _stock_metrics(code, stock, prices, days, theme_id, settings)
        if row is not None:
            evidence = _directional_evidence(code, settings.get('leadership_evidence'), days)
            if evidence:
                row['leadership_status'] = 'reviewed_directional_response_observation'
                row['leadership_evidence'] = evidence
            candidates.append(row)
    winners = {}

    def assign(role, candidates_for_role, metric, note):
        if not candidates_for_role:
            return
        best = sorted(candidates_for_role, key=lambda r: (-metric(r), r['code']))[0]
        row = winners.setdefault(best['code'], best)
        row['roles'].append(role)
        row['role_evidence'][role] = dict(basis=note, sample_size=len(candidates_for_role),
                                        observation_date=days[-1], scope=row['selection_scope'])

    assign('涨幅王', [r for r in candidates if r['round_return_pct'] is not None and r['round_return_pct'] > 0],
           lambda r: r['round_return_pct'], '窗口内有日期证据的最近观察分段至今前复权价格涨幅领先；不是真实行情起点或策略收益')
    assign('带动王', [r for r in candidates if r['leadership_evidence']],
           lambda r: len(r['leadership_evidence']), '经独立复核的分钟先行及后续响应观察；不等同于因果证明')
    def explosion(row):
        return max(v for v in (row['return_5d_pct'], row['return_1d_pct']) if v is not None)
    assign('爆发王', [r for r in candidates
                        if any(v is not None and v >= settings['explosion_min_pct']
                               for v in (r['return_5d_pct'], r['return_1d_pct']))],
           explosion, '最近1至5个交易日的前复权价格涨幅领先，且最近3日有本题材强势证据')
    return sorted(winners.values(), key=lambda r: (-len(r['roles']), r['code']))[:3]


def trade_filter(cores, market_context=None, risk_budget_pct=None):
    """Conditional research candidates; never an order, fill, or position list.

    Saved daily bars cannot establish an executable next-session entry. The
    current collector supplies none of the verified intraday plan evidence,
    so its normal result is zero actionable candidates plus research setups.
    """
    market = market_context or {}
    budget = number(risk_budget_pct)
    unique = {}
    for row in cores:
        if ordinary(row.get('code'), row.get('name')):
            unique.setdefault(row['code'], row)
    setups, candidates, blocked = [], [], []
    for row in list(unique.values())[:9]:
        height, stage = number(row.get('current_height')), row.get('lifecycle_stage')
        patterns = []
        if row.get('current_limit_up') is True and height == 1:
            patterns.append('首板后二板接力：次日换手、承接和封板需盘中确认')
        if row.get('current_limit_up') is True and height in (2, 3):
            patterns.append('三四板换手接力：次日分歧承接和换手需盘中确认')
        if stage in ('修复观察', '反包', '二次走强'):
            patterns.append('老龙头分歧后二次转强：核心身份与修复持续性需再次确认')
        if not patterns:
            blocked.append(dict(code=row['code'], reasons=['没有符合所研究三种模式的当日证据']))
            continue
        setups.append(dict(code=row['code'], name=row['name'], patterns=patterns,
                           status='conditional_research_only', entry_price=None, execution_verified=False))
        reasons = []
        if not row.get('roles'):
            reasons.append('核心角色证据不足')
        if market.get('short_term_relay_suitable') is not True or market.get('risk_assessment_verified') is not True:
            reasons.append('短线接力市场适配未确认')
        if row.get('seat', row.get('focus_seat')) not in ('A', 'B', 'C'):
            reasons.append('重点题材席位未确认')
        if budget is None or budget <= 0:
            reasons.append('回撤风险预算未设置')
        if row.get('all_day_one_word') is not False:
            reasons.append('一字板或一字板状态未知，不能确认可成交')
        plan = row.get('execution_plan') or {}
        expected_risk = number(plan.get('estimated_adverse_move_pct'))
        if expected_risk is None or expected_risk < 0 or (budget is not None and expected_risk > budget):
            reasons.append('潜在回撤未核实或超出风险预算')
        for key, message in (('liquidity_verified', '流动性未验证'),
                             ('execution_evidence_verified', '盘中入场证据未验证'),
                             ('t_plus_one_exit_risk_assessed', 'T+1退出风险未评估'),
                             ('acceleration_risk_assessed', '价格加速风险未评估')):
            if plan.get(key) is not True:
                reasons.append(message)
        if not plan.get('entry_condition') or not plan.get('invalidation_condition'):
            reasons.append('入场或失效条件缺失')
        if not str(plan.get('evidence_url', '')).startswith('https://'):
            reasons.append('入场证据来源缺失')
        try:
            observed = datetime.fromisoformat(plan['quote_asof'])
            if observed.tzinfo is None or observed.astimezone(TZ).date().isoformat() != market.get('trade_date'):
                reasons.append('盘中证据日期或时区不匹配')
        except (KeyError, TypeError, ValueError):
            reasons.append('盘中证据时间缺失')
        if reasons:
            blocked.append(dict(code=row['code'], reasons=reasons))
        elif len(candidates) < 4:
            candidates.append(dict(code=row['code'], name=row['name'], patterns=patterns,
                                   entry_condition=plan['entry_condition'],
                                   invalidation_condition=plan['invalidation_condition'],
                                   estimated_adverse_move_pct=expected_risk,
                                   status='verified_conditions_research_candidate',
                                   execution_verified=False, entry_price=None))
    return dict(candidates=candidates, research_setups=setups, blocked=blocked,
                observation_count=len(list(unique)[:9]), max_observations=9,
                max_planned_positions=4, actual_positions=None, actual_return=None,
                note='候选仍是有条件的研究优先级；未推断下单、持仓、实际买价或可成交收益。')


def _fmt(value, suffix=''):
    return '未知' if number(value) is None else f'{number(value):.2f}{suffix}'


def render_report(report):
    """Compact human output; the JSON retains the full evidence and coverage."""
    target = report.get('trade_date', '未知')
    lines = [f'# A股最强题材与龙头精选 V2｜{target}', '',
             '研究范围：普通沪深主板非ST；最多3个题材、每题材最多3只核心股。', '']
    coverage = report.get('coverage', {})
    missing = report.get('missing_data', [])
    provisional = report.get('ranking_scope') != 'verified_full_market' or bool(missing)
    if provisional:
        lines += ['当前为**已核验活跃股样本的观察排名**。历史成分或行情覆盖不足，不能表述为已确认的全市场最强；缺失值保持未知。', '']
    rankings = {r['theme_id']: r for r in report.get('rankings', [])}
    selection = report.get('selection', {})
    seats = selection.get('seats', {})
    core_by_theme = report.get('core_by_theme', {})
    for seat, label in (('A', '最强主线'), ('B', '最强挑战者'), ('C', '新晋热点')):
        value = seats.get(seat)
        ident = value.get('theme_id') if isinstance(value, dict) else value
        row = rankings.get(ident, {})
        if not ident:
            reason = '可靠新催化与最近1至3日爆发证据不足。' if seat == 'C' else '当前证据未达到席位要求。'
            lines += [f'## {label} {seat}', '', '空缺：' + reason, '']
            continue
        name = row.get('theme_name', ident)
        windows = row.get('windows', {})
        def score(window):
            item = windows.get(str(window), windows.get(window, {}))
            return _fmt(item.get('score', item.get('activity_score')))
        lines += [f'## {label} {seat}｜{name}', '',
                  f'5日 {_fmt(None) if not windows else score(5)}｜10日 {score(10)}｜20日 {score(20)}｜40日 {score(40)}｜综合 {_fmt(row.get("composite_score"))}｜观察排名 {row.get("rank") or "未知"}', '']
        recent = row.get('recent_active_days')
        if recent is not None:
            lines += [f'最近5个交易日有强势信号 {recent}日；最近活跃日期 {row.get("last_active_date") or "未知"}。', '']
        if seat == 'B':
            gap = number(selection.get('challenger_gap'))
            pending = selection.get('state', {}).get('pending')
            if gap is not None:
                lines += [f'与A的综合分差（A−B）：{gap:+.2f}；负值表示B分数暂时领先，席位仍需满足换位确认规则。', '']
            if pending:
                lines += [f'正在确认换位：领先至少 {pending.get("required_margin")}分，已持续 {pending.get("sessions")} / {pending.get("required_sessions")}个相邻交易日。', '']
        notes = value.get('reason') if isinstance(value, dict) else None
        if notes:
            lines += [str(notes), '']
        cores = core_by_theme.get(ident, [])[:3]
        for stock in cores:
            roles = '、'.join(stock.get('roles', []))
            height = number(stock.get('current_height'))
            height_text = f'{height:g}板' if height is not None else '未封板' if stock.get('current_limit_up') is False else '未知'
            lines += [f'- **{stock["name"]} {stock["code"]}｜{roles}**：'
                      f'观察轮 {_fmt(stock.get("round_return_pct"), "%")}（分段信号 {stock.get("round_start") or "未知"}）；'
                      f'5日 {_fmt(stock.get("return_5d_pct"), "%")}；距观察轮收盘峰值 {_fmt(stock.get("drawdown_pct"), "%")}；'
                      f'{stock.get("lifecycle_stage", "未知")}，当前连板 {height_text}。'
                      f'相对市场5日强度 {_fmt(stock.get("relative_strength_5d_pct"), "个百分点")}。']
            proof = [v.get('basis') for v in stock.get('role_evidence', {}).values() if isinstance(v, dict) and v.get('basis')]
            if proof:
                lines += ['  依据：' + '；'.join(dict.fromkeys(proof)) + '。']
            if stock.get('all_day_one_word') is True:
                lines += ['  风险：当日全天一字板，未验证排队成交。']
            elif stock.get('all_day_one_word') is None:
                lines += ['  风险：一字板状态及可成交性尚未验证。']
            if stock.get('round_start_left_censored'):
                lines += ['  启动点是窗口内首次有日期证据的强势信号，启动前观察不足。']
        if not cores:
            lines += ['- 核心股空缺：可验证的近期角色证据不足。']
        if not any('带动王' in r.get('roles', []) for r in cores):
            lines += ['- 带动王：待确认，日线同步上涨或先封板不足以证明带动。']
        lines += ['']
    lines += ['## 每日变化', '']
    changes = report.get('changes', selection.get('changes', []))
    if isinstance(changes, dict):
        for label, values in changes.items():
            if values:
                lines.append(f'- {label}：' + str(values))
    elif changes:
        def name_for(ident):
            return rankings.get(ident, {}).get('theme_name', ident or '空缺')
        for value in changes:
            if not isinstance(value, dict):
                lines.append('- ' + str(value))
            elif value.get('kind') == 'seat_changed':
                action = '首次记录' if value.get('previous') is None else '席位变化'
                lines.append(f'- {action} {value.get("seat")}：{name_for(value.get("previous"))} → {name_for(value.get("current"))}。')
            elif value.get('kind') == 'challenger_pending':
                lines.append('- 主线换位待确认，尚未因单日分差正式换位。')
            elif value.get('kind') == 'mainline_swapped':
                evidence = value.get('evidence', {})
                lines.append(f'- 正式主线换位：{name_for(evidence.get("incumbent"))} → {name_for(evidence.get("challenger"))}；'
                             f'领先 {evidence.get("score_gap")}分、确认 {evidence.get("sessions")}个交易日。')
            elif value.get('kind') in ('new_core', 'initial_core_observation'):
                action = '新晋核心' if value['kind'] == 'new_core' else '首次记录核心'
                lines.append(f'- {action}：{value.get("name", "")} {value.get("code")}｜' + '、'.join(value.get('roles', [])) + '。')
            elif value.get('kind') == 'removed_from_focus_pool':
                lines.append(f'- 从重点池移出：{value.get("name", "")} {value.get("code")}；'
                             f'{value.get("reason", "当日角色或题材席位证据不足")}。')
            elif value.get('kind') == 'core_role_change':
                theme = name_for(value.get('theme_id')) if value.get('theme_id') else ''
                lines.append(f'- 核心角色变化：{theme} {value.get("code")}，'
                             + '、'.join(value.get('previous', [])) + ' → ' + '、'.join(value.get('current', [])) + '。')
            else:
                lines.append('- ' + str(value))
    if not changes:
        lines += ['- 无可验证的变化；首次运行不能推造昨日席位。']
    trading = report.get('trading', {})
    lines += ['', '## 实盘研究', '',
              f'满足已验证条件的研究候选：**{len(trading.get("candidates", []))}只**；实际持仓计划上限4只。']
    if not trading.get('candidates'):
        lines += ['缺少次日盘中入场、可成交性或风险预算证据时保持0只；观察角色不自动产生买入条件。']
    lines += ['一字板排队成交与T+1退出风险需单独核实。所有价格涨幅均非实际策略收益。', '', '## 数据与质量', '']
    for key, value in coverage.items():
        if not isinstance(value, (dict, list)):
            lines.append(f'- {key}：{value}')
    if missing:
        lines += ['- 缺失：' + '；'.join(str(item) for item in missing)]
    lines += ['- 核心降级条件：连续3个已知交易日收盘下跌；最近3日无有效强势信号或可验证题材关联；同角色出现证据更充分的新核心。']
    lines += ['', '证据、完整覆盖表、角色失效条件及原始来源保存在同次运行的JSON和清单中。', '']
    return '\n'.join(lines)
