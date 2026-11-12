"""V2 adapters reuse dated observations; never manufacture historical membership."""
import hashlib
import json
import re
import time
from datetime import date, datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup

from .model import ordinary, number
from .quality import daily_price
from .run import dump, TZ
from .theme_evidence import parse_evidence


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def canonical_tags(raw, aliases):
    """Explicit label grouping, retaining unmatched topics instead of a five-theme shortlist."""
    result = set()
    for token in re.split(r'[+＋、]', raw):
        token = token.strip()
        if not token:
            continue
        matches = [name for name, words in aliases.items()
                   if any(w.casefold() in token.casefold() for w in words)]
        result.update(matches or [token])
    return sorted(result)


def parse_review(html, target, fetched_at, source_url, aliases):
    # Reuse yesterday's identity/date checks for the selected active associations.
    evidence = parse_evidence(html, target, fetched_at, source_url)
    soup = BeautifulSoup(html, 'html.parser')
    observations, seen = [], set()
    for tier in soup.select('.ladder-view-tier'):
        title = tier.select_one('h3')
        label = title.get_text(strip=True) if title else ''
        pair = re.search(r'(\d+)进(\d+)', label)
        height = int(pair[2]) if pair else 1 if label == '首板' else None
        if height is None:
            continue
        for stock in tier.select('.stock-line[data-symbol]'):
            symbol = stock['data-symbol']
            match = re.fullmatch(r'(\d{6})\.(SH|SZ|BJ)', symbol)
            link = stock.select_one('.stock-name .stock-detail-link')
            if not match or link is None:
                raise ValueError('ladder_identity_missing')
            code, name = match[1], link.get_text(strip=True)
            if ('gupiao-' + code + '.html') not in link.get('href', '') or \
                    parse_qs(urlparse(link['href']).query).get('review_date') != [target]:
                raise ValueError('ladder_stock_date_or_identity_mismatch')
            if code in seen:
                raise ValueError('duplicate_ladder_stock')
            seen.add(code)
            if not ordinary(code, name):
                continue
            reason = stock.select_one('.ladder-stock-reason summary')
            reason = reason.get('title', '') if reason else ''
            stamp = re.search(r'\d{4}-\d{2}-\d{2}', reason)
            reason_date = stamp[0] if stamp else None
            # Future/current replacement labels never backfill older observations.
            valid = reason_date is not None and reason_date <= target
            raw = re.split(r'\s*[｜|]\s*资料日期|资料日期', reason)[0].strip(' ｜|·')
            tags = canonical_tags(raw, aliases) if valid else []
            classes = stock.get('class', [])
            closed = 'status-success' in classes
            performance = stock.select_one('.ladder-performance')
            performance = performance.get('title', '') if performance else ''
            seal = re.search(r'首封\s*(\d{2}:\d{2}:\d{2})', performance)
            observations.append(dict(date=target, code=code, name=name,
                theme_ids=tags, closed_limit_up=closed, height=height if closed else None,
                broken_at_close='status-opened' in classes,
                first_seal=seal[1] if seal else None,
                all_day_one_word=None,  # website text is not an OHLC/queue verification
                published_one_word_label='一字板' in performance,
                raw_reason=raw, reason_asof=reason_date,
                theme_association_evidence=[dict(theme_id=t, date=target, basis='dated_reason', reason_asof=reason_date)
                                            for t in tags],
                mapping_confidence='dated_published_reason_business_unverified' if valid else 'unknown',
                source_url=source_url, fetched_at=fetched_at,
                source_sha256=digest(html.encode('utf-8')), historical_point_in_time_verified=False,
                business_verified=False, execution_verified=False))
    if not observations:
        raise ValueError('empty_ladder_observations')
    # Today's review-table aliases supplement only today's stock labels. No forward fill.
    by_code = {r['code']: r for r in observations}
    for row in evidence:
        if row['code'] in by_code:
            target_row = by_code[row['code']]
            tags = canonical_tags(row['theme_name'], aliases)
            target_row['theme_ids'] = sorted(set(target_row['theme_ids']) | set(tags))
            target_row['theme_association_evidence'].extend(dict(theme_id=t, date=target,
                basis='dated_active_association_table', source_sha256=row['source_sha256']) for t in tags)
            if target_row['mapping_confidence'] == 'unknown':
                target_row['mapping_confidence'] = 'dated_active_association_business_unverified'
    return observations, evidence


def get_reviews(days, run, aliases, caches=(), budget=480, delay=1.5, timeout=18, offline=False):
    """Save exact input bytes per run; cache content is immutable and hash checked."""
    run = Path(run)
    deadline = time.monotonic() + max(0, budget)
    observations, evidence, coverage = [], [], []
    for day in days:
        url = 'https://www.dabanke.com/index-' + day.replace('-', '') + '.html'
        now = datetime.now(TZ).isoformat()
        meta = dict(date=day, source_url=url, status='missing', fetched_at=None,
                    snapshot_saved_at=now, historical_point_in_time_verified=False)
        html = None
        for cache in caches:
            candidates = [Path(cache) / (day + '.html'), Path(cache) / 'raw' / (day + '.html')]
            for candidate in candidates:
                if not candidate.exists():
                    continue
                payload = candidate.read_bytes()
                source_meta = candidate.with_suffix('.meta.json')
                old = json.loads(source_meta.read_text(encoding='utf-8')) if source_meta.exists() else {}
                if old.get('sha256') and old['sha256'] != digest(payload):
                    raise ValueError('cached_review_checksum_mismatch')
                html = payload.decode('utf-8')
                meta.update(fetched_at=old.get('fetched_at'), reused=True,
                            original_fetched_at_unknown=old.get('fetched_at') is None)
                break
            if html is not None:
                break
        remaining = deadline - time.monotonic()
        if html is None and not offline and remaining > delay + 1:
            try:
                time.sleep(delay)
                response = requests.get(url, timeout=min(timeout, remaining - delay))
                response.raise_for_status()
                response.encoding = 'utf-8'
                html = response.text
                meta.update(fetched_at=now, reused=False)
            except requests.RequestException as exc:
                meta['error'] = type(exc).__name__
        if html is not None:
            try:
                rows, mapped = parse_review(html, day, meta['fetched_at'], url, aliases)
                path = run / 'raw' / (day + '.html')
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(html, encoding='utf-8', newline='')
                meta.update(status='available', sha256=digest(path.read_bytes()),
                    rows=len(rows), mapping_scope='partial_active_associations')
                dump(path.with_suffix('.meta.json'), meta)
                observations.extend(rows)
                evidence.extend(mapped)
            except ValueError as exc:
                meta.update(status='invalid', error=str(exc))
        else:
            meta['error'] = meta.get('error', 'offline_cache_miss' if offline else 'budget_exhausted')
        coverage.append(meta)
        print('v2_review', day, meta['status'], flush=True)
    return observations, evidence, coverage


def selected_inputs(data, days):
    """Snapshot selected upstream files and their bytes, not the mutable latest pointer alone."""
    inputs, coverage = [], []
    for day in days:
        daily = Path(data) / day
        pointer = daily / 'latest.json'
        info = dict(date=day, status='missing', market_quote_rows=0, mainboard_quote_rows=0)
        if pointer.is_file():
            run_id = json.loads(pointer.read_text(encoding='utf-8'))['run_id']
            if Path(run_id).name != run_id or '/' in run_id or '\\' in run_id:
                raise ValueError('unsafe_selected_run')
            root = daily / 'runs' / run_id
            summary = json.loads((root / 'summary.json').read_text(encoding='utf-8'))
            if summary.get('trading_day') is True and summary.get('trade_date') == day:
                saved = dict(date=day, run_id=run_id, files={})
                manifest_path = root / 'files.json'
                manifest = {r['path']: r for r in json.loads(manifest_path.read_text(encoding='utf-8'))} if manifest_path.exists() else {}
                for filename in ('summary.json', 'clean/limit_up.json', 'clean/broken.json',
                                 'clean/market_quotes.json', 'raw/spot.json', 'raw/spot_fallback.json'):
                    path = root / filename
                    if path.is_file():
                        payload = path.read_bytes()
                        if filename not in manifest or manifest[filename]['sha256'] != digest(payload):
                            raise ValueError('selected_input_manifest_missing_or_mismatch:' + day + ':' + filename)
                        saved['files'][filename] = dict(sha256=digest(payload), raw_json=payload.decode('utf-8'))
                inputs.append(saved)
                quotes = upstream_table(saved, 'clean/market_quotes.json')
                info.update(status='available', market_quote_rows=len(quotes),
                    mainboard_quote_rows=sum(ordinary(str(r.get('代码', '')).zfill(6), r.get('名称')) for r in quotes),
                    market_code_coverage=summary.get('market_reconciliation', {}).get('status'),
                    all_market_verified=summary.get('market_reconciliation', {}).get('all_market_verified', False))
        coverage.append(info)
    return inputs, coverage


def upstream_table(saved, key):
    item = saved.get('files', {}).get(key)
    if not item:
        return []
    if digest(item['raw_json'].encode('utf-8')) != item['sha256']:
        raise ValueError('upstream_input_checksum_mismatch')
    return json.loads(item['raw_json'])


def light_market_scan(selected):
    result = []
    for saved in selected:
        seen = set()
        for row in upstream_table(saved, 'clean/market_quotes.json'):
            code, name = str(row.get('代码', '')).zfill(6), row.get('名称')
            if not ordinary(code, name):
                continue
            if code in seen:
                raise ValueError('duplicate_archived_market_quote')
            seen.add(code)
            result.append(dict(date=saved['date'], code=code, name=name,
                open=number(row.get('今开')), high=number(row.get('最高')),
                low=number(row.get('最低')), close=number(row.get('最新价')),
                volume=number(row.get('成交量')), amount=number(row.get('成交额')),
                pct_change=number(row.get('涨跌幅')), turnover_rate=number(row.get('换手率')),
                turnover_unit='percent' if number(row.get('换手率')) is not None else None,
                volume_unit='provider_reported_unverified', amount_unit='yuan_adapter_reported',
                date_basis='existing_calendar_verified_close_collection',
                quote_timestamp=row.get('时间戳'), all_fields_independently_verified=False,
                source_run_id=saved['run_id'], adjustment='none'))
    return result


def build_daily(observations, days, review_coverage, selected):
    if any(r['date'] > days[-1] for r in observations):
        raise ValueError('future_stock_observation')
    # Single-stock company-specific reasons are retained in raw observations but
    # cannot constitute a resonating sector. Scan them every run for promotion.
    codes = {}
    for row in observations:
        for theme in row['theme_ids']:
            codes.setdefault(theme, set()).add(row['code'])
    themes = sorted(t for t, members in codes.items() if len(members) >= 3)
    available = {r['date'] for r in review_coverage if r['status'] == 'available'}
    originals = {r['date']: r for r in selected}
    by_day = {d: [r for r in observations if r['date'] == d] for d in days}
    result, crosschecks = [], []
    for day in days:
        rows = by_day[day]
        observed = {r['code'] for r in rows if r['closed_limit_up']}
        original = upstream_table(originals.get(day, {}), 'clean/limit_up.json')
        if original:
            codes = {r['code'] for r in original}
            crosschecks.append(dict(date=day, original_count=len(codes), review_count=len(observed),
                matched=codes == observed, missing_in_review=sorted(codes - observed),
                extra_in_review=sorted(observed - codes)))
        for theme in themes:
            members = [r for r in rows if theme in r['theme_ids']]
            ups = [r for r in members if r['closed_limit_up']]
            valid = day in available
            result.append(dict(date=day, theme_id=theme, theme_name=theme,
                observed_limit_up_count=len(ups) if valid else None,
                market_limit_up_count=len(original) if original else len(observed) if valid else None,
                max_height=max((r['height'] or 0 for r in ups), default=0) if valid else None,
                active_signal=bool(ups) if valid else None,
                mapping_scope='partial_active_associations',
                relative_return_pct=None, advancing_ratio=None, turnover_share=None,
                observed_broken_count=sum(r['broken_at_close'] for r in members) if valid else None,
                broken_count=None,  # partial reasons cannot establish exhaustive theme failures
                catalyst_verified=False, catalyst_evidence=[],
                observation_scope='mainboard_published_limit_up_reasons',
                count_kind='observed_lower_bound_not_full_constituents'))
    return result, crosschecks


def normalize_prices(code, rows, adjustment):
    if adjustment not in ('qfq', 'none'):
        raise ValueError('unsupported_price_adjustment')
    dates = [str(r.get('date', ''))[:10] for r in rows]
    if len(dates) != len(set(dates)):
        raise ValueError('duplicate_price_dates')
    result = []
    for row in rows:
        day = str(row.get('date', ''))[:10]
        try:
            if date.fromisoformat(day).isoformat() != day:
                continue
        except (ValueError, TypeError):
            continue
        clean = daily_price([row], day)
        if clean is None:
            continue
        if any(number(row.get(k)) is not None and number(row[k]) < 0 for k in ('volume', 'amount', 'turnover')):
            continue
        # Preserve adjustment explicitly: daily_price is a validator, not an adjustment converter.
        clean.update(code=code, adjustment=adjustment,
            turnover_rate=number(row.get('turnover')), pct_change=number(row.get('pct_change')),
            amount_unit='yuan_adapter_reported', volume_unit='provider_reported_unverified',
            turnover_unit='fraction' if number(row.get('turnover')) is not None else None)
        result.append(clean)
    return result


def core_price_candidates(selection, observations, days, limit=60):
    seats = selection.get('seats', {})
    ids = {r['theme_id'] for r in seats.values() if r}
    current = [r for r in observations if r['date'] in days[-3:] and ids.intersection(r['theme_ids'])]
    candidates = {r['code'] for r in current}
    # Price requests follow strength evidence, never current price performance known only after fetching.
    counts = {c: sum(r['closed_limit_up'] for r in observations if r['code'] == c and r['date'] in days[-10:]) for c in candidates}
    heights = {c: max((r['height'] or 0 for r in current if r['code'] == c), default=0) for c in candidates}
    return sorted(candidates, key=lambda c: (-counts[c], -heights[c], c))[:limit]


def collect_core_prices(collector, codes, days, budget=420, caches=()):
    """One history call per priority stock; full-market daily snapshots remain upstream's job."""
    rows, coverage = [], []
    deadline = time.monotonic() + max(0, budget)
    for code in codes:
        raw = None
        reused = False
        for cache in caches:
            path = Path(cache) / ('qfq_' + code + '.json')
            if not path.is_file():
                path = Path(cache) / 'raw' / ('qfq_' + code + '.json')
            meta_path = path.parent.parent / 'sources.json'
            if path.is_file() and meta_path.is_file():
                meta = json.loads(meta_path.read_text(encoding='utf-8')).get('qfq_' + code, {})
                payload = path.read_bytes()
                # Original source must declare qfq; cannot infer adjustment from a filename alone.
                params = meta.get('parameters', {})
                symbol = ('sh' if code.startswith('6') else 'sz') + code
                if meta.get('function') == 'stock_zh_a_hist_tx' and params.get('symbol') == symbol and params.get('adjust') == 'qfq' and meta.get('sha256') == digest(payload):
                    candidate = json.loads(payload)
                    cached_days = {str(r.get('date', ''))[:10] for r in candidate}
                    if params.get('end_date') == days[-1].replace('-', '') and cached_days.intersection(days):
                        raw, reused = candidate, True
                        destination = collector.root / 'raw' / ('qfq_' + code + '.json')
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        destination.write_bytes(payload)
                        collector.calls['qfq_' + code] = dict(meta, reused_from_verified_cache=True)
                        dump(collector.root / 'sources.json', collector.calls)
                        break
        remaining = deadline - time.monotonic() - collector.delay
        missing_cached = raw is not None and not {str(r.get('date', ''))[:10] for r in raw} >= set(days)
        if (raw is None or missing_cached) and remaining > 1:
            old_timeout = collector.timeout
            collector.timeout = min(20, remaining)
            try:
                fetched = collector.call(('qfq_retry_' if raw is not None else 'qfq_') + code, 'stock_zh_a_hist_tx',
                    symbol=('sh' if code.startswith('6') else 'sz') + code,
                    start_date=days[0].replace('-', ''), end_date=days[-1].replace('-', ''),
                    adjust='qfq', timeout=min(10, collector.timeout))
                if fetched:
                    fetched_dates = {r['date'] for r in normalize_prices(code, fetched, 'qfq')}
                    cached_dates = {r['date'] for r in normalize_prices(code, raw or [], 'qfq')}
                    if fetched_dates >= cached_dates:
                        raw = fetched
            finally:
                collector.timeout = old_timeout
        clean = normalize_prices(code, raw or [], 'qfq')
        clean = [r for r in clean if r['date'] in days]
        rows.extend(clean)
        have = {r['date'] for r in clean}
        coverage.append(dict(code=code, requested_sessions=len(days), valid_sessions=len(have),
            missing_dates=sorted(set(days) - have), reused=reused,
            status='available' if have == set(days) else 'partial' if have else 'missing',
            amount_rows=sum(r['amount'] is not None for r in clean),
            turnover_rows=sum(r['turnover_rate'] is not None for r in clean)))
    return rows, coverage
