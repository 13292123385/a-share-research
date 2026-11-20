# 2026-11-05 A股收盘复盘

状态：partial；抓取时间：2026-11-21T05:11:07.836913+08:00

采集范围：historical_pools_candidate_prices_indices；采集状态：partial；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"broken_count": 43, "limit_down_count": null, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-05", "open": 3646.57, "close": 3689.91, "high": 3701.59, "low": 3646.57, "volume": 571291638, "amount": 979711778222.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-05", "open": 11216.81, "close": 11471.09, "high": 11613.4, "low": 11215.48, "volume": 672558794, "amount": 1138241322280.09}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-05T00:00:00.000", "open": 2493.73, "close": 2566.8, "high": 2625.98, "low": 2493.67, "amount": 225321557.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-05T00:00:00.000", "close": 2785.55, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{}

## 一进二
{"status": "missing_dependency", "observation_rate": null, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 全市场收盘快照；不跨日套用实时数据
- limit_up:schema_error
- limit_down:empty_unverified

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 116, "prices_available": 116, "missing_archive_dates": [], "missing_price_codes": [], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"status": "not_applicable_historical", "all_market_verified": false, "note": "当前上市名单不能冒充历史名单；只对当日有效采集执行自动核验"}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: schema_error，行数=84
- yesterday_pool: ok，行数=118
- broken: ok，行数=48
- limit_down: empty_unverified，行数=0
- price_601188: ok，行数=1
- price_601208: ok，行数=1
- price_601212: ok，行数=1
- price_601366: ok，行数=1
- price_601566: ok，行数=1
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
- price_603289: ok，行数=1
- price_603402: ok，行数=1
- price_603662: ok，行数=1
- price_603767: ok，行数=1
- price_603773: ok，行数=1
- price_603777: ok，行数=1
- price_603906: ok，行数=1
- price_603950: ok，行数=1
- price_603955: ok，行数=1
- price_605111: ok，行数=1
- price_605288: ok，行数=1
- price_605376: ok，行数=1
- price_605378: ok，行数=1
- price_605388: ok，行数=1
- index_sh000001: ok，行数=1
- index_sz399001: ok，行数=1
- index_sz399006: error，行数=None
- index_retry_sz399006: error，行数=None
- index_fallback_sz399006: ok，行数=1
- index_csi932000: error，行数=None
- index_retry_csi932000: error，行数=None
- index_official_csi932000: ok，行数=1
