# 2026-11-04 A股收盘复盘

状态：partial；抓取时间：2026-11-09T04:30:49.091489+08:00

采集范围：historical_pools_candidate_prices_indices；采集状态：partial；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 96, "mainboard_height": 3.0, "first_board_candidates": 84, "all_day_one_word_excluded": 2, "one_word_unknown": 8, "broken_count": 30, "limit_down_count": 10, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-04", "open": 3605.39, "close": 3686.17, "high": 3686.17, "low": 3590.8, "volume": 599394361, "amount": 953265155867.1}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-04", "open": 10895.8, "close": 11335.69, "high": 11362.9, "low": 10826.83, "volume": 682108330, "amount": 1084429058169.67}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-04", "open": 2399.46, "close": 2544.73, "high": 2559.09, "low": 2376.28, "volume": 228849025, "amount": 549329528581.74}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-04", "open": 2627.89, "close": 2713.36, "high": 2716.1, "low": 2590.63, "volume": 328077349, "amount": 391909041854.0}]}

## 估算值
{}

## 一进二
{"status": "missing_dependency", "observation_rate": null, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 全市场收盘快照；不跨日套用实时数据
- 候选股同日OHLC缺失8只（含预算未执行）
- 首板后续跟踪存在历史名单或价格缺失，详见followup
- 上一交易日已归档涨停池；昨日涨停接口不提供昨日连板高度，不能替代该依赖

## 候选股价格覆盖
{"historical_available": 88, "historical_fetched": 88, "reused": 0, "missing_codes": ["002652", "002827", "002992", "600892", "601123", "601599", "603381", "605577"], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 97, "prices_available": 69, "missing_archive_dates": ["2026-11-03"], "missing_price_codes": ["002623", "601595", "601599", "601999", "603016", "603096", "603108", "603110", "603138", "603171", "603258", "603383", "603466", "603533", "603628", "603633", "603636", "603713", "603721", "603755", "603863", "603880", "603887", "603989", "605189", "605303", "605333", "605577"], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"status": "not_applicable_historical", "all_market_verified": false, "note": "当前上市名单不能冒充历史名单；只对当日有效采集执行自动核验"}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=118
- yesterday_pool: ok，行数=48
- broken: ok，行数=33
- limit_down: ok，行数=10
- price_000017: ok，行数=1
- price_000096: ok，行数=1
- price_000426: ok，行数=1
- price_000506: ok，行数=1
- price_000530: ok，行数=1
- price_000603: ok，行数=1
- price_000657: ok，行数=1
- price_000919: ok，行数=1
- price_000962: ok，行数=1
- price_000975: ok，行数=1
- price_001233: ok，行数=1
- price_001282: ok，行数=1
- price_001337: ok，行数=1
- price_001339: ok，行数=1
- price_001359: ok，行数=1
- price_001360: ok，行数=1
- price_001389: ok，行数=1
- price_002008: ok，行数=1
- price_002081: ok，行数=1
- price_002155: ok，行数=1
- price_002156: ok，行数=1
- price_002222: ok，行数=1
- price_002275: ok，行数=1
- price_002309: ok，行数=1
- price_002317: ok，行数=1
- price_002353: ok，行数=1
- price_002364: ok，行数=1
- price_002371: ok，行数=1
- price_002388: ok，行数=1
- price_002409: ok，行数=1
- price_002428: ok，行数=1
- price_002436: ok，行数=1
- price_002463: ok，行数=1
- price_002529: ok，行数=1
- price_002536: ok，行数=1
- price_002565: ok，行数=1
- price_002636: ok，行数=1
- price_002674: ok，行数=1
- price_002716: ok，行数=1
- price_002741: ok，行数=1
- price_002811: ok，行数=1
- price_002821: ok，行数=1
- price_002876: ok，行数=1
- price_002916: ok，行数=1
- price_002971: ok，行数=1
- price_002975: ok，行数=1
- price_002980: ok，行数=1
- price_003021: ok，行数=1
- price_003033: ok，行数=1
- price_600206: ok，行数=1
- price_600371: ok，行数=1
- price_600391: ok，行数=1
- price_600547: ok，行数=1
- price_600584: ok，行数=1
- price_600641: ok，行数=1
- price_600699: ok，行数=1
- price_600988: ok，行数=1
- price_601069: ok，行数=1
- price_601208: ok，行数=1
- price_601212: ok，行数=1
- price_603048: ok，行数=1
- price_603061: ok，行数=1
- price_603115: ok，行数=1
- price_603127: ok，行数=1
- price_603186: ok，行数=1
- price_603203: ok，行数=1
- price_603248: ok，行数=1
- price_603256: ok，行数=1
- price_603259: ok，行数=1
- price_603283: ok，行数=1
- price_603598: ok，行数=1
- price_603657: ok，行数=1
- price_603662: ok，行数=1
- price_603767: ok，行数=1
- price_603773: ok，行数=1
- price_603777: ok，行数=1
- price_603893: ok，行数=1
- price_603950: ok，行数=1
- price_603955: ok，行数=1
- price_605111: ok，行数=1
- price_605287: ok，行数=1
- price_605288: ok，行数=1
- price_605376: ok，行数=1
- price_605488: ok，行数=1
- price_000679: ok，行数=1
- price_002058: ok，行数=1
- price_002088: ok，行数=1
- price_002578: ok，行数=1
- price_000037: ok，行数=1
- price_000156: ok，行数=1
- price_000599: ok，行数=1
- price_000607: ok，行数=1
- price_000678: ok，行数=1
- price_000681: ok，行数=1
- price_000819: ok，行数=1
- price_000892: ok，行数=1
- price_001216: ok，行数=1
- price_001225: ok，行数=1
- price_001230: ok，行数=1
- price_001266: ok，行数=1
- price_001330: ok，行数=1
- price_002029: ok，行数=1
- price_002045: ok，行数=1
- price_002094: ok，行数=1
- price_002095: ok，行数=1
- price_002174: ok，行数=1
- price_002181: ok，行数=1
- price_002187: ok，行数=1
- price_002238: ok，行数=1
- price_002291: ok，行数=1
- price_002292: ok，行数=1
- price_002362: ok，行数=1
- price_002368: ok，行数=1
- price_002425: ok，行数=1
- price_002558: ok，行数=1
- price_002623: empty_unverified，行数=0
- price_002712: ok，行数=1
- price_002827: ok，行数=1
- price_002929: ok，行数=1
- price_002940: ok，行数=1
- price_002949: ok，行数=1
- price_002983: ok，行数=1
- price_002995: ok，行数=1
- price_003019: ok，行数=1
- price_600020: ok，行数=1
- price_600088: ok，行数=1
- price_600109: ok，行数=1
- price_600199: ok，行数=1
- price_600229: ok，行数=1
- price_600259: ok，行数=1
- price_600293: ok，行数=1
- price_600299: ok，行数=1
- price_600345: ok，行数=1
- price_600506: ok，行数=1
- price_600556: ok，行数=1
- price_600570: ok，行数=1
- price_600576: ok，行数=1
- price_600633: ok，行数=1
- price_600640: ok，行数=1
- price_600715: ok，行数=1
- price_600754: ok，行数=1
- price_600779: ok，行数=1
- price_600801: ok，行数=1
- price_600865: ok，行数=1
- price_600892: ok，行数=1
- price_600960: ok，行数=1
- price_601019: ok，行数=1
- price_601086: ok，行数=1
- price_601099: ok，行数=1
- price_601339: ok，行数=1
- index_sh000001: ok，行数=1
- index_sz399001: ok，行数=1
- index_sz399006: ok，行数=1
- index_csi932000: ok，行数=1
