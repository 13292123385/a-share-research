"""Allowlisted V2 research publication, isolated from daily and lifecycle feeds."""
import argparse
import base64
import hashlib
import json
import os
import re
from datetime import date
from pathlib import Path

import requests

from .v2_validate import read, validate_run

NAMESPACE = 'research-v2/'
FILENAMES = {'latest.json', 'latest.md', 'state.json', 'cores.json', 'coverage.json'}
COVERAGE_FIELDS = (
    'window_start', 'window_end', 'requested_trading_days', 'dated_review_days',
    'complete_historical_membership_days', 'archived_market_quote_days',
    'verified_full_market_ohlcv_days', 'selected_limit_pool_days',
    'independent_pool_code_matches', 'observed_stock_days', 'observed_themes_scanned',
    'ranked_resonant_themes', 'core_price_stocks', 'core_price_eligible_stocks', 'price_budget_truncated_stocks', 'core_price_valid_rows',
    'core_price_requested_rows', 'reused_lifecycle_unadjusted_rows', 'minute_data_verified_stocks',
    'business_links_verified', 'catalysts_verified', 'observed_focus_stocks',
    'formal_full_market_rank_available',
)
QUALITY_COUNTS = (
    'dated_review_days', 'complete_historical_membership_days',
    'archived_market_quote_days', 'verified_full_market_ohlcv_days',
    'selected_limit_pool_days', 'core_price_valid_rows',
    'minute_data_verified_stocks', 'business_links_verified', 'catalysts_verified',
)


def pick(value, fields):
    return {key: value[key] for key in fields if key in value}


def _state(value):
    result = pick(value, ('target_date',))
    result['seats'] = pick(value.get('seats', {}), ('A', 'B', 'C'))
    pending = value.get('pending')
    result['pending'] = pick(pending, ('challenger', 'incumbent', 'sessions',
        'observed_date', 'score_gap', 'required_margin', 'required_sessions')) if pending else None
    result['policy'] = pick(value.get('policy', {}), ('swap_margin', 'swap_confirm_sessions'))
    return result


def _seat(value):
    if value is None:
        return None
    result = pick(value, ('theme_id', 'theme_name', 'as_of', 'rank', 'composite_score',
        'activity_score', 'full_score', 'score_kind', 'seat_status',
        'recent_active_days', 'last_active_date', 'new_hotspot', 'catalyst_verified',
        'weight_coverage', 'common_windows', 'omitted_windows', 'composite_interval',
        'configured_weights', 'effective_weights', 'scope', 'missing'))
    result['windows'] = {str(k): pick(v, ('score', 'activity_score', 'full_score',
        'score_kind', 'coverage', 'requested_sessions', 'observed_sessions'))
        for k, v in value.get('windows', {}).items() if str(k) in ('5', '10', '20', '40')}
    for field in ('configured_weights', 'effective_weights'):
        if field in result:
            result[field] = pick(result[field], ('5', '10', '20', '40'))
    return result


def _core(value):
    result = pick(value, ('code', 'name', 'theme_id', 'observation_date', 'seat',
        'roles', 'role_status', 'selection_scope', 'mapping_confidence', 'round_start',
        'round_baseline_date', 'round_start_basis', 'round_start_left_censored', 'round_identity_verified', 'round_start_kind',
        'round_return_pct', 'return_5d_pct', 'return_1d_pct',
        'raw_round_price_change_pct', 'raw_price_change_5d_pct', 'adjustment',
        'return_kind', 'drawdown_pct', 'drawdown_kind', 'lifecycle_stage',
        'current_height', 'max_height', 'relative_strength_5d_pct',
        'relative_strength_unit', 'leadership_status', 'recent_strong_signal_dates',
        'current_limit_up', 'all_day_one_word', 'first_seal', 'last_close',
        'status_lost_conditions', 'risks', 'execution_verified', 'entry_price', 'actual_return'))
    result['role_evidence'] = {role: pick(item, ('basis', 'sample_size', 'observation_date', 'scope'))
        for role, item in value.get('role_evidence', {}).items()
        if role in ('涨幅王', '带动王', '爆发王') and isinstance(item, dict)}
    return result


def _trading(value):
    result = pick(value, ('observation_count', 'max_observations',
        'max_planned_positions', 'actual_positions', 'actual_return', 'note'))
    fields = ('code', 'name', 'patterns', 'status', 'entry_price', 'execution_verified',
              'entry_condition', 'invalidation_condition', 'estimated_adverse_move_pct')
    result['candidates'] = [pick(r, fields) for r in value.get('candidates', [])]
    result['research_setups'] = [pick(r, fields) for r in value.get('research_setups', [])]
    result['blocked'] = [pick(r, ('code', 'reasons')) for r in value.get('blocked', [])]
    return result


def _change(value):
    result = pick(value, ('kind', 'seat', 'previous', 'current', 'reason', 'code', 'name', 'roles', 'theme_id'))
    if isinstance(value.get('evidence'), dict):
        result['evidence'] = pick(value['evidence'], ('challenger', 'incumbent', 'sessions',
            'observed_date', 'score_gap', 'required_margin', 'required_sessions'))
    return result


def _coverage(report, inputs):
    summary = pick(report['coverage'], COVERAGE_FIELDS)
    result = dict(summary=summary,
        review_days=[pick(r, ('date', 'status', 'rows', 'mapping_scope')) for r in inputs['review_coverage']],
        market_days=[pick(r, ('date', 'status', 'market_quote_rows', 'mainboard_quote_rows',
            'market_code_coverage', 'all_market_verified')) for r in inputs['market_coverage']],
        price_stocks=[pick(r, ('code', 'status', 'requested_sessions', 'valid_sessions',
            'missing_dates', 'amount_rows', 'turnover_rows')) for r in inputs['price_coverage']])
    keys = {'review:' + r['date'] for r in inputs['review_coverage'] if r['status'] == 'available'}
    keys.update('selected:' + r['date'] for r in inputs['selected_inputs'])
    keys.update('market:' + r['date'] for r in inputs['market_coverage'] if r.get('mainboard_quote_rows', 0) > 0)
    keys.update('price:' + r['code'] + ':' + r['date'] + ':' + r.get('adjustment', 'unknown') for r in inputs['prices'])
    keys.update('price:' + r['code'] + ':' + r['date'] + ':' + r.get('adjustment', 'unknown') + ':' + field
        for r in inputs['prices'] for field in ('volume', 'amount', 'turnover_rate') if r.get(field) is not None)
    keys.update('association:' + r['date'] + ':' + r['code'] + ':' + theme
        for r in inputs.get('observations', []) for theme in r.get('theme_ids', []))
    result['coverage_keys'] = sorted(keys)
    return result


def _markdown(payload):
    def fmt(value):
        return '未知' if value is None else f'{value:.2f}' if isinstance(value, (int, float)) else str(value)
    lines = [f'# 题材与核心股 V2｜{payload["trade_date"]}', '',
        '普通沪深主板非ST；当前发布为研究观察。先检查日期、数据范围与缺失。',
        '分数为0–100的样本观察活跃度，按5/10/20/40日加权；完整历史成分与正式市场强度仍缺失。',
        '部分活跃股关联不能证明全市场最强；价格涨幅不是可成交策略收益。', '']
    for seat, title in (('A', '最强主线'), ('B', '最强挑战者'), ('C', '新晋热点')):
        row = payload['selection']['seats'][seat]
        lines += [f'## {title} {seat}', '']
        if row is None:
            lines += ['空缺：现有证据不足。', '']
            continue
        windows = row.get('windows', {})
        scores = '｜'.join(f'{k}日 {fmt(windows.get(k, {}).get("score"))}' for k in ('5', '10', '20', '40'))
        lines += [f'{row.get("theme_name", row["theme_id"])}｜{scores}｜综合 {fmt(row.get("composite_score"))}',
            f'最近5日活跃 {row.get("recent_active_days", "未知")}日；观察排名 {row.get("rank", "未知")}。', '']
        if seat == 'B':
            lines += [f'与A分差（A−B）：{fmt(payload["selection"].get("challenger_gap"))}；换位须通过持续确认。', '']
            pending = payload['selection']['state'].get('pending')
            if pending:
                lines += [f'换位确认 {pending.get("sessions")}/{pending.get("required_sessions")}日；'
                          f'领先要求 {pending.get("required_margin")}分。', '']
        cores = payload['core_by_theme'].get(row['theme_id'], [])
        for core in cores:
            height = core.get('current_height')
            height_text = f'{height:g}板' if isinstance(height, (int, float)) else '断板/未封板' if core.get('current_limit_up') is False else '未知'
            lines += [f'- **{core["name"]} {core["code"]}｜{"、".join(core.get("roles", []))}**：'
                f'观察轮 {fmt(core.get("round_return_pct"))}%；5日 {fmt(core.get("return_5d_pct"))}%；'
                f'当前回撤 {fmt(core.get("drawdown_pct"))}%；{core.get("lifecycle_stage", "未知")}。'
                f'当前{height_text}，窗口最高{fmt(core.get("max_height"))}板；'
                f'观察段起点{core.get("round_start") or "未知"}；相对市场5日强度{fmt(core.get("relative_strength_5d_pct"))}。']
            bases = [r['basis'] for r in core.get('role_evidence', {}).values() if r.get('basis')]
            if bases:
                lines += ['  依据：' + '；'.join(dict.fromkeys(bases)) + '。']
            if core.get('all_day_one_word') is True:
                lines += ['  风险：当日全天一字板，排队成交未验证。']
            if core.get('risks'):
                lines += ['  风险：' + '；'.join(core['risks'][:2]) + '。']
            if core.get('status_lost_conditions'):
                lines += ['  失位条件：' + '；'.join(core['status_lost_conditions']) + '。']
        if not cores:
            lines += ['- 核心股空缺。']
        if not any('带动王' in r.get('roles', []) for r in cores):
            lines += ['- 带动王：待确认。']
        lines += ['']
    lines += ['## 每日变化', '']
    if not payload['changes']:
        lines += ['- 无可验证变化。']
    for change in payload['changes']:
        if change['kind'] == 'seat_changed':
            lines += [f'- 席位 {change.get("seat")}：{change.get("previous") or "空缺"} → {change.get("current") or "空缺"}。']
        elif change['kind'] == 'mainline_swapped':
            proof = change.get('evidence', {})
            lines += [f'- 正式主线换位：{proof.get("incumbent")} → {proof.get("challenger")}；'
                      f'领先 {proof.get("score_gap")}分，已确认 {proof.get("sessions")}个相邻交易日。']
        elif change['kind'] in ('new_core', 'initial_core_observation'):
            label = '新晋核心' if change['kind'] == 'new_core' else '首次记录核心'
            lines += [f'- {label}：{change.get("name", "")} {change.get("code", "")}｜' + '、'.join(change.get('roles', [])) + '。']
        elif change['kind'] == 'core_role_change':
            lines += [f'- {change.get("theme_id", "")} {change.get("code")}角色：' + '、'.join(change.get('previous', [])) + ' → ' + '、'.join(change.get('current', [])) + '。']
        elif change['kind'] == 'removed_from_focus_pool':
            lines += [f'- 移出重点池：{change.get("code")}；当日席位或角色证据未达要求。']
        elif change['kind'] == 'challenger_pending':
            lines += ['- 挑战者领先正在持续确认，尚未正式换位。']
    lines += ['']
    lines += ['## 实盘研究', '', f'符合已验证条件的候选 {len(payload["trading"]["candidates"])}只；持仓计划最多4只。',
        '观察池最多9只；一字板排队成交、次日入场与T+1退出需分别验证。', '', '## 数据覆盖与缺失', '']
    summary = payload['coverage']
    lines += [f'- 日期复盘 {summary.get("dated_review_days", 0)}/40；完整历史题材成分 {summary.get("complete_historical_membership_days", 0)}/40。',
        f'- 已存全市场行情 {summary.get("archived_market_quote_days", 0)}/40；全部字段独立验证 {summary.get("verified_full_market_ohlcv_days", 0)}/40。',
        f'- 重点股价格 {summary.get("core_price_valid_rows", 0)}/{summary.get("core_price_requested_rows", 0)}条；内部候选 {summary.get("core_price_stocks", 0)}/{summary.get("core_price_eligible_stocks", 0)}只已请求；输出观察 {summary.get("observed_focus_stocks", 0)}只。']
    lines += ['- ' + r for r in payload['missing_data']]
    return '\n'.join(lines) + '\n'


def make_files(run):
    run = Path(run)
    errors = validate_run(run)
    if errors:
        raise ValueError('V2 public quality failed: ' + ';'.join(errors))
    report, summary, inputs = read(run / 'report.json'), read(run / 'summary.json'), read(run / 'analysis_inputs.json')
    if summary['trade_date'] != report['trade_date'] or summary['run_id'] != run.name:
        raise ValueError('V2 public run identity mismatch')
    state = _state(report['selection']['state'])
    cores = {ident: [_core(r) for r in values] for ident, values in report['core_by_theme'].items()}
    coverage = _coverage(report, inputs)
    selection = dict(seats={k: _seat(report['selection']['seats'].get(k)) for k in ('A', 'B', 'C')},
        challenger_gap=report['selection'].get('challenger_gap'), state=state)
    changes = [_change(r) for r in report.get('changes', [])]
    payload = dict(schema_version=1, trade_date=report['trade_date'], run_id=summary['run_id'],
        status=report['status'], ranking_scope=report['ranking_scope'], selection=selection,
        core_by_theme=cores, coverage=coverage['summary'], missing_data=report['missing_data'],
        changes=changes, trading=_trading(report['trading']), return_kind=report.get('return_kind'))
    values = {'latest.json': payload, 'state.json': state, 'cores.json': cores, 'coverage.json': coverage}
    files = {name: json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) for name, value in values.items()}
    files['latest.md'] = _markdown(payload)
    return files


def blob_sha(text):
    payload = text.encode('utf-8')
    return hashlib.sha1(b'blob ' + str(len(payload)).encode('ascii') + b'\0' + payload).hexdigest()


def _not_worse(current, previous):
    if not set(previous.get('coverage_keys', [])).issubset(current.get('coverage_keys', [])):
        return False
    for key in QUALITY_COUNTS:
        old, new = previous.get('summary', {}).get(key), current.get('summary', {}).get(key)
        if isinstance(old, (int, float)) and not isinstance(old, bool):
            if not isinstance(new, (int, float)) or isinstance(new, bool) or new < old:
                return False
    return True


def publish(files, repository, token):
    if not repository or not token:
        raise ValueError('V2 public publishing configuration missing')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+', repository) or \
            repository.split('/')[-1] in ('.', '..') or set(files) != FILENAMES:
        raise ValueError('invalid V2 public repository or file allowlist')
    payload = json.loads(files['latest.json'])
    day, run_id = payload['trade_date'], payload['run_id']
    if date.fromisoformat(day).isoformat() != day or not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]*', run_id):
        raise ValueError('unsafe V2 public archive identity')
    coverage = json.loads(files['coverage.json'])
    archive = NAMESPACE + 'archive/' + day + '/' + run_id + '/'
    session = requests.Session()
    session.headers.update({'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json'})
    base = 'https://api.github.com/repos/' + repository

    def api(path, method='GET', body=None):
        response = session.request(method, base + path, json=body, timeout=45)
        if not response.ok:
            raise RuntimeError('V2 public API HTTP ' + str(response.status_code))
        return response.json()

    def content(path, head):
        response = session.get(base + '/contents/' + path, params={'ref': head}, timeout=45)
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise RuntimeError('cannot verify V2 public content HTTP ' + str(response.status_code))
        value = response.json()
        if isinstance(value, list):
            return value
        if value.get('encoding') == 'none' or (not value.get('content') and value.get('sha')):
            # Contents API omits base64 for files above 1MB. Stay on this repo's
            # authenticated API endpoint, rather than following a remote git_url.
            value = api('/git/blobs/' + value['sha'])
            if value.get('encoding') != 'base64':
                raise ValueError('unsupported V2 public blob encoding')
        return json.loads(base64.b64decode(value['content']))

    for attempt in range(3):
        head = api('/git/ref/heads/main')['object']['sha']
        previous = api('/git/commits/' + head)
        prior = content(NAMESPACE + 'latest.json', head)
        promote = prior is None or day > prior['trade_date']
        if prior is not None and day == prior['trade_date']:
            prior_coverage = content(NAMESPACE + 'coverage.json', head)
            promote = prior_coverage is not None and _not_worse(coverage, prior_coverage)
        existing = content(archive[:-1], head)
        if existing is not None:
            expected = {name: blob_sha(value) for name, value in files.items()}
            actual = {r['name']: r['sha'] for r in existing if r.get('type') == 'file'} if isinstance(existing, list) else {}
            if actual == expected and len(existing) == len(expected):
                return dict(published=False, already_archived=True, promoted=False, archive=archive)
            raise ValueError('immutable V2 public archive conflict')
        exported = {archive + name: value for name, value in files.items()}
        if promote:
            exported.update({NAMESPACE + name: value for name, value in files.items()})
        tree = api('/git/trees', 'POST', {'base_tree': previous['tree']['sha'], 'tree': [
            dict(path=name, mode='100644', type='blob', content=value) for name, value in exported.items()]})
        commit = api('/git/commits', 'POST', {'message': 'data: archive isolated V2 research',
            'tree': tree['sha'], 'parents': [head]})
        response = session.patch(base + '/git/refs/heads/main',
            json={'sha': commit['sha'], 'force': False}, timeout=45)
        if response.ok:
            return dict(published=True, already_archived=False, promoted=promote, archive=archive)
        if response.status_code not in (409, 422):
            raise RuntimeError('V2 public ref HTTP ' + str(response.status_code))
    raise RuntimeError('public repository changed during three V2 publish attempts')


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('run')
    parser.add_argument('--output', default='v2-public')
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args(argv)
    files = make_files(args.run)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    for name, value in files.items():
        (output / name).write_text(value, encoding='utf-8', newline='')
    if args.publish:
        print(json.dumps(publish(files, os.environ.get('PUBLIC_FEED_REPOSITORY'),
            os.environ.get('PUBLIC_FEED_TOKEN')), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
