# ps_of_py


## 官方文档
[文档](https://photoshop-python-api.readthedocs.io/en/master/)



## todo
 - [ ] 多种参数调节,如指定图层位置
 - [ ] 完成更优雅的excel 交互

## 文件说明
### ps.py
创建实例
```python
:param psd_name: psd文件名
:param psd_file_path: psd文件路径,默认工作目录
:param export_folder: 导出文件夹名, 默认未default_export_folder
:param file_format: 导出文件格式，默认为png
```


接受参数
```python
:param export_name: 导出文件名
:param input_data: 图层属性数据
```

input_data格式
```python
test_dict = {
            "No1": {
                "标题/标题2": {
                    "visible": True,
                    "textItem": {
                        "contents": "标题第一次修改",
                        "size": 35,
                        "color": "#086D7A",
                    },
                },
                "显卡/GV-N5060OC-8GL": {
                    "visible": True,
                },
            },
            "No2": {
                "标题/标题2": {
                    "visible": True,
                    "textItem": {
                        "contents": "标题第一次修改",
                        "size": 35,
                        "color": "#086D7A",
                    },
                },
                "显卡/GV-N5060OC-8GL": {
                    "visible": False,
                },
            },
            "No3": {
                "标题/标题2": {
                    "visible": True,
                    "textItem": {
                        "contents": "标题第二次修改",
                        "size": 35,
                        "color": "#C218C2",
                    },
                },
                "显卡/GV-N5060GAMING OC-8GD": {
                    "visible": True,
                },
            },
        }
```

### load_data.py
读取设定的文件，返回需要的参数和信息
```python
:param sheet_name: str, sheet name
:param table_name: str or int, table name or index
