# 文件清单

| 路径 | 记录数 | 缺失字段（数量） |
|---|---:|---|
| clean/candidate_prices.csv | 0 | 无 |
| clean/candidate_prices.json | 0 | 无 |
| clean/first_board_followup.csv | 61 | entry_price:61, max_adverse_excursion:61, third_day_return:61 |
| clean/first_board_followup.json | 61 | entry_price:61, max_adverse_excursion:61, third_day_return:61 |
| clean/followup_prices.csv | 61 | 无 |
| clean/followup_prices.json | 61 | 无 |
| clean/indices.csv | 4 | 无 |
| clean/indices.json | 4 | 无 |
| clean/promotion.json | 1 | observation_rate:1, verified_tradable_rate:1 |
| clean/promotion_rows.csv | 0 | 无 |
| clean/promotion_rows.json | 0 | 无 |
| raw/broken.csv | 0 | 无 |
| raw/broken.json | 0 | 无 |
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
| raw/limit_up.csv | 0 | 无 |
| raw/limit_up.json | 0 | 无 |
| raw/yesterday_pool.csv | 0 | 无 |
| raw/yesterday_pool.json | 0 | 无 |
| report.md | — | 无 |
| sources.json | 1 | 无 |
| summary.json | 1 | 无 |

来源及原始接口参数见 files.json 的 source_refs 与 sources.json；原始失败不视为空行情。
entry_price、third_day_return、max_adverse_excursion等未验证成交字段有意保留为空。
