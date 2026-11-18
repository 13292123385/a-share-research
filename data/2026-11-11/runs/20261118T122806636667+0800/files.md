# 文件清单

| 路径 | 记录数 | 缺失字段（数量） |
|---|---:|---|
| clean/broken.csv | 19 | all_day_one_word:19, entry_price:19, height:19, last_seal:19, max_adverse_excursion:19, price_date:19, third_day_return:19 |
| clean/broken.json | 19 | all_day_one_word:19, entry_price:19, height:19, last_seal:19, max_adverse_excursion:19, price_date:19, third_day_return:19 |
| clean/candidate_prices.csv | 0 | 无 |
| clean/candidate_prices.json | 0 | 无 |
| clean/first_board_candidates.csv | 57 | entry_price:57, max_adverse_excursion:57, price_date:57, third_day_return:57 |
| clean/first_board_candidates.json | 57 | entry_price:57, max_adverse_excursion:57, price_date:57, third_day_return:57 |
| clean/first_board_followup.csv | 105 | entry_price:105, max_adverse_excursion:105, third_day_return:105 |
| clean/first_board_followup.json | 105 | entry_price:105, max_adverse_excursion:105, third_day_return:105 |
| clean/followup_prices.csv | 105 | 无 |
| clean/followup_prices.json | 105 | 无 |
| clean/indices.csv | 4 | 无 |
| clean/indices.json | 4 | 无 |
| clean/limit_up.csv | 76 | entry_price:76, max_adverse_excursion:76, price_date:76, third_day_return:76 |
| clean/limit_up.json | 76 | entry_price:76, max_adverse_excursion:76, price_date:76, third_day_return:76 |
| clean/market_quotes.csv | 5355 | quote_date:5350, quote_timestamp:5350, supplement_source:5350, volume_unit:5350, 买入:5, 卖出:5, 成交量:5, 时间戳:5, 昨收:5, 涨跌额:5 |
| clean/market_quotes.json | 5355 | quote_date:5350, quote_timestamp:5350, supplement_source:5350, volume_unit:5350, 买入:5, 卖出:5, 成交量:5, 时间戳:5, 昨收:5, 涨跌额:5 |
| clean/market_reconciliation.json | 1 | 无 |
| clean/promotion.json | 1 | verified_tradable_rate:1 |
| clean/promotion_rows.csv | 64 | entry_price:64, max_adverse_excursion:64, third_day_return:64 |
| clean/promotion_rows.json | 64 | entry_price:64, max_adverse_excursion:64, third_day_return:64 |
| clean/yesterday_pool.csv | 84 | all_day_one_word:84, amount:1, close:1, entry_price:84, first_seal:84, height:84, high:1, last_seal:84, low:1, max_adverse_excursion:84, open:1, open_count:84, price_date:83, price_source:1, third_day_return:84, volume:2 |
| clean/yesterday_pool.json | 84 | all_day_one_word:84, amount:1, close:1, entry_price:84, first_seal:84, height:84, high:1, last_seal:84, low:1, max_adverse_excursion:84, open:1, open_count:84, price_date:83, price_source:1, third_day_return:84, volume:2 |
| raw/broken.csv | 19 | 无 |
| raw/broken.json | 19 | 无 |
| raw/calendar.csv | 8797 | 无 |
| raw/calendar.json | 8797 | 无 |
| raw/index_csi932000.csv | 1 | 无 |
| raw/index_csi932000.json | 1 | 无 |
| raw/index_sh000001.csv | 1 | 无 |
| raw/index_sh000001.json | 1 | 无 |
| raw/index_sz399001.csv | 1 | 无 |
| raw/index_sz399001.json | 1 | 无 |
| raw/index_sz399006.csv | 1 | 无 |
| raw/index_sz399006.json | 1 | 无 |
| raw/limit_down.csv | 0 | 无 |
| raw/limit_down.json | 0 | 无 |
| raw/limit_up.csv | 85 | 无 |
| raw/limit_up.json | 85 | 无 |
| raw/official_szse_summary_retry.csv | 14 | 总市值:3, 流通市值:3 |
| raw/official_szse_summary_retry.json | 14 | 总市值:3, 流通市值:3 |
| raw/yesterday_pool.csv | 93 | 无 |
| raw/yesterday_pool.json | 93 | 无 |
| report.md | — | 无 |
| sources.json | 1 | 无 |
| summary.json | 1 | 无 |

来源及原始接口参数见 files.json 的 source_refs 与 sources.json；原始失败不视为空行情。
entry_price、third_day_return、max_adverse_excursion等未验证成交字段有意保留为空。
