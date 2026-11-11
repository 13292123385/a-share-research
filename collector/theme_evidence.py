"""Dated third-party active-theme evidence, never a complete constituent universe."""
import hashlib
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import pandas as pd
import requests
from bs4 import BeautifulSoup


def parse_evidence(html, target, fetched_at, source_url):
    soup = BeautifulSoup(html, 'html.parser')
    heading = soup.select_one('#concept-title strong')
    if heading is None or heading.get_text(strip=True) != target:
        raise ValueError('evidence_date_mismatch')
    result, seen = [], set()
    digest = hashlib.sha256(html.encode('utf-8')).hexdigest()
    for row in soup.select('#market-concepts tbody tr'):
        link = row.select_one('.concept-detail-link')
        if link is None:
            continue
        query = parse_qs(urlparse(link.get('href','')).query)
        name = link.get_text(strip=True)
        if query.get('date') != [target.replace('-','')] or query.get('name') != [name]:
            raise ValueError('theme_link_mismatch')
        for stock in row.select('.concept-stock'):
            match = re.fullmatch(r'(\d{6})\.(SH|SZ|BJ)', stock.get('title',''))
            detail = stock.select_one('.stock-detail-link')
            if not match or detail is None:
                raise ValueError('stock_identity_missing')
            if 'gupiao-'+match[1]+'.html' not in detail.get('href','') or parse_qs(urlparse(detail['href']).query).get('review_date') != [target]:
                raise ValueError('stock_link_mismatch')
            key = (name,match[1])
            if key in seen:
                raise ValueError('duplicate_theme_stock')
            seen.add(key)
            result.append(dict(theme_id='dabanke:'+name, theme_name=name, code=match[1],
                name=detail.get_text(strip=True), observation_date=target, fetched_at=fetched_at,
                source='打板客公开复盘', source_url=source_url, source_sha256=digest,
                mapping_kind='published_active_stock_association', coverage='partial_selected_active_stocks',
                source_price_used=False, execution_verified=False,
                note='第三方复盘展示的活跃股关联；不是完整成分、已确认涨停原因或全市场排名。历史页面可能被修订，非当时已知快照。'))
    if not result:
        raise ValueError('empty_theme_evidence')
    return result


def dated_theme_evidence(trade_date, archive_path):
    target = datetime.strptime(trade_date,'%Y-%m-%d').date().isoformat()
    url = 'https://www.dabanke.com/index-'+target.replace('-','')+'.html'
    response = requests.get(url,timeout=15)
    response.raise_for_status()
    response.encoding='utf-8'
    html=response.text
    rows=parse_evidence(html,target,datetime.now().astimezone().isoformat(),url)
    Path(archive_path).write_text(html,encoding='utf-8')
    return pd.DataFrame(rows)
