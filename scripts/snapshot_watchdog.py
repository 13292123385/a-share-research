"""Local fallback captures and publishes directly; it does not wait for Actions scheduling."""
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def local_token():
    git = shutil.which('git')
    if not git:
        for candidate in (Path(os.environ.get('ProgramFiles', 'C:/Program Files')) / 'Git/cmd/git.exe',
                          Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs/Git/cmd/git.exe'):
            if candidate.is_file():
                git = str(candidate)
                break
    if not git:
        raise RuntimeError('Git executable missing')
    result = subprocess.run([git, 'credential', 'fill'], input='protocol=https\nhost=github.com\n\n',
        cwd=ROOT, capture_output=True, text=True, timeout=30,
        env=dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='never'),
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    fields = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
    if result.returncode or not fields.get('password'):
        raise RuntimeError('Local GitHub login unavailable')
    return fields['password']


def main():
    from collector.market_snapshot import capture, session_for
    from collector.snapshot_public import publish
    from collector.snapshot_verify import verify
    now = datetime.now(ZoneInfo('Asia/Shanghai'))
    selected = session_for(now)
    if now.weekday() >= 5 or selected is None:
        print('Outside snapshot window; no collection.')
        return
    today = now.date().isoformat()
    repository = '13292123385/a-share-market-data'
    url = 'https://raw.githubusercontent.com/' + repository + '/main/market/' + selected + '/latest.json'
    try:
        response = requests.get(url, params={'v': time.time_ns()}, timeout=20)
        payload = response.json() if response.ok else {}
    except (requests.RequestException, ValueError):
        payload = {}
    if payload.get('trade_date') == today and payload.get('session') == selected and payload.get('status') == 'complete':
        # Verify bytes once per run before declaring success; no private credentials attached.
        try:
            verify(repository, selected, today)
        except (ValueError, requests.RequestException):
            print('Public snapshot verification failed; repairing publication.', flush=True)
        else:
            print(today, selected, 'complete public snapshot verified; no duplicate collection.')
            return
    token = local_token()
    snapshot = capture(str(ROOT / 'snapshot-data'), selected)
    if snapshot is None or snapshot['status'] == 'skipped':
        return
    if snapshot['status'] not in ('complete', 'partial'):
        raise RuntimeError('Trading date could not be verified')
    publish(snapshot, repository, token)
    verify(repository, selected, today)
    if snapshot['status'] != 'complete':
        raise RuntimeError('Snapshot incomplete; retained evidence and retry required')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('Snapshot fallback failed:', type(exc).__name__, flush=True)
        raise SystemExit(1)
