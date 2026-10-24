"""Offline archive invariants; partial upstream availability is not structural corruption."""
import hashlib
import json
from pathlib import Path
from .model import ordinary


def validate(root):
    errors = []
    for path in Path(root).glob('*/runs/*/summary.json'):
        summary = json.loads(path.read_text(encoding='utf-8'))
        sources = json.loads((path.parent / 'sources.json').read_text(encoding='utf-8'))
        if path.parents[2].name != summary['trade_date']:
            errors.append(str(path) + ':date mismatch')
        for key, meta in sources.items():
            if meta['status'] == 'ok':
                raw = path.parent / 'raw' / (key + '.json')
                if hashlib.sha256(raw.read_bytes()).hexdigest() != meta['sha256']:
                    errors.append(str(raw) + ':checksum mismatch')
        for file in (path.parent / 'clean').glob('*.json'):
            rows = json.loads(file.read_text(encoding='utf-8'))
            if not isinstance(rows, list):
                continue
            for r in rows:
                if 'name' in r and 'code' in r and not ordinary(r['code'], r['name']):
                    errors.append(str(file) + ':invalid universe')
                if r.get('execution_verified') is False and any(r.get(k) is not None for k in ('entry_price','third_day_return','max_adverse_excursion')):
                    errors.append(str(file) + ':unverified return')
                if r.get('all_day_one_word') is True and r.get('eligible_observation'):
                    errors.append(str(file) + ':one-word eligible')
    return errors


if __name__ == '__main__':
    import sys
    errors = validate(sys.argv[1] if len(sys.argv) > 1 else 'data')
    print('\n'.join(errors) if errors else 'Archive structural checks passed (does not assert upstream completeness).')
    raise SystemExit(bool(errors))
