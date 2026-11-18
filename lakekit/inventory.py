"""核对原始输入清单的路径、摘要、字节与物理行数。"""
from pathlib import Path
import hashlib
import json
from .physical import inspect

def load(path):
    path=Path(path)
    root=path.parent.resolve()
    manifest=json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(manifest.get('files'),list):
        raise ValueError('缺少文件清单')
    result=[]
    seen=set()
    for entry in manifest['files']:
        file=(root/entry['file']).resolve()
        if not file.is_relative_to(root) or file in seen:
            raise ValueError('文件路径越界或重复')
        seen.add(file)
        raw=file.read_bytes()
        if len(raw)!=entry['bytes'] or hashlib.sha256(raw).hexdigest()!=entry['sha256']:
            raise ValueError('清单与原始文件不符')
        item=dict(entry)
        if file.suffix=='.parquet':
            info=inspect(file)
            if info['rows']!=entry['rows']:
                raise ValueError('物理行数不符')
            item['physical_schema']=info['schema']
        result.append(item)
    return {'dataset':manifest['dataset'],'files':result}
