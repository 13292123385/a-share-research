"""User-login fallback when Windows refuses Task Scheduler registration."""
from datetime import datetime
import msvcrt
from pathlib import Path
import subprocess
import sys
import time
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
TIMES = ('15:12', '15:35', '16:15', '18:15', '21:15')


def main():
    state = ROOT / 'diagnostics' / 'watchdog'
    state.mkdir(parents=True, exist_ok=True)
    lock = (state / 'service.lock').open('a+b')
    lock.seek(0)
    lock.write(b'0')
    lock.flush()
    lock.seek(0)
    try:
        msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        return
    last_date, fired = None, set()
    while True:
        now = datetime.now(ZoneInfo('Asia/Shanghai'))
        if now.date() != last_date:
            last_date, fired = now.date(), set()
        if now.weekday() < 5 and now.hour >= 15:
            due = [stamp for stamp in TIMES if stamp <= now.strftime('%H:%M') and stamp not in fired]
            if due:
                # One check catches up all earlier missed times after login/resume.
                fired.update(due)
                result = subprocess.run([sys.executable, str(ROOT / 'scripts/daily_watchdog.py')],
                    cwd=ROOT, capture_output=True, text=True, timeout=240,
                    creationflags=subprocess.CREATE_NO_WINDOW)
                with (state / 'service.log').open('a', encoding='utf-8') as log:
                    log.write(f'{now.isoformat()} exit={result.returncode} {result.stdout.strip()}\n')
        time.sleep(60)


if __name__ == '__main__':
    main()
