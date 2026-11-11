# 2026-11-04 A股收盘复盘

状态：complete_with_limitations；抓取时间：2026-11-11T14:33:01.909631+08:00

采集范围：historical_pools_candidate_prices_indices；采集状态：complete；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 96, "mainboard_height": 3.0, "first_board_candidates": 84, "all_day_one_word_excluded": 4, "one_word_unknown": 0, "broken_count": 30, "limit_down_count": 10, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-04", "open": 3605.39, "close": 3686.17, "high": 3686.17, "low": 3590.8, "volume": 599394361, "amount": 953265155867.1}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-04", "open": 10895.8, "close": 11335.69, "high": 11362.9, "low": 10826.83, "volume": 682108330, "amount": 1084429058169.67}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-04", "open": 2399.46, "close": 2544.73, "high": 2559.09, "low": 2376.28, "volume": 228849025, "amount": 549329528581.74}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-04", "open": 2627.89, "close": 2713.36, "high": 2716.1, "low": 2590.63, "volume": 328077349, "amount": 391909041854.0}]}

## 估算值
{}

## 一进二
{"status": "observation_only", "denominator": 29, "promoted_count": 5, "broken_count": 3, "observation_rate": 0.1724137931034483, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 全市场收盘快照；不跨日套用实时数据
- 首板后续跟踪存在历史名单或价格缺失，详见followup

## 候选股价格覆盖
{"historical_available": 96, "historical_fetched": 8, "reused": 88, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 129, "prices_available": 128, "missing_archive_dates": [], "missing_price_codes": ["002623"], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"status": "not_applicable_historical", "all_market_verified": false, "note": "当前上市名单不能冒充历史名单；只对当日有效采集执行自动核验"}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=118
- yesterday_pool: ok，行数=48
- broken: ok，行数=33
- limit_down: ok，行数=10
- price_002652: ok，行数=1
- price_002827: ok，行数=1
- price_002992: ok，行数=1
- price_600892: ok，行数=1
- price_601123: ok，行数=1
- price_601599: ok，行数=1
- price_603381: ok，行数=1
- price_605577: ok，行数=1
- price_000151: ok，行数=1
- price_000591: ok，行数=1
- price_000608: ok，行数=1
- price_001318: ok，行数=1
- price_002105: ok，行数=1
- price_002300: ok，行数=1
- price_002522: ok，行数=1
- price_002580: ok，行数=1
- price_002623: empty_unverified，行数=0
- price_002692: ok，行数=1
- price_002696: ok，行数=1
- price_002805: ok，行数=1
- price_600241: ok，行数=1
- price_600327: ok，行数=1
- price_600358: ok，行数=1
- price_600558: ok，行数=1
- price_600630: ok，行数=1
- price_600778: ok，行数=1
- price_600802: ok，行数=1
- price_601188: ok，行数=1
- price_601366: ok，行数=1
- price_601566: ok，行数=1
- price_601595: ok，行数=1
- price_601999: ok，行数=1
- price_603016: ok，行数=1
- price_603096: ok，行数=1
- price_603108: ok，行数=1
- price_603110: ok，行数=1
- price_603138: ok，行数=1
- price_603171: ok，行数=1
- price_603258: ok，行数=1
- price_603289: ok，行数=1
- price_603383: ok，行数=1
- price_603402: ok，行数=1
- price_603466: ok，行数=1
- price_603533: ok，行数=1
- price_603628: ok，行数=1
- price_603633: ok，行数=1
- price_603636: ok，行数=1
- price_603713: ok，行数=1
- price_603721: ok，行数=1
- price_603755: ok，行数=1
- price_603863: ok，行数=1
- price_603880: ok，行数=1
- price_603887: ok，行数=1
- price_603906: ok，行数=1
- price_603989: ok，行数=1
- price_605189: ok，行数=1
- price_605303: ok，行数=1
- price_605333: ok，行数=1
- price_605378: ok，行数=1
- price_605388: ok，行数=1
- index_sh000001: ok，行数=1
- index_sz399001: ok，行数=1
- index_sz399006: ok，行数=1
- index_csi932000: ok，行数=1
