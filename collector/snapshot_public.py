"""Publish independently dated lunch/closing market snapshots with checksums and shards."""
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import time

import requests

FIELDS = ('代码', '名称', '最新价', '今开', '最高', '最低', '昨收', '涨跌额', '涨跌幅',
          '成交量', '成交额', '换手率', '市盈率', '市盈率-动态', '市净率', '总市值', '流通市值',
          'quote_timestamp', 'quote_status')
META = ('schema_version', 'trade_date', 'session', 'run_id', 'fetched_at', 'finished_at',
        'status', 'records', 'expected_count', 'coverage', 'quality', 'units')
COVERAGE_FIELDS = ('status', 'expected_count', 'observed_count', 'missing_codes', 'unexpected_codes',
                   'duplicate_codes', 'unavailable_rosters', 'all_market_verified')
QUALITY_FIELDS = ('invalid_codes', 'stale_codes', 'suspended_codes', 'missing_fields',
                  'required_fields', 'nullable_fields', 'issues', 'timestamp_status')


def encode(value):
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n'


def digest(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def csv_text(rows):
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=FIELDS, extrasaction='ignore', lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


def make_files(snapshot, repository):
    if snapshot.get('session') not in ('midday', 'close') or snapshot.get('status') not in ('complete', 'partial'):
        raise ValueError('not a publishable market snapshot')
    # Rows never inherit arbitrary provider/private archive fields.
    rows = [{key: row.get(key) for key in FIELDS} for row in snapshot['rows']]
    if len(rows) != snapshot['records']:
        raise ValueError('snapshot record count mismatch')
    payload = {key: snapshot.get(key) for key in META}
    for key, fields in (('coverage', COVERAGE_FIELDS), ('quality', QUALITY_FIELDS)):
        payload[key] = {name: value for name, value in (payload[key] or {}).items() if name in fields}
    payload['rows'] = rows
    session = snapshot['session']
    prefix = 'market/' + session + '/'
    base = 'https://raw.githubusercontent.com/' + repository + '/main/'
    files = {prefix + 'snapshot.json': encode(payload), prefix + 'quotes.csv': csv_text(rows)}
    manifest = {key: payload[key] for key in META}
    manifest['files'] = {
        name.rsplit('/', 1)[1]: {'url': base + name, 'sha256': digest(content), 'bytes': len(content.encode('utf-8'))}
        for name, content in files.items()}
    manifest['chunks'] = []
    for offset in range(0, len(rows), 100):
        name = prefix + 'chunks/part-' + str(offset // 100 + 1).zfill(3) + '.csv'
        content = csv_text(rows[offset:offset + 100])
        files[name] = content
        manifest['chunks'].append(dict(url=base + name, records=len(rows[offset:offset + 100]), sha256=digest(content)))
    manifest['reading_instructions'] = ('先检查trade_date、session、status、coverage和quality。'
        '下载snapshot.json或quotes.csv读取全部股票；网页工具若截断，按chunks逐片读取并核对条数与SHA256。'
        '缺失/null不可当作零；partial不可称为完整快照。午盘与收盘独立保存。')
    files[prefix + 'latest.json'] = encode(manifest)
    lines = ['# 全市场' + ('午盘' if session == 'midday' else '收盘') + '快照', '',
             f"交易日：{payload['trade_date']}；状态：{payload['status']}；股票数：{len(rows)}/{payload['expected_count']}。",
             f"采集：{payload['fetched_at']}；完成：{payload['finished_at']}。", '',
             '[完整性清单](' + base + prefix + 'latest.json) · [全部股票CSV](' + base + prefix + 'quotes.csv) · [全部股票JSON](' + base + prefix + 'snapshot.json)',
             '', manifest['reading_instructions'], '', '## 网页读取分片（每片最多100只）', '']
    lines += ['- [' + str(i + 1) + '（' + str(c['records']) + '只）](' + c['url'] + ')' for i, c in enumerate(manifest['chunks'])]
    files[prefix + 'index.md'] = '\n'.join(lines) + '\n'
    archive = 'market/archive/' + payload['trade_date'] + '/' + session + '/' + payload['run_id'] + '/'
    archived_manifest = json.loads(encode(manifest))
    for name, meta in archived_manifest['files'].items():
        meta['url'] = base + archive + name
        files[archive + name] = files[prefix + name]
    for chunk in archived_manifest['chunks']:
        relative = chunk['url'].split('/main/' + prefix, 1)[1]
        chunk['url'] = base + archive + relative
        files[archive + relative] = files[prefix + relative]
    files[archive + 'manifest.json'] = encode(archived_manifest)
    return files, manifest


def should_promote(new, old):
    if not old:
        return True
    if new['trade_date'] != old['trade_date']:
        return new['trade_date'] > old['trade_date']
    if old.get('status') == 'complete' and new['status'] != 'complete':
        return False
    return new.get('fetched_at', '') >= old.get('fetched_at', '')


def publish(snapshot, repository, token):
    if not token or not repository or repository != '13292123385/a-share-market-data':
        raise ValueError('public market repository configuration missing or unexpected')
    files, manifest = make_files(snapshot, repository)
    session_name = snapshot['session']
    prefix = 'market/' + session_name + '/'
    client = requests.Session()
    client.headers.update({'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json'})
    base = 'https://api.github.com/repos/' + repository

    def api(path, method='GET', body=None):
        for attempt in range(3):
            response = client.request(method, base + path, json=body, timeout=45)
            if response.status_code not in (429, 500, 502, 503, 504):
                break
            time.sleep(2 ** attempt)
        if not response.ok:
            raise RuntimeError(f'public snapshot {method} HTTP {response.status_code}')
        return response.json()

    # Deduplicate blobs once and reuse their SHAs for archive and stable paths.
    blobs = {}
    for content in set(files.values()):
        if len(content.encode('utf-8')) >= 50000:
            blobs[content] = api('/git/blobs', 'POST', {'content': content, 'encoding': 'utf-8'})['sha']
    for attempt in range(4):
        head = api('/git/ref/heads/main')['object']['sha']
        previous = api('/git/commits/' + head)
        old_response = client.get(base + '/contents/' + prefix + 'latest.json', params={'ref': head}, timeout=30)
        old = None
        if old_response.status_code == 200:
            import base64
            old = json.loads(base64.b64decode(old_response.json()['content']))
        elif old_response.status_code != 404:
            raise RuntimeError('cannot verify existing session manifest')
        promote = should_promote(manifest, old)
        exported = {p: c for p, c in files.items() if promote or p.startswith('market/archive/')}
        exported[prefix + 'last_attempt.json'] = encode(manifest)
        exported['market/index.json'] = encode({'schema_version': 1,
            'midday': 'https://raw.githubusercontent.com/' + repository + '/main/market/midday/latest.json',
            'close': 'https://raw.githubusercontent.com/' + repository + '/main/market/close/latest.json',
            'note': '午盘11:30后、收盘15:00后独立采集。先核对日期和完整性；超过午休时间不能补造午盘。'})
        public_base = 'https://raw.githubusercontent.com/' + repository + '/main/'
        exported['market/index.md'] = '# 全市场快照读取入口\n\n' + '\n'.join(
            '- [' + label + '](' + public_base + 'market/' + name + '/index.md)；[完整性清单](' + public_base + 'market/' + name + '/latest.json)'
            for name, label in [('midday', '午盘全部股票'), ('close', '收盘全部股票')]) + '\n\n每个时段都提供完整JSON、CSV与每片100只的分片。核对日期、status、coverage、quality后再分析。\n'
        entries = []
        for path, content in exported.items():
            entry = dict(path=path, mode='100644', type='blob')
            entry.update({'sha': blobs[content]} if content in blobs else {'content': content})
            entries.append(entry)
        tree = api('/git/trees', 'POST', {'base_tree': previous['tree']['sha'], 'tree': entries})
        commit = api('/git/commits', 'POST', {'message': 'data: publish full-market ' + snapshot['trade_date'] + ' ' + session_name,
            'tree': tree['sha'], 'parents': [head]})
        response = client.patch(base + '/git/refs/heads/main', json={'sha': commit['sha'], 'force': False}, timeout=45)
        if response.ok:
            print('Published public market snapshot:', snapshot['trade_date'], session_name, manifest['records'], commit['sha'], flush=True)
            return manifest
        if response.status_code not in (409, 422):
            raise RuntimeError('public snapshot ref HTTP ' + str(response.status_code))
    raise RuntimeError('concurrent updates prevented snapshot publication')


def load_snapshot(run_path):
    root = Path(run_path)
    content = (root / 'snapshot.json').read_bytes()
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    if hashlib.sha256(content).hexdigest() != manifest['snapshot_sha256']:
        raise ValueError('private snapshot checksum mismatch')
    return json.loads(content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('run_path')
    parser.add_argument('--publish', action='store_true')
    parser.add_argument('--output', default='snapshot-public')
    args = parser.parse_args()
    snapshot = load_snapshot(args.run_path)
    repository = os.environ.get('PUBLIC_FEED_REPOSITORY', '13292123385/a-share-market-data')
    files, _ = make_files(snapshot, repository)
    for name, content in files.items():
        out = Path(args.output) / name
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding='utf-8', newline='')
    if args.publish:
        publish(snapshot, repository, os.environ.get('PUBLIC_FEED_TOKEN'))


if __name__ == '__main__':
    main()
