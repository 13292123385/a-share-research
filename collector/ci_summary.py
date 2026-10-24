"""Expose collection completeness on the Actions run summary."""
import json
import os
from pathlib import Path


def render(summary):
    v = summary.get('verified', {})
    prices = summary.get('candidate_price_quality', {})
    followup = summary.get('followup', {})
    market = summary.get('estimates', {}).get('market', {})
    lines = [f'## {summary["trade_date"]} 收盘采集', '',
             f'数据状态：**{summary["status"]}**（测试通过不代表数据齐全）', '',
             f'- 主板涨停：{v.get("mainboard_limit_up_count", "缺失")}',
             f'- 指数：{len(v.get("indices", []))}/4',
             f'- 历史候选价格：{prices.get("historical_available", 0)}只；待补{len(prices.get("missing_codes", []))}只',
             f'- 首板后续跟踪：{followup.get("prices_available", 0)}/{followup.get("rows", 0)}条有价格',
             f'- 市场行情来源：{market.get("source", "缺失")}；范围：{market.get("scope", "缺失")}',
             '', '### 缺失项目', '']
    lines += ['- ' + item for item in summary.get('missing_data', [])] or ['- 无']
    lines += ['', '### 失败尝试（备用源成功后仍保留证据）', '']
    lines += [f'- {key}: {meta.get("status")} / {meta.get("error", "无异常类别")}'
              for key, meta in summary.get('source_failures', {}).items()] or ['- 无']
    lines += ['', '完整文件见本次运行的 Artifacts；未验证实际成交，不提供真实策略收益。', '']
    return '\n'.join(lines)


def main():
    current = os.environ.get('COLLECT_SUMMARY_FILE')
    paths = ([Path(current)] if current and Path(current).is_file() else [])
    if not os.environ.get('GITHUB_ACTIONS') and not current:
        paths = list(Path('data').glob('*/runs/*/summary.json'))
    if not paths:
        content = '## 收盘采集\n\n未产生采集摘要，请查看安装、测试与采集日志。\n'
    else:
        latest = max(paths, key=lambda p: p.stat().st_mtime_ns)
        content = render(json.loads(latest.read_text(encoding='utf-8')))
    destination = os.environ.get('GITHUB_STEP_SUMMARY')
    if destination:
        with open(destination, 'a', encoding='utf-8') as f:
            f.write(content)
    else:
        print(content)


if __name__ == '__main__':
    main()
