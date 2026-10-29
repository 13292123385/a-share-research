# 2026-10-29 A股收盘复盘

状态：complete_with_limitations；抓取时间：2026-10-29T22:03:53.311564+08:00

采集范围：closing_snapshot；采集状态：complete；研究状态：limited

## 已验证数据（仅指公开接口指定日期返回值，不代表审计或可成交）
{"mainboard_limit_up_count": 38, "mainboard_height": 4.0, "first_board_candidates": 28, "all_day_one_word_excluded": 4, "one_word_unknown": 0, "broken_count": 23, "limit_down_count": 41, "indices": [{"name": "上证指数", "symbol": "sh000001", "date": "2026-10-29T00:00:00.000", "open": 3676.77, "close": 3651.43, "high": 3678.46, "low": 3645.26, "amount": 443564144.0}, {"name": "深证成指", "symbol": "sz399001", "date": "2026-10-29T00:00:00.000", "open": 11379.0, "close": 11138.2, "high": 11379.0, "low": 11135.97, "amount": 540479121.0}, {"name": "创业板指", "symbol": "sz399006", "date": "2026-10-29T00:00:00.000", "open": 2596.22, "close": 2517.59, "high": 2597.45, "low": 2516.78, "amount": 169679341.0}, {"name": "中证2000", "symbol": "csi932000", "date": "2026-10-29T00:00:00.000", "close": 2709.19, "source": "中证指数官网", "index_code": "932000"}]}

## 估算值
{"market": {"up": 781, "down": 4728, "flat": 68, "turnover_yuan": 1570713772360.0, "records": 5577, "unknown_direction": 0, "unknown_amount": 0, "source": "新浪", "scope": "沪深北候选范围（以官方名单核验结果为准）", "note": "收盘后实时快照汇总；分页完整性和行情日期未获独立验证，可能含停牌平盘"}}

## 一进二
{"status": "observation_only", "denominator": 48, "promoted_count": 4, "broken_count": 4, "observation_rate": 0.08333333333333333, "verified_tradable_rate": null}

观察样本仅排除已知一字板，T字/短暂开板不保证成交。实际可交易晋级率与真实策略收益均缺失。

## 缺失数据
- 首板后续跟踪存在历史名单或价格缺失，详见followup

## 候选股价格覆盖
{"historical_available": 0, "historical_fetched": 0, "reused": 0, "missing_codes": [], "budget_seconds": 420, "note": "首板优先；历史价格为不复权日线，不能证明实际成交；实时快照仍为未独立核验估算"}

## 前两交易日首板后续跟踪
{"rows": 75, "prices_available": 69, "missing_archive_dates": [], "missing_price_codes": ["603926", "603992", "605060", "605288", "605366", "605566"], "budget_seconds": 300, "note": "按交易日追踪首板后第1/2个交易日，不推断成交或策略收益"}

## 市场交叉核验
{"trade_date": "2026-10-29", "status": "code_coverage_matched", "expected_count": 5577, "observed_count": 5577, "missing_codes": [], "unexpected_codes": [], "duplicate_codes": [], "unavailable_rosters": [], "exchanges": {"sh_main": {"expected": 1700, "observed": 1700, "missing_codes": []}, "sh_star": {"expected": 618, "observed": 618, "missing_codes": []}, "sz": {"expected": 2905, "observed": 2905, "missing_codes": []}, "bj": {"expected": 354, "observed": 354, "missing_codes": []}}, "all_market_verified": false, "note": "官方当前上市名单核对代码覆盖，不独立证明每只行情日期/收盘时点；停牌仍应保留且不能把缺失当平盘", "szse_turnover_check": {"status": "within_tolerance", "date_basis": "官方接口请求日期；返回表无独立日期列", "tolerance": 0.005, "official_yuan": 841614758734.24, "snapshot_yuan": 840864069196.0, "relative_difference": 0.0008919633721359661}, "initial_missing_codes": ["689009"], "daily_supplement_codes": ["689009"]}

主观题材三问及新鲜度均待人工证据与评分；总分限制0–15。收益字段待验证买入与第三交易日行情后补充。

## 接口状态
- calendar: ok，行数=8797
- limit_up: ok，行数=39
- yesterday_pool: ok，行数=72
- broken: ok，行数=25
- limit_down: ok，行数=41
- spot: error，行数=None
- spot_fallback: ok，行数=5576
- official_roster_sh_main: ok，行数=1700
- official_roster_sh_star: ok，行数=618
- official_roster_sz: error，行数=None
- official_roster_sz_retry1: ok，行数=2905
- official_roster_bj: ok，行数=354
- official_szse_summary: ok，行数=14
- market_quote_689009: ok，行数=1
- price_000058: ok，行数=1
- price_000554: ok，行数=1
- price_000559: ok，行数=1
- price_000670: ok，行数=1
- price_000888: ok，行数=1
- price_001270: ok，行数=1
- price_001296: ok，行数=1
- price_001400: ok，行数=1
- price_002011: ok，行数=1
- price_002164: ok，行数=1
- price_002172: ok，行数=1
- price_002187: ok，行数=1
- price_002205: ok，行数=1
- price_002249: ok，行数=1
- price_002265: ok，行数=1
- price_002284: ok，行数=1
- price_002526: ok，行数=1
- price_002534: ok，行数=1
- price_002623: ok，行数=1
- price_002636: ok，行数=1
- price_002696: ok，行数=1
- price_002724: ok，行数=1
- price_002741: ok，行数=1
- price_002823: ok，行数=1
- price_002862: ok，行数=1
- price_002879: ok，行数=1
- price_002889: ok，行数=1
- price_002915: ok，行数=1
- price_002943: ok，行数=1
- price_002962: ok，行数=1
- price_002975: ok，行数=1
- price_003028: ok，行数=1
- price_600078: ok，行数=1
- price_600173: ok，行数=1
- price_600303: ok，行数=1
- price_600601: ok，行数=1
- price_600626: ok，行数=1
- price_600715: ok，行数=1
- price_600785: ok，行数=1
- price_600828: ok，行数=1
- price_601086: ok，行数=1
- price_601566: ok，行数=1
- price_601956: ok，行数=1
- price_603006: ok，行数=1
- price_603037: ok，行数=1
- price_603061: ok，行数=1
- price_603081: ok，行数=1
- price_603109: ok，行数=1
- price_603131: ok，行数=1
- price_603135: ok，行数=1
- price_603219: ok，行数=1
- price_603226: ok，行数=1
- price_603303: ok，行数=1
- price_603337: ok，行数=1
- price_603370: ok，行数=1
- price_603376: ok，行数=1
- price_603418: ok，行数=1
- price_603533: ok，行数=1
- price_603565: ok，行数=1
- price_603612: ok，行数=1
- price_603626: ok，行数=1
- price_603633: ok，行数=1
- price_603667: ok，行数=1
- price_603680: ok，行数=1
- price_603758: ok，行数=1
- price_603813: ok，行数=1
- price_603868: ok，行数=1
- price_603897: ok，行数=1
- price_603920: ok，行数=1
- index_sh000001: error，行数=None
- index_retry_sh000001: error，行数=None
- index_fallback_sh000001: ok，行数=1
- index_sz399001: error，行数=None
- index_retry_sz399001: error，行数=None
- index_fallback_sz399001: ok，行数=1
- index_sz399006: error，行数=None
- index_retry_sz399006: error，行数=None
- index_fallback_sz399006: ok，行数=1
- index_csi932000: error，行数=None
- index_retry_csi932000: error，行数=None
- index_official_csi932000: ok，行数=1
