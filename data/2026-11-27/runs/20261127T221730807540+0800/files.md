# 文件清单

| 路径 | 记录数 | 缺失字段（数量） |
|---|---:|---|
| clean/broken.csv | 34 | all_day_one_word:34, entry_price:34, height:34, last_seal:34, max_adverse_excursion:34, price_date:34, third_day_return:34 |
| clean/broken.json | 34 | all_day_one_word:34, entry_price:34, height:34, last_seal:34, max_adverse_excursion:34, price_date:34, third_day_return:34 |
| clean/candidate_prices.csv | 0 | 无 |
| clean/candidate_prices.json | 0 | 无 |
| clean/first_board_candidates.csv | 286 | entry_price:286, max_adverse_excursion:286, price_date:286, third_day_return:286 |
| clean/first_board_candidates.json | 286 | entry_price:286, max_adverse_excursion:286, price_date:286, third_day_return:286 |
| clean/first_board_followup.csv | 81 | entry_price:81, max_adverse_excursion:81, third_day_return:81 |
| clean/first_board_followup.json | 81 | entry_price:81, max_adverse_excursion:81, third_day_return:81 |
| clean/followup_prices.csv | 81 | 无 |
| clean/followup_prices.json | 81 | 无 |
| clean/indices.csv | 4 | 无 |
| clean/indices.json | 4 | 无 |
| clean/limit_up.csv | 314 | entry_price:314, max_adverse_excursion:314, price_date:314, third_day_return:314 |
| clean/limit_up.json | 314 | entry_price:314, max_adverse_excursion:314, price_date:314, third_day_return:314 |
| clean/market_quotes.csv | 5581 | quote_date:5580, quote_timestamp:5580, supplement_source:5580, volume_unit:5580, 买入:1, 卖出:1, 成交量:1, 时间戳:1, 昨收:1, 涨跌额:1 |
| clean/market_quotes.json | 5581 | quote_date:5580, quote_timestamp:5580, supplement_source:5580, volume_unit:5580, 买入:1, 卖出:1, 成交量:1, 时间戳:1, 昨收:1, 涨跌额:1 |
| clean/market_reconciliation.json | 1 | 无 |
| clean/promotion.json | 1 | verified_tradable_rate:1 |
| clean/promotion_rows.csv | 48 | entry_price:48, max_adverse_excursion:48, third_day_return:48 |
| clean/promotion_rows.json | 48 | entry_price:48, max_adverse_excursion:48, third_day_return:48 |
| clean/yesterday_pool.csv | 62 | all_day_one_word:62, entry_price:62, first_seal:62, height:62, last_seal:62, max_adverse_excursion:62, open_count:62, price_date:62, third_day_return:62 |
| clean/yesterday_pool.json | 62 | all_day_one_word:62, entry_price:62, first_seal:62, height:62, last_seal:62, max_adverse_excursion:62, open_count:62, price_date:62, third_day_return:62 |
| raw/broken.csv | 42 | 无 |
| raw/broken.json | 42 | 无 |
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
| raw/limit_up.csv | 417 | 无 |
| raw/limit_up.json | 417 | 无 |
| raw/official_szse_summary_retry.csv | 14 | 总市值:3, 流通市值:3 |
| raw/official_szse_summary_retry.json | 14 | 总市值:3, 流通市值:3 |
| raw/yesterday_pool.csv | 65 | 无 |
| raw/yesterday_pool.json | 65 | 无 |
| report.md | — | 无 |
| sources.json | 1 | 无 |
| summary.json | 1 | 无 |

来源及原始接口参数见 files.json 的 source_refs 与 sources.json；原始失败不视为空行情。
entry_price、third_day_return、max_adverse_excursion等未验证成交字段有意保留为空。
