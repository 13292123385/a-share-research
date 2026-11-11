"""Independent, append-only lifecycle observations; never changes close snapshots."""
import argparse
import hashlib
import json
import os
import time
import sys
from importlib.metadata import version
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from .run import Collector, dump, table, TZ
from .quality import daily_price
from .model import ordinary, number
from .inventory import inventory
from .themes import collect_themes


def prior_tables(output, target, filename):
    """Only consume byte-verified, completed attempts no later than the target."""
    result = []
    for manifest in sorted(Path(output).glob('*/runs/*/files.json')):
        if manifest.parents[2].name > target:
            continue
        entries = json.loads(manifest.read_text(encoding='utf-8'))
        rel = 'clean/' + filename + '.json'
        entry = next((r for r in entries if r['path'] == rel), None)
        path = manifest.parent / rel
        if entry and path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256']:
            result.extend(dict(r, origin_run=manifest.parent.name) for r in json.loads(path.read_text(encoding='utf-8')))
    return result


def manual_watch(rows, days, target):
    result = []
    if len({r.get('code') for r in rows}) != len(rows):
        raise ValueError('duplicate manual watch code')
    for r in rows:
        if not ordinary(r.get('code'), r.get('name')) or not r.get('evidence_url', '').startswith('https://') or not r.get('reviewer'):
            raise ValueError('manual watch requires ordinary code, name, reviewer and https evidence')
        observed = datetime.fromisoformat(r['observed_at'])
        if observed.tzinfo is None:
            raise ValueError('manual evidence timestamp must include timezone')
        day = observed.astimezone(TZ).date().isoformat()
        first = next((d for d in sorted(days) if d >= day), None)
        if first and first <= target:
            result.append(dict(code=r['code'], name=r['name'], first_observed=first,
                observation_date=target, candidate_basis='manual_evidence', leader_confirmed=None,
                evidence_url=r['evidence_url'], reviewer=r['reviewer'], observed_at=r['observed_at'],
                theme_ids=[], theme_status='missing_evidence', last_confirmed_break_date=None,
                sessions_after_break=None, current_pool_status='not_inferred', execution_verified=False, entry_price=None))
    return result


def selected_pools(data, days, target):
    pools, refs = {}, []
    for day in sorted(set(d for d in days if d <= target)):
        pointer = Path(data) / day / 'latest.json'
        if not pointer.exists():
            pools[day] = None
            continue
        ptr = json.loads(pointer.read_text(encoding='utf-8'))
        run_id = ptr['run_id']
        if Path(run_id).name != run_id or '/' in run_id or '\\' in run_id or run_id in ('.', '..'):
            raise ValueError('unsafe run id')
        root = pointer.parent / 'runs' / run_id
        summary = json.loads((root / 'summary.json').read_text(encoding='utf-8'))
        pool = root / 'clean' / 'limit_up.json'
        if summary.get('trading_day') is not True or summary.get('trade_date') != day or not pool.exists():
            pools[day] = None
            continue
        payload = pool.read_bytes()
        rows = json.loads(payload)
        codes = [r['code'] for r in rows]
        if not rows or len(codes) != len(set(codes)):
            pools[day] = None
            continue
        pools[day] = rows
        refs.append(dict(date=day, run_id=run_id, sha256=hashlib.sha256(payload).hexdigest(), rows=rows,
                         raw_json=payload.decode('utf-8')))
    return pools, refs


def observations(pools, days, target):
    """Keep candidates indefinitely: incomplete archives cannot prematurely retire them."""
    days = sorted(set(d for d in days if d <= target))
    candidates = {}
    for day in days:
        for row in pools.get(day) or []:
            if ordinary(row.get('code'), row.get('name')) and (row.get('height') or 0) >= 4:
                candidates.setdefault(row['code'], dict(code=row['code'], name=row['name'], first_observed=day))
    result = []
    for code, candidate in sorted(candidates.items()):
        # Recover the earlier part of the observed run only across adjacent known sessions.
        index = days.index(candidate['first_observed'])
        while index > 0 and any(r['code'] == code for r in pools.get(days[index - 1]) or []):
            index -= 1
        candidate['first_observed'] = days[index]
        last_up, breaks = None, []
        for day in days:
            if day < candidate['first_observed']:
                continue
            pool = pools.get(day)
            if pool is None:
                last_up = None  # missing is not evidence of a broken streak
                continue
            up = next((r for r in pool if r['code'] == code), None)
            if up is None and last_up is True:
                breaks.append(day)
            last_up = up is not None
        broken = breaks[-1] if breaks else None
        age = len([d for d in days if broken and broken < d <= target]) if broken else None
        result.append(dict(candidate, observation_date=target, candidate_basis='archived_height_ge_4',
            leader_confirmed=None, theme_ids=[], theme_status='missing_evidence',
            last_confirmed_break_date=broken, sessions_after_break=age,
            current_pool_status='missing_archive' if pools.get(target) is None else
                'limit_up' if any(r['code'] == code for r in pools[target]) else 'not_in_limit_up_pool',
            execution_verified=False, entry_price=None))
    return result


def collect_prices(c, watch, days, target, budget, cached=()):
    deadline = time.monotonic() + max(0, budget)
    result = []
    cache = {}
    last_attempt = {}
    for row in cached:
        if row.get('attempted_at'):
            last_attempt[row['code']] = max(last_attempt.get(row['code'], ''), row['attempted_at'])
        price = row.get('price')
        if price and price.get('adjustment') == 'none' and daily_price([price], row['observation_date']):
            cache[(row['code'], row['observation_date'])] = row
    # Missing coverage first. Cached prices are never changed in place.
    for candidate in sorted(watch, key=lambda r: (last_attempt.get(r['code'], ''), r['code'])):
        code = candidate['code']
        dates = sorted(set(d for d in days if candidate['first_observed'] <= d <= target))
        prices = None
        remaining = deadline - time.monotonic() - c.delay
        needed = [d for d in dates if (code, d) not in cache or cache[(code, d)].get('status') != 'available']
        if remaining > 1 and needed:
            c.timeout = min(15, remaining)
            prices = c.call('lifecycle_price_' + code, 'stock_zh_a_hist_tx',
                symbol=('sh' if code.startswith('6') else 'sz') + code,
                start_date=needed[0].replace('-', ''), end_date=target.replace('-', ''),
                adjust='', timeout=min(10, c.timeout))
        for day in dates:
            old = cache.get((code, day))
            if old and old.get('status') == 'available':
                result.append(dict(old, reused_from_prior_run=True))
                continue
            price = daily_price(prices, day)
            if price and price['volume'] is not None and price['volume'] < 0:
                price = None
            if price is None and old:
                price = old['price']
            result.append(dict(code=code, observation_date=day, price=price,
                attempted_at=c.calls.get('lifecycle_price_' + code, {}).get('fetched_at') if isinstance(c.calls, dict) else None,
                volume_unit='provider_reported_unverified',
                status='available' if price and price['volume'] is not None else
                    'missing_volume' if price else 'missing_price',
                missing_reason=None if price and price['volume'] is not None else
                    ('budget_exhausted' if not needed or remaining <= 1 else 'provider_missing_or_invalid; suspension_not_inferred'),
                execution_verified=False, entry_price=None))
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--data', default='data')
    p.add_argument('--output', default='lifecycle-data')
    p.add_argument('--date', required=True)
    p.add_argument('--budget', type=float, default=300)
    p.add_argument('--theme-budget', type=float, default=300)
    p.add_argument('--watchlist', help='JSON evidence list; never published verbatim')
    p.add_argument('--replay', help='Offline rebuild of watch pool from saved inputs')
    a = p.parse_args()
    if a.replay:
        saved = Path(a.replay)
        inputs = json.loads((saved / 'archive_inputs.json').read_text(encoding='utf-8'))
        days = json.loads((saved / 'calendar_inputs.json').read_text(encoding='utf-8'))
        summary = json.loads((saved / 'summary.json').read_text(encoding='utf-8'))
        pools = {d: None for d in days}
        pools.update({r['date']: r['rows'] for r in inputs})
        automatic = observations(pools, days, summary['trade_date'])
        expected = json.loads((saved / 'clean' / 'leader_watch.json').read_text(encoding='utf-8'))
        actual = [r for r in expected if r['candidate_basis'] == 'archived_height_ge_4']
        keys = ('code', 'first_observed', 'last_confirmed_break_date', 'sessions_after_break', 'current_pool_status')
        if [{k: r[k] for k in keys} for r in automatic] != [{k: r[k] for k in keys} for r in actual]:
            raise ValueError('watch replay mismatch')
        print('Offline watch replay passed')
        return 0
    target = datetime.strptime(a.date, '%Y-%m-%d').date().isoformat()
    now = datetime.now(TZ)
    if target > now.date().isoformat() or (target == now.date().isoformat() and now.hour < 15):
        raise ValueError('target session has not closed')
    root = Path(a.output) / target / 'runs' / (datetime.now(TZ).strftime('%Y%m%dT%H%M%S') + '-' + uuid4().hex)
    root.mkdir(parents=True, exist_ok=False)
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as stream:
            stream.write(f'run_path={root.as_posix()}\n')
    c = Collector(root)
    dump(root / 'sources.json', {})
    dump(root / 'implementation.json', dict(python=sys.version, akshare=version('akshare'),
        modules={name: hashlib.sha256((Path(__file__).parent / (name + '.py')).read_bytes()).hexdigest()
                 for name in ('lifecycle', 'themes', 'quality', 'model', 'run', 'inventory')},
        price_budget=a.budget, theme_budget=a.theme_budget))
    calendar = c.call('calendar', 'tool_trade_date_hist_sina')
    days = sorted({str(r.get('trade_date', ''))[:10] for r in calendar or []})
    if not days or days[-1] < target or target not in days:
        dump(root / 'summary.json', dict(trade_date=target, status='calendar_unknown_or_non_session'))
        inventory(root, c.calls)
        return 2
    manual = json.loads(Path(a.watchlist).read_text(encoding='utf-8')) if a.watchlist else []
    archive_days = sorted(p.name for p in Path(a.data).glob('????-??-??') if p.is_dir() and p.name <= target)
    # Calendar before the first available archive is not a fabricated collection obligation.
    start = archive_days[0] if archive_days else target
    for r in manual:
        observed = datetime.fromisoformat(r['observed_at'])
        if observed.tzinfo is None:
            raise ValueError('manual evidence timestamp must include timezone')
        day = observed.astimezone(TZ).date().isoformat()
        if day <= target:
            start = min(start, day)
    days = [d for d in days if start <= d <= target]
    dump(root / 'calendar_inputs.json', days)
    pools, refs = selected_pools(a.data, days, target)
    watch = observations(pools, days, target)
    dump(root / 'manual_inputs.json', manual)
    seen = {r['code'] for r in watch}
    for r in manual_watch(manual, days, target):
        if r['code'] in seen:
            continue
        previous_up, breaks = None, []
        for day in days:
            if day < r['first_observed']:
                continue
            if pools.get(day) is None:
                previous_up = None
                continue
            up = any(x['code'] == r['code'] for x in pools[day])
            if previous_up is True and not up:
                breaks.append(day)
            previous_up = up
        if breaks:
            r['last_confirmed_break_date'] = breaks[-1]
            r['sessions_after_break'] = sum(breaks[-1] < d <= target for d in days)
        r['current_pool_status'] = 'missing_archive' if pools.get(target) is None else 'limit_up' if previous_up else 'not_in_limit_up_pool'
        watch.append(r)
        seen.add(r['code'])
    theme_started = time.monotonic()
    catalog, members, theme_coverage, theme_status = collect_themes(c, target,
        datetime.now(TZ).date().isoformat(), a.theme_budget,
        prior_tables(a.output, target, 'theme_coverage'))
    evidence = []
    evidence_remaining = a.theme_budget - (time.monotonic() - theme_started) - c.delay
    if not members and evidence_remaining > 1:
        c.timeout = min(c.timeout, evidence_remaining)
        evidence = c.call('dated_theme_evidence', 'dated_theme_evidence',
            trade_date=target, archive_path=str(root / 'raw' / 'dated_theme_evidence.html')) or []
        c.calls['dated_theme_evidence'].update(provider='打板客公开复盘',
            documentation='https://www.dabanke.com/index-'+target.replace('-','')+'.html',
            raw_format='日期核对后的网页解析表；HTML单独归档；第三方活跃股关联，非完整成分')
        dump(root / 'sources.json', c.calls)
    table(root / 'clean' / 'dated_theme_evidence', evidence)
    mapping = {}
    for member in members + evidence:
        mapping.setdefault(member['code'], []).append(member['theme_id'])
    for r in watch:
        r['theme_ids'] = sorted(mapping.get(r['code'], []))
        r['theme_status'] = ('observed_membership_only' if members else 'published_active_association_only') if r['theme_ids'] else 'missing_evidence'
    table(root / 'clean' / 'leader_watch', watch)
    prices = collect_prices(c, watch, days, target, a.budget, prior_tables(a.output, target, 'leader_prices'))
    table(root / 'clean' / 'leader_prices', prices)
    table(root / 'clean' / 'theme_catalog', catalog)
    table(root / 'clean' / 'theme_members', members)
    table(root / 'clean' / 'theme_coverage', theme_coverage)
    historical = prior_tables(a.output, target, 'theme_catalog') + catalog
    theme_events = {(r['theme_id'], r['observation_date']): r for r in historical}
    table(root / 'clean' / 'theme_history', [theme_events[k] for k in sorted(theme_events)])
    lifecycle = []
    for ident in sorted({r['theme_id'] for r in historical}):
        events = sorted((r for r in theme_events.values() if r['theme_id'] == ident), key=lambda r: r['observation_date'])
        codes = {r['code'] for r in members if r['theme_id'] == ident}
        coverage = next((r['status'] for r in theme_coverage if r['theme_id'] == ident), 'missing')
        ups = [r for r in pools.get(target) or [] if r['code'] in codes]
        lifecycle.append(dict(theme_id=ident, first_observed=events[0]['observation_date'],
            last_observed=events[-1]['observation_date'], observed_sessions=len(events),
            observation_date=target, membership_status=coverage,
            mainboard_limit_up_count=len(ups) if coverage == 'available' and pools.get(target) is not None else None,
            max_height=max((r.get('height') or 0 for r in ups), default=0) if coverage == 'available' and pools.get(target) is not None else None,
            lifecycle_stage=None, stage_status='not_inferred'))
    table(root / 'clean' / 'theme_lifecycle', lifecycle)
    dump(root / 'archive_inputs.json', refs)
    missing = sum(r['status'] != 'available' for r in prices)
    status = 'complete' if watch and not missing and theme_status == 'available' and pools.get(target) is not None else 'partial'
    dump(root / 'summary.json', dict(schema_version=1, trade_date=target, status=status,
        fetched_at=datetime.now(TZ).isoformat(), run_id=root.name, min_post_break_sessions=20,
        price_rows=len(prices), missing_price_rows=missing,
        price_budget=a.budget, theme_budget=a.theme_budget,
        missing_archive_dates=[d for d in days if pools.get(d) is None],
        watch_count=len(watch), theme_status=theme_status,
        dated_evidence_rows=len(evidence), evidence_scope='partial_selected_active_stocks' if evidence else 'missing',
        note='候选不是已确认龙头；逐日不复权OHLCV，缺失不推断停牌；持续保留候选，覆盖断板后至少20交易日；无成交或收益推断'))
    inventory(root, c.calls)
    print(root)
    return 0 if status == 'complete' else 2


if __name__ == '__main__':
    raise SystemExit(main())
