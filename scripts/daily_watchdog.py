"""Windows fallback trigger. Uses existing Git Credential Manager login in memory."""
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import time
from zoneinfo import ZoneInfo
import requests

REPO = '13292123385/a-share-research'
ROOT = Path(__file__).resolve().parents[1]


def main():
    now = datetime.now(ZoneInfo('Asia/Shanghai'))
    if now.weekday() >= 5 or now.hour < 15:
        print('Outside weekday closing window; no dispatch.')
        return
    credential = subprocess.run(['git', 'credential', 'fill'],
        input='protocol=https\nhost=github.com\n\n', capture_output=True, text=True,
        cwd=ROOT, env=dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='never'), timeout=30)
    fields = dict(line.split('=', 1) for line in credential.stdout.splitlines() if '=' in line)
    if credential.returncode or not fields.get('password'):
        raise RuntimeError('GitHub login unavailable; no credentials printed')
    session = requests.Session()
    session.auth = (fields.get('username', 'git'), fields['password'])
    session.headers.update({'Accept': 'application/vnd.github+json', 'Cache-Control': 'no-cache'})
    base = 'https://api.github.com/repos/' + REPO
    def get(path):
        return session.get(base + path, params={'_check': time.time_ns()}, timeout=35)
    today = now.date().isoformat()
    latest = get('/contents/data/' + today + '/latest.json')
    complete = False
    if latest.status_code == 200:
        import base64
        ptr = json.loads(base64.b64decode(latest.json()['content']))
        summary = get('/contents/data/' + today + '/runs/' + ptr['run_id'] + '/summary.json')
        if summary.ok:
            data = json.loads(base64.b64decode(summary.json()['content']))
            complete = data.get('trade_date') == today and data.get('collection_status') == 'complete'
    elif latest.status_code != 404:
        raise RuntimeError(f'archive check HTTP {latest.status_code}')
    config = ROOT / 'public-feed.json'
    published = True
    if complete and config.exists():
        settings = json.loads(config.read_text(encoding='utf-8'))
        public_url = settings.get('pages_url')
        public_url = public_url + 'latest.json' if public_url else settings.get('json_url')
        if public_url:
            # Never send the authenticated GitHub session to the public website.
            try:
                response = requests.get(public_url, params={'_check': time.time_ns()}, timeout=25)
                payload = response.json() if response.ok else {}
                published = payload.get('trade_date') == today and payload.get('collection_status') == 'complete'
            except (ValueError, requests.RequestException):
                published = False
    if complete and published:
        print(today, 'collection and public feed current; no duplicate dispatch.')
        return
    runs = get('/actions/workflows/close.yml/runs')
    runs.raise_for_status()
    if any(r['status'] in ('queued', 'pending', 'waiting', 'in_progress', 'requested') for r in runs.json()['workflow_runs']):
        print(today, 'collection already queued/running; no duplicate dispatch.')
        return
    response = session.post(base + '/actions/workflows/close.yml/dispatches',
        json={'ref': 'main', 'inputs': {'date': today}}, timeout=35)
    if response.status_code != 204:
        raise RuntimeError(f'dispatch HTTP {response.status_code}')
    print(today, 'fallback dispatch submitted; collection result still requires verification.')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        # Requests exceptions can contain network details; only print type.
        print('Fallback trigger failed:', type(exc).__name__)
        raise SystemExit(1)
