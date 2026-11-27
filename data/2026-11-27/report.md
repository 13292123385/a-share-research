# 2026-11-27 A股收盘复盘

状态：partial；抓取时间：2026-11-27T21:33:48.703164+08:00

采集范围：closing_snapshot；采集状态：partial；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 314, "mainboard_height": 6.0, "first_board_candidates": 286, "all_day_one_word_excluded": 5, "one_word_unknown": 0, "broken_count": 34, "limit_down_count": null, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-27T00:00:00.000", "open": 3482.38, "close": 3606.49, "high": 3610.72, "low": 3467.41, "amount": 634626966.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-27T00:00:00.000", "open": 10121.14, "close": 10814.02, "high": 10814.19, "low": 10075.83, "amount": 761605757.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-27T00:00:00.000", "open": 2202.82, "close": 2443.96, "high": 2444.6, "low": 2199.23, "amount": 237230124.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-27T00:00:00.000", "close": 2531.8, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{"market": {"up": 5382, "down": 181, "flat": 18, "turnover_yuan": 2017282183341.0, "records": 5581, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 41, "promoted_count": 17, "broken_count": 1, "observation_rate": 0.4146341463414634, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- limit_down:empty_unverified

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 81, "prices_available": 81, "missing_archive_dates": [], "missing_price_codes": [], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-11-27", "status": "code_coverage_matched", "expected_count": 5581, "observed_count": 5581, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 619, "observed": 619, "missing_codes": []}, "sz": {"expected": 2905, "observed": 2905, "missing_codes": []}, "bj": {"expected": 357, "observed": 357, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "within_tolerance", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005, "official_yuan": 1071217402973.8599, "snapshot_yuan": 1069947430881.0, "relative_difference": 0.0011855409455953857}, "initial_missing_codes": [], "daily_supplement_codes": [], "archived_roster_sources": {"sh_main": "20261127T203153827336+0800/raw/official_roster_sh_main.json", "sh_star": "20261127T203153827336+0800/raw/official_roster_sh_star.json", "sz": "20261127T203153827336+0800/raw/official_roster_sz.json", "bj": "20261127T203153827336+0800/raw/official_roster_bj.json"}}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=417
- yesterday_pool: ok，行数=65
- broken: ok，行数=42
- limit_down: empty_unverified，行数=0
- official_szse_summary: error，行数=None
- official_szse_summary_retry: ok，行数=14
- price_603166: ok，行数=1
- price_603203: ok，行数=1
- price_603278: ok，行数=1
- price_603324: ok，行数=1
- price_603373: ok，行数=1
- price_603386: ok，行数=1
- price_603396: ok，行数=1
- price_603586: ok，行数=1
- price_603687: ok，行数=1
- price_603703: ok，行数=1
- price_603708: ok，行数=1
- price_603887: ok，行数=1
- price_605058: ok，行数=1
- price_605136: ok，行数=1
- price_605577: ok，行数=1
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
