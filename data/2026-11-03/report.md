# 2026-11-03 A股收盘复盘

状态：complete_with_limitations；抓取时间：2026-11-10T10:11:14.131654+08:00

采集范围：historical_pools_candidate_prices_indices；采集状态：complete；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 47, "mainboard_height": 4.0, "first_board_candidates": 32, "all_day_one_word_excluded": 7, "one_word_unknown": 0, "broken_count": 30, "limit_down_count": 13, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-03", "open": 3624.58, "close": 3608.1, "high": 3624.58, "low": 3580.38, "volume": 536848407, "amount": 810829284737.9}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-03", "open": 10934.3, "close": 10876.99, "high": 11093.06, "low": 10810.42, "volume": 579125890, "amount": 892607522375.23}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-03", "open": 2429.77, "close": 2391.65, "high": 2471.9, "low": 2376.39, "volume": 189159425, "amount": 448863579984.34}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-03", "open": 2661.62, "close": 2623.84, "high": 2703.93, "low": 2606.4, "volume": 282057311, "amount": 328348660627.0}]}

## 估算值
{}

## 一进二
{"status": "observation_only", "denominator": 92, "promoted_count": 8, "broken_count": 10, "observation_rate": 0.08695652173913043, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 全市场收盘快照；不跨日套用实时数据
- 首板后续跟踪存在历史名单或价格缺失，详见followup

## 候选股价格覆盖
{"historical_available": 47, "historical_fetched": 47, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 130, "prices_available": 74, "missing_archive_dates": [], "missing_price_codes": ["002623", "600345", "600506", "600510", "600556", "600570", "600576", "600633", "600640", "600721", "600754", "600779", "600801", "600865", "600960", "601019", "601083", "601086", "601099", "601339", "601595", "601999", "603016", "603029", "603096", "603108", "603110", "603138", "603171", "603198", "603200", "603233", "603273", "603383", "603466", "603533", "603587", "603598", "603628", "603633", "603636", "603713", "603721", "603755", "603863", "603880", "603887", "603955", "603989", "605058", "605169", "605189", "605287", "605288", "605303", "605333"], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"status": "not_applicable_historical", "all_market_verified": false, "note": "当前上市名单不能冒充历史名单；只对当日有效采集执行自动核验"}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=48
- yesterday_pool: ok，行数=124
- broken: ok，行数=34
- limit_down: ok，行数=17
- price_000151: ok，行数=1
- price_000591: ok，行数=1
- price_000608: ok，行数=1
- price_000679: ok，行数=1
- price_001318: ok，行数=1
- price_002088: ok，行数=1
- price_002105: ok，行数=1
- price_002300: ok，行数=1
- price_002522: ok，行数=1
- price_002580: ok，行数=1
- price_002652: ok，行数=1
- price_002692: ok，行数=1
- price_002696: ok，行数=1
- price_002805: ok，行数=1
- price_002992: ok，行数=1
- price_600241: ok，行数=1
- price_600327: ok，行数=1
- price_600358: ok，行数=1
- price_600558: ok，行数=1
- price_600630: ok，行数=1
- price_600778: ok，行数=1
- price_600802: ok，行数=1
- price_601123: ok，行数=1
- price_601188: ok，行数=1
- price_601366: ok，行数=1
- price_601566: ok，行数=1
- price_603289: ok，行数=1
- price_603381: ok，行数=1
- price_603402: ok，行数=1
- price_603906: ok，行数=1
- price_605378: ok，行数=1
- price_605388: ok，行数=1
- price_000599: ok，行数=1
- price_000995: ok，行数=1
- price_002029: ok，行数=1
- price_002058: ok，行数=1
- price_002086: ok，行数=1
- price_002292: ok，行数=1
- price_002578: ok，行数=1
- price_002827: ok，行数=1
- price_600261: ok，行数=1
- price_600293: ok，行数=1
- price_600715: ok，行数=1
- price_600892: ok，行数=1
- price_601599: ok，行数=1
- price_603258: ok，行数=1
- price_605577: ok，行数=1
- price_000037: ok，行数=1
- price_000156: ok，行数=1
- price_000410: ok，行数=1
- price_000417: ok，行数=1
- price_000525: ok，行数=1
- price_000530: ok，行数=1
- price_000568: ok，行数=1
- price_000596: ok，行数=1
- price_000607: ok，行数=1
- price_000676: ok，行数=1
- price_000678: ok，行数=1
- price_000681: ok，行数=1
- price_000716: ok，行数=1
- price_000819: ok，行数=1
- price_000892: ok，行数=1
- price_000897: ok，行数=1
- price_001216: ok，行数=1
- price_001225: ok，行数=1
- price_001230: ok，行数=1
- price_001266: ok，行数=1
- price_001287: ok，行数=1
- price_001330: ok，行数=1
- price_002045: ok，行数=1
- price_002094: ok，行数=1
- price_002095: ok，行数=1
- price_002174: ok，行数=1
- price_002181: ok，行数=1
- price_002187: ok，行数=1
- price_002238: ok，行数=1
- price_002291: ok，行数=1
- price_002362: ok，行数=1
- price_002365: ok，行数=1
- price_002368: ok，行数=1
- price_002425: ok，行数=1
- price_002432: ok，行数=1
- price_002558: ok，行数=1
- price_002582: ok，行数=1
- price_002623: empty_unverified，行数=0
- price_002636: ok，行数=1
- price_002712: ok，行数=1
- price_002811: ok，行数=1
- price_002929: ok，行数=1
- price_002940: ok，行数=1
- price_002946: ok，行数=1
- price_002949: ok，行数=1
- price_002983: ok，行数=1
- price_002995: ok，行数=1
- price_003019: ok，行数=1
- price_600020: ok，行数=1
- price_600088: ok，行数=1
- price_600109: ok，行数=1
- price_600113: ok，行数=1
- price_600189: ok，行数=1
- price_600199: ok，行数=1
- price_600215: ok，行数=1
- price_600229: ok，行数=1
- price_600258: ok，行数=1
- price_600259: ok，行数=1
- price_600285: ok，行数=1
- price_600299: ok，行数=1
- index_sh000001: ok，行数=1
- index_sz399001: ok，行数=1
- index_sz399006: ok，行数=1
- index_csi932000: ok，行数=1
