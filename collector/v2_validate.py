"""V2 structural checks are deliberately separate from collection completeness."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

from .model import ordinary
from .quality import daily_price


def read(path):
    def invalid(value):
        raise ValueError('nonfinite_json')
    return json.loads(Path(path).read_text(encoding='utf-8'), parse_constant=invalid)


def validate_run(root):
    root = Path(root)
    errors = []
    try:
        entries = read(root / 'files.json')
        listed = {r['path'] for r in entries}
        actual = {p.relative_to(root).as_posix() for p in root.rglob('*')
                  if p.is_file() and p.name not in ('files.json', 'files.md')}
        if listed != actual or len(entries) != len(listed):
            errors.append('inventory_mismatch')
        for row in entries:
            path = root / row['path']
            if not path.resolve().is_relative_to(root.resolve()):
                errors.append('unsafe_inventory_path')
                continue
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
                errors.append('checksum_mismatch:' + row['path'])
        for path in root.rglob('*.json'):
            read(path)
        for key, meta in read(root / 'sources.json').items():
            if meta.get('status') == 'ok':
                path = root / 'raw' / (key + '.json')
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != meta.get('sha256'):
                    errors.append('source_checksum_mismatch:' + key)
        for path in (root / 'clean').glob('*.json'):
            with path.with_suffix('.csv').open(encoding='utf-8-sig', newline='') as stream:
                if len(list(csv.DictReader(stream))) != len(read(path)):
                    errors.append('csv_json_count_mismatch:' + path.name)
        inputs, report = read(root / 'analysis_inputs.json'), read(root / 'report.json')
        days = inputs['days']
        if days != sorted(set(days)) or len(days) != 40 or report['trade_date'] != days[-1]:
            errors.append('invalid_40_session_calendar')
        if root.parents[1].name != report['trade_date']:
            errors.append('run_date_mismatch')
        calendar = read(root / 'calendar_input.json')
        if hashlib.sha256(calendar['raw_json'].encode('utf-8')).hexdigest() != calendar['sha256']:
            errors.append('calendar_input_checksum')
        calendar_days = sorted({str(r['trade_date'])[:10] for r in json.loads(calendar['raw_json'])})
        end = calendar_days.index(days[-1]) + 1
        if days != calendar_days[end - 40:end] or inputs['baseline_date'] != calendar_days[end - 41]:
            errors.append('calendar_window_or_baseline_mismatch')
        for meta in inputs['review_coverage']:
            if meta['status'] == 'available':
                path = root / 'raw' / (meta['date'] + '.html')
                if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != meta['sha256']:
                    errors.append('review_input_checksum:' + meta['date'])
        seen = set()
        for row in inputs['observations']:
            key = row['date'], row['code']
            if key in seen or row['date'] not in days or not ordinary(row['code'], row['name']):
                errors.append('invalid_or_duplicate_stock_observation')
            seen.add(key)
            associations = row.get('theme_association_evidence', [])
            for theme in row['theme_ids']:
                valid = any(r['theme_id'] == theme and r['date'] == row['date'] and
                    (r['basis'] == 'dated_active_association_table' or
                     (r['basis'] == 'dated_reason' and r.get('reason_asof') and r['reason_asof'] <= row['date']))
                    for r in associations)
                if not valid:
                    errors.append('future_or_undated_theme_reason')
        price_keys = set()
        for row in inputs['prices']:
            key = row['code'], row['date'], row.get('adjustment')
            if key in price_keys or row['date'] not in [inputs['baseline_date']] + days or row.get('adjustment') not in ('none', 'qfq') or not daily_price([row], row['date']):
                errors.append('invalid_or_duplicate_core_price')
            price_keys.add(key)
        for row in report['rankings']:
            if report['coverage']['complete_historical_membership_days'] < 40 and row.get('full_score') is not None:
                errors.append('fabricated_full_score')
        seats = [r['theme_id'] for r in report['selection']['seats'].values() if r]
        if len(seats) > 3 or len(seats) != len(set(seats)):
            errors.append('seat_limit_or_duplicate')
        total = set()
        for ident, cores in report['core_by_theme'].items():
            if ident not in seats or len(cores) > 3 or len({r['code'] for r in cores}) != len(cores):
                errors.append('core_theme_or_count')
            for row in cores:
                total.add(row['code'])
                if not ordinary(row['code'], row['name']) or row.get('execution_verified') is not False or row.get('entry_price') is not None or row.get('actual_return') is not None:
                    errors.append('unverified_core_execution_or_scope')
                if '带动王' in row['roles'] and row.get('leadership_status') == 'pending_confirmation':
                    errors.append('unverified_influence_claim')
        if len(total) > 9 or len(report['trading']['candidates']) > 4:
            errors.append('observation_or_plan_limit')
        trading = report['trading']
        if trading.get('actual_positions') is not None or trading.get('actual_return') is not None:
            errors.append('fabricated_positions_or_trading_return')
        for field in ('candidates', 'research_setups', 'blocked'):
            for row in trading.get(field, []):
                if row.get('code') not in total:
                    errors.append('trading_code_outside_observation_pool')
                if field != 'blocked' and (row.get('execution_verified') is not False or row.get('entry_price') is not None or row.get('actual_return') is not None):
                    errors.append('fabricated_candidate_execution')
        for filename in ('historical_active_associations', 'stock_observations', 'core_prices', 'review_coverage', 'market_coverage', 'price_coverage'):
            expected = inputs[{'historical_active_associations': 'observations', 'stock_observations': 'observations',
                'core_prices': 'prices', 'review_coverage': 'review_coverage', 'market_coverage': 'market_coverage',
                'price_coverage': 'price_coverage'}[filename]]
            if filename != 'historical_active_associations' and read(root / 'clean' / (filename + '.json')) != expected:
                errors.append('clean_input_mismatch:' + filename)
    except (KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as exc:
        errors.append('validation_error:' + type(exc).__name__ + ':' + str(exc)[:120])
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('run')
    args = parser.parse_args(argv)
    errors = validate_run(args.run)
    if errors:
        print('\n'.join(errors))
        return 1
    print('V2 quality passed; completeness is reported separately in summary.json')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
