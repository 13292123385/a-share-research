"""Offline rolling theme research and conservative, replayable seat transitions.

Activity scores describe dated observed associations. A percentile across themes
of different breadth is a research prioritisation, not a sector index return.
Missing source dates are never turned into inactive/zero-count sessions.
"""
from copy import deepcopy
from datetime import date
import math

from .model import number


WINDOWS = (5, 10, 20, 40)
DEFAULT_WEIGHTS = {'5': .50, '10': .25, '20': .20, '40': .05}
ACTIVITY_WEIGHTS = {'persistence': .35, 'limit_up_share': .30,
                    'observed_breadth': .20, 'ladder_height': .15}
FULL_WEIGHTS = {'relative_strength': .30, 'advancing_ratio': .20,
                'turnover_share': .15, 'persistence': .15,
                'limit_up_share': .10, 'ladder_height': .10}


def _config(config=None):
    result = dict(weights=deepcopy(DEFAULT_WEIGHTS), min_mainline_sessions=10,
                  min_recent_active_days=3, swap_margin=5.0,
                  swap_confirm_sessions=2, require_catalyst=True,
                  excluded_seat_themes=[],
                  normalization_method='percentile_minmax_blend')
    result.update(config or {})
    if config and 'window_weights' in config:
        result['weights'] = config['window_weights']
    weights = {str(k): v for k, v in result['weights'].items()}
    if set(weights) != set(DEFAULT_WEIGHTS):
        raise ValueError('weights must specify 5/10/20/40 trading sessions')
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or number(v) is None or v < 0 for v in weights.values()):
        raise ValueError('weights must be finite and nonnegative')
    if not math.isclose(sum(weights.values()), 1, abs_tol=1e-9):
        raise ValueError('weights must sum to 1')
    result['weights'] = {k: float(v) for k, v in weights.items()}
    for key in ('min_mainline_sessions', 'min_recent_active_days', 'swap_confirm_sessions'):
        if not isinstance(result[key], int) or isinstance(result[key], bool) or result[key] < 1:
            raise ValueError(key + ' must be a positive integer')
    if number(result['swap_margin']) is None or result['swap_margin'] < 0:
        raise ValueError('swap_margin must be finite and nonnegative')
    exclusions = result['excluded_seat_themes']
    if not isinstance(exclusions, (list, tuple)) or any(not isinstance(t, str) or not t for t in exclusions):
        raise ValueError('excluded_seat_themes must be an exact list of nonempty theme names or ids')
    result['excluded_seat_themes'] = list(dict.fromkeys(exclusions))
    if result['normalization_method'] not in ('percentile', 'minmax', 'percentile_minmax_blend'):
        raise ValueError('unsupported normalization_method')
    return result


def _date(value):
    if not isinstance(value, str) or date.fromisoformat(value).isoformat() != value:
        raise ValueError('dates must be ISO calendar dates')
    return value


def _mean_complete(values, expected):
    return sum(values) / expected if len(values) == expected else None


def _valid(row, field, lower=0, upper=None):
    value = number(row.get(field)) if row else None
    if value is None or value < lower or (upper is not None and value > upper):
        return None
    return value


def _window(rows, days, size):
    period = days[-size:]
    available_days = len(period)
    values = [rows.get(d) for d in period]
    counts = [_valid(r, 'observed_limit_up_count') for r in values]
    signals = [r.get('active_signal') if r else None for r in values]
    known = sum(v is not None for v in counts)
    shares, heights, breadth, active = [], [], [], []
    rel, advance, turnover = [], [], []
    for r, count, signal in zip(values, counts, signals):
        total = _valid(r, 'market_limit_up_count')
        if count is not None and total is not None:
            # A source-verified empty market can only have zero observed boards.
            if total > 0:
                shares.append(count / total)
            elif count == 0:
                shares.append(0.0)
        if count is not None:
            breadth.append(float(count >= 3))
            height = _valid(r, 'max_height')
            if height is not None:
                heights.append(height)
            elif count == 0:
                heights.append(0.0)
        if isinstance(signal, bool):
            active.append(float(signal))
        if r and r.get('mapping_scope') == 'complete':
            value = number(r.get('relative_return_pct'))
            if value is not None and value > -100:
                rel.append(value)
            value = _valid(r, 'advancing_ratio', upper=1)
            if value is not None:
                advance.append(value)
            value = _valid(r, 'turnover_share', upper=1)
            if value is not None:
                turnover.append(value)
    components = {
        'persistence': _mean_complete(active, size),
        'limit_up_share': _mean_complete(shares, size),
        'observed_breadth': _mean_complete(breadth, size),
        'ladder_height': _mean_complete(heights, size),
        # The daily field is a theme-minus-market return in percentage points.
        # Its mean is an average daily relative strength, not a compound return.
        'relative_strength': _mean_complete(rel, size),
        'advancing_ratio': _mean_complete(advance, size),
        'turnover_share': _mean_complete(turnover, size),
    }
    samples = dict(persistence=len(active), limit_up_share=len(shares),
                   observed_breadth=len(breadth), ladder_height=len(heights),
                   relative_strength=len(rel), advancing_ratio=len(advance),
                   turnover_share=len(turnover))
    return dict(start=period[0], end=period[-1], requested_sessions=size,
                calendar_sessions=available_days, observed_sessions=known,
                coverage=known / size, components=components,
                component_coverage={k: v / size for k, v in samples.items()},
                units=dict(persistence='ratio', limit_up_share='ratio',
                           observed_breadth='fraction_of_sessions_with_3plus_observed_boards',
                           ladder_height='boards', relative_strength='percentage_points_per_session',
                           advancing_ratio='ratio', turnover_share='ratio'),
                full_mapping_sessions=sum(bool(r and r.get('mapping_scope') == 'complete') for r in values),
                score=None, activity_score=None, full_score=None)


def _percentiles(values):
    """Midrank percentiles; identical observations always receive identical scores."""
    if not values:
        return {}
    if len(values) == 1:
        return {next(iter(values)): 50.0}
    ordered = sorted(values.items(), key=lambda item: (item[1], item[0]))
    result, index = {}, 0
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and ordered[end][1] == ordered[index][1]:
            end += 1
        percentile = 100 * ((index + end - 1) / 2) / (len(ordered) - 1)
        result.update({ident: percentile for ident, _ in ordered[index:end]})
        index = end
    return result


def _normalize(values, method):
    """Retain magnitude as well as ordinal position in a long tail of topics."""
    percentiles = _percentiles(values)
    low = min(values.values()) if values else None
    high = max(values.values()) if values else None
    if values and high != low:
        scaled = {ident: 100 * (value - low) / (high - low) for ident, value in values.items()}
    else:
        scaled = {ident: 50.0 for ident in values}
    if method == 'percentile':
        result = percentiles
        formula = 'midrank_percentile'
    elif method == 'minmax':
        result = scaled
        formula = '100 * (value - cross_theme_min) / (cross_theme_max - cross_theme_min)'
    else:
        result = {ident: .5 * percentiles[ident] + .5 * scaled[ident] for ident in values}
        formula = '0.5 * midrank_percentile + 0.5 * cross_theme_minmax_0_to_100'
    return result, dict(method=method, formula=formula, candidate_count=len(values),
                        raw_min=low, raw_max=high, equal_value_score=50.0)


def _catalyst(rows, target, earliest):
    result = []
    for r in rows:
        if r.get('catalyst_verified') is not True:
            continue
        for item in r.get('catalyst_evidence') or []:
            if not isinstance(item, dict):
                continue
            observed = item.get('date') or item.get('observed_at', '')[:10]
            source_url = item.get('source_url') or item.get('url')
            if (isinstance(observed, str) and len(observed) == 10 and earliest <= observed <= target and
                    isinstance(source_url, str) and source_url.startswith('https://')):
                result.append(deepcopy(item))
    return result


def rank_themes(theme_daily, days, config=None):
    """Rank only current, dated evidence; all themes share identical score inputs.

    The same global window set and metric weights apply to every theme. Missing
    observations are not reweighted away for an individual theme. Full scores
    require complete dated membership plus all price/breadth/turnover components.
    """
    settings = _config(config)
    days = list(days)
    if not days or days != sorted(set(days)):
        raise ValueError('trading calendar must be nonempty, sorted and unique')
    for d in days:
        _date(d)
    days = days[-40:]
    target = days[-1]
    by_theme = {}
    names = {}
    for row in theme_daily:
        observed = _date(row['date'])
        if observed > target:
            raise ValueError('future theme observation')
        if observed < days[0]:
            continue
        if observed not in days:
            raise ValueError('theme observation outside trading calendar')
        ident = row['theme_id']
        if not isinstance(ident, str) or not ident:
            raise ValueError('theme id required')
        rows = by_theme.setdefault(ident, {})
        if observed in rows:
            raise ValueError('duplicate theme/date observation')
        signal = row.get('active_signal')
        if signal is not None and not isinstance(signal, bool):
            raise ValueError('active signal must be bool or null')
        count = _valid(row, 'observed_limit_up_count')
        total = _valid(row, 'market_limit_up_count')
        if count is not None and total is not None and count > total:
            raise ValueError('observed theme boards exceed market boards')
        rows[observed] = row
        if ident not in names or observed > names[ident][0]:
            names[ident] = (observed, row.get('theme_name') or ident)
    rankings = []
    for ident, rows in sorted(by_theme.items()):
        # A theme last active beyond the 40-session window does not rank.
        active_dates = [d for d in days if rows.get(d, {}).get('active_signal') is True]
        if not active_dates:
            continue
        recent = [rows.get(d, {}) for d in days[-5:]]
        recent_active = sum(r.get('active_signal') is True for r in recent)
        total_known = sum(_valid(rows.get(d), 'observed_limit_up_count') is not None for d in days)
        counts3 = [_valid(rows.get(d), 'observed_limit_up_count') for d in days[-3:]]
        before = [_valid(rows.get(d), 'observed_limit_up_count') for d in days[-10:-3]]
        known_before = [v for v in before if v is not None]
        known3 = [v for v in counts3 if v is not None]
        # A revival qualifies only after a quiet pre-breakout period; a missing
        # pre-breakout history does not prove a new theme.
        previous_average = sum(known_before) / len(known_before) if known_before else None
        new = bool(len(known3) == 3 and len(known_before) == 7 and
                   max(known3) >= 3 and previous_average is not None and
                   max(known3) >= max(3, 2 * previous_average) and
                   sum(v > 0 for v in known_before) <= 2 and 1 <= recent_active <= 3)
        catalyst = _catalyst([rows.get(d, {}) for d in days[-3:]], target, days[-3:][0])
        excluded = ident in settings['excluded_seat_themes'] or names[ident][1] in settings['excluded_seat_themes']
        item = dict(theme_id=ident, theme_name=names[ident][1], as_of=target,
                    previous_trading_date=days[-2] if len(days) > 1 else None,
                    windows={str(size): _window(rows, days, size) for size in WINDOWS},
                    recent_active_days=recent_active, last_active_date=active_dates[-1],
                    observed_sessions=total_known, new_hotspot=new,
                    catalyst_verified=bool(catalyst), catalyst_evidence=catalyst,
                    eligible_mainline=False, composite_score=None, activity_score=None,
                    full_score=None, score_kind='unavailable',
                    theme_kind='generic_attribute' if excluded else 'research_theme_unverified',
                    seat_excluded=excluded,
                    seat_excluded_reason='configured_generic_attribute_exclusion' if excluded else None,
                    scope='dated_observed_associations', missing=[])
        rankings.append(item)
    if not rankings:
        return []

    # Complete-data scores and partial-data scores never mix in a single rank.
    for size in WINDOWS:
        key = str(size)
        for metric in set(ACTIVITY_WEIGHTS) | set(FULL_WEIGHTS):
            values = {r['theme_id']: r['windows'][key]['components'][metric] for r in rankings
                      if r['windows'][key]['components'][metric] is not None}
            normalized, normalization = _normalize(values, settings['normalization_method'])
            for r in rankings:
                r['windows'][key].setdefault('normalized_components', {})[metric] = normalized.get(r['theme_id'])
                r['windows'][key].setdefault('normalization', {})[metric] = deepcopy(normalization)
        for r in rankings:
            w = r['windows'][key]
            norm = w['normalized_components']
            if all(norm.get(metric) is not None for metric in ACTIVITY_WEIGHTS):
                w['activity_score'] = round(sum(norm[m] * weight for m, weight in ACTIVITY_WEIGHTS.items()), 6)
            if w['full_mapping_sessions'] == size and all(norm.get(m) is not None for m in FULL_WEIGHTS):
                w['full_score'] = round(sum(norm[m] * weight for m, weight in FULL_WEIGHTS.items()), 6)

    weighted_keys = [k for k, weight in settings['weights'].items() if weight > 0]
    use_full = all(r['windows'][k]['full_score'] is not None for r in rankings for k in weighted_keys)
    basis = 'full_score' if use_full else 'activity_score'
    # Shared windows only. An individual missing theme cannot obtain a higher
    # score by dropping its weaker window. Unused windows remain explicit nulls.
    common_keys = [k for k in weighted_keys if all(r['windows'][k][basis] is not None for r in rankings)]
    weight_sum = sum(settings['weights'][k] for k in common_keys)
    for r in rankings:
        for key, w in r['windows'].items():
            w['score'] = w[basis]
            w['score_kind'] = 'full_strength' if use_full else 'partial_observed_activity'
            if w['coverage'] < 1:
                r['missing'].append('window_' + key + '_source_sessions')
        for k in weighted_keys:
            if r['windows'][k]['full_score'] is None:
                r['missing'].append('window_' + k + '_verified_membership_quotes_or_market_metrics')
        r['configured_weights'] = deepcopy(settings['weights'])
        r['normalization_method'] = settings['normalization_method']
        # Preserve the configured weights even while bootstrapping history.
        # A partial contribution has an explicit uncertainty interval; there is
        # no per-theme rescaling and no imputation of the missing window score.
        r['effective_weights'] = {k: settings['weights'][k] for k in common_keys}
        r['weight_coverage'] = weight_sum
        r['common_windows'] = common_keys
        r['omitted_windows'] = [k for k in weighted_keys if k not in common_keys]
        if weight_sum:
            r['composite_score'] = round(sum(r['windows'][k][basis] * w for k, w in r['effective_weights'].items()), 6)
            r['score_kind'] = ('full_strength' if use_full else 'partial_observed_activity') if math.isclose(weight_sum, 1) else 'partial_window_observed_activity'
            r['activity_score'] = (round(sum(r['windows'][k]['activity_score'] * w for k, w in r['effective_weights'].items()), 6)
                                   if all(r['windows'][k]['activity_score'] is not None for k in common_keys) else None)
        r['partial_composite_score'] = r['composite_score'] if weight_sum < 1 else None
        r['composite_interval'] = ([r['composite_score'], round(r['composite_score'] + 100 * (1 - weight_sum), 6)]
                                   if r['composite_score'] is not None else [None, None])
        if all(r['windows'][k]['full_score'] is not None for k in weighted_keys):
            r['full_score'] = round(sum(r['windows'][k]['full_score'] * settings['weights'][k] for k in weighted_keys), 6)
        r['eligible_mainline'] = bool(not r['seat_excluded'] and r['composite_score'] is not None and '5' in common_keys and '10' in common_keys and
                                      r['observed_sessions'] >= settings['min_mainline_sessions'] and
                                      r['recent_active_days'] >= settings['min_recent_active_days'])
        if r['new_hotspot'] and not r['catalyst_verified']:
            r['missing'].append('verified_recent_catalyst')
    rankings.sort(key=lambda r: (r['composite_score'] is None, -(r['composite_score'] or 0), r['theme_id']))
    for position, r in enumerate(rankings, 1):
        r['rank'] = position if r['composite_score'] is not None else None
    return rankings


def _seat(ident, rows):
    if ident is None:
        return None
    result = deepcopy(rows[ident])
    result['seat_status'] = ('verified_strength_research' if result['score_kind'] == 'full_strength'
                             else 'provisional_observation')
    return result


def select_seats(rankings, previous=None, config=None):
    """Select at most A/B/C and persist evidence for hysteresis between A and B."""
    settings = _config(config)
    rankings = deepcopy(rankings)
    # Reapply the current exclusion configuration when loading a saved ranking.
    # Exclusion affects seats only; the observed ranking remains auditable.
    for row in rankings:
        configured = (row['theme_id'] in settings['excluded_seat_themes'] or
                      row.get('theme_name') in settings['excluded_seat_themes'])
        if configured or row.get('seat_excluded'):
            row.update(seat_excluded=True, theme_kind='generic_attribute',
                       seat_excluded_reason='configured_generic_attribute_exclusion',
                       eligible_mainline=False)
    rows = {r['theme_id']: r for r in rankings}
    if len(rows) != len(rankings):
        raise ValueError('duplicate theme ranking')
    dates = {r['as_of'] for r in rankings}
    if len(dates) > 1:
        raise ValueError('mixed ranking dates')
    previous = deepcopy(previous or {})
    target = next(iter(dates)) if dates else None
    if target is None:
        # Empty rankings cannot supply a date. Caller may pass explicit as_of for
        # an empty market day, preserving the distinction from no run at all.
        target = settings.get('as_of')
    if target:
        _date(target)
    if previous.get('target_date') and target and previous['target_date'] > target:
        raise ValueError('future seat state')
    if target and any(item.get('date') and item['date'] > target for item in previous.get('history', [])):
        raise ValueError('future seat history')
    old_seats = previous.get('seats') or {}
    old_seats = {k: (v.get('theme_id') if isinstance(v, dict) else v) for k, v in old_seats.items()}
    eligible = [r for r in rankings if r.get('eligible_mainline') and r.get('composite_score') is not None]
    eligible.sort(key=lambda r: (-r['composite_score'], r['theme_id']))
    eligible_ids = {r['theme_id'] for r in eligible}
    current = old_seats.get('A') if old_seats.get('A') in eligible_ids else None
    pending = None
    swap_evidence = None
    if current is None and eligible:
        current = eligible[0]['theme_id']
    elif current is not None and eligible:
        contender = next((r for r in eligible if r['theme_id'] != current), None)
        if contender and contender['composite_score'] - rows[current]['composite_score'] >= settings['swap_margin']:
            prior_pending = previous.get('pending') or {}
            prior_date = previous.get('target_date')
            prior_trading_date = rows[current].get('previous_trading_date')
            same_challenge = (prior_pending.get('challenger') == contender['theme_id'] and
                              prior_pending.get('incumbent') == current)
            if same_challenge and prior_date == target:
                streak = prior_pending.get('sessions', 1)
            elif same_challenge and prior_date == prior_trading_date:
                streak = prior_pending.get('sessions', 0) + 1
            else:
                streak = 1
            pending = dict(challenger=contender['theme_id'], incumbent=current,
                           sessions=streak, observed_date=target,
                           score_gap=round(contender['composite_score'] - rows[current]['composite_score'], 6),
                           required_margin=settings['swap_margin'],
                           required_sessions=settings['swap_confirm_sessions'])
            if streak >= settings['swap_confirm_sessions']:
                swap_evidence = deepcopy(pending)
                current = contender['theme_id']
                pending = None
    challenger = next((r['theme_id'] for r in eligible if r['theme_id'] != current), None)
    new_candidates = [r for r in rankings if r['theme_id'] not in (current, challenger) and
                      not r.get('seat_excluded') and
                      r.get('new_hotspot') and r.get('composite_score') is not None and
                      (r.get('catalyst_verified') or not settings['require_catalyst'])]
    new_candidates.sort(key=lambda r: (-(r['windows']['5']['score'] or 0), -r['composite_score'], r['theme_id']))
    emerging = new_candidates[0]['theme_id'] if new_candidates else None
    selected = dict(A=current, B=challenger, C=emerging)
    changes = []
    for key, ident in selected.items():
        prior = old_seats.get(key)
        if ident != prior:
            reason = ('confirmed_challenger_margin' if key == 'A' and swap_evidence else
                      'incumbent_no_longer_eligible' if key == 'A' and prior and prior not in eligible_ids else
                      'initial_or_ranked_selection')
            changes.append(dict(kind='seat_changed', seat=key, previous=prior, current=ident, reason=reason))
    if swap_evidence:
        changes.append(dict(kind='mainline_swapped', evidence=swap_evidence))
    if pending:
        changes.append(dict(kind='challenger_pending', evidence=deepcopy(pending)))
    history = [r for r in previous.get('history', []) if r.get('date') != target]
    history.append(dict(date=target, seats=deepcopy(selected)))
    state = dict(target_date=target, seats=selected, pending=pending,
                 history=history[-40:], policy=dict(swap_margin=settings['swap_margin'],
                                                  swap_confirm_sessions=settings['swap_confirm_sessions']))
    result = dict(rankings=deepcopy(rankings), seats={k: _seat(v, rows) for k, v in selected.items()},
                  changes=changes, state=state)
    result['watch_new_hotspots'] = [r['theme_id'] for r in rankings if r.get('new_hotspot') and
                                   r['theme_id'] not in selected.values()]
    result['challenger_gap'] = (round(rows[current]['composite_score'] - rows[challenger]['composite_score'], 6)
                                if current and challenger else None)
    return result
