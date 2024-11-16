# ps_of_py

## todo
 - [ ] 多种参数调节,如指定图层位置
 - [ ] 完成更优雅的excel 交互

## 文件说明
### ps.py
创建实例
```python
:param psd_file_path: psd文件路径,默认工作目录
:param psd_name: psd文件名,默认test
:param export_folder: 导出文件夹名, 是在默认工作目录下面创建,
:param file_format: 导出文件格式，默认为png
:param suffix: 导出文件名后缀
```


接受参数
```python
:param export_name: 导出文件名
:param input_data: 图层属性数据
```

input_data格式
```python
test_dict = {
        "测试导出图片1":[
            {
                "图层路径":["第一层","第二层","文本2"],
                "visible":True,
                "文本内容":"修改为:ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "字体大小":35,
                "字体颜色":"#00A9FF",
            }
        ],
        "测试导出图片2":[
            {
                "图层路径":["文本2"],
                "visible":True,
                "文本内容":"修改为:ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "字体大小":35,
                "字体颜色":"#00A9FF",
            },
            {
                "图层路径":["文本2"],
                "visible":True,
                "文本内容":"修改为:ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "字体大小":35,
                "字体颜色":"#00A9FF",
            },
            {
                "图层路径":["第一层","第二层","文本2"],
                "visible":True,            }
            ]
}
```

### load_data.py
读取设定的文件，返回需要的参数和信息
```python
:param sheet_name: str, sheet name
:param table_name: str or int, table name or index
