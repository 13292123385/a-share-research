# 2026-11-02 A股收盘复盘

状态：partial；抓取时间：2026-11-05T00:22:49.485069+08:00

采集范围：historical_pools_candidate_prices_indices；采集状态：partial；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 108, "mainboard_height": 6.0, "first_board_candidates": 97, "all_day_one_word_excluded": 3, "one_word_unknown": 8, "broken_count": 22, "limit_down_count": 7, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-02", "open": 3614.31, "close": 3638.03, "high": 3648.13, "low": 3594.77, "volume": 565372836, "amount": 847459066880.8}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-02", "open": 10897.5, "close": 11010.68, "high": 11112.64, "low": 10813.16, "volume": 630746118, "amount": 936236271283.87}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-02", "open": 2439.08, "close": 2458.7, "high": 2500.14, "low": 2406.97, "volume": 211432374, "amount": 468709211615.64}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-02", "open": 2626.73, "close": 2681.29, "high": 2693.93, "low": 2576.02, "volume": 300109838, "amount": 354623963703.0}]}

## 估算值
{}

## 一进二
{"status": "observation_only", "denominator": 29, "promoted_count": 2, "broken_count": 3, "observation_rate": 0.06896551724137931, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 全市场收盘快照；不跨日套用实时数据
- 候选股同日OHLC缺失8只（含预算未执行）

## 候选股价格覆盖
{"historical_available": 100, "historical_fetched": 100, "reused": 0, "missing_codes": ["000995", "001219", "002086", "002172", "002275", "600189", "600261", "603587"], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 61, "prices_available": 61, "missing_archive_dates": [], "missing_price_codes": [], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"status": "not_applicable_historical", "all_market_verified": false, "note": "当前上市名单不能冒充历史名单；只对当日有效采集执行自动核验"}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=125
- yesterday_pool: ok，行数=47
- broken: ok，行数=28
- limit_down: ok，行数=8
- price_000037: ok，行数=1
- price_000156: ok，行数=1
- price_000530: ok，行数=1
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
- price_002058: ok，行数=1
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
- price_002578: ok，行数=1
- price_002623: ok，行数=1
- price_002712: ok，行数=1
- price_002811: ok，行数=1
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
- price_601595: ok，行数=1
- price_601599: ok，行数=1
- price_601999: ok，行数=1
- price_603016: ok，行数=1
- price_603096: ok，行数=1
- price_603108: ok，行数=1
- price_603110: ok，行数=1
- price_603138: ok，行数=1
- price_603171: ok，行数=1
- price_603258: ok，行数=1
- price_603383: ok，行数=1
- price_603466: ok，行数=1
- price_603533: ok，行数=1
- price_603598: ok，行数=1
- price_603628: ok，行数=1
- price_603633: ok，行数=1
- price_603636: ok，行数=1
- price_603713: ok，行数=1
- price_603721: ok，行数=1
- price_603755: ok，行数=1
- price_603863: ok，行数=1
- price_603880: ok，行数=1
- price_603887: ok，行数=1
- price_603955: ok，行数=1
- price_603989: ok，行数=1
- price_605189: ok，行数=1
- price_605287: ok，行数=1
- price_605288: ok，行数=1
- price_605303: ok，行数=1
- price_605333: ok，行数=1
- price_605577: ok，行数=1
- price_000410: ok，行数=1
- price_000417: ok，行数=1
- price_000525: ok，行数=1
- price_000568: ok，行数=1
- price_000596: ok，行数=1
- price_000676: ok，行数=1
- price_000701: ok，行数=1
- price_000716: ok，行数=1
- price_000897: ok，行数=1
- price_000995: ok，行数=1
- price_001287: ok，行数=1
- price_002086: ok，行数=1
- price_002088: ok，行数=1
- price_002149: ok，行数=1
- price_002275: ok，行数=1
- price_002277: ok，行数=1
- price_002365: ok，行数=1
- price_002432: ok，行数=1
- price_002531: ok，行数=1
- price_002565: ok，行数=1
- price_002582: ok，行数=1
- price_002636: ok，行数=1
- price_002652: ok，行数=1
- price_002679: ok，行数=1
- price_002865: ok，行数=1
- price_002946: ok，行数=1
- price_003032: ok，行数=1
- price_600113: ok，行数=1
- price_600118: ok，行数=1
- price_600189: ok，行数=1
- price_600215: ok，行数=1
- price_600258: ok，行数=1
- price_600261: ok，行数=1
- price_600285: ok，行数=1
- price_600428: ok，行数=1
- price_600501: ok，行数=1
- price_600510: ok，行数=1
- price_600592: ok，行数=1
- price_600643: ok，行数=1
- price_600721: ok，行数=1
- price_600997: ok，行数=1
- price_601083: ok，行数=1
- price_601188: ok，行数=1
- price_603029: ok，行数=1
- price_603103: ok，行数=1
- price_603198: ok，行数=1
- price_603200: ok，行数=1
- price_603233: ok，行数=1
- price_603273: ok，行数=1
- price_603382: ok，行数=1
- price_603536: ok，行数=1
- price_603587: ok，行数=1
- price_603703: ok，行数=1
- price_605058: ok，行数=1
- price_605169: ok，行数=1
- price_605179: ok，行数=1
- price_605338: ok，行数=1
- price_605598: ok，行数=1
- index_sh000001: ok，行数=1
- index_sz399001: ok，行数=1
- index_sz399006: ok，行数=1
- index_csi932000: ok，行数=1
