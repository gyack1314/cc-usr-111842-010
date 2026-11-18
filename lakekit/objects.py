"""提供内容寻址的本地对象读写，不维护表快照。"""
from pathlib import Path
import hashlib
import os
import re
import tempfile

class Objects:
    def __init__(self, root):
        self.root=Path(root)
        self.root.mkdir(parents=True,exist_ok=True)

    def path(self, digest):
        if not re.fullmatch(r'[0-9a-f]{64}',digest):
            raise ValueError('对象摘要格式错误')
        return self.root/digest[:2]/digest[2:]

    def put(self, data):
        digest=hashlib.sha256(data).hexdigest()
        target=self.path(digest)
        target.parent.mkdir(parents=True,exist_ok=True)
        fd,tmp=tempfile.mkstemp(dir=target.parent,prefix='.writing-')
        try:
            with os.fdopen(fd,'wb') as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(tmp,target)
        finally:
            Path(tmp).unlink(missing_ok=True)
        return digest

    def read(self, digest):
        data=self.path(digest).read_bytes()
        if hashlib.sha256(data).hexdigest()!=digest:
            raise ValueError('对象内容与摘要不符')
        return data

    def list(self):
        return sorted(p.parent.name+p.name for p in self.root.glob('*/*')
                      if p.is_file() and re.fullmatch(r'[0-9a-f]{64}',p.parent.name+p.name))
