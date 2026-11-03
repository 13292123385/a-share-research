"""Select a closed trading date; persistently retry missing archives across midnight."""
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def pending_date(days, now, root):
    root = Path(root)
    existing = sorted(p.name for p in root.glob('????-??-??') if p.is_dir())
    start = existing[0] if existing else now.date().isoformat()
    closed = [d for d in days if d >= start and
              (d < now.date().isoformat() or (d == now.date().isoformat() and now.hour >= 15))]
    def complete(day):
        pointer = root / day / 'latest.json'
        if not pointer.exists():
            return False
        ptr = json.loads(pointer.read_text(encoding='utf-8'))
        summary = root / day / 'runs' / ptr['run_id'] / 'summary.json'
        if not summary.exists():
            return False
        data = json.loads(summary.read_text(encoding='utf-8'))
        return data.get('trade_date') == day and data.get('status') == 'complete'
    # Get today's live snapshot first; afterwards drain older outstanding dates.
    today = now.date().isoformat()
    if today in closed and not complete(today):
        return today
    return next((d for d in closed if not complete(d)), None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date')
    args = parser.parse_args()
    if args.date:
        return subprocess.call([sys.executable, '-m', 'collector.run', '--date', args.date])
    import akshare as ak
    calendar = ak.tool_trade_date_hist_sina()
    days = sorted({str(d)[:10] for d in calendar['trade_date']})
    now = datetime.now(ZoneInfo('Asia/Shanghai'))
    if not days or days[-1] < now.date().isoformat():
        raise RuntimeError('Trading calendar does not cover today')
    target = pending_date(days, now, 'data')
    if target is None:
        print('No outstanding closed trading dates; no collection needed.', flush=True)
        return 0
    print('Collecting outstanding trading date: ' + target, flush=True)
    return subprocess.call([sys.executable, '-m', 'collector.run', '--date', target])


if __name__ == '__main__':
    raise SystemExit(main())
