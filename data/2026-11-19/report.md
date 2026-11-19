# 2026-11-19 A股收盘复盘

状态：complete；抓取时间：2026-11-19T21:18:22.039668+08:00

采集范围：closing_snapshot；采集状态：complete；研究状态：available

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 22, "mainboard_height": 3.0, "first_board_candidates": 17, "all_day_one_word_excluded": 3, "one_word_unknown": 0, "broken_count": 20, "limit_down_count": 67, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-19T00:00:00.000", "open": 3583.12, "close": 3577.62, "high": 3584.28, "low": 3547.94, "amount": 412912755.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-19T00:00:00.000", "open": 10591.73, "close": 10583.2, "high": 10664.29, "low": 10505.84, "amount": 491464197.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-19T00:00:00.000", "open": 2290.21, "close": 2293.34, "high": 2315.78, "low": 2271.99, "amount": 139991626.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-19T00:00:00.000", "close": 2485.11, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{"market": {"up": 649, "down": 4876, "flat": 55, "turnover_yuan": 1314579174221.0, "records": 5580, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 27, "promoted_count": 2, "broken_count": 3, "observation_rate": 0.07407407407407407, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 53, "prices_available": 53, "missing_archive_dates": [], "missing_price_codes": [], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-11-19", "status": "code_coverage_matched", "expected_count": 5580, "observed_count": 5580, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 619, "observed": 619, "missing_codes": []}, "sz": {"expected": 2905, "observed": 2905, "missing_codes": []}, "bj": {"expected": 356, "observed": 356, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "within_tolerance", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005, "official_yuan": 668689192249.19, "snapshot_yuan": 668191613788.0, "relative_difference": 0.0007441102188541379}, "initial_missing_codes": ["689009"], "daily_supplement_codes": ["689009"], "archived_roster_sources": {}}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=23
- yesterday_pool: ok，行数=42
- broken: ok，行数=24
- limit_down: ok，行数=68
- spot: error，行数=None
- spot_fallback: ok，行数=5579
- official_roster_sh_main: ok，行数=1700
- official_roster_sh_star: ok，行数=619
- official_roster_sz: ok，行数=2905
- official_roster_bj: ok，行数=356
- official_szse_summary: ok，行数=14
- market_quote_689009: ok，行数=1
- price_000158: ok，行数=1
- price_000410: ok，行数=1
- price_000707: ok，行数=1
- price_000711: ok，行数=1
- price_000815: ok，行数=1
- price_000889: ok，行数=1
- price_000980: ok，行数=1
- price_002042: ok，行数=1
- price_002148: ok，行数=1
- price_002194: ok，行数=1
- price_002197: ok，行数=1
- price_002226: ok，行数=1
- price_002242: ok，行数=1
- price_002272: ok，行数=1
- price_002403: ok，行数=1
- price_002451: ok，行数=1
- price_002463: ok，行数=1
- price_002535: ok，行数=1
- price_002584: ok，行数=1
- price_002652: ok，行数=1
- price_002771: ok，行数=1
- price_002843: ok，行数=1
- price_002855: ok，行数=1
- price_002889: ok，行数=1
- price_002912: ok，行数=1
- price_002916: ok，行数=1
- price_002929: ok，行数=1
- price_002955: ok，行数=1
- price_002983: ok，行数=1
- price_600156: ok，行数=1
- price_600162: ok，行数=1
- price_600186: ok，行数=1
- price_600202: ok，行数=1
- price_600206: ok，行数=1
- price_600261: ok，行数=1
- price_600336: ok，行数=1
- price_600405: ok，行数=1
- price_600410: ok，行数=1
- price_600467: ok，行数=1
- price_600619: ok，行数=1
- price_600839: ok，行数=1
- price_600881: ok，行数=1
- price_603030: ok，行数=1
- price_603078: ok，行数=1
- price_603206: ok，行数=1
- price_603220: ok，行数=1
- price_603297: ok，行数=1
- price_603324: ok，行数=1
- price_603629: ok，行数=1
- price_603657: ok，行数=1
- price_603887: ok，行数=1
- price_603931: ok，行数=1
- price_603985: ok，行数=1
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
