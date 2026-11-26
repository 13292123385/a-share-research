# 2026-11-26 A股收盘复盘

状态：complete；抓取时间：2026-11-26T20:53:31.834291+08:00

采集范围：closing_snapshot；采集状态：complete；研究状态：available

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 62, "mainboard_height": 5.0, "first_board_candidates": 48, "all_day_one_word_excluded": 7, "one_word_unknown": 0, "broken_count": 23, "limit_down_count": 3, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-26T00:00:00.000", "open": 3490.14, "close": 3476.88, "high": 3497.81, "low": 3455.04, "amount": 454062959.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-26T00:00:00.000", "open": 10184.94, "close": 10084.04, "high": 10235.5, "low": 9979.06, "amount": 544733686.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-26T00:00:00.000", "open": 2213.12, "close": 2189.82, "high": 2227.41, "low": 2155.01, "amount": 157118489.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-26T00:00:00.000", "close": 2343.85, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{"market": {"up": 1766, "down": 3642, "flat": 173, "turnover_yuan": 1325986276222.0, "records": 5581, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 33, "promoted_count": 8, "broken_count": 1, "observation_rate": 0.24242424242424243, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 54, "prices_available": 54, "missing_archive_dates": [], "missing_price_codes": [], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-11-26", "status": "code_coverage_matched", "expected_count": 5581, "observed_count": 5581, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 619, "observed": 619, "missing_codes": []}, "sz": {"expected": 2905, "observed": 2905, "missing_codes": []}, "bj": {"expected": 357, "observed": 357, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "within_tolerance", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005, "official_yuan": 704757051884.1399, "snapshot_yuan": 704000544884.0, "relative_difference": 0.0010734294862568615}, "initial_missing_codes": [], "daily_supplement_codes": [], "archived_roster_sources": {"sh_main": "20261126T173601638300+0800/raw/official_roster_sh_main.json", "sh_star": "20261126T173601638300+0800/raw/official_roster_sh_star.json", "sz": "20261126T173601638300+0800/raw/official_roster_sz_retry1.json", "bj": "20261126T173601638300+0800/raw/official_roster_bj.json"}}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=65
- yesterday_pool: ok，行数=51
- broken: ok，行数=29
- limit_down: ok，行数=5
- official_szse_summary: error，行数=None
- official_szse_summary_retry: ok，行数=14
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
