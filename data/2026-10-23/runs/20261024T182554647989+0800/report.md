# 2026-10-23 A股收盘复盘

状态：partial；抓取时间：2026-10-24T18:25:54.647989+08:00

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 64, "mainboard_height": 6.0, "first_board_candidates": 53, "all_day_one_word_excluded": 1, "one_word_unknown": 20, "broken_count": 11, "limit_down_count": 6, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-10-23T00:00:00.000", "open": 3623.57, "close": 3690.48, "high": 3691.4, "low": 3574.27, "amount": 552842912.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-10-23T00:00:00.000", "open": 11187.55, "close": 11673.83, "high": 11707.15, "low": 11043.31, "amount": 690752095.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-10-23T00:00:00.000", "open": 2534.16, "close": 2684.1, "high": 2695.08, "low": 2494.22, "amount": 222875998.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-10-23T00:00:00.000", "close": 2856.27, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{}

## 一进二
{"status": "missing_dependency", "observation_rate": null, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 全市场收盘快照；不跨日套用实时数据
- 候选股同日OHLC缺失20只（含预算未执行）
- 首板后续跟踪存在历史名单或价格缺失，详见followup
- 上一交易日已归档涨停池；昨日涨停接口不提供昨日连板高度，不能替代该依赖

## 候选股价格覆盖
{"historical_available": 44, "historical_fetched": 44, "reused": 0, "missing_codes": ["603448", "603466", "603677", "603713", "603721", "603838", "603859", "603901", "605488", "000678", "002535", "002724", "003021", "600838", "603028", "603089", "603278", "603280", "603528", "603933"], "budget_seconds": 180, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

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
- price_000156: ok，行数=1
- price_000559: ok，行数=1
- price_000700: ok，行数=1
- price_000810: ok，行数=1
- price_000972: ok，行数=1
- price_001216: ok，行数=1
- price_001283: ok，行数=1
- price_001298: ok，行数=1
- price_001301: ok，行数=1
- price_001328: ok，行数=1
- price_001359: ok，行数=1
- price_002009: ok，行数=1
- price_002026: ok，行数=1
- price_002077: ok，行数=1
- price_002241: ok，行数=1
- price_002322: ok，行数=1
- price_002343: ok，行数=1
- price_002354: ok，行数=1
- price_002380: ok，行数=1
- price_002421: ok，行数=1
- price_002439: ok，行数=1
- price_002474: ok，行数=1
- price_002612: ok，行数=1
- price_002687: ok，行数=1
- price_002747: ok，行数=1
- price_002812: ok，行数=1
- price_002931: ok，行数=1
- price_002945: ok，行数=1
- price_002979: ok，行数=1
- price_002982: ok，行数=1
- price_002988: ok，行数=1
- price_600094: ok，行数=1
- price_600215: ok，行数=1
- price_600303: ok，行数=1
- price_600506: ok，行数=1
- price_600785: ok，行数=1
- price_600865: ok，行数=1
- price_601519: ok，行数=1
- price_603081: ok，行数=1
- price_603160: ok，行数=1
- price_603171: ok，行数=1
- price_603286: ok，行数=1
- price_603337: ok，行数=1
- price_603341: ok，行数=1
- price_603448: error，行数=None
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
