<h1 align="center"> 🍃 Photoshop Python 自动化工具 🐍 </h1>

<p align="center"> 仅仅是万千尘土中的一粒</p>
<h1 align="center">让设计工作更加高效 | 让重复操作自动化</h1>
<p align="center"> <img src="https://skillicons.dev/icons?i=vscode,python,ps,git" /><br></p>




> [!TIP]
> **基于Python和Adobe Photoshop API的自动化批处理工具**

> [!NOTE]
> **需要安装Adobe Photoshop并启用脚本功能才能正常使用,不支持云服务器运行**

> [!WARNING]
> **进行PS 操作时候请勿再修改PSD**


# 🌟 官方文档 / OFFICIAL_DOCUMENTATION
[photoshop_python_api](https://photoshop-python-api.readthedocs.io/en/master/index.html)

# 🌟 特别功能 /  Special Features

> ### 🎨 自动化图层处理
>> 支持批量修改图层或图层组可见性
>>> 支持文本图层内容修改
>>> 支持字体大小,颜色,字体,删除线调整
>>> 支持图层移动和旋转
>>>> 支持嵌套图层集操作
>>>>> 支持导出多种格式文件

# ✅  代办事项 / Todolist
- [x] 核心功能实现
- [x] 多种参数调节，如指定图层位置
- [x] README编写完成
- [ ] 完成更优雅的Excel交互
- [ ] 支持更多图层属性修改


# 🪲 已知错误 / BUG

- 暂不支持文本换行


# ❓ 常见问题 / Q&A 

- Q: 为什么运行时报错找不到PSD文件？
  A: 请检查PSD文件路径是否正确，并确保Photoshop已安装且可正常运行
  
- Q: 文本图层修改后没有生效？
  A: 请确认图层名称是否完全匹配，包括嵌套层级路径

- Q: excel 的语法糖 到底用哪个
  A: 1.英文模式下的 "|" 键盘中 "shift+\"  

- Q: 常用的两个 语法
  A: 更改文本    ->   文本|图层路径
  A: 更改可显性  ->   可显性|图层路径

# 📖 使用案例 / Use Cases

### 基础使用
```python
from src.ps.ps_core import Photoshop

# 初始化Photoshop实例
with Photoshop("example.psd") as ps:
    # 定义要修改的图层数据
    input_data = {
        "图层1": {
            "visible": True,
            "textItem": {
                "contents": "新文本内容",
                "size": 24,
                "color": "#FF0000"
            }
            "move": (250, 250),
            "rotate": -180,
        }
    }
    # 执行核心处理并导出
    ps.core("output_image", input_data)
```

### 批量处理多个配置
```python
from src.ps.ps_core import Photoshop

configs = {
    "version1": {
        "标题/标题1": {
            "textItem": {
                "contents": "version1",
            },
        },
        "图片/图片1": {
            "visible": True,
        },
    },
    "version2": {
        "标题/标题1": {
            "visible": True,
            "textItem": {
                "contents": "version2",
                "size": 50,
                "color": "#086D7A",
            },
        },
        "图片/图片1": {
            "visible": True,
            "move": (250, 250),
            "rotate": -180,
        },
    },
}

with Photoshop("product_template.psd") as ps:
    for name, config in configs.items():
        ps.core(name, config)
```

# 🧡 特别感谢 / Special Thanks

- 感谢Adobe Photoshop Python API项目
- 感谢所有开源组件的支持

