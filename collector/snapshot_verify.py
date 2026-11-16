"""Verify the publicly readable bytes, date, session and complete row set, without login."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import hashlib
import io
import json
import time

import requests


def verify(repository, session, expected_day=None, expected_run=None):
    base = 'https://raw.githubusercontent.com/' + repository + '/main/market/' + session + '/'
    # A clean session: never attach private GitHub credentials to public URLs.
    client = requests.Session()
    for attempt in range(6):
        response = client.get(base + 'latest.json', params={'v': time.time_ns()}, timeout=30)
        if response.ok:
            manifest = response.json()
            if (not expected_day or manifest['trade_date'] == expected_day) and (not expected_run or manifest['run_id'] == expected_run):
                break
        time.sleep(5)
    else:
        raise ValueError('public manifest missing, outdated or not the published run')
    if manifest['session'] != session:
        raise ValueError('public session mismatch')
    counts = {}
    complete_codes = None
    for name, meta in manifest['files'].items():
        data = client.get(meta['url'], params={'v': time.time_ns()}, timeout=45)
        data.raise_for_status()
        if hashlib.sha256(data.content).hexdigest() != meta['sha256']:
            raise ValueError('public bytes checksum mismatch: ' + name)
        rows = data.json()['rows'] if name.endswith('.json') else list(csv.DictReader(io.StringIO(data.content.decode('utf-8'))))
        codes = [row['代码'] for row in rows]
        if len(codes) != manifest['records'] or len(codes) != len(set(codes)):
            raise ValueError('public records missing or duplicated')
        if complete_codes is not None and set(codes) != complete_codes:
            raise ValueError('public JSON/CSV contain different codes')
        complete_codes = set(codes)
        counts[name] = len(rows)
    if sum(c['records'] for c in manifest['chunks']) != manifest['records']:
        raise ValueError('public chunk record count mismatch')
    def check_chunk(chunk):
        data = requests.get(chunk['url'], params={'v': time.time_ns()}, timeout=30)
        data.raise_for_status()
        if hashlib.sha256(data.content).hexdigest() != chunk['sha256']:
            raise ValueError('public chunk checksum mismatch')
        rows = list(csv.DictReader(io.StringIO(data.content.decode('utf-8'))))
        if len(rows) != chunk['records']:
            raise ValueError('public chunk actual row count mismatch')
        return [row['代码'] for row in rows]
    with ThreadPoolExecutor(max_workers=4) as executor:
        chunk_codes = [code for batch in executor.map(check_chunk, manifest['chunks']) for code in batch]
    if len(chunk_codes) != manifest['records'] or len(chunk_codes) != len(set(chunk_codes)) or set(chunk_codes) != complete_codes:
        raise ValueError('public chunks do not reproduce the full market')
    print(json.dumps(dict(trade_date=manifest['trade_date'], session=session, status=manifest['status'],
                          expected=manifest['expected_count'], files_verified=counts,
                          chunks_verified=len(manifest['chunks']), anonymous=True), ensure_ascii=True), flush=True)
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--session', required=True, choices=('midday', 'close'))
    parser.add_argument('--date')
    parser.add_argument('--run-id')
    parser.add_argument('--repository', default='13292123385/a-share-market-data')
    args = parser.parse_args()
    manifest = verify(args.repository, args.session, args.date, args.run_id)
    if manifest['status'] != 'complete':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
