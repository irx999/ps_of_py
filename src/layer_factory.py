"""图层工厂"""

from photoshop.api._artlayer import ArtLayer
from photoshop.api._layerSet import LayerSet

from .ps_utils import ColorFactory


class LayerStateFactory:
    """工厂类：创建和管理图层状态"""

    @staticmethod
    def create_layer_state(layer: LayerSet | ArtLayer, layer_info: dict) -> dict:
        """
        记录图层状态信息
        :param layer: 图层对象
        :param layer_info: 图层信息
        :return: 初始状态字典
        """
        state = {}
        if "visible" in layer_info:
            state["visible"] = layer.visible
        if "move" in layer_info:
            state["move"] = (layer.bounds[0], layer.bounds[1])  # type: ignore #
        if "textItem" in layer_info:
            state["textItem"] = {}
            text_item = layer.textItem
            state["textItem"]["contents"] = text_item.contents
            state["textItem"]["size"] = text_item.size
            font_color = text_item.color.rgb
            # 将RGB颜色转换为十六进制
            state["textItem"]["color"] = ColorFactory().rgb_to_hex(
                font_color.red, font_color.green, font_color.blue
            )
        return state

    @staticmethod
    def change_layer_state(layer: LayerSet | ArtLayer, change_state: dict):
        """
        修改图层状态
        :param layer_key: 图层名称
        :param change_state: 初始状态
        :return: 修改结果
        """

        if "visible" in change_state:
            layer.visible = change_state["visible"]
        # 修改旋转角度
        if "move" in change_state:
            x = layer.bounds[0]  # type: ignore
            y = layer.bounds[1]  # type: ignore
            layer.translate(change_state["move"][0] - x, change_state["move"][1] - y)
        if "rotate" in change_state:
            layer.rotate(change_state["rotate"])
        # 如果是文本图层，修改文本属性
        if "textItem" in change_state:
            text_item_state = change_state["textItem"]
            for key, attr_name in text_item_state.items():
                if key == "color":
                    layer.textItem.color = ColorFactory.hex_to_rgb(attr_name)
                    continue
                if key == "contents":
                    if isinstance(attr_name, (int, float)):
                        attr_name = str(int(attr_name))

                setattr(layer.textItem, key, attr_name)
