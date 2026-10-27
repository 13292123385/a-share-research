"""Publish an allowlisted market-data view; never publish the private repository."""
import argparse
from datetime import datetime
import html
import json
import os
from pathlib import Path
from zoneinfo import ZoneInfo
import requests

TZ = ZoneInfo('Asia/Shanghai')
FIELDS = ('code', 'name', 'height', 'open', 'high', 'low', 'close', 'volume', 'amount',
          'price_date', 'price_source', 'industry', 'first_seal', 'last_seal', 'open_count',
          'all_day_one_word', 'eligible_observation', 'execution_verified', 'missing_fields')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def make_files(data, now=None):
    now = now or datetime.now(TZ)
    choices = []
    for ptr in Path(data).glob('*/latest.json'):
        selected = read(ptr)
        root = ptr.parent / 'runs' / selected['run_id']
        summary = read(root / 'summary.json')
        if summary.get('trading_day') is True and summary.get('status') not in ('skipped', 'diagnostic_unverified', 'calendar_unknown'):
            choices.append((summary['trade_date'], root, summary))
    if not choices:
        raise ValueError('no valid selected trading-day archive to publish')
    day, root, summary = max(choices, key=lambda item: item[0])
    # Explicit allowlist: do not copy raw provider responses, file paths or private notes.
    verified_keys = ('mainboard_limit_up_count', 'mainboard_height', 'first_board_candidates',
                     'all_day_one_word_excluded', 'one_word_unknown', 'broken_count', 'limit_down_count', 'indices')
    verified = {k: summary.get('verified', {}).get(k) for k in verified_keys}
    market_keys = ('up', 'down', 'flat', 'turnover_yuan', 'records', 'unknown_direction', 'unknown_amount', 'source', 'note')
    market = {k: summary.get('estimates', {}).get('market', {}).get(k) for k in market_keys}
    coverage = summary.get('market_reconciliation', {})
    payload = dict(trade_date=day, published_at=now.isoformat(), fetched_at=summary.get('fetched_at'),
        collection_status=summary.get('collection_status', 'partial'), status=summary.get('status'),
        research_status=summary.get('research_status', 'limited'), missing_data=summary.get('missing_data', []),
        verified=verified, market_estimates=market,
        market_coverage={k: coverage.get(k) for k in ('status', 'expected_count', 'observed_count', 'all_market_verified')},
        verified_tradable_rate=None, note='公开行情研究数据；不含私有代码、账户信息或真实策略收益。先核对trade_date和缺失项目。')
    payload['followup'] = {k: summary.get('followup', {}).get(k) for k in
        ('rows', 'prices_available', 'missing_archive_dates', 'missing_price_codes', 'note')}
    attempts = sorted(Path(data).glob('*/runs/*/summary.json'))
    latest_attempt = max((read(p) for p in attempts), key=lambda s: s.get('fetched_at', ''), default={})
    payload['last_attempt'] = {k: latest_attempt.get(k) for k in ('trade_date', 'fetched_at', 'status', 'collection_status', 'collection_failures')}
    files = {'latest.json': json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False)}
    lines = ['# A股行情最新归档', '', f'行情交易日：**{day}**', f'采集状态：{payload["collection_status"]}；研究状态：{payload["research_status"]}',
             f'抓取时间：{payload["fetched_at"]}；发布时间：{payload["published_at"]}', '',
             '读取提示：先核对行情交易日。若不是请求的日期，明确说明过期；缺失和null不能解释为零。', '',
             f'主板涨停{verified["mainboard_limit_up_count"]}只；首板{verified["first_board_candidates"]}只；指数{len(verified.get("indices") or [])}/4。',
             f'全市场代码覆盖：{coverage.get("observed_count")}/{coverage.get("expected_count")}；全部字段独立验证：{coverage.get("all_market_verified", False)}。', '', '## 缺失项目',
             *['- ' + str(item) for item in payload['missing_data']], '',
             '## 主板涨停池', '| 代码 | 名称 | 连板 | 一字板 | 观察资格 |', '|---|---|---:|---|---|']
    for filename, source in [('limit_up.json', 'limit_up'), ('first_board.json', 'first_board_candidates'), ('broken.json', 'broken'), ('limit_down.json', 'limit_down')]:
        path = root / 'clean' / (source + '.json')
        rows = [{k: row.get(k) for k in FIELDS} for row in read(path)] if path.exists() else None
        files[filename] = json.dumps(rows, ensure_ascii=False, indent=2, allow_nan=False)
        if source == 'limit_up':
            for row in rows or []:
                cells = [row.get(k) for k in ('code', 'name', 'height', 'all_day_one_word', 'eligible_observation')]
                lines.append('| ' + ' | '.join(str(x).replace('|', '\\|').replace('\n', ' ') for x in cells) + ' |')
    followup_path = root / 'clean' / 'first_board_followup.json'
    followup = []
    for row in read(followup_path) if followup_path.exists() else []:
        exported = {k: row.get(k) for k in ('code', 'name', 'first_board_date', 'sessions_since_first',
            'observation_date', 'original_eligible_observation', 'status', 'execution_verified')}
        price = row.get('price')
        exported['price'] = ({k: price.get(k) for k in ('date', 'open', 'high', 'low', 'close', 'volume', 'amount', 'source')}
                             if isinstance(price, dict) else None)
        followup.append(exported)
    files['followup.json'] = json.dumps(followup, ensure_ascii=False, indent=2, allow_nan=False)
    lines += ['', f'历史首板跟踪价格：{payload["followup"].get("prices_available")}/{payload["followup"].get("rows")}；缺失代码见latest.json。',
              '观察资格不是可成交证明；买价、真实收益及可成交晋级率未验证，继续留空。',
              '数据来源：AKShare转接东方财富/新浪/腾讯/中证官网，市场名单来自沪深北交易所；备用源失败保留于私有完整归档。',
              '同一公开目录的 latest.json 为机器入口，first_board.json 为首板候选，limit_up.json 为主板涨停，followup.json 为历史首板跟踪。', '']
    files['latest.md'] = '\n'.join(lines)
    files['START_HERE.md'] = '# 手机 GPT 读取入口\n\n请读取同目录latest.md和latest.json，核对trade_date及collection_status，再使用first_board.json/limit_up.json/followup.json分析。日期不符则说明过期，缺失不补零，不把观察统计当可成交收益。\n\n若聊天没有联网读取工具，请在浏览器打开latest.md并复制正文，或下载JSON上传。公开链接免GitHub登录，但不能替手机聊天开启工具。\n'
    return files


def publish(files, gist_id, token):
    if not token or not gist_id:
        raise ValueError('public feed publishing configuration missing')
    response = requests.patch('https://api.github.com/gists/' + gist_id,
        headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json'},
        json={'files': {name: {'content': content} for name, content in files.items()}}, timeout=45)
    if response.status_code != 200:
        raise RuntimeError(f'public feed HTTP {response.status_code}')
    print('Public market feed updated:', response.json()['html_url'], flush=True)


def publish_repository(files, repository, token):
    """Commit only the generated feed to its separate public data repository."""
    session = requests.Session()
    session.headers.update({'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json', 'Cache-Control': 'no-cache'})
    base = 'https://api.github.com/repos/' + repository
    def api(path, method='GET', body=None):
        response = session.request(method, base + path, json=body, timeout=45)
        if not response.ok:
            raise RuntimeError(f'public repository {method} HTTP {response.status_code}')
        return response.json()
    ref = api('/git/ref/heads/main')
    head = ref['object']['sha']
    previous = api('/git/commits/' + head)
    exported = dict(files)
    exported['.nojekyll'] = ''
    exported['README.md'] = files['latest.md']
    # Plain, server-delivered HTML: no JavaScript, login, or API tool needed to read.
    exported['index.html'] = ('<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>A股行情最新归档</title><style>body{max-width:1000px;margin:24px auto;padding:0 16px;font:16px/1.7 sans-serif}pre{white-space:pre-wrap;overflow-wrap:anywhere}</style>'
        '<h1>A股行情最新归档</h1><p><a href="latest.json">行情摘要JSON</a> · <a href="first_board.json">首板数据</a> · <a href="limit_up.json">涨停数据</a> · <a href="latest.md">纯文字报告</a></p>'
        '<pre>' + html.escape(files['latest.md']) + '</pre></html>')
    tree = api('/git/trees', 'POST', {'base_tree': previous['tree']['sha'],
        'tree': [dict(path=name, mode='100644', type='blob', content=content) for name, content in exported.items()]})
    commit = api('/git/commits', 'POST', {'message': 'data: refresh dated public market feed',
        'tree': tree['sha'], 'parents': [head]})
    api('/git/refs/heads/main', 'PATCH', {'sha': commit['sha'], 'force': False})
    print('Public data repository updated:', repository, commit['sha'][:7], flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--data', default='data')
    p.add_argument('--output', default='public')
    p.add_argument('--publish', action='store_true')
    args = p.parse_args()
    files = make_files(args.data)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (out / name).write_text(content, encoding='utf-8', newline='\n')
    if args.publish:
        token = os.environ.get('PUBLIC_FEED_TOKEN')
        publish(files, os.environ.get('PUBLIC_FEED_GIST_ID'), token)
        repository = os.environ.get('PUBLIC_FEED_REPOSITORY')
        if repository:
            publish_repository(files, repository, token)


if __name__ == '__main__':
    main()
