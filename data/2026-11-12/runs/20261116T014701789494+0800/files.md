# 文件清单

| 路径 | 记录数 | 缺失字段（数量） |
|---|---:|---|
| clean/broken.csv | 33 | all_day_one_word:33, entry_price:33, height:33, last_seal:33, max_adverse_excursion:33, price_date:33, third_day_return:33 |
| clean/broken.json | 33 | all_day_one_word:33, entry_price:33, height:33, last_seal:33, max_adverse_excursion:33, price_date:33, third_day_return:33 |
| clean/candidate_prices.csv | 0 | 无 |
| clean/candidate_prices.json | 0 | 无 |
| clean/first_board_candidates.csv | 26 | entry_price:26, max_adverse_excursion:26, price_date:26, third_day_return:26 |
| clean/first_board_candidates.json | 26 | entry_price:26, max_adverse_excursion:26, price_date:26, third_day_return:26 |
| clean/first_board_followup.csv | 121 | entry_price:121, max_adverse_excursion:121, third_day_return:121 |
| clean/first_board_followup.json | 121 | entry_price:121, max_adverse_excursion:121, third_day_return:121 |
| clean/followup_prices.csv | 121 | 无 |
| clean/followup_prices.json | 121 | 无 |
| clean/indices.csv | 3 | 无 |
| clean/indices.json | 3 | 无 |
| clean/limit_down.csv | 5 | all_day_one_word:5, entry_price:5, first_seal:5, height:5, max_adverse_excursion:5, open_count:5, price_date:5, third_day_return:5 |
| clean/limit_down.json | 5 | all_day_one_word:5, entry_price:5, first_seal:5, height:5, max_adverse_excursion:5, open_count:5, price_date:5, third_day_return:5 |
| clean/limit_up.csv | 37 | entry_price:37, max_adverse_excursion:37, price_date:37, third_day_return:37 |
| clean/limit_up.json | 37 | entry_price:37, max_adverse_excursion:37, price_date:37, third_day_return:37 |
| clean/market_quotes.csv | 5580 | quote_date:5579, quote_timestamp:5579, supplement_source:5579, volume_unit:5579, 买入:1, 卖出:1, 成交量:1, 时间戳:1, 昨收:1, 涨跌额:1 |
| clean/market_quotes.json | 5580 | quote_date:5579, quote_timestamp:5579, supplement_source:5579, volume_unit:5579, 买入:1, 卖出:1, 成交量:1, 时间戳:1, 昨收:1, 涨跌额:1 |
| clean/market_reconciliation.json | 1 | 无 |
| clean/promotion.json | 1 | verified_tradable_rate:1 |
| clean/promotion_rows.csv | 57 | entry_price:57, max_adverse_excursion:57, third_day_return:57 |
| clean/promotion_rows.json | 57 | entry_price:57, max_adverse_excursion:57, third_day_return:57 |
| clean/yesterday_pool.csv | 76 | all_day_one_word:76, entry_price:76, first_seal:76, height:76, last_seal:76, max_adverse_excursion:76, open_count:76, price_date:76, third_day_return:76 |
| clean/yesterday_pool.json | 76 | all_day_one_word:76, entry_price:76, first_seal:76, height:76, last_seal:76, max_adverse_excursion:76, open_count:76, price_date:76, third_day_return:76 |
| raw/broken.csv | 35 | 无 |
| raw/broken.json | 35 | 无 |
| raw/calendar.csv | 8797 | 无 |
| raw/calendar.json | 8797 | 无 |
| raw/index_fallback_sh000001.csv | 1 | 无 |
| raw/index_fallback_sh000001.json | 1 | 无 |
| raw/index_fallback_sz399001.csv | 1 | 无 |
| raw/index_fallback_sz399001.json | 1 | 无 |
| raw/index_fallback_sz399006.csv | 1 | 无 |
| raw/index_fallback_sz399006.json | 1 | 无 |
| raw/limit_down.csv | 5 | 无 |
| raw/limit_down.json | 5 | 无 |
| raw/limit_up.csv | 37 | 无 |
| raw/limit_up.json | 37 | 无 |
| raw/official_szse_summary_retry.csv | 14 | 总市值:3, 流通市值:3 |
| raw/official_szse_summary_retry.json | 14 | 总市值:3, 流通市值:3 |
| raw/yesterday_pool.csv | 85 | 无 |
| raw/yesterday_pool.json | 85 | 无 |
| report.md | — | 无 |
| sources.json | 1 | 无 |
| summary.json | 1 | 无 |

来源及原始接口参数见 files.json 的 source_refs 与 sources.json；原始失败不视为空行情。
entry_price、third_day_return、max_adverse_excursion等未验证成交字段有意保留为空。
