# 2026-11-09 A股收盘复盘

状态：partial；抓取时间：2026-11-09T16:00:45.149353+08:00

采集范围：closing_snapshot；采集状态：partial；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 50, "mainboard_height": 6.0, "first_board_candidates": 41, "all_day_one_word_excluded": 3, "one_word_unknown": 0, "broken_count": 38, "limit_down_count": 1, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-09", "open": 3659.02, "close": 3660.79, "high": 3679.09, "low": 3653.05, "volume": 427722257, "amount": 682532599935.4}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-09", "open": 11273.28, "close": 11145.49, "high": 11311.2, "low": 11145.49, "volume": 514921429, "amount": 800080739807.69}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-09", "open": 2494.63, "close": 2458.56, "high": 2511.71, "low": 2458.01, "volume": 172690070, "amount": 404936054219.04}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-09", "open": 2754.98, "close": 2737.41, "high": 2777.2, "low": 2733.53, "volume": 264957248, "amount": 314136272766.0}]}

## 估算值
{"market": {"up": 2242, "down": 3148, "flat": 189, "turnover_yuan": 1494555719600.0, "records": 5579, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 17, "promoted_count": 6, "broken_count": 8, "observation_rate": 0.35294117647058826, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 深圳A股成交额交叉核验未通过或不可比较
- 首板后续跟踪存在历史名单或价格缺失，详见followup

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 70, "prices_available": 0, "missing_archive_dates": [], "missing_price_codes": ["000029", "000428", "000525", "000533", "000595", "000635", "000700", "000710", "000889", "000995", "001258", "001269", "001308", "001316", "001330", "001393", "002045", "002086", "002131", "002135", "002307", "002310", "002313", "002318", "002343", "002421", "002506", "002596", "002712", "002773", "002865", "002889", "002929", "002973", "600156", "600207", "600229", "600261", "600278", "600327", "600371", "600396", "600481", "600539", "600540", "600569", "600683", "600865", "600986", "601188", "601595", "601929", "603068", "603098", "603151", "603185", "603212", "603297", "603313", "603366", "603500", "603682", "603699", "603737", "603876", "603956", "603990", "605069", "605188", "605339"], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-11-09", "status": "code_coverage_matched", "expected_count": 5579, "observed_count": 5579, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 618, "observed": 618, "missing_codes": []}, "sz": {"expected": 2906, "observed": 2906, "missing_codes": []}, "bj": {"expected": 355, "observed": 355, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "not_comparable", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005}, "initial_missing_codes": ["689009"], "daily_supplement_codes": ["689009"], "archived_roster_sources": {}}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=54
- yesterday_pool: ok，行数=32
- broken: ok，行数=44
- limit_down: ok，行数=1
- spot: error，行数=None
- spot_fallback: ok，行数=5578
- official_roster_sh_main: ok，行数=1700
- official_roster_sh_star: ok，行数=618
- official_roster_sz: error，行数=None
- official_roster_sz_retry1: ok，行数=2906
- official_roster_bj: ok，行数=355
- official_szse_summary: error，行数=None
- official_szse_summary_retry: ok，行数=1
- market_quote_689009: ok，行数=1
- price_000029: empty_unverified，行数=0
- price_000428: empty_unverified，行数=0
- price_000525: empty_unverified，行数=0
- price_000533: empty_unverified，行数=0
- price_000595: empty_unverified，行数=0
- price_000635: empty_unverified，行数=0
- price_000700: empty_unverified，行数=0
- price_000710: empty_unverified，行数=0
- price_000889: empty_unverified，行数=0
- price_000995: empty_unverified，行数=0
- price_001258: empty_unverified，行数=0
- price_001269: empty_unverified，行数=0
- price_001308: empty_unverified，行数=0
- price_001316: empty_unverified，行数=0
- price_001330: empty_unverified，行数=0
- price_001393: empty_unverified，行数=0
- price_002045: empty_unverified，行数=0
- price_002086: empty_unverified，行数=0
- price_002131: empty_unverified，行数=0
- price_002135: empty_unverified，行数=0
- price_002307: empty_unverified，行数=0
- price_002310: empty_unverified，行数=0
- price_002313: empty_unverified，行数=0
- price_002318: empty_unverified，行数=0
- price_002343: empty_unverified，行数=0
- price_002421: empty_unverified，行数=0
- price_002506: empty_unverified，行数=0
- price_002596: empty_unverified，行数=0
- price_002712: empty_unverified，行数=0
- price_002773: empty_unverified，行数=0
- price_002865: empty_unverified，行数=0
- price_002889: empty_unverified，行数=0
- price_002929: empty_unverified，行数=0
- price_002973: empty_unverified，行数=0
- price_600156: empty_unverified，行数=0
- price_600207: empty_unverified，行数=0
- price_600229: empty_unverified，行数=0
- price_600261: empty_unverified，行数=0
- price_600278: empty_unverified，行数=0
- price_600327: empty_unverified，行数=0
- price_600371: empty_unverified，行数=0
- price_600396: empty_unverified，行数=0
- price_600481: empty_unverified，行数=0
- price_600539: empty_unverified，行数=0
- price_600540: empty_unverified，行数=0
- price_600569: empty_unverified，行数=0
- price_600683: empty_unverified，行数=0
- price_600865: empty_unverified，行数=0
- price_600986: empty_unverified，行数=0
- price_601188: empty_unverified，行数=0
- price_601595: empty_unverified，行数=0
- price_601929: empty_unverified，行数=0
- price_603068: empty_unverified，行数=0
- price_603098: empty_unverified，行数=0
- price_603151: empty_unverified，行数=0
- price_603185: empty_unverified，行数=0
- price_603212: empty_unverified，行数=0
- price_603297: empty_unverified，行数=0
- price_603313: empty_unverified，行数=0
- price_603366: empty_unverified，行数=0
- price_603500: empty_unverified，行数=0
- price_603682: empty_unverified，行数=0
- price_603699: empty_unverified，行数=0
- price_603737: empty_unverified，行数=0
- price_603876: empty_unverified，行数=0
- price_603956: empty_unverified，行数=0
- price_603990: empty_unverified，行数=0
- price_605069: empty_unverified，行数=0
- price_605188: empty_unverified，行数=0
- price_605339: empty_unverified，行数=0
- index_sh000001: ok，行数=1
- index_sz399001: ok，行数=1
- index_sz399006: ok，行数=1
- index_csi932000: ok，行数=1
