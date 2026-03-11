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

# 🧠  更改日志 / CHANGE_LOGS


> ## [0.3.2] - 2026-03-11
> 
> 【🎉新增】
> - 合并文件夹中会 创建一个汇总文件夹 来收集所有创建的文件





> ## [0.3.1] - 2026-03-11
> 
> 【🎉新增】
> - 修改了UI页面
> - 增加了日志查看
> 
> 【🔨修复】
> - 修复了文本内容如果填入的是一个整数的浮点数有0.1 的问题







> ## [0.0.2] - 2026-03-11
> 
> 【🎉新增】
> - 图层移动和旋转功能支持
> - 嵌套图层集操作支持
> - 批量处理多个配置示例
> - 更完善的错误处理和日志记录
> 
> 【🔨修复】
> - 修复文本图层修改可能不生效的问题
> - 优化PSD文件路径处理逻辑
> - 改进图层状态管理机制
> 
> 【✨优化】
> - 完善使用文档和示例代码
> - 优化上下文管理器资源释放
> - 提升批量处理性能

> ## [0.0.1] - 2025-10-25
> 
> 【🎉新增】
> - 项目基础框架搭建
> - 图层可见性控制功能
> - 文本图层内容修改功能
> - 字体大小和颜色调整功能
> - 批量导出图片功能
> 
> 【🔨修复】
> - 图层状态恢复机制
> - 多次修改同一图层的问题
> 
> 【✨优化】
> - 代码结构优化，采用工厂模式
> - 日志记录功能增强
> - 错误处理机制完善