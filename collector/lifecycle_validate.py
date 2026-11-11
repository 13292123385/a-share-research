"""Structural quality and reproducibility checks for the isolated lifecycle archive."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from .quality import daily_price
from .lifecycle import observations


def read(path):
    def invalid(value):
        raise ValueError('nonfinite JSON')
    return json.loads(path.read_text(encoding='utf-8'), parse_constant=invalid)


def validate_run(root):
    errors = []
    root = Path(root)
    try:
        summary = read(root / 'summary.json')
        if summary['trade_date'] != root.parents[1].name:
            errors.append('date mismatch')
        entries = read(root / 'files.json')
        listed = {r['path'] for r in entries}
        actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name not in ('files.json', 'files.md')}
        if listed != actual or len(listed) != len(entries):
            errors.append('inventory mismatch')
        for r in entries:
            file = root / r['path']
            if not file.resolve().is_relative_to(root.resolve()):
                errors.append('unsafe inventory path')
                continue
            if not file.exists() or hashlib.sha256(file.read_bytes()).hexdigest() != r['sha256']:
                errors.append(r['path'] + ':checksum mismatch')
        for path in root.rglob('*.json'):
            read(path)
        for key, meta in read(root / 'sources.json').items():
            if meta.get('status') == 'ok':
                raw = root / 'raw' / (key + '.json')
                if not raw.is_file() or hashlib.sha256(raw.read_bytes()).hexdigest() != meta.get('sha256'):
                    errors.append('source raw checksum mismatch')
        for path in (root / 'clean').glob('*.json'):
            rows = read(path)
            with path.with_suffix('.csv').open(encoding='utf-8-sig', newline='') as stream:
                if len(list(csv.DictReader(stream))) != len(rows):
                    errors.append(path.name + ':csv count mismatch')
        if summary.get('status') == 'calendar_unknown_or_non_session':
            return errors
        days = read(root / 'calendar_inputs.json')
        target = summary['trade_date']
        if days != sorted(set(days)) or not days or days[-1] != target:
            errors.append('calendar invalid')
        inputs = read(root / 'archive_inputs.json')
        pools = {day: None for day in days}
        for r in inputs:
            if hashlib.sha256(r['raw_json'].encode('utf-8')).hexdigest() != r['sha256'] or json.loads(r['raw_json']) != r['rows']:
                errors.append('archive input hash mismatch')
            if r['date'] not in days:
                errors.append('future or noncalendar archive input')
            pools[r['date']] = r['rows']
        watch = read(root / 'clean' / 'leader_watch.json')
        automatic = observations(pools, days, target)
        keys = ('code', 'first_observed', 'last_confirmed_break_date', 'sessions_after_break', 'current_pool_status')
        saved = [r for r in watch if r['candidate_basis'] == 'archived_height_ge_4']
        if [{k:r[k] for k in keys} for r in saved] != [{k:r[k] for k in keys} for r in automatic]:
            errors.append('watch replay mismatch')
        rows = read(root / 'clean' / 'leader_prices.json')
        pairs = [(r['code'], r['observation_date']) for r in rows]
        required = {(r['code'], day) for r in watch for day in days if r['first_observed'] <= day <= target}
        if len(pairs) != len(set(pairs)) or set(pairs) != required:
            errors.append('daily tracking coverage mismatch')
        for r in rows:
            price = r.get('price')
            if price and (price.get('adjustment') != 'none' or not daily_price([price], r['observation_date'])):
                errors.append('invalid daily price')
            if r['status'] == 'available' and (price is None or price.get('volume') is None or price['volume'] < 0):
                errors.append('invalid OHLCV coverage')
            if not r.get('execution_verified') is False or r.get('entry_price') is not None:
                errors.append('unverified execution claim')
        coverage = {r['theme_id']:r for r in read(root / 'clean' / 'theme_coverage.json')}
        members = read(root / 'clean' / 'theme_members.json')
        seen = set()
        for r in members:
            pair = (r['theme_id'], r['code'])
            if pair in seen or r['observation_date'] != target or r.get('historical_valid_from') is not None:
                errors.append('invalid point-in-time membership')
            seen.add(pair)
            if coverage.get(r['theme_id'], {}).get('status') != 'available':
                errors.append('unavailable membership claimed')
        for ident, r in coverage.items():
            if r['status'] == 'available' and r['member_count'] != sum(m['theme_id'] == ident for m in members):
                errors.append('member count mismatch')
        evidence_file = root / 'clean' / 'dated_theme_evidence.json'
        if evidence_file.exists():
            evidence = read(evidence_file)
            evidence_pairs = set()
            for r in evidence:
                pair = (r['theme_id'], r['code'])
                if pair in evidence_pairs or r['observation_date'] != target or r.get('coverage') != 'partial_selected_active_stocks' or r.get('source_price_used') is not False:
                    errors.append('invalid dated theme evidence')
                evidence_pairs.add(pair)
                html = root / 'raw' / 'dated_theme_evidence.html'
                if not html.exists() or hashlib.sha256(html.read_text(encoding='utf-8').encode('utf-8')).hexdigest() != r['source_sha256']:
                    errors.append('dated evidence HTML mismatch')
        if summary.get('status') == 'complete' and (any(r['status'] != 'available' for r in rows) or summary['theme_status'] != 'available'):
            errors.append('false completeness')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(type(exc).__name__ + ':invalid archive')
    return errors


def main():
    p = argparse.ArgumentParser()
    p.add_argument('root')
    args = p.parse_args()
    roots = sorted(Path(args.root).glob('*/runs/*/summary.json'))
    errors = [str(p.parent) + ':' + error for p in roots for error in validate_run(p.parent)]
    errors += [str(p) + ':incomplete attempt without summary' for p in Path(args.root).glob('*/runs/*')
               if p.is_dir() and not (p / 'summary.json').exists()]
    if not roots:
        errors.append('no lifecycle archives')
    print('\n'.join(errors) if errors else f'{len(roots)} lifecycle runs validated')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
