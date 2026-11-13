# 2026-11-13 A股收盘复盘

状态：partial；抓取时间：2026-11-13T17:37:18.723685+08:00

采集范围：closing_snapshot；采集状态：partial；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 35, "mainboard_height": 4.0, "first_board_candidates": 28, "all_day_one_word_excluded": 1, "one_word_unknown": 0, "broken_count": 19, "limit_down_count": 33, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-13T00:00:00.000", "open": 3658.72, "close": 3634.35, "high": 3669.44, "low": 3623.84, "amount": 472293657.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-13T00:00:00.000", "open": 11236.16, "close": 10968.79, "high": 11253.31, "low": 10941.11, "amount": 559255208.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-13T00:00:00.000", "open": 2525.39, "close": 2426.08, "high": 2528.99, "low": 2417.22, "amount": 170437467.0}]}

## 估算值
{"market": {"up": 765, "down": 4748, "flat": 66, "turnover_yuan": 1667073599118.0, "records": 5579, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 24, "promoted_count": 3, "broken_count": 3, "observation_rate": 0.125, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 首板后续跟踪存在历史名单或价格缺失，详见followup
- 中证2000指定日期收盘值

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 83, "prices_available": 67, "missing_archive_dates": [], "missing_price_codes": ["000635", "603042", "603083", "603135", "603175", "603228", "603258", "603289", "603330", "603396", "603586", "603725", "603730", "603958", "605169", "605222"], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-11-13", "status": "code_coverage_matched", "expected_count": 5579, "observed_count": 5579, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 619, "observed": 619, "missing_codes": []}, "sz": {"expected": 2905, "observed": 2905, "missing_codes": []}, "bj": {"expected": 355, "observed": 355, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "within_tolerance", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005, "official_yuan": 885698956320.94, "snapshot_yuan": 885006883726.0, "relative_difference": 0.0007813858083503979}, "initial_missing_codes": ["689009"], "daily_supplement_codes": ["689009"], "archived_roster_sources": {}}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=37
- yesterday_pool: ok，行数=37
- broken: ok，行数=21
- limit_down: ok，行数=33
- spot: error，行数=None
- spot_fallback: ok，行数=5578
- official_roster_sh_main: ok，行数=1700
- official_roster_sh_star: ok，行数=619
- official_roster_sz: error，行数=None
- official_roster_sz_retry1: ok，行数=2905
- official_roster_bj: ok，行数=355
- official_szse_summary: ok，行数=14
- market_quote_689009: ok，行数=1
- price_000026: ok，行数=1
- price_000407: ok，行数=1
- price_000545: ok，行数=1
- price_000573: ok，行数=1
- price_000631: ok，行数=1
- price_000635: empty_unverified，行数=0
- price_000995: ok，行数=1
- price_001282: ok，行数=1
- price_001331: ok，行数=1
- price_001358: ok，行数=1
- price_002021: ok，行数=1
- price_002076: ok，行数=1
- price_002086: ok，行数=1
- price_002110: ok，行数=1
- price_002148: ok，行数=1
- price_002154: ok，行数=1
- price_002164: ok，行数=1
- price_002172: ok，行数=1
- price_002187: ok，行数=1
- price_002205: ok，行数=1
- price_002278: ok，行数=1
- price_002281: ok，行数=1
- price_002362: ok，行数=1
- price_002384: ok，行数=1
- price_002463: ok，行数=1
- price_002520: ok，行数=1
- price_002529: ok，行数=1
- price_002593: ok，行数=1
- price_002628: ok，行数=1
- price_002633: ok，行数=1
- price_002693: ok，行数=1
- price_002696: ok，行数=1
- price_002703: ok，行数=1
- price_002713: ok，行数=1
- price_002765: ok，行数=1
- price_002779: ok，行数=1
- price_002795: ok，行数=1
- price_002837: ok，行数=1
- price_002886: ok，行数=1
- price_002913: ok，行数=1
- price_002916: ok，行数=1
- price_002919: ok，行数=1
- price_002957: ok，行数=1
- price_002975: ok，行数=1
- price_002980: ok，行数=1
- price_003032: ok，行数=1
- price_600076: ok，行数=1
- price_600103: ok，行数=1
- price_600162: ok，行数=1
- price_600228: ok，行数=1
- price_600293: ok，行数=1
- price_600467: ok，行数=1
- price_600558: ok，行数=1
- price_600569: ok，行数=1
- price_600629: ok，行数=1
- price_600776: ok，行数=1
- price_600802: ok，行数=1
- price_600853: ok，行数=1
- price_600857: ok，行数=1
- price_600876: ok，行数=1
- price_601091: ok，行数=1
- price_601188: ok，行数=1
- price_601566: ok，行数=1
- price_601606: ok，行数=1
- price_601869: ok，行数=1
- price_601929: ok，行数=1
- price_603028: ok，行数=1
- price_603040: ok，行数=1
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
