"""Republish an already saved session even after its live capture window has ended."""
import argparse
from datetime import date, datetime
import json
import os
from pathlib import Path
import re
from zoneinfo import ZoneInfo

from .snapshot_public import load_snapshot


def recover(output, trade_date, session):
    date.fromisoformat(trade_date)
    if session not in ('midday', 'close'):
        raise ValueError('invalid session')
    daily = Path(output) / trade_date / session
    pointer = json.loads((daily / 'latest.json').read_text(encoding='utf-8'))
    run_id = pointer['run_id']
    if not re.fullmatch(r'[A-Za-z0-9_+\-]+', run_id):
        raise ValueError('invalid saved run identity')
    root = daily / 'runs' / run_id
    snapshot = load_snapshot(root)
    if snapshot.get('trade_date') != trade_date or snapshot.get('session') != session:
        raise ValueError('saved snapshot date or session mismatch')
    if snapshot.get('status') not in ('complete', 'partial'):
        raise ValueError('saved attempt not publishable')
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as stream:
            stream.write(f'run_path={root.as_posix()}\nstatus={snapshot["status"]}\nsession={session}\n')
    print('Recovering saved snapshot:', trade_date, session, run_id, snapshot['status'], flush=True)
    return snapshot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--session', choices=('auto', 'midday', 'close'), default='auto')
    parser.add_argument('--date', type=date.fromisoformat)
    parser.add_argument('--output', default='snapshot-data')
    args = parser.parse_args()
    now = datetime.now(ZoneInfo('Asia/Shanghai'))
    session = args.session if args.session != 'auto' else 'close' if now.hour >= 15 else 'midday'
    snapshot = recover(args.output, (args.date or now.date()).isoformat(), session)
    if snapshot['status'] != 'complete':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
