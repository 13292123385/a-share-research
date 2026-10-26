"""Offline archive invariants; partial upstream availability is not structural corruption."""
import hashlib
import json
import csv
from pathlib import Path
from .model import ordinary


def validate(root):
    errors = []
    paths = list(Path(root).glob('*/runs/*/summary.json'))
    if not paths:
        return [str(root) + ':no archived summaries']
    for path in paths:
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
        manifest = path.parent / 'files.json'
        if summary.get('schema_version', 1) >= 2 and not manifest.exists():
            errors.append(str(manifest) + ':missing file inventory')
        if manifest.exists():
            entries = json.loads(manifest.read_text(encoding='utf-8'))
            listed = {entry['path'] for entry in entries}
            actual = {p.relative_to(path.parent).as_posix() for p in path.parent.rglob('*')
                      if p.is_file() and p.name not in ('files.json', 'files.md')}
            if listed != actual or len(listed) != len(entries):
                errors.append(str(manifest) + ':file inventory mismatch')
            for entry in entries:
                file = path.parent / entry['path']
                if not file.resolve().is_relative_to(path.parent.resolve()):
                    errors.append(str(manifest) + ':unsafe path')
                    continue
                if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != entry['sha256']:
                    errors.append(str(file) + ':inventory checksum mismatch')
        for file in list((path.parent / 'raw').glob('*.json')) + list((path.parent / 'clean').glob('*.json')):
            def reject_constant(value):
                raise ValueError('nonfinite JSON number')
            try:
                value = json.loads(file.read_text(encoding='utf-8'), parse_constant=reject_constant)
            except (ValueError, OSError):
                errors.append(str(file) + ':invalid JSON')
                continue
            paired = file.with_suffix('.csv')
            if not isinstance(value, list):
                continue
            if not paired.is_file():
                errors.append(str(paired) + ':missing CSV pair')
                continue
            with paired.open(encoding='utf-8-sig', newline='') as f:
                rows = list(csv.DictReader(f))
            if len(rows) != len(value):
                errors.append(str(paired) + ':CSV/JSON record count mismatch')
    return errors


if __name__ == '__main__':
    import sys
    errors = validate(sys.argv[1] if len(sys.argv) > 1 else 'data')
    print('\n'.join(errors) if errors else 'Archive structural checks passed (does not assert upstream completeness).')
    raise SystemExit(bool(errors))
