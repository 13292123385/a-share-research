"""Capture timestamped, roster-checked midday and closing A-share snapshots.

This is independent of the closing research collector: intraday observations must
never be labelled as daily closing prices. All times use Asia/Shanghai.
"""
import argparse
from collections import Counter
from datetime import datetime, time
import hashlib
import json
import os
from pathlib import Path
import re
import time as clock
from zoneinfo import ZoneInfo

import requests

from .model import number
from .reconcile import ROSTERS, roster_codes
from .run import Collector

TZ = ZoneInfo('Asia/Shanghai')
NUMERIC_FIELDS = {
    '最新价': (3, 1), '昨收': (4, 1), '今开': (5, 1),
    '成交量': (6, 100), '涨跌额': (31, 1), '涨跌幅': (32, 1),
    '最高': (33, 1), '最低': (34, 1), '成交额': (37, 10000),
    '换手率': (38, 1), '市盈率': (39, 1),
    '流通市值': (44, 100000000), '总市值': (45, 100000000),
    '市净率': (46, 1),
}
# Valuation can be undefined (for example newly listed or loss-making shares).
# Such gaps are published explicitly and are never replaced by zero.
REQUIRED_FIELDS = ('最新价', '昨收', '今开', '最高', '最低', '涨跌额',
                   '涨跌幅', '成交量', '成交额')
UNITS = {'成交量': '股', '成交额': '元', '总市值': '元', '流通市值': '元',
         '换手率': '%', '涨跌幅': '%', '最新价': '元/股'}


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    temp.replace(path)


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def session_for(now, requested='auto'):
    """Return a valid session or None; an afternoon quote cannot fill midday."""
    now = now.astimezone(TZ)
    t = now.time().replace(tzinfo=None)
    if requested not in ('auto', 'midday', 'close'):
        raise ValueError('invalid_session')
    if requested in ('auto', 'midday') and time(11, 30) <= t < time(13):
        return 'midday'
    if requested in ('auto', 'close') and time(15) <= t:
        return 'close'
    return None


def symbol_for(code, exchange):
    if exchange in ('sh_main', 'sh_star'):
        return 'sh' + code
    if exchange == 'sz':
        return 'sz' + code
    if exchange == 'bj':
        return 'bj' + code
    raise ValueError('unknown_exchange')


def parse_quote(symbol, fields, trade_date, session, fetched_at=None):
    if not re.fullmatch(r'(?:sh|sz|bj)\d{6}', symbol):
        raise ValueError('invalid_symbol')
    if len(fields) < 47 or fields[2] != symbol[2:] or not fields[1].strip():
        raise ValueError('quote_identity_or_schema')
    row = {'代码': fields[2], '名称': fields[1], 'symbol': symbol,
           'source': 'Tencent qt.gtimg.cn', 'quote_timestamp': None}
    for name, (index, multiplier) in NUMERIC_FIELDS.items():
        value = number(fields[index])
        row[name] = value * multiplier if value is not None else None
    missing = [name for name in NUMERIC_FIELDS if row[name] is None]
    invalid = []
    stamp = None
    try:
        stamp = datetime.strptime(fields[30], '%Y%m%d%H%M%S').replace(tzinfo=TZ)
        row['quote_timestamp'] = stamp.isoformat()
    except (ValueError, TypeError):
        invalid.append('quote_timestamp')
    in_session = bool(stamp and stamp.date().isoformat() == trade_date and
                      (time(11, 29) <= stamp.time().replace(tzinfo=None) < time(13)
                       if session == 'midday' else
                       stamp.time().replace(tzinfo=None) >= time(14, 59)))
    if stamp and fetched_at and stamp > fetched_at.astimezone(TZ):
        invalid.append('quote_timestamp_in_future')
    if not in_session:
        invalid.append('quote_date_or_session')
    if any(row[name] is None for name in REQUIRED_FIELDS):
        invalid.append('required_fields_missing')
    if any(row[name] is not None and row[name] < 0 for name in
           ('今开', '最高', '最低', '成交量', '成交额', '换手率', '总市值', '流通市值')):
        invalid.append('negative_nonnegative_field')
    if any(row[name] is not None and row[name] <= 0 for name in ('最新价', '昨收')):
        invalid.append('nonpositive_price')
    no_trade = (row['成交量'] == 0 and row['成交额'] == 0 and
                row['今开'] == row['最高'] == row['最低'] == 0)
    prices = [row[name] for name in ('今开', '最高', '最低', '最新价')]
    if all(v is not None for v in prices) and not no_trade:
        opening, high, low, latest = prices
        if not 0 < low <= min(opening, latest) <= max(opening, latest) <= high:
            invalid.append('ohlc_order')
    row['quote_status'] = ('stale' if not in_session else 'invalid' if invalid else
                           'suspended_or_no_trade' if no_trade else 'fresh')
    row['suspension_verified'] = False
    row['missing_fields'] = missing
    row['validation_errors'] = invalid
    return row


def parse_batch(text, symbols, trade_date, session, fetched_at=None):
    """Parse all responses, retaining duplicates so coverage validation can fail."""
    requested = set(symbols)
    rows, errors = [], {}
    for match in re.finditer(r'v_((?:sh|sz|bj)\d{6})="([^"\r\n]*)";', text):
        symbol = match[1]
        if symbol not in requested:
            errors[symbol] = 'unexpected_symbol'
            continue
        try:
            rows.append(parse_quote(symbol, match[2].split('~'), trade_date, session, fetched_at))
        except ValueError as exc:
            errors[symbol] = str(exc)
    received = {row['symbol'] for row in rows}
    for symbol in requested - received:
        errors.setdefault(symbol, 'missing_quote')
    return rows, errors


def validate_snapshot(rows, expected_codes, unavailable_rosters=()):
    codes = [row['代码'] for row in rows]
    counts = Counter(codes)
    expected = set(expected_codes)
    observed = set(codes)
    duplicate = sorted(code for code, count in counts.items() if count > 1)
    invalid = sorted({row['代码'] for row in rows if row.get('validation_errors')})
    stale = sorted({row['代码'] for row in rows if row.get('quote_status') == 'stale'})
    coverage = dict(status='matched' if expected and observed == expected and not duplicate and
                    not unavailable_rosters else 'incomplete', expected_count=len(expected) if not
                    unavailable_rosters else None, observed_count=len(observed),
                    missing_codes=sorted(expected - observed), unexpected_codes=sorted(observed - expected),
                    duplicate_codes=duplicate, unavailable_rosters=list(unavailable_rosters))
    quality = dict(invalid_codes=invalid, stale_codes=stale,
                   suspended_codes=sorted({row['代码'] for row in rows
                       if row.get('quote_status') == 'suspended_or_no_trade'}),
                   missing_fields={row['代码']: row['missing_fields'] for row in rows if row.get('missing_fields')},
                   required_fields=list(REQUIRED_FIELDS),
                   nullable_fields=sorted(set(NUMERIC_FIELDS) - set(REQUIRED_FIELDS)),
                   issues=['估值等非必需字段缺失保留null；完整表示名单和必需行情字段通过本次校验，不代表独立审计。'])
    return ('complete' if coverage['status'] == 'matched' and not invalid else 'partial'), coverage, quality


def load_rosters(collector, output, trade_date):
    cache = Path(output) / trade_date / 'rosters.json'
    try:
        cached = read_json(cache) if cache.exists() else {}
        if not isinstance(cached, dict):
            cached = {}
    except (OSError, ValueError):
        # An interrupted or invalid cache is not a valid exchange roster.
        cached = {}
    rosters, unavailable = {}, []
    for name, function, kwargs, code_key, date_key in ROSTERS:
        rows = cached.get(name)
        if roster_codes(rows, code_key, date_key, trade_date) is None:
            for attempt in range(3):
                rows = collector.call(f'snapshot_roster_{name}_{attempt}', function, **kwargs)
                if roster_codes(rows, code_key, date_key, trade_date) is not None:
                    break
        if roster_codes(rows, code_key, date_key, trade_date) is None:
            unavailable.append(name)
        else:
            rosters[name] = rows
    if rosters:
        write_json(cache, rosters)
    symbols = []
    for name, _, _, code_key, date_key in ROSTERS:
        codes = roster_codes(rosters.get(name), code_key, date_key, trade_date)
        symbols.extend(symbol_for(code, name) for code in sorted(codes or []))
    return symbols, unavailable


def collect_quotes(symbols, trade_date, session, request_session=None, now_fn=None):
    requester = request_session or requests.Session()
    now_fn = now_fn or (lambda: datetime.now(TZ))
    rows, errors = [], {}
    for start in range(0, len(symbols), 80):
        batch = symbols[start:start + 80]
        best = []
        batch_errors = {}
        for attempt in range(3):
            if session_for(now_fn(), session) != session:
                errors['session_window'] = 'capture_window_ended'
                break
            try:
                response = requester.get('https://qt.gtimg.cn/q=' + ','.join(batch), timeout=(8, 20))
                response.raise_for_status()
                # The upstream Content-Type specifies GBK; do not trust chardet.
                text = response.content.decode('gb18030')
                parsed, batch_errors = parse_batch(text, batch, trade_date, session, now_fn())
                if len(parsed) > len(best) or (len(parsed) == len(best) and
                    sum(not r['validation_errors'] for r in parsed) >=
                    sum(not r['validation_errors'] for r in best)):
                    best = parsed
                if len(parsed) == len(batch) and not batch_errors and not any(r['validation_errors'] for r in parsed):
                    break
            except (requests.RequestException, UnicodeError, ValueError) as exc:
                batch_errors = {'batch_' + str(start // 80): type(exc).__name__}
            if attempt < 2:
                clock.sleep(1 + attempt)
        rows.extend(best)
        errors.update(batch_errors)
        print(f'snapshot batch {start // 80 + 1}: rows={len(best)}/{len(batch)}', flush=True)
    return rows, errors


def archive_snapshot(output, snapshot):
    daily = Path(output) / snapshot['trade_date'] / snapshot['session']
    root = daily / 'runs' / snapshot['run_id']
    write_json(root / 'snapshot.json', snapshot)
    manifest = {key: value for key, value in snapshot.items() if key != 'rows'}
    manifest['snapshot_sha256'] = hashlib.sha256((root / 'snapshot.json').read_bytes()).hexdigest()
    manifest['snapshot_file'] = 'snapshot.json'
    write_json(root / 'manifest.json', manifest)
    pointer = daily / 'latest.json'
    old = read_json(pointer) if pointer.exists() else None
    # An invalid new attempt must not hide a complete snapshot of this session.
    promote = snapshot['status'] in ('complete', 'partial') and (not old or
              old.get('status') != 'complete' or snapshot['status'] == 'complete')
    if promote:
        write_json(pointer, dict(manifest, run_path=str(root.as_posix())))
    write_json(daily / 'last_attempt.json', dict(manifest, run_path=str(root.as_posix())))
    return root, promote


def capture(output='snapshot-data', session='auto', now=None, collector_factory=Collector,
            request_session=None, now_fn=None):
    now = (now or datetime.now(TZ)).astimezone(TZ)
    selected = session_for(now, session)
    if selected is None:
        print('Snapshot skipped: outside the requested session capture window.', flush=True)
        return None
    trade_date = now.date().isoformat()
    selected_pointer = Path(output) / trade_date / selected / 'latest.json'
    if selected_pointer.exists():
        previous = read_json(selected_pointer)
        existing = selected_pointer.parent / 'runs' / previous['run_id']
        if previous.get('status') == 'complete' and (existing / 'snapshot.json').exists():
            content = (existing / 'snapshot.json').read_bytes()
            if hashlib.sha256(content).hexdigest() == previous.get('snapshot_sha256'):
                print('Reusing verified complete snapshot:', trade_date, selected, flush=True)
                if os.environ.get('GITHUB_OUTPUT'):
                    with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as stream:
                        stream.write(f'run_path={existing.as_posix()}\nstatus=complete\nsession={selected}\n')
                return json.loads(content)
    run_id = now.strftime('%Y%m%dT%H%M%S%f%z')
    root = Path(output) / trade_date / selected / 'runs' / run_id
    collector = collector_factory(root, timeout=20, delay=.2)
    calendar = collector.call('snapshot_calendar', 'tool_trade_date_hist_sina')
    try:
        days = sorted({str(row['trade_date'])[:10] for row in calendar or []})
        for day in days:
            datetime.strptime(day, '%Y-%m-%d')
    except (KeyError, ValueError, TypeError):
        days = []
    covered = bool(days and days[0] <= trade_date <= days[-1])
    status = 'calendar_unknown' if not covered else 'skipped' if trade_date not in days else None
    snapshot = dict(schema_version=1, trade_date=trade_date, session=selected,
                    run_id=run_id, fetched_at=now.isoformat(), status=status,
                    units=UNITS, source='Tencent qt.gtimg.cn; official SSE/SZSE/BSE rosters', rows=[])
    if status is None:
        symbols, unavailable = load_rosters(collector, output, trade_date)
        rows, errors = collect_quotes(symbols, trade_date, selected, request_session, now_fn)
        status, coverage, quality = validate_snapshot(rows, [s[2:] for s in symbols], unavailable)
        snapshot.update(status=status, rows=sorted(rows, key=lambda row: row['代码']),
                        coverage=coverage, quality=quality, request_errors=errors,
                        records=len(rows), expected_count=coverage['expected_count'])
    else:
        snapshot.update(records=0, expected_count=None, coverage=None, quality=None,
                        reason='trade_calendar_unavailable' if status == 'calendar_unknown' else 'non_trading_day')
    snapshot['finished_at'] = (now_fn() if now_fn else datetime.now(TZ)).isoformat()
    root, promoted = archive_snapshot(output, snapshot)
    print(f'Snapshot {trade_date} {selected}: {snapshot["status"]} '
          f'{snapshot["records"]}/{snapshot["expected_count"]}; promoted={promoted}', flush=True)
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as stream:
            stream.write(f'run_path={root.as_posix()}\nstatus={snapshot["status"]}\nsession={selected}\n')
    return snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session', choices=('auto', 'midday', 'close'), default='auto')
    parser.add_argument('--output', default='snapshot-data')
    args = parser.parse_args()
    snapshot = capture(args.output, args.session)
    raise SystemExit(0 if snapshot is None or snapshot['status'] in ('complete', 'skipped') else 2)


if __name__ == '__main__':
    main()
