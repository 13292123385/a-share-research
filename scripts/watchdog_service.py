"""User-login fallback when Windows refuses Task Scheduler registration."""
from datetime import datetime
import msvcrt
from pathlib import Path
import subprocess
import sys
import time
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
TIMES = tuple(f'{h:02d}:{m:02d}' for h in (11, 12, 15, 16, 17) for m in range(0, 60, 10) if h != 11 or m >= 30) + ('18:15', '21:15')


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
        if now.weekday() < 5 and now.hour >= 11:
            due = [stamp for stamp in TIMES if stamp <= now.strftime('%H:%M') and stamp not in fired]
            if due:
                # One check catches up all earlier missed times after login/resume.
                fired.update(due)
                scripts = ['snapshot_watchdog.py']
                if now.hour >= 15:
                    scripts.append('daily_watchdog.py')
                for script in scripts:
                    try:
                        result = subprocess.run([sys.executable, str(ROOT / 'scripts' / script)],
                            cwd=ROOT, capture_output=True, text=True, timeout=1100,
                            creationflags=subprocess.CREATE_NO_WINDOW)
                        message = f'{script} exit={result.returncode} {result.stdout.strip()}'
                    except Exception as exc:
                        message = f'{script} failed={type(exc).__name__}'
                    with (state / 'service.log').open('a', encoding='utf-8') as log:
                        log.write(f'{now.isoformat()} {message}\n')
        time.sleep(20)


if __name__ == '__main__':
    main()
