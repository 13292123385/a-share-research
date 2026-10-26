# 文件清单

| 路径 | 记录数 | 缺失字段（数量） |
|---|---:|---|
| clean/broken.csv | 11 | all_day_one_word:11, amount:11, close:11, entry_price:11, height:11, high:11, last_seal:11, low:11, max_adverse_excursion:11, open:11, price_date:11, price_source:11, third_day_return:11, volume:11 |
| clean/broken.json | 11 | all_day_one_word:11, amount:11, close:11, entry_price:11, height:11, high:11, last_seal:11, low:11, max_adverse_excursion:11, open:11, price_date:11, price_source:11, third_day_return:11, volume:11 |
| clean/candidate_prices.csv | 64 | 无 |
| clean/candidate_prices.json | 64 | 无 |
| clean/first_board_candidates.csv | 53 | entry_price:53, max_adverse_excursion:53, third_day_return:53 |
| clean/first_board_candidates.json | 53 | entry_price:53, max_adverse_excursion:53, third_day_return:53 |
| clean/first_board_followup.csv | 0 | 无 |
| clean/first_board_followup.json | 0 | 无 |
| clean/followup_prices.csv | 0 | 无 |
| clean/followup_prices.json | 0 | 无 |
| clean/indices.csv | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3 |
| clean/indices.json | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3 |
| clean/limit_down.csv | 6 | all_day_one_word:6, amount:6, close:6, entry_price:6, first_seal:6, height:6, high:6, low:6, max_adverse_excursion:6, open:6, open_count:6, price_date:6, price_source:6, third_day_return:6, volume:6 |
| clean/limit_down.json | 6 | all_day_one_word:6, amount:6, close:6, entry_price:6, first_seal:6, height:6, high:6, low:6, max_adverse_excursion:6, open:6, open_count:6, price_date:6, price_source:6, third_day_return:6, volume:6 |
| clean/limit_up.csv | 64 | entry_price:64, max_adverse_excursion:64, third_day_return:64 |
| clean/limit_up.json | 64 | entry_price:64, max_adverse_excursion:64, third_day_return:64 |
| clean/promotion.json | 1 | observation_rate:1, verified_tradable_rate:1 |
| clean/promotion_rows.csv | 0 | 无 |
| clean/promotion_rows.json | 0 | 无 |
| clean/yesterday_pool.csv | 30 | all_day_one_word:30, amount:19, close:19, entry_price:30, first_seal:30, height:30, high:19, last_seal:30, low:19, max_adverse_excursion:30, open:19, open_count:30, price_date:19, price_source:19, third_day_return:30, volume:19 |
| clean/yesterday_pool.json | 30 | all_day_one_word:30, amount:19, close:19, entry_price:30, first_seal:30, height:30, high:19, last_seal:30, low:19, max_adverse_excursion:30, open:19, open_count:30, price_date:19, price_source:19, third_day_return:30, volume:19 |
| raw/broken.csv | 12 | 无 |
| raw/broken.json | 12 | 无 |
| raw/calendar.csv | 8797 | 无 |
| raw/calendar.json | 8797 | 无 |
| raw/index_fallback_sh000001.csv | 1 | 无 |
| raw/index_fallback_sh000001.json | 1 | 无 |
| raw/index_fallback_sz399001.csv | 1 | 无 |
| raw/index_fallback_sz399001.json | 1 | 无 |
| raw/index_fallback_sz399006.csv | 1 | 无 |
| raw/index_fallback_sz399006.json | 1 | 无 |
| raw/index_official_csi932000.csv | 1 | 无 |
| raw/index_official_csi932000.json | 1 | 无 |
| raw/limit_down.csv | 6 | 无 |
| raw/limit_down.json | 6 | 无 |
| raw/limit_up.csv | 82 | 无 |
| raw/limit_up.json | 82 | 无 |
| raw/yesterday_pool.csv | 33 | 无 |
| raw/yesterday_pool.json | 33 | 无 |
| report.md | — | 无 |
| sources.json | 1 | 无 |
| summary.json | 1 | 无 |

来源及原始接口参数见 files.json 的 source_refs 与 sources.json；原始失败不视为空行情。
entry_price、third_day_return、max_adverse_excursion等未验证成交字段有意保留为空。
