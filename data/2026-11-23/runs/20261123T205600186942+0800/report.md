# 2026-11-23 A股收盘复盘

状态：complete；抓取时间：2026-11-23T20:56:00.186942+08:00

采集范围：closing_snapshot；采集状态：complete；研究状态：available

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 117, "mainboard_height": 5.0, "first_board_candidates": 102, "all_day_one_word_excluded": 3, "one_word_unknown": 0, "broken_count": 19, "limit_down_count": 3, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-23T00:00:00.000", "open": 3503.52, "close": 3538.95, "high": 3544.6, "low": 3476.65, "amount": 512192714.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-23T00:00:00.000", "open": 10155.6, "close": 10454.37, "high": 10510.18, "low": 10118.02, "amount": 607372090.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-23T00:00:00.000", "open": 2195.52, "close": 2280.2, "high": 2297.73, "low": 2188.45, "amount": 188251199.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-23T00:00:00.000", "close": 2443.92, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{"market": {"up": 4658, "down": 783, "flat": 140, "turnover_yuan": 1563961806390.0, "records": 5581, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 20, "promoted_count": 10, "broken_count": 1, "observation_rate": 0.5, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 39, "prices_available": 39, "missing_archive_dates": [], "missing_price_codes": [], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-11-23", "status": "code_coverage_matched", "expected_count": 5581, "observed_count": 5581, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 619, "observed": 619, "missing_codes": []}, "sz": {"expected": 2905, "observed": 2905, "missing_codes": []}, "bj": {"expected": 357, "observed": 357, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "within_tolerance", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005, "official_yuan": 815158140826.98, "snapshot_yuan": 814294312027.0, "relative_difference": 0.0010597070147684766}, "initial_missing_codes": ["689009"], "daily_supplement_codes": ["689009"], "archived_roster_sources": {}}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=146
- yesterday_pool: ok，行数=28
- broken: ok，行数=24
- limit_down: ok，行数=3
- spot: error，行数=None
- spot_fallback: ok，行数=5580
- official_roster_sh_main: ok，行数=1700
- official_roster_sh_star: ok，行数=619
- official_roster_sz: error，行数=None
- official_roster_sz_retry1: ok，行数=2905
- official_roster_bj: ok，行数=357
- official_szse_summary: ok，行数=14
- market_quote_689009: ok，行数=1
- price_000530: ok，行数=1
- price_000593: ok，行数=1
- price_000607: ok，行数=1
- price_000656: ok，行数=1
- price_000678: ok，行数=1
- price_000823: ok，行数=1
- price_001358: ok，行数=1
- price_002077: ok，行数=1
- price_002086: ok，行数=1
- price_002165: ok，行数=1
- price_002199: ok，行数=1
- price_002242: ok，行数=1
- price_002418: ok，行数=1
- price_002420: ok，行数=1
- price_002548: ok，行数=1
- price_002579: ok，行数=1
- price_002642: ok，行数=1
- price_002741: ok，行数=1
- price_002749: ok，行数=1
- price_600327: ok，行数=1
- price_600360: ok，行数=1
- price_600371: ok，行数=1
- price_600467: ok，行数=1
- price_600520: ok，行数=1
- price_600619: ok，行数=1
- price_601616: ok，行数=1
- price_603004: ok，行数=1
- price_603078: ok，行数=1
- price_603386: ok，行数=1
- price_603466: ok，行数=1
- price_603813: ok，行数=1
- price_603928: ok，行数=1
- price_603931: ok，行数=1
- price_603948: ok，行数=1
- price_603960: ok，行数=1
- price_605018: ok，行数=1
- price_605058: ok，行数=1
- price_605178: ok，行数=1
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
