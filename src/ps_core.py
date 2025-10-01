"""This is a python script for photosop"""

import os
import time

from photoshop import Session

from src.logger import Logger
from src.timer import timer

logger = Logger(__name__, log_name="core", debug_mode=True)


class Photoshop:
    """Photoshop 类"""

    def __init__(
        self,
        psd_name: str,
        psd__dir_path: str = None,
        export_folder: str = None,
        file_format: str = "png",
    ):
        """
        初始化Photoshop类
        :param psd_file_path: psd文件路径,默认工作目录
        :param psd_name: psd文件名,默认test
        :param export_folder: 导出文件夹名, 是在默认工作目录下面创建,
        :param file_format: 导出文件格式，默认为png
        """
        self.psd_name = psd_name
        self.psd__dir_path = psd__dir_path
        self.export_folder = self.export_folder_set(export_folder)
        self.file_format = file_format

        self.init()

    def init(self):
        self.psd_file_path = self.psd_file_path_set()
        with Session(file_path=self.psd_file_path, action="open") as ps_session:
            self.ps_session = ps_session
            self.doc = ps_session.active_document

            self.saveoptions = self.saveoptions_set(self.file_format)
            self.layer_list: dict = {}  # 图层列表

            self.layer_initial_state: dict = {}  # 图层初始状态
            self.layer_current_state: dict = {}  # 图层当前状态

            self.run_time_record_list = []

    def reconnect(self):
        """重新建立 Photoshop 会话"""
        self.init()

    def __str__(self) -> str:
        str = f"""
        当前执行的psd文件为：{self.ps_session.active_document.name}
        
        文件路径为：{self.psd_file_path}

        当前psd尺寸为  {self.doc.width} * {self.doc.height}

        当前psd的具有图层：{
            [
                _artLayers.name
                for _artLayers in self.ps_session.active_document.artLayers
            ]
        }
        当前psd的具有图层集：{
            [
                _layerSets.name
                for _layerSets in self.ps_session.active_document.layerSets
            ]
        }

        """
        return str

    def psd_file_path_set(self) -> str:
        """返回psd文件路径"""
        base_path = self.psd__dir_path or os.path.join(os.getcwd(), "psd")
        ans = os.path.join(base_path, f"{self.psd_name}.psd")

        if not os.path.isfile(ans) and not os.path.isdir(ans[:-1] + "b"):
            raise FileNotFoundError("psd或psb文件均不存在")
        return ans

    def export_folder_set(self, export_folder: str | None) -> str:
        """返回导出文件夹路径"""
        try:
            if not export_folder or export_folder.strip() == "":
                export_folder = "default_export_folder"

            full_path = os.path.join(os.getcwd(), export_folder)

            if not os.path.exists(full_path):
                os.makedirs(full_path)
                logger.info(f"创建文件夹 {full_path} 成功")

            return full_path

        except Exception as e:
            logger.error(f"创建文件夹 {export_folder} 失败: {e}")
            return ""

    def saveoptions_set(self, file_format: str):
        """设置psd导出选项"""
        match file_format:
            case "jpg" | "jpeg":
                return self.ps_session.JPEGSaveOptions()
            case _:
                return self.ps_session.PNGSaveOptions()

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

    def ps_saveas(self, export_name: str) -> bool:
        try:
            self.doc.saveAs(
                f"{self.export_folder}/{export_name}.{self.file_format}",
                self.saveoptions,
                asCopy=True,
            )
            logger.info(
                f"导出{export_name}.{self.file_format}到{self.export_folder}成功"
            )
            return True
        except Exception as e:
            logger.info(
                f"导出{export_name}.{self.file_format}到{self.export_folder}失败\n {e}"
            )
            return False

    @timer()
    def core(self, export_name: str, input_data: dict):
        """核心函数"""
        start_time = time.time()

        # 1.找当已经 修改的记录中但是接下来的不需要修改 及 需要恢复的
        current_all_initialized = set(self.layer_current_state.keys())

        for 需要恢复的 in current_all_initialized - input_data.keys():
            initial_state = self.layer_initial_state.get(需要恢复的, {})
            if not initial_state:
                continue
            logger.info(f"正在恢复图层 {需要恢复的} 到初始状态")
            try:
                self.change_layer_state(需要恢复的, initial_state)

                del self.layer_initial_state[需要恢复的]
            except Exception as e:
                logger.error(f"恢复图层 {需要恢复的} 失败: {e}")

        for layer_name, layer_info in input_data.items():
            # 2. 执行任务之前看是否修改的属性需要记录 修改前状态
            if layer_name not in self.layer_initial_state:
                logger.debug(f"图层 {layer_name} 需要记录初始状态")
                # 有visible 属性直接记录
                if layer_info.get("visible", False):
                    self.save_initial_layer_state(layer_name, layer_info)
                # 有 文本属性  中的size 或者 color
                elif "textItem" in layer_info and any(
                    layer_info["textItem"].get(key) for key in ["size", "color"]
                ):
                    self.save_initial_layer_state(layer_name, layer_info)

            current_state = self.layer_current_state.get(layer_name, {})

            # 增加对textItem属性的检查
            if "textItem" in current_state and "textItem" in layer_info:
                current_text_item = current_state["textItem"]
                new_text_item = layer_info["textItem"]

                # 如果之前修改过字体大小或颜色，但这次不需要修改
                if (current_text_item.get("size") is not None and "size" not in new_text_item) or \
                   (current_text_item.get("color") is not None and "color" not in new_text_item):
                    logger.info(f"图层 {layer_name} 需要先恢复字体大小和颜色到初始状态")
                    self.restore_text_item_to_initial(layer_name)

            # 3. 判断是否需要真正修改
            if current_state != layer_info:
                logger.info(
                    f"图层 {layer_name} 状态不一致\n修改前: {current_state}\n修改后: {layer_info}"
                )
                logger.debug(f"图层 {layer_name} 需要修改")
                # 4. 执行修改
                self.change_layer_state(layer_name, layer_info)
                self.layer_current_state[layer_name] = layer_info
            else:
                logger.info(f"图层 {layer_name} 状态一致，无需修改")

        # 5. 导出文件
        self.ps_saveas(export_name)

        self.run_time_record_list.append(time.time() - start_time)

    def get_layer_by_layername(self, layername: str):
        """根据层名获取图层"""

        if layername in self.layer_list:
            return self.layer_list[layername]

        layer_path = layername.split("/")
        change_layer_list = []

        # 根路径
        current_layer = self.ps_session.active_document

        for layer_item in layer_path[:-1]:
            try:
                current_layer = current_layer.layerSets.getByName(layer_item)
            except Exception:
                logger.info(f"未找到图层集 '{layer_item}' 在路径 {layer_path}")
                break
        else:
            final_name = layer_path[-1]
            target_layer = None
            # 有限查找图层集
            if final_name in [ls.name for ls in current_layer.layerSets]:
                target_layer = current_layer.layerSets.getByName(final_name)

            # 再有限查找图层
            elif final_name in [al.name for al in current_layer.artLayers]:
                target_layer = current_layer.artLayers.getByName(final_name)

            if target_layer:
                change_layer_list.append(target_layer)
            else:
                logger.info(f"未找到图层 '{final_name}' 在路径 {layer_path}")

            copy_name = final_name + " 拷贝"
            if copy_name in [ls.name for ls in current_layer.layerSets]:
                change_layer_list.append(current_layer.layerSets.getByName(copy_name))
            elif copy_name in [al.name for al in current_layer.artLayers]:
                change_layer_list.append(current_layer.artLayers.getByName(copy_name))

        self.layer_list[layername] = change_layer_list
        return change_layer_list

    def restore_all_layers_to_initial(self):
        """
        将所有图层恢复到初始状态
        """
        logger.info("开始恢复所有图层到初始状态...END")
        for layer_key, initial_state in self.layer_initial_state.items():
            self.change_layer_state(layer_key, initial_state)

        # 清空当前状态缓存
        self.layer_current_state.clear()
        logger.info("所有图层已恢复到初始状态...END")

        # self.doc.close()

    def save_initial_layer_state(self, layername: str, layerinfo: dict):
        if layername not in self.layer_initial_state:
            try:
                target_layers = self.get_layer_by_layername(layername)
                for target_layer in target_layers:
                    if target_layer:
                        state = {}
                        if "visible" in layerinfo:
                            state["visible"] = target_layer.visible
                        if "textItem" in layerinfo:
                            state["textItem"] = {}
                            text_item = target_layer.textItem
                            state["textItem"]["contents"] = text_item.contents
                            state["textItem"]["size"] = text_item.size
                            font_color = text_item.color.rgb
                            state["textItem"]["color"] = self.rgb_to_hex(
                                font_color.red, font_color.green, font_color.blue
                            )

                        # 同时保存初始状态 和 当前状态
                        self.layer_initial_state[layername] = state.copy()
                        self.layer_current_state[layername] = state.copy()

                        logger.info(f"保存初始状态成功: {layername=}, {state=}")
            except Exception as e:
                logger.info(f"无法保存图层 {layername} 的初始状态: {e}")

    def change_layer_state(self, layer_key: str, initial_state: dict) -> None:
        try:
            for target_layer in self.get_layer_by_layername(layer_key):
                if target_layer:
                    # 修改可见性
                    if "visible" in initial_state:
                        target_layer.visible = initial_state["visible"]
                    # 如果是文本图层，修改文本属性
                    if "textItem" in initial_state:
                        text_item_state = initial_state["textItem"]
                        for key, attr_name in text_item_state.items():
                            if key == "color":
                                target_layer.textItem.color = self.hex_to_rgb(attr_name)
                                continue
                            if key == "contents":
                                if isinstance(attr_name, (int, float)):
                                    attr_name = str(int(attr_name))

                            setattr(target_layer.textItem, key, attr_name)
                    logger.info(f"图层 {layer_key} 已修改属性 {initial_state}")
                else:
                    logger.info(f"图层 {layer_key} 不存在，修改")

        except Exception as e:
            logger.error(f"修改图层 {layer_key} 失败: {e}")

    def restore_text_item_to_initial(self, layer_name: str):
        """将指定图层的文本属性恢复到初始状态"""
        initial_state = self.layer_initial_state.get(layer_name, {})
        if "textItem" in initial_state:
            self.change_layer_state(layer_name, initial_state)
            logger.info(f"图层 {layer_name} 的文本属性已恢复到初始状态")

if __name__ == "__main__":
    pass
