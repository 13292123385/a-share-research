# 2026-11-17 A股收盘复盘

状态：complete；抓取时间：2026-11-17T19:51:53.517809+08:00

采集范围：closing_snapshot；采集状态：complete；研究状态：available

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 32, "mainboard_height": 3.0, "first_board_candidates": 26, "all_day_one_word_excluded": 3, "one_word_unknown": 0, "broken_count": 16, "limit_down_count": 66, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-17", "open": 3585.67, "close": 3584.58, "high": 3604.98, "low": 3565.59, "volume": 444074698, "amount": 690514639035.9}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-17", "open": 10605.17, "close": 10638.52, "high": 10768.06, "low": 10556.29, "volume": 537885638, "amount": 767179957875.19}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-17", "open": 2299.97, "close": 2292.2, "high": 2343.15, "low": 2263.74, "volume": 165287320, "amount": 369315656403.11}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-17", "open": 2614.85, "close": 2589.95, "high": 2663.48, "low": 2573.21, "volume": 267415618, "amount": 290905169905.0}]}

## 估算值
{"market": {"up": 1326, "down": 4119, "flat": 135, "turnover_yuan": 1467532916628.0, "records": 5580, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 19, "promoted_count": 5, "broken_count": 2, "observation_rate": 0.2631578947368421, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 47, "prices_available": 47, "missing_archive_dates": [], "missing_price_codes": [], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-11-17", "status": "code_coverage_matched", "expected_count": 5580, "observed_count": 5580, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 619, "observed": 619, "missing_codes": []}, "sz": {"expected": 2905, "observed": 2905, "missing_codes": []}, "bj": {"expected": 356, "observed": 356, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "within_tolerance", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005, "official_yuan": 767969265599.51, "snapshot_yuan": 767142298839.0, "relative_difference": 0.0010768227291810223}, "initial_missing_codes": ["689009"], "daily_supplement_codes": ["689009"], "archived_roster_sources": {}}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=37
- yesterday_pool: ok，行数=32
- broken: ok，行数=20
- limit_down: ok，行数=67
- spot: error，行数=None
- spot_fallback: ok，行数=5579
- official_roster_sh_main: error，行数=None
- official_roster_sh_main_retry1: ok，行数=1700
- official_roster_sh_star: ok，行数=619
- official_roster_sz: error，行数=None
- official_roster_sz_retry1: ok，行数=2905
- official_roster_bj: ok，行数=356
- official_szse_summary: ok，行数=14
- market_quote_689009: ok，行数=1
- price_000156: ok，行数=1
- price_000521: ok，行数=1
- price_000533: ok，行数=1
- price_000595: ok，行数=1
- price_000628: ok，行数=1
- price_000665: ok，行数=1
- price_000766: ok，行数=1
- price_000819: ok，行数=1
- price_001318: ok，行数=1
- price_001393: ok，行数=1
- price_002035: ok，行数=1
- price_002042: ok，行数=1
- price_002058: ok，行数=1
- price_002124: ok，行数=1
- price_002356: ok，行数=1
- price_002419: ok，行数=1
- price_002425: ok，行数=1
- price_002520: ok，行数=1
- price_002548: ok，行数=1
- price_002685: ok，行数=1
- price_002739: ok，行数=1
- price_002748: ok，行数=1
- price_002819: ok，行数=1
- price_002853: ok，行数=1
- price_002861: ok，行数=1
- price_002905: ok，行数=1
- price_002959: ok，行数=1
- price_600386: ok，行数=1
- price_600410: ok，行数=1
- price_600651: ok，行数=1
- price_600715: ok，行数=1
- price_600822: ok，行数=1
- price_600936: ok，行数=1
- price_600977: ok，行数=1
- price_601188: ok，行数=1
- price_601929: ok，行数=1
- price_603103: ok，行数=1
- price_603118: ok，行数=1
- price_603166: ok，行数=1
- price_603286: ok，行数=1
- price_603636: ok，行数=1
- price_603686: ok，行数=1
- price_603767: ok，行数=1
- price_603928: ok，行数=1
- price_603983: ok，行数=1
- price_605318: ok，行数=1
- price_605378: ok，行数=1
- index_sh000001: ok，行数=1
- index_sz399001: ok，行数=1
- index_sz399006: ok，行数=1
- index_csi932000: ok，行数=1
