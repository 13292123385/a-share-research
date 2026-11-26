# 文件清单

| 路径 | 记录数 | 缺失字段（数量） |
|---|---:|---|
| clean/broken.csv | 23 | all_day_one_word:23, entry_price:23, height:23, last_seal:23, max_adverse_excursion:23, price_date:23, third_day_return:23 |
| clean/broken.json | 23 | all_day_one_word:23, entry_price:23, height:23, last_seal:23, max_adverse_excursion:23, price_date:23, third_day_return:23 |
| clean/candidate_prices.csv | 0 | 无 |
| clean/candidate_prices.json | 0 | 无 |
| clean/first_board_candidates.csv | 48 | entry_price:48, max_adverse_excursion:48, price_date:48, third_day_return:48 |
| clean/first_board_candidates.json | 48 | entry_price:48, max_adverse_excursion:48, price_date:48, third_day_return:48 |
| clean/first_board_followup.csv | 54 | entry_price:54, max_adverse_excursion:54, third_day_return:54 |
| clean/first_board_followup.json | 54 | entry_price:54, max_adverse_excursion:54, third_day_return:54 |
| clean/followup_prices.csv | 54 | 无 |
| clean/followup_prices.json | 54 | 无 |
| clean/indices.csv | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3 |
| clean/indices.json | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3 |
| clean/limit_down.csv | 3 | all_day_one_word:3, entry_price:3, first_seal:3, height:3, max_adverse_excursion:3, open_count:3, price_date:3, third_day_return:3 |
| clean/limit_down.json | 3 | all_day_one_word:3, entry_price:3, first_seal:3, height:3, max_adverse_excursion:3, open_count:3, price_date:3, third_day_return:3 |
| clean/limit_up.csv | 62 | entry_price:62, max_adverse_excursion:62, price_date:62, third_day_return:62 |
| clean/limit_up.json | 62 | entry_price:62, max_adverse_excursion:62, price_date:62, third_day_return:62 |
| clean/market_quotes.csv | 5581 | quote_date:5580, quote_timestamp:5580, supplement_source:5580, volume_unit:5580, 买入:1, 卖出:1, 成交量:1, 时间戳:1, 昨收:1, 涨跌额:1 |
| clean/market_quotes.json | 5581 | quote_date:5580, quote_timestamp:5580, supplement_source:5580, volume_unit:5580, 买入:1, 卖出:1, 成交量:1, 时间戳:1, 昨收:1, 涨跌额:1 |
| clean/market_reconciliation.json | 1 | 无 |
| clean/promotion.json | 1 | verified_tradable_rate:1 |
| clean/promotion_rows.csv | 33 | entry_price:33, max_adverse_excursion:33, third_day_return:33 |
| clean/promotion_rows.json | 33 | entry_price:33, max_adverse_excursion:33, third_day_return:33 |
| clean/yesterday_pool.csv | 46 | all_day_one_word:46, entry_price:46, first_seal:46, height:46, last_seal:46, max_adverse_excursion:46, open_count:46, price_date:46, third_day_return:46 |
| clean/yesterday_pool.json | 46 | all_day_one_word:46, entry_price:46, first_seal:46, height:46, last_seal:46, max_adverse_excursion:46, open_count:46, price_date:46, third_day_return:46 |
| raw/broken.csv | 29 | 无 |
| raw/broken.json | 29 | 无 |
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
| raw/limit_down.csv | 5 | 无 |
| raw/limit_down.json | 5 | 无 |
| raw/limit_up.csv | 65 | 无 |
| raw/limit_up.json | 65 | 无 |
| raw/official_szse_summary_retry.csv | 14 | 总市值:3, 流通市值:3 |
| raw/official_szse_summary_retry.json | 14 | 总市值:3, 流通市值:3 |
| raw/yesterday_pool.csv | 51 | 无 |
| raw/yesterday_pool.json | 51 | 无 |
| report.md | — | 无 |
| sources.json | 1 | 无 |
| summary.json | 1 | 无 |

来源及原始接口参数见 files.json 的 source_refs 与 sources.json；原始失败不视为空行情。
entry_price、third_day_return、max_adverse_excursion等未验证成交字段有意保留为空。
