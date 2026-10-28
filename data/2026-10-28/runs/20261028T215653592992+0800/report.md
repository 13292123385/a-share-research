# 2026-10-28 A股收盘复盘

状态：complete；抓取时间：2026-10-28T21:56:53.592992+08:00

采集范围：closing_snapshot；采集状态：complete；研究状态：available

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 58, "mainboard_height": 5.0, "first_board_candidates": 50, "all_day_one_word_excluded": 1, "one_word_unknown": 0, "broken_count": 49, "limit_down_count": 5, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-10-28T00:00:00.000", "open": 3676.92, "close": 3681.47, "high": 3684.49, "low": 3652.37, "amount": 433622829.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-10-28T00:00:00.000", "open": 11359.08, "close": 11473.18, "high": 11529.6, "low": 11292.7, "amount": 538092409.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-10-28T00:00:00.000", "open": 2593.15, "close": 2634.76, "high": 2647.63, "low": 2562.9, "amount": 181409982.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-10-28T00:00:00.000", "close": 2800.7, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{"market": {"up": 4156, "down": 1239, "flat": 181, "turnover_yuan": 1642102182726.0, "records": 5576, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 24, "promoted_count": 5, "broken_count": 1, "observation_rate": 0.20833333333333334, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 58, "prices_available": 58, "missing_archive_dates": [], "missing_price_codes": [], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-10-28", "status": "code_coverage_matched", "expected_count": 5576, "observed_count": 5576, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 618, "observed": 618, "missing_codes": []}, "sz": {"expected": 2905, "observed": 2905, "missing_codes": []}, "bj": {"expected": 353, "observed": 353, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "within_tolerance", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005, "official_yuan": 878559843759.9199, "snapshot_yuan": 877431225639.0, "relative_difference": 0.0012846229302830897}, "initial_missing_codes": ["689009"], "daily_supplement_codes": ["689009"]}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=72
- yesterday_pool: ok，行数=41
- broken: ok，行数=69
- limit_down: ok，行数=5
- spot: error，行数=None
- spot_fallback: ok，行数=5575
- official_roster_sh_main: ok，行数=1700
- official_roster_sh_star: ok，行数=618
- official_roster_sz: error，行数=None
- official_roster_sz_retry1: ok，行数=2905
- official_roster_bj: ok，行数=353
- official_szse_summary: ok，行数=14
- market_quote_689009: ok，行数=1
- price_000058: ok，行数=1
- price_000411: ok，行数=1
- price_000635: ok，行数=1
- price_000888: ok，行数=1
- price_000995: ok，行数=1
- price_001219: ok，行数=1
- price_001225: ok，行数=1
- price_001317: ok，行数=1
- price_001318: ok，行数=1
- price_001331: ok，行数=1
- price_001400: ok，行数=1
- price_002011: ok，行数=1
- price_002086: ok，行数=1
- price_002093: ok，行数=1
- price_002095: ok，行数=1
- price_002178: ok，行数=1
- price_002187: ok，行数=1
- price_002205: ok，行数=1
- price_002249: ok，行数=1
- price_002284: ok，行数=1
- price_002578: ok，行数=1
- price_002623: ok，行数=1
- price_002696: ok，行数=1
- price_002708: ok，行数=1
- price_002724: ok，行数=1
- price_002795: ok，行数=1
- price_002820: ok，行数=1
- price_002823: ok，行数=1
- price_002869: ok，行数=1
- price_600303: ok，行数=1
- price_600558: ok，行数=1
- price_600626: ok，行数=1
- price_600715: ok，行数=1
- price_600785: ok，行数=1
- price_600822: ok，行数=1
- price_600826: ok，行数=1
- price_600828: ok，行数=1
- price_600980: ok，行数=1
- price_601086: ok，行数=1
- price_601566: ok，行数=1
- price_601900: ok，行数=1
- price_601956: ok，行数=1
- price_603037: ok，行数=1
- price_603138: ok，行数=1
- price_603200: ok，行数=1
- price_603258: ok，行数=1
- price_603331: ok，行数=1
- price_603370: ok，行数=1
- price_603376: ok，行数=1
- price_603565: ok，行数=1
- price_603657: ok，行数=1
- price_603683: ok，行数=1
- price_603716: ok，行数=1
- price_603719: ok，行数=1
- price_603758: ok，行数=1
- price_603813: ok，行数=1
- price_603955: ok，行数=1
- price_605333: ok，行数=1
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
