"""Small free-provider adapters with explicit identity and timestamp checks."""
from datetime import datetime, time
import re
import pandas as pd
import requests
from .model import number


def parse_tencent_quote(payload, symbol, trade_date):
    if not re.fullmatch(r'(?:sh|sz|bj)\d{6}', symbol):
        raise ValueError('invalid_symbol')
    match = re.fullmatch(r'\s*v_' + re.escape(symbol) + r'="([^"]*)";\s*', payload)
    if not match:
        raise ValueError('quote_schema')
    fields = match[1].split('~')
    if len(fields) < 38 or fields[2] != symbol[2:]:
        raise ValueError('quote_identity')
    stamp = datetime.strptime(fields[30], '%Y%m%d%H%M%S')
    if stamp.date().isoformat() != trade_date or stamp.time() < time(15):
        raise ValueError('quote_date_or_not_closed')
    close, opening, high, low, pct, amount = [number(fields[i]) for i in (3, 5, 33, 34, 32, 37)]
    if None in (close, opening, high, low, pct, amount) or amount < 0 or not 0 < low <= min(opening, close) <= max(opening, close) <= high:
        raise ValueError('quote_values')
    return {'代码': fields[2], '名称': fields[1], '今开': opening, '最高': high, '最低': low,
            '最新价': close, '涨跌幅': pct, '成交额': amount * 10000,
            'quote_date': trade_date, 'quote_timestamp': stamp.isoformat(),
            'supplement_source': '腾讯实时单股报价，成交额字段37由万元转元',
            '成交量': None, 'volume_unit': '未独立确认单位，未换算'}


def tencent_quote(symbol, trade_date):
    if not re.fullmatch(r'(?:sh|sz|bj)\d{6}', symbol):
        raise ValueError('invalid_symbol')
    response = requests.get('https://qt.gtimg.cn/q=' + symbol, timeout=10)
    response.raise_for_status()
    response.encoding = 'gbk'
    return pd.DataFrame([parse_tencent_quote(response.text, symbol, trade_date)])
