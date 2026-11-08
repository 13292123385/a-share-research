# 2026-11-05 A股收盘复盘

状态：partial；抓取时间：2026-11-08T22:58:11.925838+08:00

采集范围：historical_pools_candidate_prices_indices；采集状态：partial；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 71, "mainboard_height": 4.0, "first_board_candidates": 51, "all_day_one_word_excluded": 5, "one_word_unknown": 0, "broken_count": 43, "limit_down_count": null, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-05", "open": 3646.57, "close": 3689.91, "high": 3701.59, "low": 3646.57, "volume": 571291638, "amount": 979711778222.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-05T00:00:00.000", "open": 11216.81, "close": 11471.09, "high": 11613.4, "low": 11215.48, "amount": 672558794.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-05T00:00:00.000", "open": 2493.73, "close": 2566.8, "high": 2625.98, "low": 2493.67, "amount": 225321557.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-05T00:00:00.000", "close": 2785.55, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{}

## 一进二
{"status": "missing_dependency", "observation_rate": null, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 全市场收盘快照；不跨日套用实时数据
- 首板后续跟踪存在历史名单或价格缺失，详见followup
- limit_down:empty_unverified
- 上一交易日已归档涨停池；昨日涨停接口不提供昨日连板高度，不能替代该依赖

## 候选股价格覆盖
{"historical_available": 71, "historical_fetched": 71, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 0, "prices_available": 0, "missing_archive_dates": ["2026-11-04", "2026-11-03"], "missing_price_codes": [], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"status": "not_applicable_historical", "all_market_verified": false, "note": "当前上市名单不能冒充历史名单；只对当日有效采集执行自动核验"}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=84
- yesterday_pool: ok，行数=118
- broken: ok，行数=48
- limit_down: empty_unverified，行数=0
- price_000029: ok，行数=1
- price_000428: ok，行数=1
- price_000533: ok，行数=1
- price_000635: ok，行数=1
- price_000700: ok，行数=1
- price_000710: ok，行数=1
- price_000889: ok，行数=1
- price_000995: ok，行数=1
- price_001269: ok，行数=1
- price_001330: ok，行数=1
- price_001393: ok，行数=1
- price_002045: ok，行数=1
- price_002086: ok，行数=1
- price_002131: ok，行数=1
- price_002135: ok，行数=1
- price_002307: ok，行数=1
- price_002313: ok，行数=1
- price_002318: ok，行数=1
- price_002343: ok，行数=1
- price_002421: ok，行数=1
- price_002506: ok，行数=1
- price_002596: ok，行数=1
- price_002773: ok，行数=1
- price_002865: ok，行数=1
- price_002929: ok，行数=1
- price_600261: ok，行数=1
- price_600396: ok，行数=1
- price_600481: ok，行数=1
- price_600539: ok，行数=1
- price_600569: ok，行数=1
- price_600683: ok，行数=1
- price_600865: ok，行数=1
- price_600986: ok，行数=1
- price_601929: ok，行数=1
- price_603068: ok，行数=1
- price_603098: ok，行数=1
- price_603151: ok，行数=1
- price_603185: ok，行数=1
- price_603212: ok，行数=1
- price_603297: ok，行数=1
- price_603313: ok，行数=1
- price_603500: ok，行数=1
- price_603682: ok，行数=1
- price_603699: ok，行数=1
- price_603737: ok，行数=1
- price_603876: ok，行数=1
- price_603956: ok，行数=1
- price_603990: ok，行数=1
- price_605069: ok，行数=1
- price_605188: ok，行数=1
- price_605339: ok，行数=1
- price_000017: ok，行数=1
- price_000603: ok，行数=1
- price_001360: ok，行数=1
- price_002081: ok，行数=1
- price_002088: ok，行数=1
- price_002309: ok，行数=1
- price_002388: ok，行数=1
- price_002529: ok，行数=1
- price_002565: ok，行数=1
- price_002578: ok，行数=1
- price_003033: ok，行数=1
- price_600206: ok，行数=1
- price_600641: ok，行数=1
- price_601599: ok，行数=1
- price_603381: ok，行数=1
- price_603598: ok，行数=1
- price_603657: ok，行数=1
- price_603893: ok，行数=1
- price_605287: ok，行数=1
- price_605488: ok，行数=1
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
