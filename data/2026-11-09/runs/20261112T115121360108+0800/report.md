# 2026-11-09 A股收盘复盘

状态：complete_with_limitations；抓取时间：2026-11-12T11:51:21.360108+08:00

采集范围：closing_snapshot；采集状态：complete；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 50, "mainboard_height": 6.0, "first_board_candidates": 41, "all_day_one_word_excluded": 3, "one_word_unknown": 0, "broken_count": 38, "limit_down_count": 1, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-09", "open": 3659.02, "close": 3660.79, "high": 3679.09, "low": 3653.05, "volume": 427722257, "amount": 682532599935.4}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-09T00:00:00.000", "open": 11273.28, "close": 11145.49, "high": 11311.2, "low": 11145.49, "amount": 514921429.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-09T00:00:00.000", "open": 2494.63, "close": 2458.56, "high": 2511.71, "low": 2458.01, "amount": 165434913.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-09T00:00:00.000", "close": 2737.41, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{"market": {"up": 2242, "down": 3148, "flat": 189, "turnover_yuan": 1494555719600.0, "records": 5579, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 17, "promoted_count": 6, "broken_count": 8, "observation_rate": 0.35294117647058826, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 首板后续跟踪存在历史名单或价格缺失，详见followup

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 70, "prices_available": 69, "missing_archive_dates": [], "missing_price_codes": ["605339"], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-11-09", "status": "code_coverage_matched", "expected_count": 5579, "observed_count": 5579, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 618, "observed": 618, "missing_codes": []}, "sz": {"expected": 2906, "observed": 2906, "missing_codes": []}, "bj": {"expected": 355, "observed": 355, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "within_tolerance", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005, "official_yuan": 800876347428.54, "snapshot_yuan": 800044830451.0, "relative_difference": 0.0010382588775531706}, "initial_missing_codes": [], "daily_supplement_codes": [], "archived_roster_sources": {"sh_main": "20261109T160045149353+0800/raw/official_roster_sh_main.json", "sh_star": "20261109T160045149353+0800/raw/official_roster_sh_star.json", "sz": "20261109T160045149353+0800/raw/official_roster_sz_retry1.json", "bj": "20261109T160045149353+0800/raw/official_roster_bj.json"}}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=54
- yesterday_pool: ok，行数=32
- broken: ok，行数=44
- limit_down: ok，行数=1
- official_szse_summary: error，行数=None
- official_szse_summary_retry: ok，行数=14
- price_000029: ok，行数=1
- price_000428: ok，行数=1
- price_000525: ok，行数=1
- price_000533: ok，行数=1
- price_000595: ok，行数=1
- price_000635: ok，行数=1
- price_000700: ok，行数=1
- price_000710: ok，行数=1
- price_000889: ok，行数=1
- price_000995: ok，行数=1
- price_001258: ok，行数=1
- price_001269: ok，行数=1
- price_001308: ok，行数=1
- price_001316: ok，行数=1
- price_001330: ok，行数=1
- price_001393: ok，行数=1
- price_002045: ok，行数=1
- price_002086: ok，行数=1
- price_002131: ok，行数=1
- price_002135: ok，行数=1
- price_002307: ok，行数=1
- price_002310: ok，行数=1
- price_002313: ok，行数=1
- price_002318: ok，行数=1
- price_002343: ok，行数=1
- price_002421: ok，行数=1
- price_002506: ok，行数=1
- price_002596: ok，行数=1
- price_002712: ok，行数=1
- price_002773: ok，行数=1
- price_002865: ok，行数=1
- price_002889: ok，行数=1
- price_002929: ok，行数=1
- price_002973: ok，行数=1
- price_600156: ok，行数=1
- price_600207: ok，行数=1
- price_600229: ok，行数=1
- price_600261: ok，行数=1
- price_600278: ok，行数=1
- price_600327: ok，行数=1
- price_600371: ok，行数=1
- price_600396: ok，行数=1
- price_600481: ok，行数=1
- price_600539: ok，行数=1
- price_600540: ok，行数=1
- price_600569: ok，行数=1
- price_600683: ok，行数=1
- price_600865: ok，行数=1
- price_600986: ok，行数=1
- price_601188: ok，行数=1
- price_601595: ok，行数=1
- price_601929: ok，行数=1
- price_603068: ok，行数=1
- price_603098: ok，行数=1
- price_603151: ok，行数=1
- price_603185: ok，行数=1
- price_603212: ok，行数=1
- price_603297: ok，行数=1
- price_603313: ok，行数=1
- price_603366: ok，行数=1
- price_603500: ok，行数=1
- price_603682: ok，行数=1
- price_603699: ok，行数=1
- price_603737: ok，行数=1
- price_603876: ok，行数=1
- price_603956: ok，行数=1
- price_603990: ok，行数=1
- price_605069: ok，行数=1
- price_605188: ok，行数=1
- index_sh000001: ok，行数=1
- index_sz399001: error，行数=None
- index_retry_sz399001: error，行数=None
- index_fallback_sz399001: ok，行数=1
- index_sz399006: error，行数=None
- index_retry_sz399006: error，行数=None
- index_fallback_sz399006: ok，行数=1
- index_csi932000: error，行数=None
- index_retry_csi932000: error，行数=None
- index_official_csi932000: ok，行数=1
