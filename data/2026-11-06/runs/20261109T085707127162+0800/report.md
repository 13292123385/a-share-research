# 2026-11-06 A股收盘复盘

状态：complete_with_limitations；抓取时间：2026-11-09T08:57:07.127162+08:00

采集范围：historical_pools_candidate_prices_indices；采集状态：complete；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 29, "mainboard_height": 5.0, "first_board_candidates": 19, "all_day_one_word_excluded": 2, "one_word_unknown": 0, "broken_count": 12, "limit_down_count": 15, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-11-06", "open": 3612.15, "close": 3649.18, "high": 3660.49, "low": 3610.2, "volume": 477042561, "amount": 772634566231.1}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-11-06", "open": 11044.56, "close": 11175.78, "high": 11303.22, "low": 11044.56, "volume": 569400962, "amount": 885159900792.13}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-11-06", "open": 2438.72, "close": 2465.23, "high": 2506.97, "low": 2438.72, "volume": 189023618, "amount": 444017074033.47}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-11-06", "open": 2685.43, "close": 2718.86, "high": 2755.82, "low": 2684.93, "volume": 279135089, "amount": 324743813942.0}]}

## 估算值
{}

## 一进二
{"status": "observation_only", "denominator": 50, "promoted_count": 3, "broken_count": 2, "observation_rate": 0.06, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 全市场收盘快照；不跨日套用实时数据
- 首板后续跟踪存在历史名单或价格缺失，详见followup

## 候选股价格覆盖
{"historical_available": 29, "historical_fetched": 29, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 135, "prices_available": 77, "missing_archive_dates": [], "missing_price_codes": ["003033", "600206", "600391", "600396", "600481", "600539", "600547", "600569", "600584", "600641", "600683", "600699", "600865", "600986", "600988", "601069", "601208", "601212", "601929", "603048", "603061", "603068", "603098", "603115", "603127", "603151", "603185", "603186", "603203", "603212", "603248", "603256", "603259", "603283", "603297", "603313", "603500", "603598", "603662", "603682", "603699", "603737", "603767", "603773", "603777", "603876", "603893", "603950", "603955", "603956", "603990", "605069", "605111", "605188", "605287", "605288", "605376", "605488"], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"status": "not_applicable_historical", "all_market_verified": false, "note": "当前上市名单不能冒充历史名单；只对当日有效采集执行自动核验"}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=32
- yesterday_pool: ok，行数=84
- broken: ok，行数=14
- limit_down: ok，行数=15
- price_000525: ok，行数=1
- price_000595: ok，行数=1
- price_001258: ok，行数=1
- price_001308: ok，行数=1
- price_001316: ok，行数=1
- price_002310: ok，行数=1
- price_002712: ok，行数=1
- price_002889: ok，行数=1
- price_002973: ok，行数=1
- price_600156: ok，行数=1
- price_600207: ok，行数=1
- price_600229: ok，行数=1
- price_600278: ok，行数=1
- price_600327: ok，行数=1
- price_600371: ok，行数=1
- price_600540: ok，行数=1
- price_601188: ok，行数=1
- price_601595: ok，行数=1
- price_603366: ok，行数=1
- price_002086: ok，行数=1
- price_002088: ok，行数=1
- price_002388: ok，行数=1
- price_002578: ok，行数=1
- price_002929: ok，行数=1
- price_600261: ok，行数=1
- price_601599: ok，行数=1
- price_603381: ok，行数=1
- price_603657: ok，行数=1
- price_605339: ok，行数=1
- price_000017: ok，行数=1
- price_000029: ok，行数=1
- price_000096: ok，行数=1
- price_000426: ok，行数=1
- price_000428: ok，行数=1
- price_000506: ok，行数=1
- price_000530: ok，行数=1
- price_000533: ok，行数=1
- price_000603: ok，行数=1
- price_000635: ok，行数=1
- price_000657: ok，行数=1
- price_000700: ok，行数=1
- price_000710: ok，行数=1
- price_000889: ok，行数=1
- price_000919: ok，行数=1
- price_000962: ok，行数=1
- price_000975: ok，行数=1
- price_000995: ok，行数=1
- price_001233: ok，行数=1
- price_001269: ok，行数=1
- price_001282: ok，行数=1
- price_001330: ok，行数=1
- price_001337: ok，行数=1
- price_001339: ok，行数=1
- price_001359: ok，行数=1
- price_001360: ok，行数=1
- price_001389: ok，行数=1
- price_001393: ok，行数=1
- price_002008: ok，行数=1
- price_002045: ok，行数=1
- price_002081: ok，行数=1
- price_002131: ok，行数=1
- price_002135: ok，行数=1
- price_002155: ok，行数=1
- price_002156: ok，行数=1
- price_002222: ok，行数=1
- price_002275: ok，行数=1
- price_002307: ok，行数=1
- price_002309: ok，行数=1
- price_002313: ok，行数=1
- price_002317: ok，行数=1
- price_002318: ok，行数=1
- price_002343: ok，行数=1
- price_002353: ok，行数=1
- price_002364: ok，行数=1
- price_002371: ok，行数=1
- price_002409: ok，行数=1
- price_002421: ok，行数=1
- price_002428: ok，行数=1
- price_002436: ok，行数=1
- price_002463: ok，行数=1
- price_002506: ok，行数=1
- price_002529: ok，行数=1
- price_002536: ok，行数=1
- price_002565: ok，行数=1
- price_002596: ok，行数=1
- price_002636: ok，行数=1
- price_002674: ok，行数=1
- price_002716: ok，行数=1
- price_002741: ok，行数=1
- price_002773: ok，行数=1
- price_002811: ok，行数=1
- price_002821: ok，行数=1
- price_002865: ok，行数=1
- price_002876: ok，行数=1
- price_002916: ok，行数=1
- price_002971: ok，行数=1
- price_002975: ok，行数=1
- price_002980: ok，行数=1
- price_003021: ok，行数=1
- index_sh000001: ok，行数=1
- index_sz399001: ok，行数=1
- index_sz399006: ok，行数=1
- index_csi932000: ok，行数=1
