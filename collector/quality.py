"""Date-checked candidate prices and monotonic daily snapshot selection."""
import json
import time
from .model import number, ordinary


def daily_price(rows, target):
    matched = [r for r in (rows or []) if str(r.get('date', ''))[:10] == target]
    if len(matched) != 1:
        return None
    r = matched[0]
    o, h, low, close = [number(r.get(k)) for k in ('open', 'high', 'low', 'close')]
    if None in (o, h, low, close) or not 0 < low <= min(o, close) <= max(o, close) <= h:
        return None
    return dict(date=target, open=o, high=h, low=low, close=close,
                volume=number(r.get('volume')), amount=number(r.get('amount')),
                adjustment='none', source='AKShare / 腾讯')


def candidate_prices(c, pool, quotes, target, budget, cached=()):
    deadline = time.monotonic() + max(0, budget)
    prices, missing = [], []
    original_timeout = c.timeout
    # Stable priority; an interrupted budget must not masquerade as full coverage.
    candidates = sorted((r for r in (pool or []) if ordinary(str(r.get('代码', '')).zfill(6), r.get('名称'))),
                        key=lambda r: (number(r.get('连板数')) != 1, str(r['代码'])))
    codes = {str(r['代码']).zfill(6) for r in candidates}
    for row in cached:
        code = row.get('code')
        price = daily_price([row], target) if row.get('adjustment') == 'none' else None
        if code in codes and code not in quotes and price is not None:
            prices.append(dict(code=code, **price, reused_from_prior_run=True))
            quotes[code] = {'今开': price['open'], '最高': price['high'],
                            '最低': price['low'], '最新价': price['close']}
    try:
        for r in candidates:
            code = str(r['代码']).zfill(6)
            if code in quotes:
                continue
            remaining = deadline - time.monotonic() - c.delay
            if remaining <= 1:
                missing.append(code)
                continue
            c.timeout = min(original_timeout, 15, remaining)
            rows = c.call('price_' + code, 'stock_zh_a_hist_tx',
                          symbol=('sh' if code.startswith('6') else 'sz') + code,
                          start_date=target.replace('-', ''), end_date=target.replace('-', ''),
                          adjust='', timeout=min(c.timeout, 10))
            price = daily_price(rows, target)
            if price is None:
                missing.append(code)
                if rows:
                    c.calls['price_' + code]['status'] = 'date_or_schema_error'
                continue
            prices.append(dict(code=code, **price))
            quotes[code] = {'今开': price['open'], '最高': price['high'],
                            '最低': price['low'], '最新价': price['close']}
    finally:
        c.timeout = original_timeout
    return prices, missing


def coverage(summary):
    v = summary.get('verified', {})
    # Compare sets, never replace a stronger cohort with a weaker one.
    result = {'pool'} if v.get('mainboard_limit_up_count') is not None else set()
    result.update('index:' + r['symbol'] for r in v.get('indices', []))
    result.update('price:' + code for code in summary.get('price_coverage', []))
    result.update(k for k in ('broken_count', 'limit_down_count') if v.get(k) is not None)
    if summary.get('estimates', {}).get('market'):
        result.add('market')
    if summary.get('promotion', {}).get('observation_rate') is not None:
        result.add('promotion')
    return result


def select_snapshot(daily, summary):
    pointer = daily / 'latest.json'
    if pointer.exists():
        old = json.loads(pointer.read_text(encoding='utf-8'))
        prior = daily / 'runs' / old['run_id'] / 'summary.json'
        if prior.exists():
            previous = json.loads(prior.read_text(encoding='utf-8'))
            if previous.get('status') == 'complete' and summary['status'] != 'complete':
                return False
            if not coverage(summary).issuperset(coverage(previous)):
                return False
    pointer.write_text(json.dumps({'run_id': summary['run_id'], 'status': summary['status']},
                                  ensure_ascii=False, indent=2), encoding='utf-8')
    return True
