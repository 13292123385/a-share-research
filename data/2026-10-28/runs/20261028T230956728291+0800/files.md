# 文件清单

| 路径 | 记录数 | 缺失字段（数量） |
|---|---:|---|
| clean/broken.csv | 49 | all_day_one_word:49, entry_price:49, height:49, last_seal:49, max_adverse_excursion:49, price_date:49, third_day_return:49 |
| clean/broken.json | 49 | all_day_one_word:49, entry_price:49, height:49, last_seal:49, max_adverse_excursion:49, price_date:49, third_day_return:49 |
| clean/candidate_prices.csv | 0 | 无 |
| clean/candidate_prices.json | 0 | 无 |
| clean/first_board_candidates.csv | 50 | entry_price:50, max_adverse_excursion:50, price_date:50, third_day_return:50 |
| clean/first_board_candidates.json | 50 | entry_price:50, max_adverse_excursion:50, price_date:50, third_day_return:50 |
| clean/first_board_followup.csv | 58 | entry_price:58, max_adverse_excursion:58, third_day_return:58 |
| clean/first_board_followup.json | 58 | entry_price:58, max_adverse_excursion:58, third_day_return:58 |
| clean/followup_prices.csv | 58 | 无 |
| clean/followup_prices.json | 58 | 无 |
| clean/indices.csv | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3 |
| clean/indices.json | 4 | amount:1, high:1, index_code:3, low:1, open:1, source:3 |
| clean/limit_down.csv | 5 | all_day_one_word:5, entry_price:5, first_seal:5, height:5, max_adverse_excursion:5, open_count:5, price_date:5, third_day_return:5 |
| clean/limit_down.json | 5 | all_day_one_word:5, entry_price:5, first_seal:5, height:5, max_adverse_excursion:5, open_count:5, price_date:5, third_day_return:5 |
| clean/limit_up.csv | 58 | entry_price:58, max_adverse_excursion:58, price_date:58, third_day_return:58 |
| clean/limit_up.json | 58 | entry_price:58, max_adverse_excursion:58, price_date:58, third_day_return:58 |
| clean/market_quotes.csv | 5576 | quote_date:5575, quote_timestamp:5575, supplement_source:5575, volume_unit:5575, 买入:1, 卖出:1, 成交量:1, 时间戳:1, 昨收:1, 涨跌额:1 |
| clean/market_quotes.json | 5576 | quote_date:5575, quote_timestamp:5575, supplement_source:5575, volume_unit:5575, 买入:1, 卖出:1, 成交量:1, 时间戳:1, 昨收:1, 涨跌额:1 |
| clean/market_reconciliation.json | 1 | 无 |
| clean/promotion.json | 1 | verified_tradable_rate:1 |
| clean/promotion_rows.csv | 25 | entry_price:25, max_adverse_excursion:25, third_day_return:25 |
| clean/promotion_rows.json | 25 | entry_price:25, max_adverse_excursion:25, third_day_return:25 |
| clean/yesterday_pool.csv | 36 | all_day_one_word:36, entry_price:36, first_seal:36, height:36, last_seal:36, max_adverse_excursion:36, open_count:36, price_date:36, third_day_return:36 |
| clean/yesterday_pool.json | 36 | all_day_one_word:36, entry_price:36, first_seal:36, height:36, last_seal:36, max_adverse_excursion:36, open_count:36, price_date:36, third_day_return:36 |
| raw/broken.csv | 69 | 无 |
| raw/broken.json | 69 | 无 |
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
| raw/limit_up.csv | 72 | 无 |
| raw/limit_up.json | 72 | 无 |
| raw/market_quote_689009.csv | 1 | 成交量:1 |
| raw/market_quote_689009.json | 1 | 成交量:1 |
| raw/official_roster_bj.csv | 353 | 无 |
| raw/official_roster_bj.json | 353 | 无 |
| raw/official_roster_sh_main.csv | 1700 | 无 |
| raw/official_roster_sh_main.json | 1700 | 无 |
| raw/official_roster_sh_star.csv | 618 | 无 |
| raw/official_roster_sh_star.json | 618 | 无 |
| raw/official_roster_sz_retry1.csv | 2905 | 无 |
| raw/official_roster_sz_retry1.json | 2905 | 无 |
| raw/official_szse_summary.csv | 14 | 总市值:3, 流通市值:3 |
| raw/official_szse_summary.json | 14 | 总市值:3, 流通市值:3 |
| raw/spot_fallback.csv | 5575 | 无 |
| raw/spot_fallback.json | 5575 | 无 |
| raw/yesterday_pool.csv | 41 | 无 |
| raw/yesterday_pool.json | 41 | 无 |
| report.md | — | 无 |
| sources.json | 1 | 无 |
| summary.json | 1 | 无 |

来源及原始接口参数见 files.json 的 source_refs 与 sources.json；原始失败不视为空行情。
entry_price、third_day_return、max_adverse_excursion等未验证成交字段有意保留为空。
