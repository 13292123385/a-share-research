# 2026-11-24 A股收盘复盘

状态：complete；抓取时间：2026-11-28T11:56:53.755212+08:00

采集范围：closing_snapshot；采集状态：complete；研究状态：available

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 47, "mainboard_height": 4.0, "first_board_candidates": 21, "all_day_one_word_excluded": 10, "one_word_unknown": 0, "broken_count": 57, "limit_down_count": 2, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-24", "open": 3567.84, "close": 3548.37, "high": 3585.22, "low": 3539.01, "volume": 493526296, "amount": 771861010308.7}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-24", "open": 10708.62, "close": 10423.6, "high": 10729.13, "low": 10418.11, "volume": 590663196, "amount": 883224915525.93}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-24", "open": 2368.7, "close": 2278.99, "high": 2376.34, "low": 2278.99, "volume": 192416694, "amount": 453945224581.06}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-24", "open": 2507.19, "close": 2449.61, "high": 2533.82, "low": 2438.36, "volume": 298274370, "amount": 333492977007.0}]}

## 估算值
{"market": {"up": 1952, "down": 3498, "flat": 131, "turnover_yuan": 1667800445242.0, "records": 5581, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 95, "promoted_count": 14, "broken_count": 19, "observation_rate": 0.14736842105263157, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 124, "prices_available": 124, "missing_archive_dates": [], "missing_price_codes": [], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-11-24", "status": "code_coverage_matched", "expected_count": 5581, "observed_count": 5581, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 619, "observed": 619, "missing_codes": []}, "sz": {"expected": 2905, "observed": 2905, "missing_codes": []}, "bj": {"expected": 357, "observed": 357, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "within_tolerance", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005, "official_yuan": 883941580704.93, "snapshot_yuan": 883186708709.0, "relative_difference": 0.0008539840328905613}, "initial_missing_codes": [], "daily_supplement_codes": [], "archived_roster_sources": {"sh_main": "20261124T190012817684+0800/raw/official_roster_sh_main.json", "sh_star": "20261124T190012817684+0800/raw/official_roster_sh_star.json", "sz": "20261124T190012817684+0800/raw/official_roster_sz_retry1.json", "bj": "20261124T190012817684+0800/raw/official_roster_bj.json"}}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=55
- yesterday_pool: ok，行数=146
- broken: ok，行数=68
- limit_down: ok，行数=2
- official_szse_summary: error，行数=None
- official_szse_summary_retry: ok，行数=14
- price_600371: ok，行数=1
- price_600467: ok，行数=1
- price_600814: ok，行数=1
- price_600838: ok，行数=1
- price_600980: ok，行数=1
- price_601177: ok，行数=1
- price_601188: ok，行数=1
- price_601595: ok，行数=1
- price_601599: ok，行数=1
- price_601689: ok，行数=1
- price_603004: ok，行数=1
- price_603009: ok，行数=1
- price_603037: ok，行数=1
- price_603040: ok，行数=1
- price_603048: ok，行数=1
- price_603051: ok，行数=1
- price_603103: ok，行数=1
- price_603119: ok，行数=1
- price_603127: ok，行数=1
- price_603131: ok，行数=1
- price_603151: ok，行数=1
- price_603166: ok，行数=1
- price_603175: ok，行数=1
- price_603179: ok，行数=1
- price_603236: ok，行数=1
- price_603278: ok，行数=1
- price_603283: ok，行数=1
- price_603286: ok，行数=1
- price_603305: ok，行数=1
- price_603337: ok，行数=1
- price_603386: ok，行数=1
- price_603466: ok，行数=1
- price_603516: ok，行数=1
- price_603528: ok，行数=1
- price_603533: ok，行数=1
- price_603598: ok，行数=1
- price_603626: ok，行数=1
- price_603662: ok，行数=1
- price_603666: ok，行数=1
- price_603667: ok，行数=1
- price_603706: ok，行数=1
- price_603728: ok，行数=1
- price_603893: ok，行数=1
- price_603901: ok，行数=1
- price_603920: ok，行数=1
- price_603926: ok，行数=1
- price_603948: ok，行数=1
- price_603960: ok，行数=1
- price_605018: ok，行数=1
- price_605058: ok，行数=1
- price_605287: ok，行数=1
- price_605288: ok，行数=1
- price_605398: ok，行数=1
- price_605488: ok，行数=1
- price_605577: ok，行数=1
- index_sh000001: ok，行数=1
- index_sz399001: ok，行数=1
- index_sz399006: ok，行数=1
- index_csi932000: ok，行数=1
