import math
import re

PREFIXES = ('600', '601', '603', '605', '000', '001', '002', '003')


def number(value):
    try:
        n = float(value)
        return n if math.isfinite(n) else None
    except (TypeError, ValueError):
        return None


def ordinary(code, name):
    return bool(re.fullmatch(r'\d{6}', str(code))) and str(code).startswith(PREFIXES) and bool(name) and not re.search(r'ST|退', str(name), re.I)


def normalize(rows, spot=None):
    result = []
    for r in rows:
        code = str(r.get('代码', '')).zfill(6)
        name = r.get('名称')
        if not ordinary(code, name):
            continue
        quote = (spot or {}).get(code, {})
        o, h, low, close = [number(quote.get(k)) for k in ('今开', '最高', '最低', '最新价')]
        # Only apply to a confirmed closing limit-up pool. Missing OHLC is unknown.
        one_word = None if None in (o, h, low, close) else o == h == low == close
        fields = {'code': code, 'name': name, 'height': number(r.get('连板数')),
                  'first_seal': r.get('首次封板时间'), 'last_seal': r.get('最后封板时间'),
                  'open_count': number(r.get('炸板次数')), 'industry': r.get('所属行业'),
                  'all_day_one_word': one_word, 'execution_verified': False,
                  'eligible_observation': one_word is False,
                  'entry_price': None, 'third_day_return': None, 'max_adverse_excursion': None,
                  'return_kind': '未验证成交，不是实际策略收益'}
        fields['missing_fields'] = [k for k, v in fields.items() if v is None]
        result.append(fields)
    return result


def theme_score(space=None, catalyst=None, recognition=None, freshness=None):
    values = (space, catalyst, recognition)
    if any(v is not None and (not isinstance(v, (float, int)) or not 0 <= v <= 5) for v in values):
        raise ValueError('三问分值必须在0-5')
    if freshness is not None and freshness not in (-1, 0, 1):
        raise ValueError('新鲜度必须为-1/0/1')
    total = None if None in (*values, freshness) else max(0, min(15, sum(values) + freshness))
    return dict(industrial_space=space, catalyst_persistence=catalyst, market_recognition=recognition,
                freshness=freshness, total=total, evidence=[], reviewer=None)


def promotion(yesterday, today, broken):
    """Unknown execution => verified rate remains null, never a fabricated strategy rate."""
    if yesterday is None or today is None or broken is None:
        return {'status': 'missing_dependency', 'observation_rate': None, 'verified_tradable_rate': None, 'rows': []}
    current = {r['code']: r for r in today}
    busted = {r['code'] for r in broken}
    rows = []
    for r in yesterday:
        if r['height'] != 1:
            continue
        t = current.get(r['code'])
        rows.append({'code': r['code'], 'promoted': bool(t and t['height'] == 2),
                     'broken_at_close': r['code'] in busted,
                     'eligible_observation': bool(r['eligible_observation'] and (not t or t['eligible_observation'])),
                     'execution_verified': False, 'entry_price': None, 'third_day_return': None,
                     'max_adverse_excursion': None})
    eligible = [r for r in rows if r['eligible_observation']]
    return {'status': 'observation_only', 'denominator': len(eligible),
            'promoted_count': sum(r['promoted'] for r in eligible),
            'broken_count': sum(r['broken_at_close'] for r in eligible),
            'observation_rate': sum(r['promoted'] for r in eligible) / len(eligible) if eligible else None,
            'verified_tradable_rate': None, 'rows': rows}
