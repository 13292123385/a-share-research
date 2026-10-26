"""Per-file record counts, nullable fields, provenance and byte checksums."""
import csv
import hashlib
import json
from pathlib import Path


def inventory(root, sources):
    root = Path(root)
    files = []
    successful = [k for k, v in sources.items() if v.get('status') == 'ok']
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.name in ('files.json', 'files.md'):
            continue
        rel = path.relative_to(root).as_posix()
        rows = None
        if path.suffix == '.json':
            value = json.loads(path.read_text(encoding='utf-8'))
            rows = value if isinstance(value, list) else [value]
        elif path.suffix == '.csv':
            with path.open(encoding='utf-8-sig', newline='') as f:
                rows = list(csv.DictReader(f))
        nulls = {}
        keys = sorted({k for r in (rows or []) if isinstance(r, dict) for k in r})
        for key in keys:
            count = sum(r.get(key) is None or r.get(key) == '' for r in rows if isinstance(r, dict))
            if count:
                nulls[key] = count
        raw_key = path.stem if path.parent.name == 'raw' else None
        refs = [raw_key] if raw_key in sources else successful
        if path.parent.name == 'clean':
            if path.stem in ('limit_up', 'first_board_candidates'):
                refs = [k for k in successful if k == 'limit_up' or k.startswith(('price_', 'spot', 'market_quote_', 'market_supplement_'))]
            elif path.stem in ('broken', 'limit_down', 'yesterday_pool'):
                refs = [k for k in successful if k == path.stem]
            elif path.stem == 'indices':
                refs = [k for k in successful if k.startswith('index_')]
            elif path.stem in ('candidate_prices', 'followup_prices', 'first_board_followup'):
                refs = [k for k in successful if k.startswith(('price_', 'spot', 'market_quote_', 'market_supplement_'))]
            elif path.stem == 'market_quotes':
                refs = [k for k in successful if k.startswith(('spot', 'market_quote_', 'market_supplement_'))]
        origins = sorted({r['origin_run'] for r in (rows or []) if isinstance(r, dict) and r.get('origin_run')})
        files.append(dict(path=rel, records=len(rows) if rows is not None else None,
            bytes=path.stat().st_size, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            fields=keys, missing_fields=nulls, source_refs=refs, origin_runs=origins,
            provenance='raw provider adapter result; see sources.json' if raw_key else
                       'derived; reused prices carry origin_run; research-only nulls are intentional'))
    (root / 'files.json').write_text(json.dumps(files, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# 文件清单', '', '| 路径 | 记录数 | 缺失字段（数量） |', '|---|---:|---|']
    lines += [f'| {r["path"]} | {r["records"] if r["records"] is not None else "—"} | '
              + (', '.join(f'{k}:{v}' for k, v in r['missing_fields'].items()) or '无') + ' |' for r in files]
    lines += ['', '来源及原始接口参数见 files.json 的 source_refs 与 sources.json；原始失败不视为空行情。',
              'entry_price、third_day_return、max_adverse_excursion等未验证成交字段有意保留为空。', '']
    (root / 'files.md').write_text('\n'.join(lines), encoding='utf-8', newline='\n')
    return files


def classify(summary, historical, pool_keys=('limit_up', 'yesterday_pool', 'broken', 'limit_down')):
    """Collection success is separate from unavailable research dependencies."""
    v = summary['verified']
    failures = []
    source_failures = summary.get('source_failures', {})
    failures.extend(k for k in pool_keys if k in source_failures)
    if v.get('mainboard_limit_up_count') is None:
        failures.append('limit_up')
    if len(v.get('indices', [])) != 4:
        failures.append('indices')
    if summary.get('candidate_price_quality', {}).get('missing_codes'):
        failures.append('candidate_prices')
    if not historical:
        market = summary.get('estimates', {}).get('market')
        if not market or market.get('unknown_direction', 0) or market.get('unknown_amount', 0):
            failures.append('market_snapshot')
        check = summary.get('market_reconciliation', {})
        if check.get('status') != 'code_coverage_matched':
            failures.append('market_coverage')
        if check.get('szse_turnover_check', {}).get('status') != 'within_tolerance':
            failures.append('market_turnover')
    summary['collection_scope'] = 'historical_pools_candidate_prices_indices' if historical else 'closing_snapshot'
    summary['collection_status'] = 'partial' if failures else 'complete'
    summary['collection_failures'] = sorted(set(failures))
    summary['research_status'] = 'limited' if summary['missing_data'] else 'available'
    summary['status'] = ('partial' if failures else
                         'complete_with_limitations' if summary['missing_data'] else 'complete')
