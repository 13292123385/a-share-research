"""Retry publication from saved private archives without resampling old sessions."""
from datetime import datetime
import os
from pathlib import Path
from zoneinfo import ZoneInfo

from .snapshot_recover import recover
from .snapshot_public import publish
from .snapshot_verify import verify


def main():
    day = datetime.now(ZoneInfo('Asia/Shanghai')).date().isoformat()
    repository = os.environ.get('PUBLIC_FEED_REPOSITORY', '13292123385/a-share-market-data')
    failures = 0
    for session in ('midday', 'close'):
        if not (Path('snapshot-data') / day / session / 'latest.json').exists():
            print('No saved session to redeliver:', day, session, flush=True)
            continue
        try:
            snapshot = recover('snapshot-data', day, session)
            publish(snapshot, repository, os.environ.get('PUBLIC_FEED_TOKEN'))
            manifest = verify(repository, session, day)
            if manifest['status'] != 'complete':
                failures += 1
        except Exception as exc:
            print('Saved-session delivery failed:', session, type(exc).__name__, flush=True)
            failures += 1
    raise SystemExit(1 if failures else 0)


if __name__ == '__main__':
    main()
