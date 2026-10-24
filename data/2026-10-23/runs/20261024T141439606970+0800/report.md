# 2026-10-23 A股收盘复盘

状态：partial；抓取时间：2026-10-24T14:14:39.606970+08:00

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 64, "mainboard_height": 6.0, "first_board_candidates": 53, "all_day_one_word_excluded": 0, "one_word_unknown": 64, "broken_count": 11, "limit_down_count": 6, "indices": []}

## 估算值
{}

## 一进二
{"status": "missing_dependency", "observation_rate": null, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 全市场收盘快照及历史OHLC；不跨日套用实时数据
- 上证指数指定日期收盘值
- 深证成指指定日期收盘值
- 创业板指指定日期收盘值
- 中证2000指定日期收盘值
- index_sh000001:error
- index_retry_sh000001:error
- index_fallback_sh000001:error
- index_sz399001:error
- index_retry_sz399001:error
- index_fallback_sz399001:error
- index_sz399006:error
- index_retry_sz399006:error
- index_fallback_sz399006:error
- index_csi932000:error
- index_retry_csi932000:error
- 上一交易日已归档涨停池；昨日涨停接口不提供昨日连板高度，不能替代该依赖

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=82
- yesterday_pool: ok，行数=33
- broken: ok，行数=12
- limit_down: ok，行数=6
- index_sh000001: error，行数=None
- index_retry_sh000001: error，行数=None
- index_fallback_sh000001: error，行数=None
- index_sz399001: error，行数=None
- index_retry_sz399001: error，行数=None
- index_fallback_sz399001: error，行数=None
- index_sz399006: error，行数=None
- index_retry_sz399006: error，行数=None
- index_fallback_sz399006: error，行数=None
- index_csi932000: error，行数=None
- index_retry_csi932000: error，行数=None
