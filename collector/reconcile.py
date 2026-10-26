"""Compare snapshot membership to exchange rosters, without inferring timestamps."""
import re
from collections import Counter
from datetime import date
from .model import number
from .quality import daily_price

ROSTERS = [('sh_main', 'stock_info_sh_name_code', {'symbol': '主板A股'}, '证券代码', '上市日期'),
           ('sh_star', 'stock_info_sh_name_code', {'symbol': '科创板'}, '证券代码', '上市日期'),
           ('sz', 'stock_info_sz_name_code', {'symbol': 'A股列表'}, 'A股代码', 'A股上市日期'),
           ('bj', 'stock_info_bj_name_code', {}, '证券代码', '上市日期')]


def roster_codes(rows, code_key, date_key, target):
    if not rows:
        return None
    codes = []
    for row in rows:
        code = str(row.get(code_key, ''))
        listed = str(row.get(date_key, ''))[:10]
        if not re.fullmatch(r'\d{6}', code) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', listed):
            return None
        try:
            date.fromisoformat(listed)
        except ValueError:
            return None
        if listed <= target:
            codes.append(code)
    return set(codes) if codes and len(codes) == len(set(codes)) else None


def reconcile_market(spot, rosters, target, szse=None):
    observed_codes = [str(r.get('代码', '')) for r in (spot or [])]
    observed = set(observed_codes)
    expected, groups, unavailable = set(), {}, []
    for name, _, _, code_key, date_key in ROSTERS:
        codes = roster_codes(rosters.get(name), code_key, date_key, target)
        if codes is None:
            unavailable.append(name)
            continue
        expected.update(codes)
        groups[name] = dict(expected=len(codes), observed=len(observed & codes),
                            missing_codes=sorted(codes - observed))
    duplicates = sorted(code for code, count in Counter(observed_codes).items() if count > 1)
    result = dict(trade_date=target, status='unavailable' if not spot or unavailable else
                  'code_coverage_matched' if observed == expected and not duplicates else 'differences_found',
                  expected_count=len(expected) if not unavailable else None, observed_count=len(observed),
                  missing_codes=sorted(expected - observed),
                  unexpected_codes=sorted(observed - expected) if not unavailable else None,
                  duplicate_codes=duplicates, unavailable_rosters=unavailable, exchanges=groups,
                  all_market_verified=False,
                  note='官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘')
    categories = [r for r in (szse or []) if r.get('证券类别') in ('主板A股', '创业板A股')]
    official_amounts = [number(r.get('成交金额')) for r in categories]
    sz_codes = roster_codes(rosters.get('sz'), 'A股代码', 'A股上市日期', target)
    sz_rows = [r for r in (spot or []) if str(r.get('代码')) in (sz_codes or set())]
    amounts = [number(r.get('成交额')) for r in sz_rows]
    comparable = (len(categories) == 2 and len({r['证券类别'] for r in categories}) == 2
                  and None not in official_amounts and sz_codes is not None and bool(sz_rows)
                  and {str(r['代码']) for r in sz_rows} == sz_codes and None not in amounts and not duplicates
                  and all(v >= 0 for v in amounts) and all(v >= 0 for v in official_amounts))
    if comparable:
        official, snapshot = sum(official_amounts), sum(amounts)
        comparable = official > 0 and snapshot >= 0
    result['szse_turnover_check'] = dict(status='not_comparable',
        date_basis='官方接口请求日期；返回表无独立日期列', tolerance=0.005)
    if comparable:
        relative = abs(snapshot - official) / official
        result['szse_turnover_check'].update(status='within_tolerance' if relative <= .005 else 'mismatch',
            official_yuan=official, snapshot_yuan=snapshot, relative_difference=relative)
    return result


def collect_reconciliation(c, spot, target):
    rosters = {}
    for name, function, kwargs, code_key, date_key in ROSTERS:
        rows = c.call('official_roster_' + name, function, **kwargs)
        rosters[name] = rows
        if rows and roster_codes(rows, code_key, date_key, target) is None:
            c.calls['official_roster_' + name]['status'] = 'schema_error'
    szse = c.call('official_szse_summary', 'stock_szse_summary', date=target.replace('-', ''))
    result = reconcile_market(spot, rosters, target, szse)
    initial_missing, supplements = result['missing_codes'], []
    # Bound requests; enrich only an existing snapshot with small roster gaps.
    if spot and not result['unavailable_rosters']:
        names = {str(r.get(code_key)): r.get('证券简称', r.get('A股简称'))
                 for name, _, _, code_key, _ in ROSTERS for r in (rosters.get(name) or [])}
        original_timeout = c.timeout
        try:
            c.timeout = min(original_timeout, 12)
            for code in initial_missing[:5]:
                if not code.startswith(('60', '68', '00', '30')):
                    continue
                symbol = ('sh' if code.startswith(('60', '68')) else 'sz') + code
                quoted = c.call('market_quote_' + code, 'tencent_quote', symbol=symbol, trade_date=target)
                if quoted and len(quoted) == 1 and quoted[0].get('代码') == code and quoted[0].get('quote_date') == target:
                    spot.append(quoted[0])
                    supplements.append(code)
                    continue
                rows = c.call('market_supplement_' + code, 'stock_zh_a_hist_tx',
                    symbol=symbol,
                    start_date=target.replace('-', ''), end_date=target.replace('-', ''), adjust='', timeout=10)
                price = daily_price(rows, target)
                if price is None or price['amount'] is None or price['amount'] < 0:
                    continue
                spot.append({'代码': code, '名称': names.get(code), '今开': price['open'],
                    '最高': price['high'], '最低': price['low'], '最新价': price['close'],
                    '成交额': price['amount'], '成交量': price['volume'], '涨跌幅': None,
                    'quote_date': target, 'supplement_source': '腾讯不复权日线',
                    'note': '无除权参考价，不从前收盘推算涨跌幅；涨跌方向仍缺失'})
                supplements.append(code)
        finally:
            c.timeout = original_timeout
        result = reconcile_market(spot, rosters, target, szse)
    result.update(initial_missing_codes=initial_missing, daily_supplement_codes=supplements)
    return result
