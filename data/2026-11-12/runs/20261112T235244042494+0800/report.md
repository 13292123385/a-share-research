# 2026-11-12 A股收盘复盘

状态：partial；抓取时间：2026-11-12T23:52:44.042494+08:00

采集范围：closing_snapshot；采集状态：partial；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 37, "mainboard_height": 5.0, "first_board_candidates": 26, "all_day_one_word_excluded": 3, "one_word_unknown": 0, "broken_count": 33, "limit_down_count": 5, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-12T00:00:00.000", "open": 3673.06, "close": 3655.83, "high": 3699.58, "low": 3647.44, "amount": 496533033.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-12T00:00:00.000", "open": 11361.82, "close": 11197.98, "high": 11515.65, "low": 11193.26, "amount": 632899416.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-12T00:00:00.000", "open": 2559.16, "close": 2509.43, "high": 2620.25, "low": 2508.29, "amount": 196927278.0}]}

## 估算值
{"market": {"up": 875, "down": 4635, "flat": 70, "turnover_yuan": 1945871950570.0, "records": 5580, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 56, "promoted_count": 4, "broken_count": 11, "observation_rate": 0.07142857142857142, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 中证2000指定日期收盘值

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 121, "prices_available": 121, "missing_archive_dates": [], "missing_price_codes": [], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-11-12", "status": "code_coverage_matched", "expected_count": 5580, "observed_count": 5580, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 619, "observed": 619, "missing_codes": []}, "sz": {"expected": 2906, "observed": 2906, "missing_codes": []}, "bj": {"expected": 355, "observed": 355, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "within_tolerance", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005, "official_yuan": 1053383505717.29, "snapshot_yuan": 1052514534941.0, "relative_difference": 0.0008249329627563542}, "initial_missing_codes": [], "daily_supplement_codes": [], "archived_roster_sources": {"sh_main": "20261112T204759202564+0800/raw/official_roster_sh_main.json", "sh_star": "20261112T204759202564+0800/raw/official_roster_sh_star.json", "sz": "20261112T204759202564+0800/raw/official_roster_sz_retry1.json", "bj": "20261112T204759202564+0800/raw/official_roster_bj.json"}}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=37
- yesterday_pool: ok，行数=85
- broken: ok，行数=35
- limit_down: ok，行数=5
- official_szse_summary: error，行数=None
- official_szse_summary_retry: ok，行数=14
- price_003032: ok，行数=1
- price_600076: ok，行数=1
- price_600103: ok，行数=1
- price_600162: ok，行数=1
- price_600228: ok，行数=1
- price_600261: ok，行数=1
- price_600281: ok，行数=1
- price_600293: ok，行数=1
- price_600510: ok，行数=1
- price_600629: ok，行数=1
- price_600776: ok，行数=1
- price_600778: ok，行数=1
- price_600793: ok，行数=1
- price_600829: ok，行数=1
- price_600876: ok，行数=1
- price_601595: ok，行数=1
- price_601869: ok，行数=1
- price_603028: ok，行数=1
- price_603037: ok，行数=1
- price_603040: ok，行数=1
- price_603042: ok，行数=1
- price_603058: ok，行数=1
- price_603083: ok，行数=1
- price_603135: ok，行数=1
- price_603215: ok，行数=1
- price_603228: ok，行数=1
- price_603258: ok，行数=1
- price_603278: ok，行数=1
- price_603283: ok，行数=1
- price_603289: ok，行数=1
- price_603330: ok，行数=1
- price_603381: ok，行数=1
- price_603396: ok，行数=1
- price_603466: ok，行数=1
- price_603533: ok，行数=1
- price_603536: ok，行数=1
- price_603586: ok，行数=1
- price_603598: ok，行数=1
- price_603602: ok，行数=1
- price_603666: ok，行数=1
- price_603679: ok，行数=1
- price_603725: ok，行数=1
- price_603730: ok，行数=1
- price_603809: ok，行数=1
- price_603893: ok，行数=1
- price_603955: ok，行数=1
- price_605255: ok，行数=1
- price_605258: ok，行数=1
- price_605398: ok，行数=1
- price_605488: ok，行数=1
- price_605577: ok，行数=1
- price_605598: ok，行数=1
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
- index_official_csi932000: error，行数=None
