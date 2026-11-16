# 2026-11-16 A股收盘复盘

状态：complete；抓取时间：2026-11-16T19:30:54.557243+08:00

采集范围：closing_snapshot；采集状态：complete；研究状态：available

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 30, "mainboard_height": 4.0, "first_board_candidates": 19, "all_day_one_word_excluded": 1, "one_word_unknown": 0, "broken_count": 16, "limit_down_count": 59, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-16T00:00:00.000", "open": 3611.54, "close": 3602.57, "high": 3623.12, "low": 3586.57, "amount": 461643487.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-16T00:00:00.000", "open": 10881.91, "close": 10690.78, "high": 10881.91, "low": 10642.37, "amount": 520171170.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-16T00:00:00.000", "open": 2395.52, "close": 2320.02, "high": 2398.19, "low": 2308.9, "amount": 152931711.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-16T00:00:00.000", "close": 2636.87, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{"market": {"up": 1136, "down": 4344, "flat": 99, "turnover_yuan": 1494156780853.0, "records": 5579, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 27, "promoted_count": 7, "broken_count": 2, "observation_rate": 0.25925925925925924, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 54, "prices_available": 54, "missing_archive_dates": [], "missing_price_codes": [], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-11-16", "status": "code_coverage_matched", "expected_count": 5579, "observed_count": 5579, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 619, "observed": 619, "missing_codes": []}, "sz": {"expected": 2905, "observed": 2905, "missing_codes": []}, "bj": {"expected": 355, "observed": 355, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "within_tolerance", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005, "official_yuan": 778677057191.89, "snapshot_yuan": 778218116846.0, "relative_difference": 0.0005893847027483662}, "initial_missing_codes": ["689009"], "daily_supplement_codes": ["689009"], "archived_roster_sources": {}}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=32
- yesterday_pool: ok，行数=36
- broken: ok，行数=16
- limit_down: ok，行数=60
- spot: error，行数=None
- spot_fallback: ok，行数=5578
- official_roster_sh_main: ok，行数=1700
- official_roster_sh_star: ok，行数=619
- official_roster_sz: error，行数=None
- official_roster_sz_retry1: ok，行数=2905
- official_roster_bj: ok，行数=355
- official_szse_summary: ok，行数=14
- market_quote_689009: ok，行数=1
- price_000573: ok，行数=1
- price_000595: ok，行数=1
- price_000665: ok，行数=1
- price_000766: ok，行数=1
- price_000819: ok，行数=1
- price_000995: ok，行数=1
- price_001358: ok，行数=1
- price_001393: ok，行数=1
- price_002021: ok，行数=1
- price_002042: ok，行数=1
- price_002086: ok，行数=1
- price_002124: ok，行数=1
- price_002172: ok，行数=1
- price_002187: ok，行数=1
- price_002205: ok，行数=1
- price_002425: ok，行数=1
- price_002520: ok，行数=1
- price_002548: ok，行数=1
- price_002628: ok，行数=1
- price_002685: ok，行数=1
- price_002693: ok，行数=1
- price_002696: ok，行数=1
- price_002739: ok，行数=1
- price_002748: ok，行数=1
- price_002819: ok，行数=1
- price_002853: ok，行数=1
- price_002905: ok，行数=1
- price_600410: ok，行数=1
- price_600467: ok，行数=1
- price_600558: ok，行数=1
- price_600569: ok，行数=1
- price_600651: ok，行数=1
- price_600715: ok，行数=1
- price_600802: ok，行数=1
- price_600853: ok，行数=1
- price_600857: ok，行数=1
- price_600977: ok，行数=1
- price_601091: ok，行数=1
- price_601188: ok，行数=1
- price_601566: ok，行数=1
- price_601606: ok，行数=1
- price_601929: ok，行数=1
- price_603103: ok，行数=1
- price_603166: ok，行数=1
- price_603175: ok，行数=1
- price_603286: ok，行数=1
- price_603636: ok，行数=1
- price_603686: ok，行数=1
- price_603767: ok，行数=1
- price_603928: ok，行数=1
- price_603958: ok，行数=1
- price_605169: ok，行数=1
- price_605222: ok，行数=1
- price_605318: ok，行数=1
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
