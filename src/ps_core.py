"""This is a python script for photoshop"""

import os
import time

from loguru import logger
from photoshop import Session
from photoshop.api._artlayer import ArtLayer
from photoshop.api._layerSet import LayerSet

from .layer_factory import LayerStateFactory
from .ps_utils import ExportOptionsFactory

logger.add("core.log", rotation="1 MB")


class Photoshop:
    """Photoshop操作类"""

    def __init__(
        self,
        psd_name: str,
        psd_dir_path: str = None,
        export_folder: str = "default_export_folder",
        file_format: str = "png",
    ):
        """
        初始化Photoshop类
        :param psd_name: psd文件名
        :param psd_dir_path: psd文件路径,默认工作目录下的psd文件夹
        :param export_folder: 导出文件夹名,是在默认工作目录下创建
        :param file_format: 导出文件格式，默认为png
        """
        self.psd_name = psd_name
        self.psd_dir_path = psd_dir_path
        self.export_folder = self._create_export_folder(export_folder)
        self.file_format = file_format.lower()

        # 初始化PS会话
        self._init_ps_session()

    def _init_ps_session(self):
        """
        初始化Photoshop会话
        """
        self.psd_file_path = self._get_psd_file_path()
        with Session(file_path=self.psd_file_path, action="open") as ps_session:
            self.ps_session = ps_session
            self.doc = ps_session.active_document

            # 使用工厂创建导出选项
            self.saveoptions = ExportOptionsFactory.create_export_options(
                self.file_format
            )
        # 初始化图层相关属性
        self.layer_dict: dict = {}  # 图层列表
        self.layer_initial_state: dict = {}  # 图层初始状态
        self.layer_current_state: dict = {}  # 图层当前状态
        self.run_time_record: dict = {}  # 运行时间记录

    def _get_psd_file_path(self) -> str | None:
        """
        获取PSD文件路径
        :return: PSD文件完整路径
        """
        try:
            base_path = self.psd_dir_path or os.path.join(os.getcwd(), "psd")
            # 尝试PSD和PSB两种格式
            for ext in [".psd", ".psb"]:
                file_path = os.path.join(base_path, f"{self.psd_name}{ext}")
                if os.path.isfile(file_path):
                    return file_path
        except Exception as e:
            logger.error(f"获取PSD文件路径失败: {e}")
            raise FileNotFoundError(f"找不到PSD文件: {self.psd_name}")

    def _create_export_folder(self, export_folder: str) -> str:
        """
        创建导出文件夹
        :param export_folder: 导出文件夹名
        :return: 导出文件夹完整路径
        """
        try:
            full_path = os.path.join(os.getcwd(), export_folder)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
                logger.warning(f"创建文件夹 {full_path} 成功")
            return full_path

        except Exception as e:
            raise FileNotFoundError(f"创建文件夹 {full_path} 失败: {e}")

    def get_psd_info(self) -> dict:
        """
        返回当前psd文件信息，包括所有图层集及其对应的图层
        """
        # 获取顶层图层
        top_level_layers = [
            layer.name for layer in self.ps_session.active_document.artLayers
        ]

        # 构建图层集及其子图层的详细信息
        layerset_details = []
        for layer_set in self.ps_session.active_document.layerSets:
            layers_in_set = [layer.name for layer in layer_set.artLayers]
            layerset_details.append(f"{layer_set.name}: {layers_in_set}")

        return {
            "name": self.ps_session.active_document.name,
            "psd_file_path": self.psd_file_path,
            "psd_size": {"width": self.doc.width, "height": self.doc.height},
            "top_level_layers": top_level_layers,
            "layerset_details": chr(10).join(layerset_details),
        }

    def ps_saveas(self, export_name: str):
        """保存文件到指定路径"""
        try:
            self.doc.saveAs(
                f"{self.export_folder}/{export_name}.{self.file_format}",
                self.saveoptions,
                asCopy=True,
            )
            logger.info(
                f"导出{export_name}.{self.file_format}到{self.export_folder}成功"
            )
        except Exception as e:
            logger.info(
                f"导出{export_name}.{self.file_format}到{self.export_folder}失败\n {e}"
            )
            raise Exception(f"保存文件到指定路径失败: {e}")

    def change_layer_state(self, layer_name: str, change_state: dict):
        """修改图层状态"""
        layer_list = self.get_layer_by_layername(layer_name)
        for layer in layer_list:
            LayerStateFactory.change_layer_state(layer, change_state)
            self.layer_current_state[layer_name] = change_state

    def core(self, export_name: str, input_data: dict):
        """核心处理函数"""
        start_time = time.time()

        # 1.查找已经修改但接下来不需要修改的图层，需要恢复的图层
        current_all_initialized = set(self.layer_current_state.keys())
        for layer_to_restore in current_all_initialized - input_data.keys():
            initial_state = self.layer_initial_state.get(layer_to_restore, {})
            if not initial_state:
                continue
            logger.info(f"正在恢复图层 {layer_to_restore} 到初始状态")
            try:
                self.change_layer_state(layer_to_restore, initial_state)

                del self.layer_initial_state[layer_to_restore]
            except Exception as e:
                logger.error(f"恢复图层 {layer_to_restore} 失败: {e}")

        # 2. 执行任务之前看是否修改的属性需要记录修改前状态
        for layer_name, change_state in input_data.items():
            if layer_name not in self.layer_initial_state:
                logger.debug(f"图层 {layer_name} 需要记录初始状态")
                # 有visible属性直接记录
                if change_state.get("visible", False):
                    self.save_initial_layer_state(layer_name, change_state)

                elif change_state.get("move", False):
                    self.save_initial_layer_state(layer_name, change_state)
                # 有文本属性中的size或者color
                elif "textItem" in change_state and any(
                    change_state["textItem"].get(key) for key in ["size", "color"]
                ):
                    self.save_initial_layer_state(layer_name, change_state)

            current_state = self.layer_current_state.get(layer_name, {})

            # 增加对move属性的检查
            if "move" in current_state:
                current_move = current_state["move"]
                new_move = change_state.get("move", None)
                # 如果之前修改过位置或旋转，但这次不需要修改
                if current_move is not None and new_move is None:
                    logger.info(f"图层 {layer_name} 需要先恢复位置到初始状态")
                    self.change_layer_state(
                        layer_name,
                        self.layer_initial_state.get(layer_name, {}),
                    )

            # 增加对textItem属性的检查
            if "textItem" in current_state and "textItem" in change_state:
                current_text_item = current_state["textItem"]
                new_text_item = change_state["textItem"]

                # 如果之前修改过字体大小或颜色，但这次不需要修改
                if (
                    current_text_item.get("size") is not None
                    and "size" not in new_text_item
                ) or (
                    current_text_item.get("color") is not None
                    and "color" not in new_text_item
                ):
                    logger.info(f"图层 {layer_name} 需要先恢复字体大小和颜色到初始状态")
                    self.restore_text_item_to_initial(layer_name)

            # 3. 判断是否需要真正修改
            if current_state != change_state:
                logger.info(
                    f"图层 {layer_name} 状态不一致\n修改前: {current_state}\n修改后: {change_state}"
                )
                logger.debug(f"图层 {layer_name} 需要修改")
                # 4. 执行修改
                self.change_layer_state(layer_name, change_state)
            else:
                logger.info(f"图层 {layer_name} 状态一致，无需修改")

        # 5. 导出文件
        self.ps_saveas(export_name)

        # 6. 记录运行时间
        self.run_time_record[export_name] = time.time() - start_time

    def get_layer_by_layername(self, layername: str) -> list[LayerSet | ArtLayer]:
        """根据层名获取图层"""

        if layername in self.layer_dict:
            # 如果层名在图层列表中，则直接返回
            return self.layer_dict[layername]

        layer_path = layername.split("/")
        final_name = layer_path[-1]
        copy_name = f"{final_name} 拷贝"
        change_layer_list = []

        # 根路径
        root_path = self.ps_session.active_document
        # 循环找到最后一个节点
        for layer_item in layer_path[:-1]:
            try:
                current_layer = root_path.layerSets.getByName(layer_item)
            except Exception:
                logger.error(f"未找到图层集 '{layer_item}' 在路径 {layer_path}")
                break
        else:
            layerSets_list = [layerSet.name for layerSet in current_layer.layerSets]
            artLayers_list = [artLayer.name for artLayer in current_layer.artLayers]
            # 优先查找图层集
            if final_name in layerSets_list:
                target_layer = current_layer.layerSets.getByName(final_name)
                change_layer_list.append(target_layer)
                if copy_name in layerSets_list:
                    target_layer = current_layer.layerSets.getByName(copy_name)
                    change_layer_list.append(target_layer)
            # 再查找图层
            elif final_name in artLayers_list:
                target_layer = current_layer.artLayers.getByName(final_name)
                change_layer_list.append(target_layer)
                if copy_name in artLayers_list:
                    target_layer = current_layer.artLayers.getByName(copy_name)
                    change_layer_list.append(target_layer)

            else:
                logger.error(f"未找到图层 '{final_name}' 在路径 {layer_path}")

        self.layer_dict[layername] = change_layer_list
        return change_layer_list

    def restore_all_layers_to_initial(self):
        """
        将所有图层恢复到初始状态
        """
        logger.info("开始恢复所有图层到初始状态...START")
        for layer_key, initial_state in self.layer_initial_state.items():
            self.change_layer_state(layer_key, initial_state)

        # 清空当前状态缓存
        self.layer_current_state.clear()
        logger.info("所有图层已恢复到初始状态...END")

    def save_initial_layer_state(self, layername: str, layerinfo: dict):
        """保存图层初始状态"""
        if layername not in self.layer_initial_state:
            target_layers = self.get_layer_by_layername(layername)
            for target_layer in target_layers:
                # 使用工厂创建初始状态
                state = LayerStateFactory.create_layer_state(target_layer, layerinfo)

                # 同时保存初始状态和当前状态
                self.layer_initial_state[layername] = state.copy()
                self.layer_current_state[layername] = state.copy()

                logger.info(f"保存初始状态成功: {layername=}, {state=}")

    def restore_text_item_to_initial(self, layer_name: str):
        """将指定图层的文本属性恢复到初始状态"""
        initial_state = self.layer_initial_state.get(layer_name, {})
        if "textItem" in initial_state:
            self.change_layer_state(layer_name, initial_state)
            logger.info(f"图层 {layer_name} 的文本属性已恢复到初始状态")
