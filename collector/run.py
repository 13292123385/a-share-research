"""python -m collector.run [--date YYYY-MM-DD] [--probe]"""
import argparse
import csv
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, date
from pathlib import Path
from zoneinfo import ZoneInfo

from .model import normalize, number, promotion, theme_score
from .quality import candidate_prices, select_snapshot

TZ = ZoneInfo('Asia/Shanghai')


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')


def table(path, rows):
    dump(path.with_suffix('.json'), rows)
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with path.with_suffix('.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys or ['status'])
        w.writeheader()
        w.writerows({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in r.items()} for r in rows)


class Collector:
    def __init__(self, root, timeout=45, delay=2):
        self.root, self.timeout, self.delay = root, timeout, delay
        self.calls = {}

    def call(self, key, function, **kwargs):
        path = self.root / 'raw' / f'{key}.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        started = datetime.now(TZ).isoformat()
        provider = '新浪' if 'sina' in function else '腾讯' if function.endswith('_tx') else '东方财富'
        meta = dict(function=function, provider='AKShare / ' + provider,
                    parameters=kwargs, fetched_at=started, status='error', rows=None, missing_fields=[])
        meta['documentation'] = 'https://akshare.akfamily.xyz/data/stock/stock.html'
        meta['raw_format'] = 'AKShare返回表（非原始HTTP响应）'
        meta['requested_trade_date'] = kwargs.get('date') or kwargs.get('end_date')
        rows = None
        try:
            time.sleep(self.delay)
            p = subprocess.run([sys.executable, '-m', 'collector.worker', function, str(path), json.dumps(kwargs)],
                               capture_output=True, timeout=self.timeout, encoding='utf-8', errors='replace')
            if p.returncode:
                # Exception type only: do not persist URLs, proxy credentials or environment.
                raise RuntimeError(p.stderr.strip().splitlines()[-1].split(':')[0][:100] if p.stderr.strip() else 'worker_error')
            rows = json.loads(path.read_text(encoding='utf-8'))
            table(path, rows)
            meta.update(status='ok' if rows else 'empty_unverified', rows=len(rows),
                        sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        except subprocess.TimeoutExpired:
            meta['error'] = 'TimeoutExpired'
        except Exception as e:
            meta['error'] = str(e)[:100]
        meta['finished_at'] = datetime.now(TZ).isoformat()
        self.calls[key] = meta
        dump(self.root / 'sources.json', self.calls)
        print(f'{key}: {meta["status"]} rows={meta["rows"]}' +
              (f' error={meta["error"]}' if meta.get('error') else ''), flush=True)
        return rows if meta['status'] == 'ok' else None


def check_rows(c, key, rows, required):
    if rows is None:
        return None
    missing = [k for k in required if any(k not in r or r[k] is None for r in rows)]
    codes = [str(r.get('代码')) for r in rows]
    if missing or len(codes) != len(set(codes)):
        c.calls[key].update(status='schema_error', missing_fields=missing, duplicate_codes=len(codes) != len(set(codes)))
        return None
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--date', type=date.fromisoformat)
    p.add_argument('--probe', action='store_true', help='诊断模式：日历失败仍尝试指定日接口，但数据不得成为每日有效快照')
    p.add_argument('--output', default='data')
    p.add_argument('--timeout', type=int, default=45)
    p.add_argument('--price-budget', type=int, default=180,
                   help='候选股历史价格补采总秒数，0为关闭；超预算保留缺失')
    args = p.parse_args()
    now = datetime.now(TZ)
    target = args.date or now.date()
    run_id = now.strftime('%Y%m%dT%H%M%S%f%z')
    root = Path(args.output) / target.isoformat() / 'runs' / run_id
    c = Collector(root, args.timeout)
    calendar = c.call('calendar', 'tool_trade_date_hist_sina')
    try:
        days = sorted({date.fromisoformat(str(r['trade_date'])[:10]).isoformat() for r in calendar}) if calendar else []
    except (KeyError, ValueError, TypeError):
        days = []
        c.calls['calendar'].update(status='schema_error', missing_fields=['trade_date'])
    covered = bool(days and days[-1] >= target.isoformat())
    trading = covered and target.isoformat() in days
    closed = target < now.date() or (target == now.date() and now.hour >= 15)
    valid = trading and closed and target <= now.date()
    summary = dict(schema_version=1, trade_date=target.isoformat(), fetched_at=now.isoformat(), run_id=run_id,
                   calendar_covered=covered, trading_day=trading if covered else None,
                   status='collecting' if valid else 'calendar_unknown' if not covered else 'skipped',
                   missing_data=[], estimates={}, verified={}, theme=theme_score())
    if valid or args.probe:
        d = target.strftime('%Y%m%d')
        frames = {}
        for key, function in [('limit_up','stock_zt_pool_em'), ('yesterday_pool','stock_zt_pool_previous_em'),
                              ('broken','stock_zt_pool_zbgc_em'), ('limit_down','stock_zt_pool_dtgc_em')]:
            rows = c.call(key, function, date=d)
            required = ['代码','名称'] + (['连板数','首次封板时间','最后封板时间','炸板次数'] if key == 'limit_up' else [])
            frames[key] = check_rows(c, key, rows, required)
        spot = None
        # Live spot has no reliable historical date. Never use today's OHLC for another day.
        if target == now.date() and closed:
            spot = check_rows(c, 'spot', c.call('spot', 'stock_zh_a_spot_em'), ['代码','名称','涨跌幅','成交额','今开','最高','最低','最新价'])
        quotes = {str(r['代码']).zfill(6): r for r in (spot or [])}
        if spot:
            changes = [number(r['涨跌幅']) for r in spot]
            amounts = [number(r['成交额']) for r in spot]
            summary['estimates']['market'] = dict(up=sum(v > 0 for v in changes if v is not None),
                down=sum(v < 0 for v in changes if v is not None), flat=sum(v == 0 for v in changes if v is not None),
                turnover_yuan=sum(v for v in amounts if v is not None), records=len(spot),
                note='收盘后实时快照汇总，含沪深北；分页完整性和行情日期未获独立验证，可能含停牌平盘')
        else:
            summary['missing_data'].append('全市场收盘快照；不跨日套用实时数据')
        cached_prices = []
        previous_pointer = root.parents[1] / 'latest.json'
        if previous_pointer.exists():
            ptr = json.loads(previous_pointer.read_text(encoding='utf-8'))
            cache = root.parent / ptr['run_id'] / 'clean' / 'candidate_prices.json'
            if cache.exists():
                cached_prices = json.loads(cache.read_text(encoding='utf-8'))
        prices, missing_prices = candidate_prices(c, frames['limit_up'], quotes,
                                                  target.isoformat(), args.price_budget, cached_prices)
        table(root / 'clean' / 'candidate_prices', prices)
        summary['price_coverage'] = sorted(quotes)
        summary['candidate_price_quality'] = dict(historical_available=len(prices),
            historical_fetched=sum(not r.get('reused_from_prior_run') for r in prices),
            reused=sum(bool(r.get('reused_from_prior_run')) for r in prices),
            missing_codes=missing_prices, budget_seconds=args.price_budget,
            note='首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算')
        if missing_prices:
            summary['missing_data'].append(f'候选股同日OHLC缺失{len(missing_prices)}只（含预算未执行）')
        clean = {}
        for key, rows in frames.items():
            clean[key] = normalize(rows, quotes) if rows is not None else None
            if key != 'limit_up' and clean[key] is not None:
                for row in clean[key]:
                    row.update(all_day_one_word=None, eligible_observation=False)
            if clean[key] is not None:
                table(root / 'clean' / key, clean[key])
        today = clean['limit_up']
        if today is not None:
            candidates = [r for r in today if r['height'] == 1]
            table(root / 'clean' / 'first_board_candidates', candidates)
            summary['verified']['mainboard_limit_up_count'] = len(today)
            summary['verified']['mainboard_height'] = max((r['height'] for r in today if r['height'] is not None), default=None)
            summary['verified']['first_board_candidates'] = len(candidates)
            summary['verified']['all_day_one_word_excluded'] = sum(r['all_day_one_word'] is True for r in today)
            summary['verified']['one_word_unknown'] = sum(r['all_day_one_word'] is None for r in today)
        for key in ('broken', 'limit_down'):
            summary['verified'][key + '_count'] = len(clean[key]) if clean[key] is not None else None
        indices = []
        for name, symbol in [('上证指数','sh000001'), ('深证成指','sz399001'), ('创业板指','sz399006'), ('中证2000','csi932000')]:
            rows = c.call('index_' + symbol, 'stock_zh_index_daily_em', symbol=symbol, start_date=d, end_date=d)
            if rows is None:
                rows = c.call('index_retry_' + symbol, 'stock_zh_index_daily_em', symbol=symbol, start_date=d, end_date=d)
            if rows is None and symbol.startswith(('sh', 'sz')):
                rows = c.call('index_fallback_' + symbol, 'stock_zh_index_daily_tx', symbol=symbol,
                              start_date=d, end_date=d)
                c.calls['index_fallback_' + symbol]['provider'] = 'AKShare / 腾讯'
            matched = [r for r in (rows or []) if str(r.get('date',''))[:10] == target.isoformat()]
            if len(matched) == 1 and number(matched[0].get('close')) is not None:
                indices.append(dict(name=name, symbol=symbol, **matched[0]))
            else:
                summary['missing_data'].append(name + '指定日期收盘值')
                if rows:
                    c.calls['index_' + symbol]['status'] = 'date_or_schema_error'
        table(root / 'clean' / 'indices', indices)
        summary['verified']['indices'] = indices
        previous = None
        earlier = [x for x in days if x < target.isoformat()]
        if earlier:
            prev_date = earlier[-1]
            pointer = Path(args.output) / prev_date / 'latest.json'
            if pointer.exists():
                ptr = json.loads(pointer.read_text(encoding='utf-8'))
                prior = Path(args.output) / prev_date / 'runs' / ptr['run_id'] / 'clean' / 'limit_up.json'
                if prior.exists():
                    previous = json.loads(prior.read_text(encoding='utf-8'))
        result = promotion(previous, today, clean['broken'])
        dump(root / 'clean' / 'promotion.json', result)
        table(root / 'clean' / 'promotion_rows', result['rows'])
        summary['promotion'] = {k:v for k,v in result.items() if k != 'rows'}
        summary['source_failures'] = {k: v for k, v in c.calls.items() if v['status'] != 'ok'}
        summary['missing_data'] += [k + ':' + c.calls[k]['status'] for k, rows in frames.items() if rows is None]
        if previous is None:
            summary['missing_data'].append('上一交易日已归档涨停池；昨日涨停接口不提供昨日连板高度，不能替代该依赖')
        summary['status'] = ('complete' if not summary['missing_data'] else 'partial') if valid else 'diagnostic_unverified'
    dump(root / 'sources.json', c.calls)
    dump(root / 'summary.json', summary)
    report = [f'# {target} A股收盘复盘', '', f'状态：{summary["status"]}；抓取时间：{now.isoformat()}', '',
              '## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）',
              json.dumps(summary['verified'], ensure_ascii=False), '',
              '## 估算值', json.dumps(summary['estimates'], ensure_ascii=False), '',
              '## 一进二', json.dumps(summary.get('promotion', {}), ensure_ascii=False), '',
              '观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。', '',
              '## 缺失数据', *['- ' + s for s in summary['missing_data']], '',
              '## 候选股价格覆盖', json.dumps(summary.get('candidate_price_quality', {}), ensure_ascii=False), '',
              '主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。', '',
              '## 接口状态', *[f'- {k}: {v["status"]}，行数={v["rows"]}' for k,v in c.calls.items()]]
    if not valid:
        report.append('日历未确认、非交易日或未收盘，本次不得解释为有效收盘快照。')
    (root / 'report.md').write_text('\n'.join(report) + '\n', encoding='utf-8')
    daily = Path(args.output) / target.isoformat()
    (daily / 'report.md').write_text('\n'.join(report) + '\n', encoding='utf-8')
    # Preserve every attempt. Only promote valid, reasonably complete snapshots.
    if valid and today is not None:
        summary['selected_as_latest'] = select_snapshot(daily, summary)
        dump(root / 'summary.json', summary)
    print(str(root), flush=True)
    return 0 if summary['status'] in ('complete', 'skipped') else 2


if __name__ == '__main__':
    raise SystemExit(main())
