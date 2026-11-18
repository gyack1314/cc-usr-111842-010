# 实验湖表更新层合并与在线压实

此工程提供研究原始资料的物理检查和内容寻址对象工具。资料全部合成，不对应真实个人、研究结论或医疗建议。当前没有逻辑湖表目录、来源接收进度或跨表查询版本；单个文件的读取成功仅证明该物理文件可以打开。

Python 3.11，依赖 DuckDB 1.4.1、PyArrow 22.0.0。安装使用 `python -m pip install -r requirements.txt`。可以执行 `docker build -t research-lake .` 后运行 `docker run --rm research-lake`，镜像默认检查原始资料清单，不访问外部业务服务。

`python -m lakekit data/inventory.json` 校验实际文件摘要、大小和 Parquet 行数。`python -m unittest discover -s tests -v` 检查对象损坏、路径约束及独立 JSON 与 Parquet 的值一致性。`python -m compileall -q lakekit tests` 检查源码语法。入口可从工程根目录运行。

`data/seed.json` 与同名 Parquet 表保存同一份原始值，`data/events.json` 保存尚未应用的业务动作，`data/contracts.json` 记录输入字段和标识约定。事件不是已有功能的执行结果。字段与空值以这些可访问资料为依据，工具不替使用者应用事件或生成业务结论。

`lakekit.objects.Objects` 提供对象按摘要写入、读取校验及完整本地目录枚举；它没有快照、引用或事务语义。`lakekit.physical` 仅打开明确指定的单个 Parquet，`lakekit.inventory` 核对种子清单。新能力可复用这些工具，但对逻辑仓湖行为与兼容方式不预设内部结构。
