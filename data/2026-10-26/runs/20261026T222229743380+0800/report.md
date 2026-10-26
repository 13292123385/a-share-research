# 2026-10-26 A股收盘复盘

状态：complete_with_limitations；抓取时间：2026-10-26T22:22:29.743380+08:00

采集范围：closing_snapshot；采集状态：complete；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 47, "mainboard_height": 4.0, "first_board_candidates": 33, "all_day_one_word_excluded": 2, "one_word_unknown": 0, "broken_count": 18, "limit_down_count": 25, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-10-26T00:00:00.000", "open": 3671.0, "close": 3697.52, "high": 3699.01, "low": 3664.82, "amount": 432794318.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-10-26T00:00:00.000", "open": 11560.36, "close": 11534.38, "high": 11638.79, "low": 11432.29, "amount": 542597712.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-10-26T00:00:00.000", "open": 2645.74, "close": 2638.23, "high": 2671.81, "low": 2601.09, "amount": 177585733.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-10-26T00:00:00.000", "close": 2818.98, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{"market": {"up": 2252, "down": 3157, "flat": 168, "turnover_yuan": 1623091874110.0, "records": 5577, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 52, "promoted_count": 8, "broken_count": 7, "observation_rate": 0.15384615384615385, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 首板后续跟踪存在历史名单或价格缺失，详见followup

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 53, "prices_available": 53, "missing_archive_dates": ["2026-10-22"], "missing_price_codes": [], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-10-26", "status": "code_coverage_matched", "expected_count": 5577, "observed_count": 5577, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 618, "observed": 618, "missing_codes": []}, "sz": {"expected": 2906, "observed": 2906, "missing_codes": []}, "bj": {"expected": 353, "observed": 353, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "within_tolerance", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005, "official_yuan": 862966322223.53, "snapshot_yuan": 862232973771.0, "relative_difference": 0.0008497996198049471}, "initial_missing_codes": ["689009"], "daily_supplement_codes": ["689009"]}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=55
- yesterday_pool: ok，行数=82
- broken: ok，行数=23
- limit_down: ok，行数=26
- spot: error，行数=None
- spot_fallback: ok，行数=5576
- official_roster_sh_main: ok，行数=1700
- official_roster_sh_star: ok，行数=618
- official_roster_sz: error，行数=None
- official_roster_sz_retry1: ok，行数=2906
- official_roster_bj: ok，行数=353
- official_szse_summary: ok，行数=14
- market_quote_689009: ok，行数=1
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
