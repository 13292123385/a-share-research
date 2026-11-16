"""Warm an already allocated cloud runner before the two observation windows."""
from datetime import datetime
import time
from zoneinfo import ZoneInfo

TZ = ZoneInfo('Asia/Shanghai')


def seconds_until_capture(now):
    now = now.astimezone(TZ)
    if now.weekday() >= 5:
        return 0
    for hour, minute, start_hour in ((11, 30, 11), (15, 0, 14)):
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if start_hour <= now.hour and now < target:
            return (target - now).total_seconds()
    return 0


def main():
    while True:
        now = datetime.now(TZ)
        remaining = seconds_until_capture(now)
        if remaining <= 0:
            print('Cloud runner ready for capture:', now.isoformat(), flush=True)
            return
        print('Cloud runner allocated; seconds until capture:', int(remaining), flush=True)
        time.sleep(min(30, remaining))


if __name__ == '__main__':
    main()
