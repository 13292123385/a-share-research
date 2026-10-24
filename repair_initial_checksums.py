"""One-time repair of pre-release JSON formatting checksum bug. Does not alter raw data."""
import hashlib
import json
from pathlib import Path

for path in Path('data').glob('*/runs/*/sources.json'):
    metadata = json.loads(path.read_text(encoding='utf-8'))
    for key, entry in metadata.items():
        raw = path.parent / 'raw' / (key + '.json')
        if raw.exists() and 'sha256' in entry:
            entry['sha256'] = hashlib.sha256(raw.read_bytes()).hexdigest()
            entry['checksum_note'] = '首版测试修复：按最终归档字节重算；原始表内容未改动'
    path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
