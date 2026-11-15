# 文件清单

| 路径 | 记录数 | 缺失字段（数量） |
|---|---:|---|
| clean/broken.csv | 12 | all_day_one_word:12, amount:12, close:12, entry_price:12, height:12, high:12, last_seal:12, low:12, max_adverse_excursion:12, open:12, price_date:12, price_source:12, third_day_return:12, volume:12 |
| clean/broken.json | 12 | all_day_one_word:12, amount:12, close:12, entry_price:12, height:12, high:12, last_seal:12, low:12, max_adverse_excursion:12, open:12, price_date:12, price_source:12, third_day_return:12, volume:12 |
| clean/candidate_prices.csv | 0 | 无 |
| clean/candidate_prices.json | 0 | 无 |
| clean/first_board_followup.csv | 135 | entry_price:135, max_adverse_excursion:135, third_day_return:135 |
| clean/first_board_followup.json | 135 | entry_price:135, max_adverse_excursion:135, third_day_return:135 |
| clean/followup_prices.csv | 135 | 无 |
| clean/followup_prices.json | 135 | 无 |
| clean/indices.csv | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3, volume:1 |
| clean/indices.json | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3, volume:1 |
| clean/limit_down.csv | 15 | all_day_one_word:15, amount:15, close:15, entry_price:15, first_seal:15, height:15, high:15, low:15, max_adverse_excursion:15, open:15, open_count:15, price_date:15, price_source:15, third_day_return:15, volume:15 |
| clean/limit_down.json | 15 | all_day_one_word:15, amount:15, close:15, entry_price:15, first_seal:15, height:15, high:15, low:15, max_adverse_excursion:15, open:15, open_count:15, price_date:15, price_source:15, third_day_return:15, volume:15 |
| clean/promotion.json | 1 | observation_rate:1, verified_tradable_rate:1 |
| clean/promotion_rows.csv | 0 | 无 |
| clean/promotion_rows.json | 0 | 无 |
| clean/yesterday_pool.csv | 71 | all_day_one_word:71, amount:71, close:71, entry_price:71, first_seal:71, height:71, high:71, last_seal:71, low:71, max_adverse_excursion:71, open:71, open_count:71, price_date:71, price_source:71, third_day_return:71, volume:71 |
| clean/yesterday_pool.json | 71 | all_day_one_word:71, amount:71, close:71, entry_price:71, first_seal:71, height:71, high:71, last_seal:71, low:71, max_adverse_excursion:71, open:71, open_count:71, price_date:71, price_source:71, third_day_return:71, volume:71 |
| raw/broken.csv | 14 | 无 |
| raw/broken.json | 14 | 无 |
| raw/calendar.csv | 8797 | 无 |
| raw/calendar.json | 8797 | 无 |
| raw/index_official_csi932000.csv | 1 | 无 |
| raw/index_official_csi932000.json | 1 | 无 |
| raw/index_sh000001.csv | 1 | 无 |
| raw/index_sh000001.json | 1 | 无 |
| raw/index_sz399001.csv | 1 | 无 |
| raw/index_sz399001.json | 1 | 无 |
| raw/index_sz399006.csv | 1 | 无 |
| raw/index_sz399006.json | 1 | 无 |
| raw/limit_down.csv | 15 | 无 |
| raw/limit_down.json | 15 | 无 |
| raw/limit_up.csv | 32 | 无 |
| raw/limit_up.json | 32 | 无 |
| raw/yesterday_pool.csv | 84 | 无 |
| raw/yesterday_pool.json | 84 | 无 |
| report.md | — | 无 |
| sources.json | 1 | 无 |
| summary.json | 1 | 无 |

来源及原始接口参数见 files.json 的 source_refs 与 sources.json；原始失败不视为空行情。
entry_price、third_day_return、max_adverse_excursion等未验证成交字段有意保留为空。
