"""Track archived first-board cohorts by trading session, without assumed trades."""
import json
import re
from pathlib import Path
from .model import ordinary
from .quality import daily_price


def archived_cohorts(output, days, target):
    earlier = sorted({d for d in days if d < target}, reverse=True)[:2]
    cohorts, missing = [], []
    for age, day in enumerate(earlier, 1):
        daily = Path(output) / day
        pointer = daily / 'latest.json'
        if not pointer.exists():
            missing.append(day)
            continue
        run_id = json.loads(pointer.read_text(encoding='utf-8'))['run_id']
        pool = daily / 'runs' / run_id / 'clean' / 'limit_up.json'
        if not pool.exists():
            missing.append(day)
            continue
        for row in json.loads(pool.read_text(encoding='utf-8')):
            if row.get('height') == 1 and ordinary(row.get('code'), row.get('name')):
                cohorts.append(dict(row, first_board_date=day, sessions_since_first=age))
    return cohorts, missing


def followup_rows(cohorts, prices, target):
    rows = []
    for cohort in cohorts:
        code = cohort['code']
        price = daily_price([prices[code]], target) if code in prices else None
        rows.append(dict(code=code, name=cohort['name'], first_board_date=cohort['first_board_date'],
            sessions_since_first=cohort['sessions_since_first'], observation_date=target,
            original_eligible_observation=cohort.get('eligible_observation'),
            status='price_available' if price else 'missing_price', price=price,
            execution_verified=False, entry_price=None, third_day_return=None,
            max_adverse_excursion=None, note='不复权日线观察，非买入记录；未计算策略收益'))
    return rows


def normalize_sina_spot(rows, include_beijing=False):
    result = []
    for r in rows or []:
        code = str(r.get('代码', ''))
        if not re.fullmatch(r'(?:sh|sz|bj)?\d{6}', code):
            continue
        code = code.removeprefix('sh').removeprefix('sz').removeprefix('bj')
        prefixes = ('60', '68', '00', '30') + (('43', '83', '87', '88', '92') if include_beijing else ())
        if not code.startswith(prefixes):
            continue
        result.append(dict(r, **{'代码': code, '今开': r.get('今开', r.get('开盘'))}))
    return result
