# 2026-11-06 A股收盘复盘

状态：complete_with_limitations；抓取时间：2026-11-18T22:06:30.948133+08:00

采集范围：historical_pools_candidate_prices_indices；采集状态：complete；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 29, "mainboard_height": 5.0, "first_board_candidates": 19, "all_day_one_word_excluded": 2, "one_word_unknown": 0, "broken_count": 12, "limit_down_count": 15, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-06", "open": 3612.15, "close": 3649.18, "high": 3660.49, "low": 3610.2, "volume": 477042561, "amount": 772634566231.1}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-06", "open": 11044.56, "close": 11175.78, "high": 11303.22, "low": 11044.56, "volume": 569400962, "amount": 885159900792.13}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-06T00:00:00.000", "open": 2438.72, "close": 2465.23, "high": 2506.97, "low": 2438.72, "amount": 181680656.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-06T00:00:00.000", "close": 2718.86, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{}

## 一进二
{"status": "observation_only", "denominator": 50, "promoted_count": 3, "broken_count": 2, "observation_rate": 0.06, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 全市场收盘快照；不跨日套用实时数据

## 候选股价格覆盖
{"historical_available": 29, "historical_fetched": 0, "reused": 29, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 135, "prices_available": 135, "missing_archive_dates": [], "missing_price_codes": [], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"status": "not_applicable_historical", "all_market_verified": false, "note": "当前上市名单不能冒充历史名单；只对当日有效采集执行自动核验"}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=32
- yesterday_pool: ok，行数=84
- broken: ok，行数=14
- limit_down: ok，行数=15
- index_sh000001: ok，行数=1
- index_sz399001: ok，行数=1
- index_sz399006: error，行数=None
- index_retry_sz399006: error，行数=None
- index_fallback_sz399006: ok，行数=1
- index_csi932000: error，行数=None
- index_retry_csi932000: error，行数=None
- index_official_csi932000: ok，行数=1
