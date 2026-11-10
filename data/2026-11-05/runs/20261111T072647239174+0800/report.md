# 2026-11-05 A股收盘复盘

状态：partial；抓取时间：2026-11-11T07:26:47.239174+08:00

采集范围：historical_pools_candidate_prices_indices；采集状态：partial；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"broken_count": 43, "limit_down_count": null, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-05", "open": 3646.57, "close": 3689.91, "high": 3701.59, "low": 3646.57, "volume": 571291638, "amount": 979711778222.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-05", "open": 11216.81, "close": 11471.09, "high": 11613.4, "low": 11215.48, "volume": 672558794, "amount": 1138241322280.09}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-05", "open": 2493.73, "close": 2566.8, "high": 2625.98, "low": 2493.67, "volume": 231283658, "amount": 578564247279.27}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-05", "open": 2690.27, "close": 2785.55, "high": 2798.18, "low": 2689.07, "volume": 318988132, "amount": 397301287111.0}]}

## 估算值
{}

## 一进二
{"status": "missing_dependency", "observation_rate": null, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 全市场收盘快照；不跨日套用实时数据
- 首板后续跟踪存在历史名单或价格缺失，详见followup
- limit_up:schema_error
- limit_down:empty_unverified

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 116, "prices_available": 88, "missing_archive_dates": [], "missing_price_codes": ["601208", "601212", "601366", "601566", "603048", "603061", "603115", "603127", "603186", "603203", "603248", "603256", "603259", "603283", "603289", "603402", "603662", "603767", "603773", "603777", "603906", "603950", "603955", "605111", "605288", "605376", "605378", "605388"], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"status": "not_applicable_historical", "all_market_verified": false, "note": "当前上市名单不能冒充历史名单；只对当日有效采集执行自动核验"}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: schema_error，行数=84
- yesterday_pool: ok，行数=118
- broken: ok，行数=48
- limit_down: empty_unverified，行数=0
- price_000096: ok，行数=1
- price_000151: ok，行数=1
- price_000426: ok，行数=1
- price_000506: ok，行数=1
- price_000530: ok，行数=1
- price_000591: ok，行数=1
- price_000608: ok，行数=1
- price_000657: ok，行数=1
- price_000679: ok，行数=1
- price_000919: ok，行数=1
- price_000962: ok，行数=1
- price_000975: ok，行数=1
- price_001233: ok，行数=1
- price_001282: ok，行数=1
- price_001318: ok，行数=1
- price_001337: ok，行数=1
- price_001339: ok，行数=1
- price_001359: ok，行数=1
- price_001389: ok，行数=1
- price_002008: ok，行数=1
- price_002105: ok，行数=1
- price_002155: ok，行数=1
- price_002156: ok，行数=1
- price_002222: ok，行数=1
- price_002275: ok，行数=1
- price_002300: ok，行数=1
- price_002317: ok，行数=1
- price_002353: ok，行数=1
- price_002364: ok，行数=1
- price_002371: ok，行数=1
- price_002409: ok，行数=1
- price_002428: ok，行数=1
- price_002436: ok，行数=1
- price_002463: ok，行数=1
- price_002522: ok，行数=1
- price_002536: ok，行数=1
- price_002580: ok，行数=1
- price_002636: ok，行数=1
- price_002652: ok，行数=1
- price_002674: ok，行数=1
- price_002692: ok，行数=1
- price_002696: ok，行数=1
- price_002716: ok，行数=1
- price_002741: ok，行数=1
- price_002805: ok，行数=1
- price_002811: ok，行数=1
- price_002821: ok，行数=1
- price_002876: ok，行数=1
- price_002916: ok，行数=1
- price_002971: ok，行数=1
- price_002975: ok，行数=1
- price_002980: ok，行数=1
- price_002992: ok，行数=1
- price_003021: ok，行数=1
- price_600241: ok，行数=1
- price_600327: ok，行数=1
- price_600358: ok，行数=1
- price_600371: ok，行数=1
- price_600391: ok，行数=1
- price_600547: ok，行数=1
- price_600558: ok，行数=1
- price_600584: ok，行数=1
- price_600630: ok，行数=1
- price_600699: ok，行数=1
- price_600778: ok，行数=1
- price_600802: ok，行数=1
- price_600988: ok，行数=1
- price_601069: ok，行数=1
- price_601123: ok，行数=1
- price_601188: ok，行数=1
- index_sh000001: ok，行数=1
- index_sz399001: ok，行数=1
- index_sz399006: ok，行数=1
- index_csi932000: ok，行数=1
