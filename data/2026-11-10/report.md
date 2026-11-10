# 2026-11-10 A股收盘复盘

状态：partial；抓取时间：2026-11-10T23:29:09.419160+08:00

采集范围：closing_snapshot；采集状态：partial；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 84, "mainboard_height": 7.0, "first_board_candidates": 64, "all_day_one_word_excluded": 3, "one_word_unknown": 0, "broken_count": 15, "limit_down_count": null, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-10", "open": 3682.04, "close": 3663.72, "high": 3683.73, "low": 3660.72, "volume": 404865177, "amount": 673951893240.3}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-10", "open": 11313.32, "close": 11241.54, "high": 11315.53, "low": 11217.01, "volume": 526862998, "amount": 830863077298.74}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-10", "open": 2518.44, "close": 2494.4, "high": 2520.01, "low": 2487.56, "volume": 180385788, "amount": 418447832760.79}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-10", "open": 2778.61, "close": 2804.56, "high": 2806.86, "low": 2777.91, "volume": 274072910, "amount": 332584539514.0}]}

## 估算值
{"market": {"up": 4273, "down": 1149, "flat": 158, "turnover_yuan": 1516745141638.0, "records": 5580, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 40, "promoted_count": 14, "broken_count": 2, "observation_rate": 0.35, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- limit_down:empty_unverified

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 60, "prices_available": 60, "missing_archive_dates": [], "missing_price_codes": [], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-11-10", "status": "code_coverage_matched", "expected_count": 5580, "observed_count": 5580, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 619, "observed": 619, "missing_codes": []}, "sz": {"expected": 2906, "observed": 2906, "missing_codes": []}, "bj": {"expected": 355, "observed": 355, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "within_tolerance", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005, "official_yuan": 831908668027.2, "snapshot_yuan": 830819945243.0, "relative_difference": 0.001308704700459203}, "initial_missing_codes": [], "daily_supplement_codes": [], "archived_roster_sources": {"sh_main": "20261110T175618142836+0800/raw/official_roster_sh_main.json", "sh_star": "20261110T175618142836+0800/raw/official_roster_sh_star.json", "sz": "20261110T175618142836+0800/raw/official_roster_sz_retry1.json", "bj": "20261110T175618142836+0800/raw/official_roster_bj.json"}}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=93
- yesterday_pool: ok，行数=55
- broken: ok，行数=19
- limit_down: empty_unverified，行数=0
- official_szse_summary: error，行数=None
- official_szse_summary_retry: ok，行数=14
- index_sh000001: ok，行数=1
- index_sz399001: ok，行数=1
- index_sz399006: ok，行数=1
- index_csi932000: ok，行数=1
