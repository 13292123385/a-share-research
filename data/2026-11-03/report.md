# 2026-11-03 A股收盘复盘

状态：complete_with_limitations；抓取时间：2026-11-14T01:48:08.217307+08:00

采集范围：historical_pools_candidate_prices_indices；采集状态：complete；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 47, "mainboard_height": 4.0, "first_board_candidates": 32, "all_day_one_word_excluded": 7, "one_word_unknown": 0, "broken_count": 30, "limit_down_count": 13, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-03T00:00:00.000", "open": 3624.58, "close": 3608.1, "high": 3624.58, "low": 3580.38, "amount": 536848407.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-03T00:00:00.000", "open": 10934.3, "close": 10876.99, "high": 11093.06, "low": 10810.42, "amount": 579125890.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-03T00:00:00.000", "open": 2429.77, "close": 2391.65, "high": 2471.9, "low": 2376.39, "amount": 182783959.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-03T00:00:00.000", "close": 2623.84, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{}

## 一进二
{"status": "observation_only", "denominator": 92, "promoted_count": 8, "broken_count": 10, "observation_rate": 0.08695652173913043, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 全市场收盘快照；不跨日套用实时数据
- 首板后续跟踪存在历史名单或价格缺失，详见followup

## 候选股价格覆盖
{"historical_available": 47, "historical_fetched": 0, "reused": 47, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 130, "prices_available": 129, "missing_archive_dates": [], "missing_price_codes": ["002623"], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"status": "not_applicable_historical", "all_market_verified": false, "note": "当前上市名单不能冒充历史名单；只对当日有效采集执行自动核验"}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=48
- yesterday_pool: ok，行数=124
- broken: ok，行数=34
- limit_down: ok，行数=17
- price_002623: empty_unverified，行数=0
- price_600345: ok，行数=1
- price_600506: ok，行数=1
- price_600510: ok，行数=1
- price_600556: ok，行数=1
- price_600570: ok，行数=1
- price_600576: ok，行数=1
- price_600633: ok，行数=1
- price_600640: ok，行数=1
- price_600721: ok，行数=1
- price_600754: ok，行数=1
- price_600779: ok，行数=1
- price_600801: ok，行数=1
- price_600865: ok，行数=1
- price_600960: ok，行数=1
- price_601019: ok，行数=1
- price_601083: ok，行数=1
- price_601086: ok，行数=1
- price_601099: ok，行数=1
- price_601339: ok，行数=1
- price_601595: ok，行数=1
- price_601999: ok，行数=1
- price_603016: ok，行数=1
- price_603029: ok，行数=1
- price_603096: ok，行数=1
- price_603108: ok，行数=1
- price_603110: ok，行数=1
- price_603138: ok，行数=1
- price_603171: ok，行数=1
- price_603198: ok，行数=1
- price_603200: ok，行数=1
- price_603233: ok，行数=1
- price_603273: ok，行数=1
- price_603383: ok，行数=1
- price_603466: ok，行数=1
- price_603533: ok，行数=1
- price_603587: ok，行数=1
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
- price_605058: ok，行数=1
- price_605169: ok，行数=1
- price_605189: ok，行数=1
- price_605287: ok，行数=1
- price_605288: ok，行数=1
- price_605303: ok，行数=1
- price_605333: ok，行数=1
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
