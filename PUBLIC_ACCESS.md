# 手机读取与自动采集恢复（2026-10-27）

原仓库 `a-share-research` 保持私有，采集程序和完整档案均沿用原项目。另建 `a-share-market-data` 仅发布允许公开的行情摘要和股票池，不复制代码、私人备注、账户或原始诊断。

## 手机 GPT 可用入口

- [公开行情仓库首页](https://github.com/13292123385/a-share-market-data)：GPT网页读取已实测成功。
- [纯文字报告](https://raw.githubusercontent.com/13292123385/a-share-market-data/main/latest.md)：GPT网页读取已实测成功。
- [机器摘要](https://raw.githubusercontent.com/13292123385/a-share-market-data/main/latest.json)。
- [首板候选](https://raw.githubusercontent.com/13292123385/a-share-market-data/main/first_board.json)。
- [主板涨停](https://raw.githubusercontent.com/13292123385/a-share-market-data/main/limit_up.json)。
- [历史首板跟踪](https://raw.githubusercontent.com/13292123385/a-share-market-data/main/followup.json)。
- [普通网页](https://13292123385.github.io/a-share-market-data/)：匿名HTTP200，静态HTML无需运行脚本；当前GPT网页工具未成功抓取此新域名，因此手机优先用上述已验证的GitHub/原始文件入口。

可直接给手机GPT：

> 联网读取 https://raw.githubusercontent.com/13292123385/a-share-market-data/main/latest.md 和同目录 latest.json，再按需读取 first_board.json、limit_up.json、followup.json。先核对 trade_date、collection_status 和 last_attempt。若不是今天的有效交易日归档，要明确说明日期和缺失；不要拿旧数据冒充今天，不把观察资格当可成交证明。

此前电脑通过本机Git Credential Manager登录读取私有仓库；该访问方式不能推定为手机聊天已具备。本次公开入口已经免除仓库登录要求，但无法替手机聊天启用联网工具。没有联网工具的聊天仍需上传或粘贴报告。

Gist备用：[入口](https://gist.github.com/13292123385/76d482aa7394dbc3a2125e7bb1bf9f2e)。匿名下载已实测HTTP200，但GPT网页工具拒绝抓取，故不作为手机主入口。所有公开URL和目标记录在 `public-feed.json`，不含凭据。

## 今天没有自动归档的核查结论

截至10月27日20:52，Actions API没有当天收盘后schedule运行记录，`data/2026-10-27/latest.json`为404。工作流仍active且cron存在。当天00:41的绿色运行是手动触发，不能解释为当天收盘采集成功。仓库日志无法证明GitHub调度缺席的进一步平台原因，不将其编造成Python采集错误。

已手动补采：[运行40507367701](https://github.com/13292123385/a-share-research/actions/runs/40507367701)实际成功，四指数、5577/5577市场代码覆盖、主板涨停36、首板25、一字板未知0。该轮历史首板价格71/86，剩余15只明确保留缺失，并继续复用缓存补齐。失败不是空行情，缺失不补零。

## 自动采集和发布补强

- 保留北京时间15:05、15:20、15:40；增加16:17至22:17每小时补采。GitHub仍可能延迟/丢弃调度，增加时点不等于平台可用性保证。
- 新增Windows备用检查：15:12、15:35、16:15、18:15、21:15及登录后补查。已有完整当日采集且公开入口日期正确则不重复触发；发现缺失且无运行中的作业时，触发原GitHub工作流，交易日仍由采集器日历确认。
- 本机Task Scheduler注册遭系统拒绝，已安装当前用户Startup快捷方式并启动无窗口检查进程。日志 `diagnostics/watchdog/service.log` 已确认检查生效。关闭电脑/退出用户后该备用不工作，GitHub调度仍保留；无需常驻完整采集器。
- 每次归档质量校验通过后，以字段白名单生成公开文件，自动更新Gist及纯行情发布仓库，Pages随公开数据提交更新。失败尝试状态另列，最新选用归档日期始终保留，不修改为发布时间。
- 发布凭据仅通过原仓库Actions加密Secret `PUBLIC_FEED_TOKEN`使用；Gist ID/公开目标分别为仓库Variables，不在代码、数据或日志写入令牌。该凭据沿用本机已有GitHub登录，未扩大其已有权限；工作流及Secret仅应由可信仓库写入者管理。
- 数据机器人提交前先rebase远端，减少人工代码推送与自动归档并发造成的非快进拒绝；冲突仍显式失败，不覆盖他人修改。

31项测试通过，包含公开字段白名单、不发布私人字段、旧归档日期不冒充失败当天及空目录拒绝发布；原有行情校验不变。今天补采、匿名公开下载及GPT网页读取均已实测，新增工作流自动发布还需记录实际云端结果。

卸载本机备用：删除当前用户Startup目录中的 `A-share-research closing watchdog.lnk`，并停止命令行指向本项目 `scripts/watchdog_service.py` 的pythonw进程；不要结束其他Python进程。
