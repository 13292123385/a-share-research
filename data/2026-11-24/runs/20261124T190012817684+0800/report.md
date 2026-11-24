# 2026-11-24 A股收盘复盘

状态：complete_with_limitations；抓取时间：2026-11-24T19:00:12.817684+08:00

采集范围：closing_snapshot；采集状态：complete；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 47, "mainboard_height": 4.0, "first_board_candidates": 21, "all_day_one_word_excluded": 10, "one_word_unknown": 0, "broken_count": 57, "limit_down_count": 2, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-24T00:00:00.000", "open": 3567.84, "close": 3548.37, "high": 3585.22, "low": 3539.01, "amount": 493526296.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-24T00:00:00.000", "open": 10708.62, "close": 10423.6, "high": 10729.13, "low": 10418.11, "amount": 590663196.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-24T00:00:00.000", "open": 2368.7, "close": 2278.99, "high": 2376.34, "low": 2278.99, "amount": 183501191.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-24T00:00:00.000", "close": 2449.61, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{"market": {"up": 1952, "down": 3498, "flat": 131, "turnover_yuan": 1667800445242.0, "records": 5581, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 95, "promoted_count": 14, "broken_count": 19, "observation_rate": 0.14736842105263157, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 首板后续跟踪存在历史名单或价格缺失，详见followup

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 124, "prices_available": 69, "missing_archive_dates": [], "missing_price_codes": ["600371", "600467", "600814", "600838", "600980", "601177", "601188", "601595", "601599", "601689", "603004", "603009", "603037", "603040", "603048", "603051", "603103", "603119", "603127", "603131", "603151", "603166", "603175", "603179", "603236", "603278", "603283", "603286", "603305", "603337", "603386", "603466", "603516", "603528", "603533", "603598", "603626", "603662", "603666", "603667", "603706", "603728", "603893", "603901", "603920", "603926", "603948", "603960", "605018", "605058", "605287", "605288", "605398", "605488", "605577"], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-11-24", "status": "code_coverage_matched", "expected_count": 5581, "observed_count": 5581, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 619, "observed": 619, "missing_codes": []}, "sz": {"expected": 2905, "observed": 2905, "missing_codes": []}, "bj": {"expected": 357, "observed": 357, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "within_tolerance", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005, "official_yuan": 883941580704.93, "snapshot_yuan": 883186708709.0, "relative_difference": 0.0008539840328905613}, "initial_missing_codes": ["689009"], "daily_supplement_codes": ["689009"], "archived_roster_sources": {}}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=55
- yesterday_pool: ok，行数=146
- broken: ok，行数=68
- limit_down: ok，行数=2
- spot: error，行数=None
- spot_fallback: ok，行数=5580
- official_roster_sh_main: ok，行数=1700
- official_roster_sh_star: ok，行数=619
- official_roster_sz: error，行数=None
- official_roster_sz_retry1: ok，行数=2905
- official_roster_bj: ok，行数=357
- official_szse_summary: ok，行数=14
- market_quote_689009: ok，行数=1
- price_000026: ok，行数=1
- price_000530: ok，行数=1
- price_000559: ok，行数=1
- price_000593: ok，行数=1
- price_000607: ok，行数=1
- price_000636: ok，行数=1
- price_000678: ok，行数=1
- price_000700: ok，行数=1
- price_000711: ok，行数=1
- price_000766: ok，行数=1
- price_000819: ok，行数=1
- price_000823: ok，行数=1
- price_001229: ok，行数=1
- price_001266: ok，行数=1
- price_001278: ok，行数=1
- price_001283: ok，行数=1
- price_001326: ok，行数=1
- price_001330: ok，行数=1
- price_001331: ok，行数=1
- price_001358: ok，行数=1
- price_001360: ok，行数=1
- price_001400: ok，行数=1
- price_002009: ok，行数=1
- price_002036: ok，行数=1
- price_002045: ok，行数=1
- price_002046: ok，行数=1
- price_002086: ok，行数=1
- price_002122: ok，行数=1
- price_002148: ok，行数=1
- price_002164: ok，行数=1
- price_002172: ok，行数=1
- price_002173: ok，行数=1
- price_002199: ok，行数=1
- price_002242: ok，行数=1
- price_002248: ok，行数=1
- price_002249: ok，行数=1
- price_002289: ok，行数=1
- price_002343: ok，行数=1
- price_002414: ok，行数=1
- price_002527: ok，行数=1
- price_002548: ok，行数=1
- price_002565: ok，行数=1
- price_002584: ok，行数=1
- price_002623: ok，行数=1
- price_002642: ok，行数=1
- price_002655: ok，行数=1
- price_002685: ok，行数=1
- price_002687: ok，行数=1
- price_002696: ok，行数=1
- price_002703: ok，行数=1
- price_002708: ok，行数=1
- price_002724: ok，行数=1
- price_002741: ok，行数=1
- price_002747: ok，行数=1
- price_002749: ok，行数=1
- price_002815: ok，行数=1
- price_002896: ok，行数=1
- price_002913: ok，行数=1
- price_002931: ok，行数=1
- price_002983: ok，行数=1
- price_003021: ok，行数=1
- price_003028: ok，行数=1
- price_003032: ok，行数=1
- price_003033: ok，行数=1
- price_003041: ok，行数=1
- price_600103: ok，行数=1
- price_600156: ok，行数=1
- price_600327: ok，行数=1
- price_600360: ok，行数=1
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
