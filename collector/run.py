"""python -m collector.run [--date YYYY-MM-DD] [--probe]"""
import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, date
from pathlib import Path
from zoneinfo import ZoneInfo

from .model import normalize, number, promotion, theme_score
from .quality import candidate_prices, select_snapshot, collect_index
from .followup import archived_cohorts, followup_rows, normalize_sina_spot
from .reconcile import collect_reconciliation
from .inventory import inventory, classify

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
        provider = ('中证指数官网' if function.endswith('_csindex') else
                    '上海证券交易所' if function.startswith(('stock_sse_', 'stock_info_sh_')) else
                    '深圳证券交易所' if function.startswith(('stock_szse_', 'stock_info_sz_')) else
                    '北京证券交易所' if function.startswith('stock_info_bj_') else
                    '新浪' if 'sina' in function or function == 'stock_zh_a_spot' else
                    '腾讯' if function.endswith('_tx') or function == 'tencent_quote' else '东方财富')
        meta = dict(function=function, provider=('直接请求 / ' if function == 'tencent_quote' else 'AKShare / ') + provider,
                    parameters=kwargs, fetched_at=started, status='error', rows=None, missing_fields=[])
        meta['documentation'] = 'https://akshare.akfamily.xyz/data/stock/stock.html'
        meta['raw_format'] = ('腾讯免费报价解析表（非HTTP原文）' if function == 'tencent_quote'
                              else 'AKShare返回表（非原始HTTP响应）')
        if function == 'tencent_quote':
            meta['documentation'] = 'https://gu.qq.com/' + kwargs['symbol'] + '/gp'
        meta['requested_trade_date'] = kwargs.get('date') or kwargs.get('end_date') or kwargs.get('trade_date')
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
    if not rows:
        c.calls[key].update(status='empty_unverified', rows=0)
        return None
    missing = [k for k in required if any(k not in r or r[k] is None for r in rows)]
    codes = [str(r.get('代码', '')).zfill(6) for r in rows]
    invalid = [code for code in codes if not re.fullmatch(r'\d{6}', code)]
    if missing or invalid or len(codes) != len(set(codes)):
        c.calls[key].update(status='schema_error', missing_fields=missing, duplicate_codes=len(codes) != len(set(codes)))
        if invalid:
            c.calls[key]['invalid_codes'] = invalid
        return None
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--date', type=date.fromisoformat)
    p.add_argument('--probe', action='store_true', help='诊断模式：日历失败仍尝试指定日接口，但数据不得成为每日有效快照')
    p.add_argument('--output', default='data')
    p.add_argument('--timeout', type=int, default=45)
    p.add_argument('--price-budget', type=int, default=420,
                   help='候选股历史价格补采总秒数，0为关闭；超预算保留缺失')
    p.add_argument('--followup-budget', type=int, default=300,
                   help='前两个交易日首板后续价格补采总秒数，0为关闭')
    args = p.parse_args()
    if args.timeout <= 0 or args.price_budget < 0 or args.followup_budget < 0:
        p.error('timeout必须大于0，补采预算不得为负数')
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
    covered = bool(days and days[0] <= target.isoformat() <= days[-1])
    trading = covered and target.isoformat() in days
    closed = target < now.date() or (target == now.date() and now.hour >= 15)
    valid = trading and closed and target <= now.date()
    summary = dict(schema_version=2, trade_date=target.isoformat(), fetched_at=now.isoformat(), run_id=run_id,
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
        spot_source, spot_scope = '东方财富', '沪深北（未独立核验完整性）'
        # Live spot has no reliable historical date. Never use today's OHLC for another day.
        if target == now.date() and closed:
            spot = check_rows(c, 'spot', c.call('spot', 'stock_zh_a_spot_em'), ['代码','名称','涨跌幅','成交额','今开','最高','最低','最新价'])
            if spot is None:
                rows = c.call('spot_fallback', 'stock_zh_a_spot')
                normalized = normalize_sina_spot(rows, include_beijing=True) if rows is not None else None
                if rows and not normalized:
                    c.calls['spot_fallback']['status'] = 'schema_error'
                spot = check_rows(c, 'spot_fallback', normalized or None,
                                  ['代码','名称','涨跌幅','成交额','今开','最高','最低','最新价'])
                spot_source, spot_scope = '新浪', '沪深北候选范围（以官方名单核验结果为准）'
        if target == now.date() and valid:
            reconciliation = collect_reconciliation(c, spot, target.isoformat())
            dump(root / 'clean' / 'market_reconciliation.json', reconciliation)
            summary['market_reconciliation'] = reconciliation
            if reconciliation['status'] != 'code_coverage_matched':
                summary['missing_data'].append('行情与官方名单代码覆盖不一致或无法核验，详见market_reconciliation')
            if reconciliation['szse_turnover_check']['status'] != 'within_tolerance':
                summary['missing_data'].append('深圳A股成交额交叉核验未通过或不可比较')
        else:
            summary['market_reconciliation'] = dict(status='not_applicable_historical',
                all_market_verified=False, note='当前上市名单不能冒充历史名单；只对当日有效采集执行自动核验')
        quotes = {str(r['代码']).zfill(6): r for r in (spot or [])}
        if spot:
            changes = [number(r['涨跌幅']) for r in spot]
            amounts = [number(r['成交额']) for r in spot]
            summary['estimates']['market'] = dict(up=sum(v > 0 for v in changes if v is not None),
                down=sum(v < 0 for v in changes if v is not None), flat=sum(v == 0 for v in changes if v is not None),
                turnover_yuan=sum(v for v in amounts if v is not None), records=len(spot),
                unknown_direction=sum(v is None for v in changes),
                unknown_amount=sum(v is None for v in amounts),
                source=spot_source, scope=spot_scope,
                note='收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘')
            if None in changes or None in amounts:
                summary['missing_data'].append('市场汇总含未知涨跌方向或成交额，汇总只计已知项，不能视为完整总量')
            table(root / 'clean' / 'market_quotes', spot)
        else:
            summary['missing_data'].append('全市场收盘快照；不跨日套用实时数据')
        cached_prices = []
        previous_pointer = root.parents[1] / 'latest.json'
        if previous_pointer.exists():
            ptr = json.loads(previous_pointer.read_text(encoding='utf-8'))
            cache = root.parent / ptr['run_id'] / 'clean' / 'candidate_prices.json'
            if cache.exists():
                cached_prices = [dict(r, origin_run=r.get('origin_run') or ptr['run_id'])
                                 for r in json.loads(cache.read_text(encoding='utf-8'))]
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
        cohorts, missing_cohorts = archived_cohorts(args.output, days, target.isoformat())
        followup_pool = [{'代码': r['code'], '名称': r['name'], '连板数': 1} for r in
                         {r['code']: r for r in cohorts}.values()]
        historical_quotes = {r['code']: {'今开': r['open'], '最高': r['high'],
                            '最低': r['low'], '最新价': r['close']} for r in prices}
        followup_cache = []
        if previous_pointer.exists():
            cache = root.parent / ptr['run_id'] / 'clean' / 'followup_prices.json'
            if cache.exists():
                followup_cache = [dict(r, origin_run=r.get('origin_run') or ptr['run_id'])
                                  for r in json.loads(cache.read_text(encoding='utf-8'))]
        followup_prices, missing_followup = candidate_prices(c, followup_pool, historical_quotes,
            target.isoformat(), args.followup_budget, cached_prices + followup_cache)
        all_historical = {r['code']: r for r in prices + followup_prices}
        table(root / 'clean' / 'followup_prices',
              [all_historical[r['代码']] for r in followup_pool if r['代码'] in all_historical])
        tracked = followup_rows(cohorts, all_historical, target.isoformat())
        table(root / 'clean' / 'first_board_followup', tracked)
        summary['followup'] = dict(rows=len(tracked), prices_available=sum(r['status'] == 'price_available' for r in tracked),
            missing_archive_dates=missing_cohorts, missing_price_codes=missing_followup,
            budget_seconds=args.followup_budget, note='按交易日追踪首板后第1/2个交易日，不推断成交或策略收益')
        summary['followup_price_coverage'] = sorted(all_historical.keys() & {r['code'] for r in cohorts})
        if missing_cohorts or missing_followup:
            summary['missing_data'].append('首板后续跟踪存在历史名单或价格缺失，详见followup')
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
            matched = collect_index(c, symbol, target.isoformat())
            if matched is not None:
                indices.append(dict(name=name, symbol=symbol, **matched))
            else:
                summary['missing_data'].append(name + '指定日期收盘值')
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
        if valid:
            classify(summary, target < now.date())
        else:
            summary['status'] = 'diagnostic_unverified'
    dump(root / 'sources.json', c.calls)
    dump(root / 'summary.json', summary)
    report = [f'# {target} A股收盘复盘', '', f'状态：{summary["status"]}；抓取时间：{now.isoformat()}', '',
              f'采集范围：{summary.get("collection_scope", "未有效采集")}；采集状态：{summary.get("collection_status", "未执行")}；研究状态：{summary.get("research_status", "未执行")}', '',
              '## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）',
              json.dumps(summary['verified'], ensure_ascii=False), '',
              '## 估算值', json.dumps(summary['estimates'], ensure_ascii=False), '',
              '## 一进二', json.dumps(summary.get('promotion', {}), ensure_ascii=False), '',
              '观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。', '',
              '## 缺失数据', *['- ' + s for s in summary['missing_data']], '',
              '## 候选股价格覆盖', json.dumps(summary.get('candidate_price_quality', {}), ensure_ascii=False), '',
              '## 前两交易日首板后续跟踪', json.dumps(summary.get('followup', {}), ensure_ascii=False), '',
              '## 市场交叉核验', json.dumps(summary.get('market_reconciliation', {}), ensure_ascii=False), '',
              '主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。', '',
              '## 接口状态', *[f'- {k}: {v["status"]}，行数={v["rows"]}' for k,v in c.calls.items()]]
    if not valid:
        report.append('日历未确认、非交易日或未收盘，本次不得解释为有效收盘快照。')
    (root / 'report.md').write_text('\n'.join(report) + '\n', encoding='utf-8', newline='\n')
    daily = Path(args.output) / target.isoformat()
    (daily / 'report.md').write_text('\n'.join(report) + '\n', encoding='utf-8', newline='\n')
    # Preserve every attempt. Only promote valid, reasonably complete snapshots.
    if valid and today is not None:
        summary['selected_as_latest'] = select_snapshot(daily, summary)
        dump(root / 'summary.json', summary)
    inventory(root, c.calls)
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as f:
            f.write(f'summary_path={root / "summary.json"}\n')
    print(str(root), flush=True)
    return 0 if summary['status'] in ('complete', 'complete_with_limitations', 'skipped') else 2


if __name__ == '__main__':
    raise SystemExit(main())
