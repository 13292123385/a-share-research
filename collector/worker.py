"""Isolate each public API call: parent enforces a hard wall-clock timeout."""
import argparse
import json
from pathlib import Path
import akshare as ak
from .providers import tencent_quote
from .theme_evidence import dated_theme_evidence


def main():
    p = argparse.ArgumentParser()
    p.add_argument('function')
    p.add_argument('output')
    p.add_argument('kwargs')
    a = p.parse_args()
    function = {'tencent_quote': tencent_quote, 'dated_theme_evidence': dated_theme_evidence}.get(a.function)
    if function is None:
        function = getattr(ak, a.function)
    frame = function(**json.loads(a.kwargs))
    Path(a.output).write_text(frame.to_json(orient='records', force_ascii=False, date_format='iso'), encoding='utf-8')


if __name__ == '__main__':
    main()
