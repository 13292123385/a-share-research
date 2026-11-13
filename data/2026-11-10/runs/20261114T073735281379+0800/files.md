# 文件清单

| 路径 | 记录数 | 缺失字段（数量） |
|---|---:|---|
| clean/broken.csv | 15 | all_day_one_word:15, entry_price:15, height:15, last_seal:15, max_adverse_excursion:15, price_date:15, third_day_return:15 |
| clean/broken.json | 15 | all_day_one_word:15, entry_price:15, height:15, last_seal:15, max_adverse_excursion:15, price_date:15, third_day_return:15 |
| clean/candidate_prices.csv | 0 | 无 |
| clean/candidate_prices.json | 0 | 无 |
| clean/first_board_candidates.csv | 64 | entry_price:64, max_adverse_excursion:64, price_date:64, third_day_return:64 |
| clean/first_board_candidates.json | 64 | entry_price:64, max_adverse_excursion:64, price_date:64, third_day_return:64 |
| clean/first_board_followup.csv | 60 | entry_price:60, max_adverse_excursion:60, third_day_return:60 |
| clean/first_board_followup.json | 60 | entry_price:60, max_adverse_excursion:60, third_day_return:60 |
| clean/followup_prices.csv | 60 | 无 |
| clean/followup_prices.json | 60 | 无 |
| clean/indices.csv | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3, volume:2 |
| clean/indices.json | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3, volume:2 |
| clean/limit_up.csv | 84 | entry_price:84, max_adverse_excursion:84, price_date:84, third_day_return:84 |
| clean/limit_up.json | 84 | entry_price:84, max_adverse_excursion:84, price_date:84, third_day_return:84 |
| clean/market_quotes.csv | 5580 | quote_date:5579, quote_timestamp:5579, supplement_source:5579, volume_unit:5579, 买入:1, 卖出:1, 成交量:1, 时间戳:1, 昨收:1, 涨跌额:1 |
| clean/market_quotes.json | 5580 | quote_date:5579, quote_timestamp:5579, supplement_source:5579, volume_unit:5579, 买入:1, 卖出:1, 成交量:1, 时间戳:1, 昨收:1, 涨跌额:1 |
| clean/market_reconciliation.json | 1 | 无 |
| clean/promotion.json | 1 | verified_tradable_rate:1 |
| clean/promotion_rows.csv | 41 | entry_price:41, max_adverse_excursion:41, third_day_return:41 |
| clean/promotion_rows.json | 41 | entry_price:41, max_adverse_excursion:41, third_day_return:41 |
| clean/yesterday_pool.csv | 51 | all_day_one_word:51, entry_price:51, first_seal:51, height:51, last_seal:51, max_adverse_excursion:51, open_count:51, price_date:51, third_day_return:51 |
| clean/yesterday_pool.json | 51 | all_day_one_word:51, entry_price:51, first_seal:51, height:51, last_seal:51, max_adverse_excursion:51, open_count:51, price_date:51, third_day_return:51 |
| raw/broken.csv | 19 | 无 |
| raw/broken.json | 19 | 无 |
| raw/calendar.csv | 8797 | 无 |
| raw/calendar.json | 8797 | 无 |
| raw/index_fallback_sz399006.csv | 1 | 无 |
| raw/index_fallback_sz399006.json | 1 | 无 |
| raw/index_official_csi932000.csv | 1 | 无 |
| raw/index_official_csi932000.json | 1 | 无 |
| raw/index_sh000001.csv | 1 | 无 |
| raw/index_sh000001.json | 1 | 无 |
| raw/index_sz399001.csv | 1 | 无 |
| raw/index_sz399001.json | 1 | 无 |
| raw/limit_down.csv | 0 | 无 |
| raw/limit_down.json | 0 | 无 |
| raw/limit_up.csv | 93 | 无 |
| raw/limit_up.json | 93 | 无 |
| raw/official_szse_summary_retry.csv | 14 | 总市值:3, 流通市值:3 |
| raw/official_szse_summary_retry.json | 14 | 总市值:3, 流通市值:3 |
| raw/yesterday_pool.csv | 55 | 无 |
| raw/yesterday_pool.json | 55 | 无 |
| report.md | — | 无 |
| sources.json | 1 | 无 |
| summary.json | 1 | 无 |

来源及原始接口参数见 files.json 的 source_refs 与 sources.json；原始失败不视为空行情。
entry_price、third_day_return、max_adverse_excursion等未验证成交字段有意保留为空。
