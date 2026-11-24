# 文件清单

| 路径 | 记录数 | 缺失字段（数量） |
|---|---:|---|
| clean/broken.csv | 30 | all_day_one_word:30, amount:30, close:30, entry_price:30, height:30, high:30, last_seal:30, low:30, max_adverse_excursion:30, open:30, price_date:30, price_source:30, third_day_return:30, volume:30 |
| clean/broken.json | 30 | all_day_one_word:30, amount:30, close:30, entry_price:30, height:30, high:30, last_seal:30, low:30, max_adverse_excursion:30, open:30, price_date:30, price_source:30, third_day_return:30, volume:30 |
| clean/candidate_prices.csv | 96 | 无 |
| clean/candidate_prices.json | 96 | 无 |
| clean/first_board_candidates.csv | 84 | entry_price:84, max_adverse_excursion:84, third_day_return:84 |
| clean/first_board_candidates.json | 84 | entry_price:84, max_adverse_excursion:84, third_day_return:84 |
| clean/first_board_followup.csv | 129 | entry_price:129, max_adverse_excursion:129, price:1, third_day_return:129 |
| clean/first_board_followup.json | 129 | entry_price:129, max_adverse_excursion:129, price:1, third_day_return:129 |
| clean/followup_prices.csv | 128 | 无 |
| clean/followup_prices.json | 128 | 无 |
| clean/indices.csv | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3, volume:3 |
| clean/indices.json | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3, volume:3 |
| clean/limit_down.csv | 10 | all_day_one_word:10, amount:10, close:10, entry_price:10, first_seal:10, height:10, high:10, low:10, max_adverse_excursion:10, open:10, open_count:10, price_date:10, price_source:10, third_day_return:10, volume:10 |
| clean/limit_down.json | 10 | all_day_one_word:10, amount:10, close:10, entry_price:10, first_seal:10, height:10, high:10, low:10, max_adverse_excursion:10, open:10, open_count:10, price_date:10, price_source:10, third_day_return:10, volume:10 |
| clean/limit_up.csv | 96 | entry_price:96, max_adverse_excursion:96, third_day_return:96 |
| clean/limit_up.json | 96 | entry_price:96, max_adverse_excursion:96, third_day_return:96 |
| clean/promotion.json | 1 | verified_tradable_rate:1 |
| clean/promotion_rows.csv | 32 | entry_price:32, max_adverse_excursion:32, third_day_return:32 |
| clean/promotion_rows.json | 32 | entry_price:32, max_adverse_excursion:32, third_day_return:32 |
| clean/yesterday_pool.csv | 47 | all_day_one_word:47, amount:35, close:35, entry_price:47, first_seal:47, height:47, high:35, last_seal:47, low:35, max_adverse_excursion:47, open:35, open_count:47, price_date:35, price_source:35, third_day_return:47, volume:35 |
| clean/yesterday_pool.json | 47 | all_day_one_word:47, amount:35, close:35, entry_price:47, first_seal:47, height:47, high:35, last_seal:47, low:35, max_adverse_excursion:47, open:35, open_count:47, price_date:35, price_source:35, third_day_return:47, volume:35 |
| raw/broken.csv | 33 | 无 |
| raw/broken.json | 33 | 无 |
| raw/calendar.csv | 8797 | 无 |
| raw/calendar.json | 8797 | 无 |
| raw/index_fallback_sz399001.csv | 1 | 无 |
| raw/index_fallback_sz399001.json | 1 | 无 |
| raw/index_fallback_sz399006.csv | 1 | 无 |
| raw/index_fallback_sz399006.json | 1 | 无 |
| raw/index_official_csi932000.csv | 1 | 无 |
| raw/index_official_csi932000.json | 1 | 无 |
| raw/index_sh000001.csv | 1 | 无 |
| raw/index_sh000001.json | 1 | 无 |
| raw/limit_down.csv | 10 | 无 |
| raw/limit_down.json | 10 | 无 |
| raw/limit_up.csv | 118 | 无 |
| raw/limit_up.json | 118 | 无 |
| raw/price_002623.csv | 0 | 无 |
| raw/price_002623.json | 0 | 无 |
| raw/yesterday_pool.csv | 48 | 无 |
| raw/yesterday_pool.json | 48 | 无 |
| report.md | — | 无 |
| sources.json | 1 | 无 |
| summary.json | 1 | 无 |

来源及原始接口参数见 files.json 的 source_refs 与 sources.json；原始失败不视为空行情。
entry_price、third_day_return、max_adverse_excursion等未验证成交字段有意保留为空。
