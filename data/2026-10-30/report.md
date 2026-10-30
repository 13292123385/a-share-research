# 2026-10-30 A股收盘复盘

状态：complete；抓取时间：2026-10-30T23:05:31.583721+08:00

采集范围：closing_snapshot；采集状态：complete；研究状态：available

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 42, "mainboard_height": 5.0, "first_board_candidates": 33, "all_day_one_word_excluded": 3, "one_word_unknown": 0, "broken_count": 24, "limit_down_count": 82, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-10-30T00:00:00.000", "open": 3605.65, "close": 3599.02, "high": 3660.21, "low": 3595.26, "amount": 497973940.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-10-30T00:00:00.000", "open": 10871.13, "close": 10833.78, "high": 11171.58, "low": 10833.78, "amount": 608472237.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-10-30T00:00:00.000", "open": 2434.8, "close": 2413.63, "high": 2518.24, "low": 2413.63, "amount": 194139714.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-10-30T00:00:00.000", "close": 2616.74, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{"market": {"up": 893, "down": 4602, "flat": 82, "turnover_yuan": 1687710165206.0, "records": 5577, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 26, "promoted_count": 4, "broken_count": 2, "observation_rate": 0.15384615384615385, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 78, "prices_available": 78, "missing_archive_dates": [], "missing_price_codes": [], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-10-30", "status": "code_coverage_matched", "expected_count": 5577, "observed_count": 5577, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 618, "observed": 618, "missing_codes": []}, "sz": {"expected": 2905, "observed": 2905, "missing_codes": []}, "bj": {"expected": 354, "observed": 354, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "within_tolerance", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005, "official_yuan": 910829563860.88, "snapshot_yuan": 910159774864.0, "relative_difference": 0.0007353615028050499}, "initial_missing_codes": ["689009"], "daily_supplement_codes": ["689009"]}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=47
- yesterday_pool: ok，行数=39
- broken: ok，行数=31
- limit_down: ok，行数=82
- spot: error，行数=None
- spot_fallback: ok，行数=5576
- official_roster_sh_main: ok，行数=1700
- official_roster_sh_star: ok，行数=618
- official_roster_sz: error，行数=None
- official_roster_sz_retry1: ok，行数=2905
- official_roster_bj: ok，行数=354
- official_szse_summary: ok，行数=14
- market_quote_689009: ok，行数=1
- price_603667: ok，行数=1
- price_603680: ok，行数=1
- price_603703: ok，行数=1
- price_603868: ok，行数=1
- price_603897: ok，行数=1
- price_603920: ok，行数=1
- price_603926: ok，行数=1
- price_603992: ok，行数=1
- price_605060: ok，行数=1
- price_605179: ok，行数=1
- price_605288: ok，行数=1
- price_605338: ok，行数=1
- price_605366: ok，行数=1
- price_605566: ok，行数=1
- price_605598: ok，行数=1
- index_sh000001: error，行数=None
- index_retry_sh000001: error，行数=None
- index_fallback_sh000001: ok，行数=1
- index_sz399001: error，行数=None
- index_retry_sz399001: error，行数=None
- index_fallback_sz399001: ok，行数=1
- index_sz399006: error，行数=None
- index_retry_sz399006: error，行数=None
- index_fallback_sz399006: ok，行数=1
- index_csi932000: error，行数=None
- index_retry_csi932000: error，行数=None
- index_official_csi932000: ok，行数=1
