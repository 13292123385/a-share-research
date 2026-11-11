"""Isolated allowlisted public namespace; close-report files are never updated."""
import argparse
import json
import os
from pathlib import Path
import requests
from .lifecycle_validate import read, validate_run


def make_files(root):
    root = Path(root)
    errors = validate_run(root)
    if errors:
        raise ValueError('lifecycle quality failed: ' + ';'.join(errors))
    summary = read(root / 'summary.json')
    if summary.get('status') not in ('complete', 'partial'):
        raise ValueError('no calendar-verified lifecycle snapshot')
    clean = root / 'clean'
    watch_fields = ('code', 'name', 'first_observed', 'observation_date', 'candidate_basis',
                    'leader_confirmed', 'theme_ids', 'theme_status', 'last_confirmed_break_date',
                    'sessions_after_break', 'current_pool_status', 'execution_verified', 'entry_price')
    watch = [{k:r.get(k) for k in watch_fields} for r in read(clean / 'leader_watch.json')]
    price_fields = ('code', 'observation_date', 'price', 'status', 'missing_reason', 'volume_unit', 'execution_verified', 'entry_price')
    prices = [{k:r.get(k) for k in price_fields} for r in read(clean / 'leader_prices.json')]
    payload = {k:summary.get(k) for k in ('trade_date', 'run_id', 'status', 'fetched_at', 'min_post_break_sessions',
                'watch_count', 'price_rows', 'missing_price_rows', 'theme_status', 'missing_archive_dates', 'note')}
    payload['coverage'] = sorted(['watch:' + r['code'] for r in watch] +
        ['catalog:' + r['theme_id'] for r in read(clean / 'theme_catalog.json')] +
        ['price:' + r['code'] + ':' + r['observation_date'] for r in prices if r['status'] == 'available'] +
        ['theme:' + r['theme_id'] for r in read(clean / 'theme_coverage.json') if r['status'] == 'available'])
    values = {'latest.json': payload, 'leader_watch.json': watch, 'leader_prices.json': prices}
    for name in ('theme_catalog', 'theme_members', 'theme_coverage', 'theme_history', 'theme_lifecycle'):
        values[name + '.json'] = [{k:v for k,v in r.items() if k != 'origin_run'} for r in read(clean / (name + '.json'))]
    result = {name:json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) for name,value in values.items()}
    result['README.md'] = (f'# 题材与龙头观察数据\n\n交易日：{payload["trade_date"]}；状态：{payload["status"]}。\n\n'
        '先检查日期与缺失。四板候选不是确认龙头；概念成分只证明抓取时归属。价格缺失不代表停牌，观察不保证成交，不计算真实收益。'
        '\n\n原每日收盘报告仍在仓库根目录；本目录独立发布。\n')
    return result


def publish(files, repository, token):
    if not repository or not token:
        raise ValueError('public lifecycle publishing configuration missing')
    session = requests.Session()
    session.headers.update({'Authorization':'Bearer ' + token, 'Accept':'application/vnd.github+json'})
    base = 'https://api.github.com/repos/' + repository

    def api(path, method='GET', body=None):
        response = session.request(method, base + path, json=body, timeout=45)
        if not response.ok:
            raise RuntimeError(f'lifecycle public API HTTP {response.status_code}')
        return response.json()

    payload = json.loads(files['latest.json'])
    archive = 'lifecycle/archive/' + payload['trade_date'] + '/' + payload['run_id'] + '/'
    # Retry only optimistic ref races; each attempt builds on the newest remote tree.
    for attempt in range(3):
        head = api('/git/ref/heads/main')['object']['sha']
        previous = api('/git/commits/' + head)
        old = session.get(base + '/contents/lifecycle/latest.json', params={'ref':head}, timeout=45)
        if old.status_code == 200:
            import base64
            prior = json.loads(base64.b64decode(old.json()['content']))
            promote = payload['trade_date'] > prior['trade_date'] or (payload['trade_date'] == prior['trade_date'] and
                set(prior.get('coverage', [])).issubset(payload['coverage']) and
                set(prior.get('missing_archive_dates', [])) >= set(payload.get('missing_archive_dates', [])))
        elif old.status_code == 404:
            promote = True
        else:
            raise RuntimeError('cannot verify public lifecycle pointer')
        existing = session.get(base + '/contents/' + archive + 'latest.json', params={'ref':head}, timeout=45)
        if existing.status_code == 200:
            import base64
            if base64.b64decode(existing.json()['content']).decode('utf-8') == files['latest.json']:
                return  # exact run already committed; idempotent rerun
            raise ValueError('immutable public lifecycle archive conflict')
        if existing.status_code != 404:
            raise RuntimeError('cannot verify immutable lifecycle archive')
        exported = {archive + name:content for name,content in files.items()}
        if promote:
            exported.update({'lifecycle/' + name:content for name,content in files.items()})
        tree = api('/git/trees', 'POST', {'base_tree':previous['tree']['sha'], 'tree':[
            dict(path=name, mode='100644', type='blob', content=content) for name,content in exported.items()]})
        commit = api('/git/commits', 'POST', {'message':'data: archive lifecycle observations', 'tree':tree['sha'], 'parents':[head]})
        response = session.patch(base + '/git/refs/heads/main', json={'sha':commit['sha'], 'force':False}, timeout=45)
        if response.ok:
            return
        if response.status_code not in (409, 422):
            raise RuntimeError(f'lifecycle public ref HTTP {response.status_code}')
    raise RuntimeError('public repository changed during three publish attempts')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('run')
    p.add_argument('--output', default='lifecycle-public')
    p.add_argument('--publish', action='store_true')
    a = p.parse_args()
    files = make_files(a.run)
    out = Path(a.output)
    out.mkdir(parents=True, exist_ok=True)
    for name,content in files.items():
        (out / name).write_text(content, encoding='utf-8')
    if a.publish:
        publish(files, os.environ.get('PUBLIC_FEED_REPOSITORY'), os.environ.get('PUBLIC_FEED_TOKEN'))


if __name__ == '__main__':
    main()
