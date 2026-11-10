# 文件清单

| 路径 | 记录数 | 缺失字段（数量） |
|---|---:|---|
| clean/broken.csv | 22 | all_day_one_word:22, amount:22, close:22, entry_price:22, height:22, high:22, last_seal:22, low:22, max_adverse_excursion:22, open:22, price_date:22, price_source:22, third_day_return:22, volume:22 |
| clean/broken.json | 22 | all_day_one_word:22, amount:22, close:22, entry_price:22, height:22, high:22, last_seal:22, low:22, max_adverse_excursion:22, open:22, price_date:22, price_source:22, third_day_return:22, volume:22 |
| clean/candidate_prices.csv | 108 | origin_run:8, reused_from_prior_run:8 |
| clean/candidate_prices.json | 108 | origin_run:8, reused_from_prior_run:8 |
| clean/first_board_candidates.csv | 97 | entry_price:97, max_adverse_excursion:97, third_day_return:97 |
| clean/first_board_candidates.json | 97 | entry_price:97, max_adverse_excursion:97, third_day_return:97 |
| clean/first_board_followup.csv | 61 | entry_price:61, max_adverse_excursion:61, third_day_return:61 |
| clean/first_board_followup.json | 61 | entry_price:61, max_adverse_excursion:61, third_day_return:61 |
| clean/followup_prices.csv | 61 | origin_run:6, reused_from_prior_run:6 |
| clean/followup_prices.json | 61 | origin_run:6, reused_from_prior_run:6 |
| clean/indices.csv | 4 | 无 |
| clean/indices.json | 4 | 无 |
| clean/limit_down.csv | 7 | all_day_one_word:7, amount:7, close:7, entry_price:7, first_seal:7, height:7, high:7, low:7, max_adverse_excursion:7, open:7, open_count:7, price_date:7, price_source:7, third_day_return:7, volume:7 |
| clean/limit_down.json | 7 | all_day_one_word:7, amount:7, close:7, entry_price:7, first_seal:7, height:7, high:7, low:7, max_adverse_excursion:7, open:7, open_count:7, price_date:7, price_source:7, third_day_return:7, volume:7 |
| clean/limit_up.csv | 108 | entry_price:108, max_adverse_excursion:108, third_day_return:108 |
| clean/limit_up.json | 108 | entry_price:108, max_adverse_excursion:108, third_day_return:108 |
| clean/promotion.json | 1 | verified_tradable_rate:1 |
| clean/promotion_rows.csv | 33 | entry_price:33, max_adverse_excursion:33, third_day_return:33 |
| clean/promotion_rows.json | 33 | entry_price:33, max_adverse_excursion:33, third_day_return:33 |
| clean/yesterday_pool.csv | 42 | all_day_one_word:42, amount:31, close:31, entry_price:42, first_seal:42, height:42, high:31, last_seal:42, low:31, max_adverse_excursion:42, open:31, open_count:42, price_date:31, price_source:31, third_day_return:42, volume:31 |
| clean/yesterday_pool.json | 42 | all_day_one_word:42, amount:31, close:31, entry_price:42, first_seal:42, height:42, high:31, last_seal:42, low:31, max_adverse_excursion:42, open:31, open_count:42, price_date:31, price_source:31, third_day_return:42, volume:31 |
| raw/broken.csv | 28 | 无 |
| raw/broken.json | 28 | 无 |
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
| raw/limit_down.csv | 8 | 无 |
| raw/limit_down.json | 8 | 无 |
| raw/limit_up.csv | 125 | 无 |
| raw/limit_up.json | 125 | 无 |
| raw/price_000995.csv | 1 | 无 |
| raw/price_000995.json | 1 | 无 |
| raw/price_001219.csv | 1 | 无 |
| raw/price_001219.json | 1 | 无 |
| raw/price_002086.csv | 1 | 无 |
| raw/price_002086.json | 1 | 无 |
| raw/price_002172.csv | 1 | 无 |
| raw/price_002172.json | 1 | 无 |
| raw/price_002275.csv | 1 | 无 |
| raw/price_002275.json | 1 | 无 |
| raw/price_600189.csv | 1 | 无 |
| raw/price_600189.json | 1 | 无 |
| raw/price_600261.csv | 1 | 无 |
| raw/price_600261.json | 1 | 无 |
| raw/price_603587.csv | 1 | 无 |
| raw/price_603587.json | 1 | 无 |
| raw/yesterday_pool.csv | 47 | 无 |
| raw/yesterday_pool.json | 47 | 无 |
| report.md | — | 无 |
| sources.json | 1 | 无 |
| summary.json | 1 | 无 |

来源及原始接口参数见 files.json 的 source_refs 与 sources.json；原始失败不视为空行情。
entry_price、third_day_return、max_adverse_excursion等未验证成交字段有意保留为空。
