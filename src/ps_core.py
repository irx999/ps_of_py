"""This is a python script for photosop"""

import os
import time

from photoshop import Session


class Photoshop:
    """Photoshop 类"""

    def __init__(
        self,
        psd_name: str,
        psd_file_path: str = None,
        export_folder: str = None,
        file_format: str = "png",
        suffix: str = "",
    ):
        """
        初始化Photoshop类
        :param psd_file_path: psd文件路径,默认工作目录
        :param psd_name: psd文件名,默认test
        :param export_folder: 导出文件夹名, 是在默认工作目录下面创建,
        :param file_format: 导出文件格式，默认为png
        :param suffix: 导出文件名后缀
        """
        self.psd_name = psd_name
        self.psd_file_path = self.psd_file_path_set(psd_file_path)
        self.export_folder = self.export_folder_set(export_folder)
        self.file_format = file_format
        self.suffix = suffix if suffix else ""

        with Session(file_path=self.psd_file_path, action="open") as ps_session:
            doc = ps_session.active_document
            print(f"打开{self.psd_file_path}成功")
        self.ps_session = ps_session
        self.doc = doc
        # # 最外层图层集
        self.layer_outermost_set_name = [
            _layerSets.name for _layerSets in self.doc.layerSets
        ]
        self.saveoptions = self.ps_save_options(file_format)

        # 设置导出选项

    def psd_file_path_set(self, psd_file_path: str = None) -> str:
        """返回psd文件路径"""
        if psd_file_path is None:
            ans = f"{os.getcwd()}/psd/{self.psd_name}.psd"
        else:
            ans = f"{psd_file_path}/{self.psd_name}.psd"
        if not os.path.isfile(ans):
            ans = ans[:-1] + "b"
            if not os.path.isfile(ans):
                raise FileNotFoundError("psd或psb文件均不存在")
        return ans

    def export_folder_set(self, export_folder: str) -> str:
        """返回导出文件夹路径"""
        if export_folder is None or export_folder == "":
            export_folder = "default_export_folder"
        export_folder = f"{os.getcwd()}/{export_folder}"
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)
            print(f"创建文件夹{export_folder}成功")
        return export_folder

    def ps_save_options(self, file_format: str):
        """设置psd导出选项"""
        match file_format:
            case "jpg" | "jpeg":
                return self.ps_session.JPEGSaveOptions()
            case _:
                return self.ps_session.PNGSaveOptions()

    def ps_saveas(self, export_name: str) -> bool:
        try:
            self.doc.saveAs(
                f"{self.export_folder}/{export_name}{self.suffix}.{self.file_format}",
                self.saveoptions,
                asCopy=True,
            )
            print(f"导出{export_name}.{self.file_format}到{self.export_folder}成功")
            return True
        except Exception as e:
            print(
                f"导出{export_name}.{self.file_format}到{self.export_folder}失败\n {e}"
            )
            return False

    def open_os(self):
        pass

    def task_run(self, task: list[dict[str, dict]]):
        for index in range(len(task)):
            data_cache = self.layer_changer(task[index].values())
            self.ps_saveas(task[index].keys())

            self.layer_changer(data_cache)

    def core(self, export_name: str, input_data: dict) -> None:
        """
        :param export_name: 导出文件名
        :param input_data: 图层属性数据
        :return: None
        """
        # 修改图层属性
        data_cache = self.layer_changer(input_data)
        # 保存图片
        self.ps_saveas(export_name)
        # 提取缓存数据
        data_cache = [
            item for item in data_cache if "字体大小" in item or "visible" in item
        ]
        # 恢复图层属性
        self.layer_changer(data_cache)

    def rgb_to_hex(self, r, g, b):
        """
        :param r: 红色值
        :param g: 绿色值
        :param b: 蓝色值
        :return: 16进制颜色值
        """
        return f"#{r:02x}{g:02x}{b:02x}"

    def hex_to_rgb(self, hex_color: str):
        """
        :param ps_session: 实例化后的photoshop对象
        :param hex_color: 16进制颜色值
        :return: photoshop的SolidColor对象
        """

        def a(hex_color):
            hex_color = hex_color.lstrip("#")
            return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

        r, g, b = a(hex_color)
        text_color = self.ps_session.SolidColor()
        text_color.rgb.red = r
        text_color.rgb.green = g
        text_color.rgb.blue = b
        return text_color

    def layer_changer(self, input_data_list: list):
        """
        :param ps_doc: 实例化后的ps对象
        :param input_data_list: 传输的数据
        [
            {
                图层路径:list,
                可显性:bool,
                修改内容:str,
                字体大小:float,
                字体颜色:"#00A9FF"
            },
            {
                图层路径:["第一层","第二层","文本2"],,
                可显性:bool,
                修改内容:str,
                字体大小:float,
                字体颜色:"#00A9FF"
            },
        ...]
        :return: 修改该图层之前的属性,
        """
        data_cache_list = []

        for input_data in input_data_list:
            # 等待修改的图层集
            change_layer_list = []

            data_cache = {"图层路径": input_data["图层路径"]}
            # 先拿到需要修改的图层对象
            layer_name = self.ps_session.active_document
            for layer_item in input_data["图层路径"]:
                # 如果是图层路径的最后一个
                if layer_item == input_data["图层路径"][-1]:
                    layer_item = str(layer_item)
                    # 如果该名字是在组合中 他就是一个组合
                    if layer_item in [name.name for name in layer_name.layerSets]:
                        change_layer_list.append(
                            layer_name.layerSets.getByName(layer_item)
                        )
                    # 反之就是一个图层了
                    else:
                        change_layer_list.append(
                            layer_name.artLayers.getByName(layer_item)
                        )
                    # 这里会判断一个拷贝图层的属性是否需要修改
                    if layer_item + " 拷贝" in [
                        name.name for name in layer_name.layerSets
                    ]:
                        change_layer_list.append(
                            layer_name.layerSets.getByName(layer_item + " 拷贝")
                        )
                    if layer_item + " 拷贝" in [
                        name.name for name in layer_name.artLayers
                    ]:
                        change_layer_list.append(
                            layer_name.artLayers.getByName(layer_item + " 拷贝")
                        )
                else:
                    layer_name = layer_name.layerSets.getByName(layer_item)

            # 等待修改的图层集

            # 开始修改图层属性
            for layer_name in change_layer_list:
                if "visible" in input_data:
                    data_cache["visible"] = layer_name.visible
                    layer_name.visible = input_data["visible"]
                if "文本内容" in input_data:
                    data_cache["文本内容"] = layer_name.textItem.contents
                    layer_name.textItem.contents = str(input_data["文本内容"])
                if "字体大小" in input_data:
                    data_cache["字体大小"] = layer_name.textItem.size
                    layer_name.textItem.size = input_data["字体大小"]
                if "字体颜色" in input_data:
                    font_color = layer_name.textItem.color.rgb
                    data_cache["字体颜色"] = self.rgb_to_hex(
                        font_color.red, font_color.green, font_color.blue
                    )
                    layer_name.textItem.color = self.hex_to_rgb(input_data["字体颜色"])

            # 返回修改之前的属性
            data_cache_list.append(data_cache)
        return data_cache_list


if __name__ == "__main__":
    start_time = time.time()
    ps = Photoshop(
        psd_file_path="",
        psd_name="test",
        export_folder="",
        file_format="png",
        suffix="",
    )

    test_dict = {
        "test": [
            {
                "图层路径": ["第一层", "第二层", "文本2"],
                "visible": True,
                "文本内容": "修改为:ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "字体大小": 35,
                "字体颜色": "#00A9FF",
            }
        ],
        "test2": [
            {
                "图层路径": ["文本2"],
                "visible": True,
                "文本内容": "修改为:ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "字体大小": 35,
                "字体颜色": "#00A9FF",
            },
            {
                "图层路径": ["文本2"],
                "visible": True,
                "文本内容": "修改为:ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "字体大小": 35,
                "字体颜色": "#00A9FF",
            },
        ],
    }

    for key, value in test_dict.items():
        ps.core(key, value)
    print(f"总共耗时{time.time() - start_time}秒")
