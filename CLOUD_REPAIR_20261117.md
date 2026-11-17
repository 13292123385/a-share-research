# Cloud capture repair: 2026-11-17

Observed chain: no timely noon scheduled run; BSE roster timed out at 20 seconds in emergency run 44016860346 (5224 stocks, explicitly partial); initial public publication crashed on null trade_date; raw file cache retained a placeholder and the query fallback encountered HTTP 403.

Repairs: separate 90-second BSE budget; persist same-day rosters; handle null initial pointers; check out current main; bind schedules to the intended session; report missed capture windows as failure; query the Pages mirror with raw fallback and immutable archives. Preserve SHA256, date, session, run-ID and row-count checks.

Cloud run 44017609191 successfully saved the 2026-11-17 midday snapshot, run ID 20261117T123039394573+0800, at 12:30:39 through 12:31:33 Asia/Shanghai: 5580 of 5580 stocks, complete. Both private/public GitHub archives and the actual GPT market_status/query_market tools were verified. SHA256: ffd8b376c6f7e7ec756e09927bed19690bcae460e5b400f178951eaf30a7ac75.

Validation: 143 Python tests and 9 query-service tests passed. Query deployment appgdep_6afbda3ff928819195e781da50757456 succeeded.

Remaining limit: collection uses GitHub-hosted runners. GitHub schedules can be delayed or dropped. The separate Sites status monitor only detects/alerts; an independent capture trigger remains unprovisioned. Today's recovery was remotely started with the existing local login, but collection itself ran in the cloud. Future automatic timeliness is not guaranteed. Today's closing session had not occurred at verification time.
