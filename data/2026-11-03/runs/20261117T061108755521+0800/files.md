# 文件清单

| 路径 | 记录数 | 缺失字段（数量） |
|---|---:|---|
| clean/broken.csv | 30 | all_day_one_word:30, amount:30, close:30, entry_price:30, height:30, high:30, last_seal:30, low:30, max_adverse_excursion:30, open:30, price_date:30, price_source:30, third_day_return:30, volume:30 |
| clean/broken.json | 30 | all_day_one_word:30, amount:30, close:30, entry_price:30, height:30, high:30, last_seal:30, low:30, max_adverse_excursion:30, open:30, price_date:30, price_source:30, third_day_return:30, volume:30 |
| clean/candidate_prices.csv | 47 | 无 |
| clean/candidate_prices.json | 47 | 无 |
| clean/first_board_candidates.csv | 32 | entry_price:32, max_adverse_excursion:32, third_day_return:32 |
| clean/first_board_candidates.json | 32 | entry_price:32, max_adverse_excursion:32, third_day_return:32 |
| clean/first_board_followup.csv | 130 | entry_price:130, max_adverse_excursion:130, price:1, third_day_return:130 |
| clean/first_board_followup.json | 130 | entry_price:130, max_adverse_excursion:130, price:1, third_day_return:130 |
| clean/followup_prices.csv | 129 | 无 |
| clean/followup_prices.json | 129 | 无 |
| clean/indices.csv | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3, volume:3 |
| clean/indices.json | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3, volume:3 |
| clean/limit_down.csv | 13 | all_day_one_word:13, amount:13, close:13, entry_price:13, first_seal:13, height:13, high:13, low:13, max_adverse_excursion:13, open:13, open_count:13, price_date:13, price_source:13, third_day_return:13, volume:13 |
| clean/limit_down.json | 13 | all_day_one_word:13, amount:13, close:13, entry_price:13, first_seal:13, height:13, high:13, low:13, max_adverse_excursion:13, open:13, open_count:13, price_date:13, price_source:13, third_day_return:13, volume:13 |
| clean/limit_up.csv | 47 | entry_price:47, max_adverse_excursion:47, third_day_return:47 |
| clean/limit_up.json | 47 | entry_price:47, max_adverse_excursion:47, third_day_return:47 |
| clean/promotion.json | 1 | verified_tradable_rate:1 |
| clean/promotion_rows.csv | 97 | entry_price:97, max_adverse_excursion:97, third_day_return:97 |
| clean/promotion_rows.json | 97 | entry_price:97, max_adverse_excursion:97, third_day_return:97 |
| clean/yesterday_pool.csv | 107 | all_day_one_word:107, amount:92, close:92, entry_price:107, first_seal:107, height:107, high:92, last_seal:107, low:92, max_adverse_excursion:107, open:92, open_count:107, price_date:92, price_source:92, third_day_return:107, volume:92 |
| clean/yesterday_pool.json | 107 | all_day_one_word:107, amount:92, close:92, entry_price:107, first_seal:107, height:107, high:92, last_seal:107, low:92, max_adverse_excursion:107, open:92, open_count:107, price_date:92, price_source:92, third_day_return:107, volume:92 |
| raw/broken.csv | 34 | 无 |
| raw/broken.json | 34 | 无 |
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
| raw/limit_down.csv | 17 | 无 |
| raw/limit_down.json | 17 | 无 |
| raw/limit_up.csv | 48 | 无 |
| raw/limit_up.json | 48 | 无 |
| raw/price_002623.csv | 0 | 无 |
| raw/price_002623.json | 0 | 无 |
| raw/yesterday_pool.csv | 124 | 无 |
| raw/yesterday_pool.json | 124 | 无 |
| report.md | — | 无 |
| sources.json | 1 | 无 |
| summary.json | 1 | 无 |

来源及原始接口参数见 files.json 的 source_refs 与 sources.json；原始失败不视为空行情。
entry_price、third_day_return、max_adverse_excursion等未验证成交字段有意保留为空。
