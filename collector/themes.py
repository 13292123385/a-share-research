"""Point-in-time concept snapshots. No current-to-historical constituent backfill."""
import re
import time
from .model import number


def collect_themes(c, target, today, budget, prior=()):
    if target != today:
        return [], [], [], 'historical_membership_unavailable'
    deadline = time.monotonic() + max(0, budget)
    original_timeout = c.timeout

    def call(key, function, **kwargs):
        remaining = deadline - time.monotonic() - c.delay
        if remaining <= 1:
            return None, 'budget_exhausted'
        c.timeout = min(original_timeout, 15, remaining)
        rows = c.call(key, function, **kwargs)
        return rows, 'available' if rows else c.calls[key]['status']

    try:
        raw, status = call('concept_catalog', 'stock_board_concept_name_em')
        if raw is None:
            return [], [], [], status
        ids = [str(r.get('板块代码', '')) for r in raw]
        if not raw or len(ids) != len(set(ids)) or any(not re.fullmatch(r'BK\d+', x) for x in ids) or any(not r.get('板块名称') for r in raw):
            return [], [], [], 'schema_error'
        catalog, members, coverage = [], [], []
        # Oldest successful membership first; repeated runs rotate instead of starving later IDs.
        last = {}
        for r in prior:
            if r.get('status') == 'available':
                last[r['theme_id']] = max(last.get(r['theme_id'], ''), r['observed_at'])
        for r in sorted(raw, key=lambda r: (last.get(r['板块代码'], ''), r['板块代码'])):
            ident, name = r['板块代码'], r.get('板块名称')
            stamp = c.calls['concept_catalog']['fetched_at']
            catalog.append(dict(theme_id=ident, name=name, observation_date=target,
                observed_at=stamp, source='AKShare / 东方财富',
                close=number(r.get('最新价')), change_pct=number(r.get('涨跌幅')),
                rising_count=number(r.get('上涨家数')), falling_count=number(r.get('下跌家数')),
                lifecycle_stage=None, stage_status='not_inferred'))
            rows, state = call('concept_members_' + ident, 'stock_board_concept_cons_em', symbol=ident)
            codes = [str(x.get('代码', '')) for x in rows or []]
            if rows and (len(codes) != len(set(codes)) or any(not re.fullmatch(r'\d{6}', x) for x in codes)):
                rows, state = None, 'schema_error'
            observed = c.calls.get('concept_members_' + ident, {}).get('fetched_at', stamp)
            coverage.append(dict(theme_id=ident, observation_date=target, observed_at=observed,
                                 status=state, member_count=len(rows) if rows else None))
            for member in rows or []:
                members.append(dict(theme_id=ident, code=member['代码'], name=member.get('名称'),
                    observation_date=target, observed_at=observed, source='AKShare / 东方财富',
                    mapping_kind='provider_concept_membership', historical_valid_from=None,
                    note='仅证明抓取时接口归属，不证明历史归属或题材龙头'))
        return catalog, members, coverage, 'available' if all(r['status'] == 'available' for r in coverage) else 'partial'
    finally:
        c.timeout = original_timeout
