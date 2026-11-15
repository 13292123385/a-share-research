# 文件清单

| 路径 | 记录数 | 缺失字段（数量） |
|---|---:|---|
| clean/broken.csv | 38 | all_day_one_word:38, entry_price:38, height:38, last_seal:38, max_adverse_excursion:38, price_date:38, third_day_return:38 |
| clean/broken.json | 38 | all_day_one_word:38, entry_price:38, height:38, last_seal:38, max_adverse_excursion:38, price_date:38, third_day_return:38 |
| clean/candidate_prices.csv | 0 | 无 |
| clean/candidate_prices.json | 0 | 无 |
| clean/first_board_candidates.csv | 41 | entry_price:41, max_adverse_excursion:41, price_date:41, third_day_return:41 |
| clean/first_board_candidates.json | 41 | entry_price:41, max_adverse_excursion:41, price_date:41, third_day_return:41 |
| clean/first_board_followup.csv | 70 | entry_price:70, max_adverse_excursion:70, third_day_return:70 |
| clean/first_board_followup.json | 70 | entry_price:70, max_adverse_excursion:70, third_day_return:70 |
| clean/followup_prices.csv | 70 | origin_run:1, reused_from_prior_run:1 |
| clean/followup_prices.json | 70 | origin_run:1, reused_from_prior_run:1 |
| clean/indices.csv | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3, volume:2 |
| clean/indices.json | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3, volume:2 |
| clean/limit_down.csv | 1 | all_day_one_word:1, entry_price:1, first_seal:1, height:1, max_adverse_excursion:1, open_count:1, price_date:1, third_day_return:1 |
| clean/limit_down.json | 1 | all_day_one_word:1, entry_price:1, first_seal:1, height:1, max_adverse_excursion:1, open_count:1, price_date:1, third_day_return:1 |
| clean/limit_up.csv | 50 | entry_price:50, max_adverse_excursion:50, price_date:50, third_day_return:50 |
| clean/limit_up.json | 50 | entry_price:50, max_adverse_excursion:50, price_date:50, third_day_return:50 |
| clean/market_quotes.csv | 5579 | quote_date:5578, quote_timestamp:5578, supplement_source:5578, volume_unit:5578, 买入:1, 卖出:1, 成交量:1, 时间戳:1, 昨收:1, 涨跌额:1 |
| clean/market_quotes.json | 5579 | quote_date:5578, quote_timestamp:5578, supplement_source:5578, volume_unit:5578, 买入:1, 卖出:1, 成交量:1, 时间戳:1, 昨收:1, 涨跌额:1 |
| clean/market_reconciliation.json | 1 | 无 |
| clean/promotion.json | 1 | verified_tradable_rate:1 |
| clean/promotion_rows.csv | 19 | entry_price:19, max_adverse_excursion:19, third_day_return:19 |
| clean/promotion_rows.json | 19 | entry_price:19, max_adverse_excursion:19, third_day_return:19 |
| clean/yesterday_pool.csv | 29 | all_day_one_word:29, entry_price:29, first_seal:29, height:29, last_seal:29, max_adverse_excursion:29, open_count:29, price_date:29, third_day_return:29 |
| clean/yesterday_pool.json | 29 | all_day_one_word:29, entry_price:29, first_seal:29, height:29, last_seal:29, max_adverse_excursion:29, open_count:29, price_date:29, third_day_return:29 |
| raw/broken.csv | 44 | 无 |
| raw/broken.json | 44 | 无 |
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
| raw/limit_down.csv | 1 | 无 |
| raw/limit_down.json | 1 | 无 |
| raw/limit_up.csv | 54 | 无 |
| raw/limit_up.json | 54 | 无 |
| raw/official_szse_summary_retry.csv | 14 | 总市值:3, 流通市值:3 |
| raw/official_szse_summary_retry.json | 14 | 总市值:3, 流通市值:3 |
| raw/price_605339.csv | 1 | 无 |
| raw/price_605339.json | 1 | 无 |
| raw/yesterday_pool.csv | 32 | 无 |
| raw/yesterday_pool.json | 32 | 无 |
| report.md | — | 无 |
| sources.json | 1 | 无 |
| summary.json | 1 | 无 |

来源及原始接口参数见 files.json 的 source_refs 与 sources.json；原始失败不视为空行情。
entry_price、third_day_return、max_adverse_excursion等未验证成交字段有意保留为空。
