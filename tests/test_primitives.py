"""核验原始对象和物理表工具的实际行为。"""
from pathlib import Path
import json
import tempfile
import unittest
from lakekit.objects import Objects
from lakekit.inventory import load
from lakekit.physical import rows

ROOT=Path(__file__).resolve().parents[1]

class Storage(unittest.TestCase):
    def test_content_identity_and_corruption(self):
        with tempfile.TemporaryDirectory() as directory:
            store=Objects(directory)
            first=store.put(b'parquet-input-1')
            self.assertEqual(first,store.put(b'parquet-input-1'))
            self.assertNotEqual(first,store.put(b'parquet-input-2'))
            self.assertEqual(store.read(first),b'parquet-input-1')
            self.assertEqual(len(store.list()),2)
            store.path(first).write_bytes(b'changed')
            with self.assertRaises(ValueError):store.read(first)
            with self.assertRaises(ValueError):store.read('../escape')

    def test_independent_json_parquet_values(self):
        data=json.loads((ROOT/'data/seed.json').read_text(encoding='utf-8'))
        manifest=load(ROOT/'data/inventory.json')
        parquet=[entry for entry in manifest['files'] if entry['file'].endswith('.parquet')]
        self.assertEqual(len(parquet),len(data))
        for table,expected in data.items():
            self.assertEqual(rows(ROOT/'data'/f'{table}.parquet'),expected)

    def test_manifest_rejects_escape_and_wrong_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            file=root/'object.bin';file.write_bytes(b'abc')
            manifest=root/'inventory.json'
            manifest.write_text(json.dumps({'files':[{'file':'../outside.bin'}]}))
            with self.assertRaises(ValueError):load(manifest)
            manifest.write_text(json.dumps({'files':[{'file':'object.bin','bytes':3,'sha256':'0'*64}]}))
            with self.assertRaises(ValueError):load(manifest)

if __name__=='__main__':unittest.main()
