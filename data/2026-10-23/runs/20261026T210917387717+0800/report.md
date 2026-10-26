# 2026-10-23 A股收盘复盘

状态：complete_with_limitations；抓取时间：2026-10-26T21:09:17.387717+08:00

采集范围：historical_pools_candidate_prices_indices；采集状态：complete；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 64, "mainboard_height": 6.0, "first_board_candidates": 53, "all_day_one_word_excluded": 4, "one_word_unknown": 0, "broken_count": 11, "limit_down_count": 6, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-10-23T00:00:00.000", "open": 3623.57, "close": 3690.48, "high": 3691.4, "low": 3574.27, "amount": 552842912.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-10-23T00:00:00.000", "open": 11187.55, "close": 11673.83, "high": 11707.15, "low": 11043.31, "amount": 690752095.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-10-23T00:00:00.000", "open": 2534.16, "close": 2684.1, "high": 2695.08, "low": 2494.22, "amount": 222875998.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-10-23T00:00:00.000", "close": 2856.27, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{}

## 一进二
{"status": "missing_dependency", "observation_rate": null, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 全市场收盘快照；不跨日套用实时数据
- 首板后续跟踪存在历史名单或价格缺失，详见followup
- 上一交易日已归档涨停池；昨日涨停接口不提供昨日连板高度，不能替代该依赖

## 候选股价格覆盖
{"historical_available": 64, "historical_fetched": 20, "reused": 44, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 0, "prices_available": 0, "missing_archive_dates": ["2026-10-22", "2026-10-21"], "missing_price_codes": [], "budget_seconds": 90, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"status": "not_applicable_historical", "all_market_verified": false, "note": "当前上市名单不能冒充历史名单；只对当日有效采集执行自动核验"}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=82
- yesterday_pool: ok，行数=33
- broken: ok，行数=12
- limit_down: ok，行数=6
- price_603448: ok，行数=1
- price_603466: ok，行数=1
- price_603677: ok，行数=1
- price_603713: ok，行数=1
- price_603721: ok，行数=1
- price_603838: ok，行数=1
- price_603859: ok，行数=1
- price_603901: ok，行数=1
- price_605488: ok，行数=1
- price_000678: ok，行数=1
- price_002535: ok，行数=1
- price_002724: ok，行数=1
- price_003021: ok，行数=1
- price_600838: ok，行数=1
- price_603028: ok，行数=1
- price_603089: ok，行数=1
- price_603278: ok，行数=1
- price_603280: ok，行数=1
- price_603528: ok，行数=1
- price_603933: ok，行数=1
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
