"""Independent V2 analysis on top of existing collectors and archived evidence."""
import argparse
import hashlib
import json
import os
import sys
from importlib.metadata import version
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from .inventory import inventory
from .run import Collector, dump, table, TZ
from .v2_data import (get_reviews, selected_inputs, build_daily, core_price_candidates,
                      collect_core_prices, upstream_table)
from .v2_data import light_market_scan
from .v2_scoring import rank_themes, select_seats
from .v2_core import select_cores, trade_filter, render_report
from .lifecycle import prior_tables


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def selection_trace(observations, days, reviews, selected, config, previous=None):
    daily, checks = build_daily(observations, days, reviews, selected)
    history = []
    if previous:
        rankings = rank_themes(daily, days, config)
        selection = select_seats(rankings, previous, dict(config, as_of=days[-1]))
        history.append(dict(date=days[-1], state=selection['state'], changes=selection['changes']))
    else:
        # First deployment reconstructs only a retrospective evidence trace;
        # it is never presented as states actually published on those dates.
        for index, day in enumerate(days):
            prefix_days = days[:index + 1]
            subset, _ = build_daily([r for r in observations if r['date'] <= day], prefix_days,
                [r for r in reviews if r['date'] <= day], [r for r in selected if r['date'] <= day])
            rankings = rank_themes(subset, days[:index + 1], config)
            selection = select_seats(rankings, previous, dict(config, as_of=day))
            previous = selection['state']
            history.append(dict(date=day, state=previous, changes=selection['changes'],
                                kind='retrospective_reconstruction_not_historical_signal'))
    return daily, checks, rankings, selection, history


def compute(inputs):
    """Deterministic output: no clock, filesystem, network or mutable source lookups."""
    days, config = inputs['days'], inputs['config']
    observations, prices = inputs['observations'], inputs['prices']
    daily, checks, rankings, selection, history = selection_trace(observations, days,
        inputs['review_coverage'], inputs['selected_inputs'], config, inputs.get('previous_state'))
    selection = {k: v for k, v in selection.items() if k != 'rankings'}
    core_by_theme, all_cores = {}, []
    for seat, row in selection['seats'].items():
        if not row:
            continue
        cores = select_cores(row['theme_id'], observations, prices, days,
                             dict(config, baseline_date=inputs.get('baseline_date')))
        for core in cores:
            core['seat'] = seat
        core_by_theme[row['theme_id']] = cores
        all_cores.extend(cores)
    changes = list(selection['changes'])
    previous_cores = inputs.get('previous_cores', {})
    old_by_code = {r['code']: r for values in previous_cores.values() for r in values}
    new_by_code = {r['code']: r for r in all_cores}
    for code in sorted(new_by_code.keys() - old_by_code.keys()):
        changes.append(dict(kind='new_core' if previous_cores else 'initial_core_observation', code=code,
            name=new_by_code[code]['name'], roles=new_by_code[code]['roles']))
    for code in sorted(old_by_code.keys() - new_by_code.keys()):
        changes.append(dict(kind='removed_from_focus_pool', code=code,
            reason='题材席位或当日角色证据未达要求；不删除历史记录'))
    old_roles = {(theme, row['code']): row['roles'] for theme, rows in previous_cores.items() for row in rows}
    new_roles = {(theme, row['code']): row['roles'] for theme, rows in core_by_theme.items() for row in rows}
    for theme, code in sorted(old_roles.keys() & new_roles.keys()):
        if old_roles[(theme, code)] != new_roles[(theme, code)]:
            changes.append(dict(kind='core_role_change', code=code, theme_id=theme,
                previous=old_roles[(theme, code)], current=new_roles[(theme, code)]))
    quote_days = sum(r['mainboard_quote_rows'] > 0 for r in inputs['market_coverage'])
    matched = sum(r['matched'] for r in checks)
    coverage = dict(window_start=days[0], window_end=days[-1], requested_trading_days=len(days),
        dated_review_days=sum(r['status'] == 'available' for r in inputs['review_coverage']),
        complete_historical_membership_days=0,
        archived_market_quote_days=quote_days, verified_full_market_ohlcv_days=0,
        selected_limit_pool_days=len(inputs['selected_inputs']),
        independent_pool_code_matches=f'{matched}/{len(checks)}',
        observed_stock_days=len(observations), observed_themes_scanned=len({t for r in observations for t in r['theme_ids']}),
        ranked_resonant_themes=len(rankings), core_price_stocks=len(inputs['price_coverage']),
        core_price_eligible_stocks=len(inputs.get('price_eligible_codes', inputs['price_coverage'])),
        price_budget_truncated_stocks=max(0, len(inputs.get('price_eligible_codes', [])) - len(inputs['price_coverage'])),
        core_price_valid_rows=sum(r['adjustment'] == 'qfq' for r in prices),
        reused_lifecycle_unadjusted_rows=sum(r['adjustment'] == 'none' for r in prices),
        core_price_requested_rows=sum(r['requested_sessions'] for r in inputs['price_coverage']),
        minute_data_verified_stocks=0, business_links_verified=0, catalysts_verified=0,
        observed_focus_stocks=len(new_by_code), formal_full_market_rank_available=False)
    missing = ['完整历史题材成分未知，不能用当前成员倒填；正式全市场强度与相对市场收益为空',
        f'40日全主板轻量行情仅有{quote_days}/{len(days)}日已存快照，快照字段未全部独立核验',
        '题材上涨广度、全成分成交份额及全成分炸板数缺少完整分母',
        '第三方历史复盘可能修订，不是当时已知快照，不能用于无偏信号回测',
        '真实业务和新催化未独立验证，C席位可空缺；带动关系待确认',
        '分钟行情、盘口及次日可执行入场缺失，成交与真实策略收益未知']
    if any(not r['matched'] for r in checks):
        missing.append('部分第三方涨停代码与原已选归档不一致，见cross_checks；不覆盖原归档')
    if any(r['status'] != 'available' for r in inputs['review_coverage']):
        missing.append('部分交易日复盘源缺失，不解释为题材零活跃')
    if any(r['status'] != 'available' for r in inputs['price_coverage']):
        missing.append('部分重点股票日线未补全，相关角色收益保留未知')
    if coverage['price_budget_truncated_stocks']:
        missing.append(f"重点价格预算仅覆盖{coverage['core_price_stocks']}/{coverage['core_price_eligible_stocks']}只近期关联股；角色是在有行情样本内比较")
    return dict(schema_version=1, trade_date=days[-1], status='partial_research',
        ranking_scope='dated_partial_active_associations', coverage=coverage,
        rankings=rankings, selection=selection, core_by_theme=core_by_theme,
        changes=changes, state_history=history, cross_checks=checks,
        trading=trade_filter(all_cores, dict(trade_date=days[-1])), missing_data=missing,
        return_kind='复权价格变动研究，非已验证可成交收益',
        automation=inputs.get('automation', {}))


def previous_input(output, target):
    candidates = sorted(Path(output).glob('*/runs/*/report.json'), reverse=True)
    for path in candidates:
        if path.parents[2].name >= target:
            continue
        manifest = path.parent / 'files.json'
        if not manifest.exists():
            continue
        entries = read(manifest)
        item = next((r for r in entries if r['path'] == 'report.json'), None)
        if item and hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256']:
            report = read(path)
            return report['selection']['state'], report['core_by_theme']
    return None, {}


def calendar_input(data, target, supplied=None):
    choices = [Path(supplied)] if supplied else sorted(Path(data).glob('*/runs/*/raw/calendar.json'), reverse=True)
    for path in choices:
        raw = read(path)
        days = sorted({str(r['trade_date'])[:10] for r in raw})
        if days and days[0] <= target <= days[-1] and target in days:
            payload = path.read_bytes()
            return days, dict(sha256=hashlib.sha256(payload).hexdigest(), raw_json=payload.decode('utf-8'),
                              source='existing_sina_trade_calendar', reused=True)
    raise ValueError('existing_verified_calendar_does_not_cover_target')


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', required=True)
    parser.add_argument('--data', default='data')
    parser.add_argument('--lifecycle-data', default='lifecycle-data')
    parser.add_argument('--output', default='analysis-data')
    parser.add_argument('--config', default='config/v2.json')
    parser.add_argument('--calendar')
    parser.add_argument('--history-cache', action='append', default=[])
    parser.add_argument('--price-cache', action='append', default=[])
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--replay')
    parser.add_argument('--allow-partial', action='store_true', help='CI执行通过不代表数据完整，summary仍标partial')
    args = parser.parse_args(argv)
    if args.replay:
        root = Path(args.replay)
        from .v2_validate import validate_run
        errors = validate_run(root)
        if errors:
            raise ValueError(';'.join(errors))
        result = compute(read(root / 'analysis_inputs.json'))
        if result != read(root / 'report.json'):
            raise ValueError('offline_v2_report_replay_mismatch')
        print('V2 offline replay passed')
        return 0
    target = datetime.strptime(args.date, '%Y-%m-%d').date().isoformat()
    now = datetime.now(TZ)
    if target > now.date().isoformat() or (target == now.date().isoformat() and now.hour < 15):
        raise ValueError('target_session_has_not_closed')
    config = read(args.config)
    full_calendar, calendar = calendar_input(args.data, target, args.calendar)
    end = full_calendar.index(target) + 1
    days = full_calendar[max(0, end - 40):end]
    if len(days) != 40:
        raise ValueError('fewer_than_40_confirmed_trading_sessions')
    baseline = full_calendar[end - 41] if end > 40 else None
    root = Path(args.output) / target / 'runs' / (now.strftime('%Y%m%dT%H%M%S') + '-' + uuid4().hex)
    root.mkdir(parents=True, exist_ok=False)
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as stream:
            stream.write(f'run_path={root.as_posix()}\n')
    collector = Collector(root)
    dump(root / 'sources.json', {})
    dump(root / 'calendar_input.json', calendar)
    previous_runs = sorted(Path(args.output).glob('*/runs/*'), reverse=True)
    history_caches = list(previous_runs) + [Path(p) for p in args.history_cache]
    observations, associations, reviews = get_reviews(days, root, config['aliases'], history_caches,
        budget=0 if args.offline else config['history_budget_seconds'],
        delay=config['history_request_delay'], timeout=config['history_timeout'], offline=args.offline)
    selected, market_coverage = selected_inputs(args.data, days)
    market_scan = light_market_scan(selected)
    # Original archives already own the large raw snapshots. Keep exact hashes,
    # a normalized light scan and only the replay dependencies, without duplicating
    # every raw and cleaned full-market table into each analysis input JSON.
    dump(root / 'upstream_refs.json', [dict(date=r['date'], run_id=r['run_id'],
        files={name: v['sha256'] for name, v in r['files'].items()}) for r in selected])
    selected = [dict(r, files={name: v for name, v in r['files'].items()
        if name in ('clean/limit_up.json', 'clean/broken.json')}) for r in selected]
    # Reuse original, date-bound first-seal and one-word verification where available.
    by_key = {(r['date'], r['code']): r for r in observations}
    for day_input in selected:
        for original in upstream_table(day_input, 'clean/limit_up.json'):
            row = by_key.get((day_input['date'], original['code']))
            if row:
                row['first_seal'] = original.get('first_seal') or row['first_seal']
                row['all_day_one_word'] = original.get('all_day_one_word')
                row['one_word_basis'] = original.get('price_source')
    prior_state, prior_cores = previous_input(args.output, target)
    daily, _, _, selection, _ = selection_trace(observations, days, reviews, selected, config, prior_state)
    eligible_codes = core_price_candidates(selection, observations, days, 100000)
    codes = eligible_codes[:config['max_core_price_requests']]
    # Also keep recently active established lifecycle candidates within selected themes.
    price_days = ([baseline] if baseline else []) + days
    prices, price_coverage = collect_core_prices(collector, codes, price_days,
        budget=0 if args.offline else config['price_budget_seconds'], caches=args.price_cache + [str(r) for r in previous_runs])
    lifecycle_prices = {}
    for row in prior_tables(args.lifecycle_data, target, 'leader_prices'):
        if row['code'] in codes and row['observation_date'] in price_days and row.get('price') and row['price'].get('adjustment') == 'none':
            key = row['code'], row['observation_date']
            lifecycle_prices[key] = dict(row['price'], code=row['code'],
                reused_from_lifecycle=True, volume_unit=row.get('volume_unit', 'provider_reported_unverified'))
    prices.extend(lifecycle_prices.values())
    inputs = dict(days=days, baseline_date=baseline, config=config, observations=observations,
        prices=prices, review_coverage=reviews, selected_inputs=selected,
        market_coverage=market_coverage, price_coverage=price_coverage,
        price_eligible_codes=eligible_codes,
        previous_state=prior_state, previous_cores=prior_cores,
        automation=dict(mode='isolated_analysis', daily_close_integration=False,
            github_run_id=os.environ.get('GITHUB_RUN_ID'), github_ref=os.environ.get('GITHUB_REF')))
    dump(root / 'analysis_inputs.json', inputs)
    table(root / 'clean' / 'historical_active_associations', associations)
    table(root / 'clean' / 'stock_observations', observations)
    table(root / 'clean' / 'theme_daily', daily)
    table(root / 'clean' / 'core_prices', prices)
    table(root / 'clean' / 'review_coverage', reviews)
    table(root / 'clean' / 'market_coverage', market_coverage)
    table(root / 'clean' / 'market_scan', market_scan)
    table(root / 'clean' / 'price_coverage', price_coverage)
    report = compute(inputs)
    dump(root / 'report.json', report)
    (root / 'report.md').write_text(render_report(report), encoding='utf-8')
    dump(root / 'summary.json', dict(trade_date=target, run_id=root.name, status=report['status'],
        coverage=report['coverage'], missing_data=report['missing_data']))
    dump(root / 'implementation.json', dict(python=sys.version,
        dependencies={name: version(name) for name in ('akshare', 'pandas', 'requests', 'beautifulsoup4', 'tzdata')},
        modules={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in Path(__file__).parent.glob('*.py')}, config_sha256=hashlib.sha256(Path(args.config).read_bytes()).hexdigest()))
    inventory(root, collector.calls)
    from .v2_validate import validate_run
    errors = validate_run(root)
    if errors:
        raise ValueError(';'.join(errors))
    print(root, flush=True)
    return 0 if args.allow_partial else 2


if __name__ == '__main__':
    raise SystemExit(main())
