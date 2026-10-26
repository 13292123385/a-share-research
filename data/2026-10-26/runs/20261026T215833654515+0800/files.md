# 文件清单

| 路径 | 记录数 | 缺失字段（数量） |
|---|---:|---|
| clean/broken.csv | 18 | all_day_one_word:18, entry_price:18, height:18, last_seal:18, max_adverse_excursion:18, price_date:18, third_day_return:18 |
| clean/broken.json | 18 | all_day_one_word:18, entry_price:18, height:18, last_seal:18, max_adverse_excursion:18, price_date:18, third_day_return:18 |
| clean/candidate_prices.csv | 0 | 无 |
| clean/candidate_prices.json | 0 | 无 |
| clean/first_board_candidates.csv | 33 | entry_price:33, max_adverse_excursion:33, price_date:33, third_day_return:33 |
| clean/first_board_candidates.json | 33 | entry_price:33, max_adverse_excursion:33, price_date:33, third_day_return:33 |
| clean/first_board_followup.csv | 53 | entry_price:53, max_adverse_excursion:53, third_day_return:53 |
| clean/first_board_followup.json | 53 | entry_price:53, max_adverse_excursion:53, third_day_return:53 |
| clean/followup_prices.csv | 53 | 无 |
| clean/followup_prices.json | 53 | 无 |
| clean/indices.csv | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3 |
| clean/indices.json | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3 |
| clean/limit_down.csv | 25 | all_day_one_word:25, entry_price:25, first_seal:25, height:25, max_adverse_excursion:25, open_count:25, price_date:25, third_day_return:25 |
| clean/limit_down.json | 25 | all_day_one_word:25, entry_price:25, first_seal:25, height:25, max_adverse_excursion:25, open_count:25, price_date:25, third_day_return:25 |
| clean/limit_up.csv | 47 | entry_price:47, max_adverse_excursion:47, price_date:47, third_day_return:47 |
| clean/limit_up.json | 47 | entry_price:47, max_adverse_excursion:47, price_date:47, third_day_return:47 |
| clean/market_quotes.csv | 5576 | 无 |
| clean/market_quotes.json | 5576 | 无 |
| clean/market_reconciliation.json | 1 | expected_count:1, unexpected_codes:1 |
| clean/promotion.json | 1 | verified_tradable_rate:1 |
| clean/promotion_rows.csv | 53 | entry_price:53, max_adverse_excursion:53, third_day_return:53 |
| clean/promotion_rows.json | 53 | entry_price:53, max_adverse_excursion:53, third_day_return:53 |
| clean/yesterday_pool.csv | 64 | all_day_one_word:64, entry_price:64, first_seal:64, height:64, last_seal:64, max_adverse_excursion:64, open_count:64, price_date:64, third_day_return:64 |
| clean/yesterday_pool.json | 64 | all_day_one_word:64, entry_price:64, first_seal:64, height:64, last_seal:64, max_adverse_excursion:64, open_count:64, price_date:64, third_day_return:64 |
| raw/broken.csv | 23 | 无 |
| raw/broken.json | 23 | 无 |
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
| raw/limit_down.csv | 26 | 无 |
| raw/limit_down.json | 26 | 无 |
| raw/limit_up.csv | 55 | 无 |
| raw/limit_up.json | 55 | 无 |
| raw/official_roster_bj.csv | 353 | 无 |
| raw/official_roster_bj.json | 353 | 无 |
| raw/official_roster_sh_main.csv | 1700 | 无 |
| raw/official_roster_sh_main.json | 1700 | 无 |
| raw/official_roster_sh_star.csv | 618 | 无 |
| raw/official_roster_sh_star.json | 618 | 无 |
| raw/official_szse_summary.csv | 14 | 总市值:3, 流通市值:3 |
| raw/official_szse_summary.json | 14 | 总市值:3, 流通市值:3 |
| raw/spot_fallback.csv | 5576 | 无 |
| raw/spot_fallback.json | 5576 | 无 |
| raw/yesterday_pool.csv | 82 | 无 |
| raw/yesterday_pool.json | 82 | 无 |
| report.md | — | 无 |
| sources.json | 1 | 无 |
| summary.json | 1 | 无 |

来源及原始接口参数见 files.json 的 source_refs 与 sources.json；原始失败不视为空行情。
entry_price、third_day_return、max_adverse_excursion等未验证成交字段有意保留为空。
