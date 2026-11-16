"""Publish an allowlisted market-data view; never publish the private repository."""
import argparse
from datetime import datetime
import hashlib
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
MARKET_FIELDS = ('代码', '名称', '最新价', '涨跌幅', '涨跌额', '今开', '最高', '最低',
                 '昨收', '成交量', '成交额', '振幅', '换手率', '量比', '市盈率-动态',
                 '市净率', '总市值', '流通市值', '涨速', '5分钟涨跌', '60日涨跌幅',
                 '年初至今涨跌幅', 'quote_date', 'quote_timestamp', 'volume_unit')
MARKET_PART_SIZE = 100


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def market_files(root, day, summary):
    """Export every archived quote, including explicit nulls, through a field allowlist."""
    quote_path = root / 'clean' / 'market_quotes.json'
    raw = read(quote_path) if quote_path.is_file() else None
    if raw is not None and not isinstance(raw, list):
        raise ValueError('market quote archive must be a row list')
    rows = [{key: row.get(key) for key in MARKET_FIELDS} for row in raw] if raw is not None else None
    coverage = summary.get('market_reconciliation', {})
    meta = dict(trade_date=day, fetched_at=summary.get('fetched_at'),
                records=len(rows) if rows is not None else None,
                status='available' if rows else 'missing',
                source=summary.get('estimates', {}).get('market', {}).get('source'),
                coverage_status=coverage.get('status'),
                expected_count=coverage.get('expected_count'),
                all_market_verified=coverage.get('all_market_verified', False),
                note='日线归档中的逐股实时快照；不保证报价日期及收盘时点。null是缺失，不是零。')
    files, parts = {}, []
    for offset in range(0, len(rows or []), MARKET_PART_SIZE):
        part_rows = rows[offset:offset + MARKET_PART_SIZE]
        name = f'market_snapshot/part-{len(parts) + 1:03d}.json'
        part = dict(trade_date=day, fetched_at=meta['fetched_at'], records=len(part_rows), rows=part_rows)
        files[name] = json.dumps(part, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
        parts.append(dict(file=name, records=len(part_rows),
                          first_code=part_rows[0]['代码'], last_code=part_rows[-1]['代码']))
    manifest = dict(meta, fields=list(MARKET_FIELDS), parts=parts)
    files['market_snapshot/manifest.json'] = json.dumps(manifest, ensure_ascii=False, indent=2, allow_nan=False)
    files['market_snapshot.json'] = json.dumps(dict(meta, rows=rows), ensure_ascii=False,
                                               separators=(',', ':'), allow_nan=False)
    return files, dict(meta, file='market_snapshot.json', manifest='market_snapshot/manifest.json')


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
    files, payload['market_snapshot'] = market_files(root, day, summary)
    files['latest.json'] = json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False)
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
    lines += ['## 全市场逐股快照',
              '[完整JSON](market_snapshot.json) · [分块目录](market_snapshot/manifest.json)',
              f'归档记录数：{payload["market_snapshot"]["records"]}；状态：{payload["market_snapshot"]["status"]}。',
              '读取全部记录时按分块目录依次读取所有part，并核对记录数之和；单次网页读取可能截断完整JSON。',
              '此处来自日线归档，交易日与本报告相同。',
              '[每日午盘、收盘独立完整快照入口](market/index.md)：分别核对交易日、时段和报价时间。', '']
    files['latest.md'] = '\n'.join(lines)
    files['START_HERE.md'] = '# 手机 GPT 读取入口\n\n每日午盘、下午收盘的独立完整快照，先读取[market/index.md](market/index.md)，分别核对各时段的交易日、状态和报价时间。\n\n日报读取同目录latest.md和latest.json，核对trade_date及collection_status。日报的全市场逐股快照读取market_snapshot/manifest.json并依次读取列出的全部分块，或下载完整market_snapshot.json；该快照交易日以日报为准。核对记录数，不把摘要或网页截断当作全量。首板、涨停和跟踪另见first_board.json/limit_up.json/followup.json。日期不符则说明过期，缺失不补零，不把观察统计当可成交收益。\n\nGist只存摘要，全市场文件以公开数据仓库为准。若聊天没有联网读取工具，请下载JSON上传。\n'
    return files


def publish(files, gist_id, token):
    if not token or not gist_id:
        raise ValueError('public feed publishing configuration missing')
    # Gist is a small summary mirror. Keep megabytes of quotes and nested chunk
    # paths in the public repository, avoiding Gist truncation and filename limits.
    gist_files = {name: {'content': content} for name, content in files.items()
                  if name != 'market_snapshot.json' and not name.startswith('market_snapshot/')}
    repository = os.environ.get('PUBLIC_FEED_REPOSITORY')
    if repository:
        gist_files['FULL_MARKET.md'] = {'content':
            '# 全市场逐股快照\n\n请读取公开仓库的[分块目录]('
            f'https://raw.githubusercontent.com/{repository}/main/market_snapshot/manifest.json'
            ')并依次读取全部分块。Gist只镜像摘要。\n'}
    response = requests.patch('https://api.github.com/gists/' + gist_id,
        headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json'},
        json={'files': gist_files}, timeout=45)
    if response.status_code != 200:
        raise RuntimeError(f'public feed HTTP {response.status_code}')
    print('Public market feed updated:', response.json()['html_url'], flush=True)


def publish_repository(files, repository, token):
    """Commit only the generated feed to its separate public data repository."""
    session = requests.Session()
    session.headers.update({'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json', 'Cache-Control': 'no-cache'})
    base = 'https://api.github.com/repos/' + repository
    class RepositoryError(RuntimeError):
        def __init__(self, method, status):
            super().__init__(f'public repository {method} HTTP {status}')
            self.status = status

    def api(path, method='GET', body=None):
        response = session.request(method, base + path, json=body, timeout=45)
        if not response.ok:
            raise RepositoryError(method, response.status_code)
        return response.json()

    # Large content is uploaded once even when used in both stable and archive
    # paths. Trees stay small, and retries can reuse already-created blobs.
    blobs = {}
    def entries(exported):
        tree = []
        for name, content in exported.items():
            entry = dict(path=name, mode='100644', type='blob')
            encoded = content.encode('utf-8')
            if len(encoded) >= 50 * 1024:
                key = hashlib.sha256(encoded).hexdigest()
                if key not in blobs:
                    blobs[key] = api('/git/blobs', 'POST', {'content': content, 'encoding': 'utf-8'})['sha']
                entry['sha'] = blobs[key]
            else:
                entry['content'] = content
            tree.append(entry)
        return tree

    payload = json.loads(files['latest.json'])
    stamp = payload['published_at'].replace(':', '').replace('+', '_')
    archive = 'archive/' + payload['trade_date'] + '/' + stamp + '/'
    # Plain, server-delivered HTML: no JavaScript, login, or API tool needed to read.
    index = ('<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>A股行情最新归档</title><style>body{max-width:1000px;margin:24px auto;padding:0 16px;font:16px/1.7 sans-serif}pre{white-space:pre-wrap;overflow-wrap:anywhere}</style>'
        '<h1>A股行情最新归档</h1><p><a href="latest.json">行情摘要JSON</a> · <a href="market_snapshot/manifest.json">全市场分块目录</a> · <a href="market_snapshot.json">完整逐股快照</a> · <a href="first_board.json">首板数据</a> · <a href="limit_up.json">涨停数据</a> · <a href="latest.md">纯文字报告</a></p>'
        '<pre>' + html.escape(files['latest.md']) + '</pre></html>')
    for attempt in range(3):
        ref = api('/git/ref/heads/main')
        head = ref['object']['sha']
        previous = api('/git/commits/' + head)
        old_response = session.get(base + '/contents/latest.json', params={'ref': head}, timeout=45)
        if old_response.status_code == 200:
            import base64
            old = json.loads(base64.b64decode(old_response.json()['content']))
            rank = {'complete': 3, 'complete_with_limitations': 2, 'partial': 1}
            promote = payload['trade_date'] > old['trade_date'] or (payload['trade_date'] == old['trade_date'] and
                rank.get(payload.get('status'), 0) >= rank.get(old.get('status'), 0) and
                set(payload.get('missing_data', [])).issubset(old.get('missing_data', [])))
        elif old_response.status_code == 404:
            promote = True
        else:
            raise RuntimeError('Cannot verify existing latest')
        exported = {archive + name: content for name, content in files.items()}
        if promote:
            exported.update(files)
            exported.update({'.nojekyll': '', 'README.md': files['latest.md'], 'index.html': index})
        tree = api('/git/trees', 'POST', {'base_tree': previous['tree']['sha'], 'tree': entries(exported)})
        commit = api('/git/commits', 'POST', {
            'message': 'data: refresh dated public market feed' if promote else 'data: preserve historical attempt',
            'tree': tree['sha'], 'parents': [head]})
        try:
            api('/git/refs/heads/main', 'PATCH', {'sha': commit['sha'], 'force': False})
        except RepositoryError as exc:
            if exc.status not in (409, 422) or attempt == 2:
                raise
            continue
        print('Public data repository updated:', repository, commit['sha'][:7], flush=True)
        return promote


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
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8', newline='\n')
    if args.publish:
        token = os.environ.get('PUBLIC_FEED_TOKEN')
        repository = os.environ.get('PUBLIC_FEED_REPOSITORY')
        if repository:
            if publish_repository(files, repository, token):
                publish(files, os.environ.get('PUBLIC_FEED_GIST_ID'), token)


if __name__ == '__main__':
    main()
