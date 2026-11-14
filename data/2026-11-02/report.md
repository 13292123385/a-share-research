# 2026-11-02 A股收盘复盘

状态：complete_with_limitations；抓取时间：2026-11-14T14:32:10.118143+08:00

采集范围：historical_pools_candidate_prices_indices；采集状态：complete；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 108, "mainboard_height": 6.0, "first_board_candidates": 97, "all_day_one_word_excluded": 5, "one_word_unknown": 0, "broken_count": 22, "limit_down_count": 7, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-02", "open": 3614.31, "close": 3638.03, "high": 3648.13, "low": 3594.77, "volume": 565372836, "amount": 847459066880.8}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-02", "open": 10897.5, "close": 11010.68, "high": 11112.64, "low": 10813.16, "volume": 630746118, "amount": 936236271283.87}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-02T00:00:00.000", "open": 2439.08, "close": 2458.7, "high": 2500.14, "low": 2406.97, "amount": 206324226.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-02T00:00:00.000", "close": 2681.29, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{}

## 一进二
{"status": "observation_only", "denominator": 32, "promoted_count": 5, "broken_count": 3, "observation_rate": 0.15625, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 全市场收盘快照；不跨日套用实时数据

## 候选股价格覆盖
{"historical_available": 108, "historical_fetched": 0, "reused": 108, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

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
- index_sh000001: ok，行数=1
- index_sz399001: ok，行数=1
- index_sz399006: error，行数=None
- index_retry_sz399006: error，行数=None
- index_fallback_sz399006: ok，行数=1
- index_csi932000: error，行数=None
- index_retry_csi932000: error，行数=None
- index_official_csi932000: ok，行数=1
