"""读取一个明确指定的物理表，不推断逻辑版本。"""
from pathlib import Path
import duckdb
import pyarrow.parquet as pq

def inspect(path):
    file=pq.ParquetFile(path)
    return {'rows':file.metadata.num_rows,'row_groups':file.metadata.num_row_groups,
            'schema':str(file.schema_arrow)}

def rows(path):
    connection=duckdb.connect(':memory:')
    try:
        relation=connection.read_parquet(str(Path(path)))
        names=relation.columns
        return [dict(zip(names,row)) for row in relation.fetchall()]
    finally:
        connection.close()
