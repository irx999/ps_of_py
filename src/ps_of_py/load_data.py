"""本模块包含用于加载和预处理数据的函数"""

from itertools import zip_longest
from typing import Any, Dict, List

import xlwings as xw
from loguru import logger

logger.add("./logs/LoadData.log", rotation="1 MB")


class LoadData:
    """该类用于加载和预处理数据"""

    def __init__(self, sheet_name: str = None, table_name: str | int = 0):
        """
        初始化LoadData类
        :param sheet_name: 工作表名称
        :param table_name: 表格名称或索引
        """
        try:
            if sheet_name:
                self.sheet = xw.books.active.sheets[sheet_name]
            else:
                self.sheet = xw.sheets.active
            # 读取表格
            self.table = self.sheet.tables[table_name]
            # 读取表格的表头
            self.table_header = self.table.header_row_range.value
            # 读取表格中的数据
            self.table_values = self.table.data_body_range.value
            # 读取当前选择的单元格
            self.selected_ranges: str | list[str] = (
                self.sheet.api.Application.Selection.Value
            )
            # 读取表格中写入的导出配置信息
            try:
                self.settings = self.read_settings()
            except Exception:
                logger.debug("无法读取表格中的配置信息,请检查您的excel文件")
        except OSError as e:
            logger.error(f"无法读取您的表格,请检查您的excel文件{e}")
        except Exception:
            raise FileNotFoundError("当前未选中工作簿或不存在")

    def read_settings(self) -> dict:
        """读取导出配置信息"""
        try:
            if self.sheet.range("colse_ps").value == "是":
                colse_ps = True
            else:
                colse_ps = False
        except Exception:
            colse_ps = True

        try:
            settings: dict = {
                "psd_name": self.sheet.range("psd_name").value,
                "psd_dir_path": self.sheet.range("psd_file_path").value,
                "export_folder": self.sheet.range("export_folder").value,
                "file_format": self.sheet.range("file_format").value,
                "suffix": self.sheet.range("suffix").value,
                "colse_ps": colse_ps,
            }
        except ValueError as e:
            print(f"无法读取到表格中的配置信息,将使用默认配置\n{e}")
            settings: dict = {
                "psd_name": None,
                "psd_file_path": None,
                "export_folder": "默认名称",
                "file_format": "png",
                "suffix": "",
                "colse_ps": False,
            }
        return settings

    def read_range(self) -> List[Dict[str, Any]]:
        """读取表格数据并返回列表"""
        result_list = []

        for row in self.table_values:
            row_dict = {
                k: v for k, v in zip_longest(self.table_header, row, fillvalue=None)
            }
            result_list.append(row_dict)
        return result_list

    def filter_data(
        self, input_data: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """过滤数据，构造图层修改指令"""
        result_dict = {}
        for row_dict in input_data:
            # 创建一个所有图层的字典
            layer_dict = {
                "其他信息": {},
                "修改信息": {},
            }
            for header in row_dict.keys():
                if row_dict[header] is not None:
                    # 创建单个图层的字典
                    layer_info = {}
                    # 匹配标题属性
                    header_parts = header.split("|")

                    match header_parts:
                        # 匹配修改文本图层属性
                        case ["文本", *layer_list]:
                            layer_info["图层路径"] = layer_list

                            layer_info["textItem"] = {}
                            cell_value_parts = str(row_dict[header]).split("|")
                            # 验证文本属性
                            validate_cell_value_parts(row_dict[header])
                            match cell_value_parts:
                                case [
                                    str(text),
                                    str(font_size),
                                    str(font_color),
                                    str(strikeThru),
                                ]:
                                    layer_info["textItem"]["contents"] = text
                                    if font_size != "":
                                        layer_info["textItem"]["size"] = int(font_size)
                                    if font_color != "":
                                        layer_info["textItem"]["color"] = font_color
                                    if strikeThru != "":
                                        layer_info["textItem"]["strikeThru"] = int(
                                            strikeThru
                                        )
                                case [str(text), str(font_size), str(font_color)]:
                                    layer_info["textItem"]["contents"] = text
                                    layer_info["textItem"]["size"] = int(font_size)
                                    layer_info["textItem"]["color"] = font_color
                                case [str(text), str(font_size)]:
                                    layer_info["textItem"]["contents"] = text
                                    layer_info["textItem"]["size"] = int(font_size)
                                case _:
                                    layer_info["textItem"]["contents"] = row_dict[
                                        header
                                    ]
                            # 修复数据错误, 这里统一转化成str 格式 并移除 .0 并且这个.0 必须是结尾

                            text_content = str(layer_info["textItem"]["contents"])
                            if text_content.endswith(".0"):
                                layer_info["textItem"]["contents"] = text_content[:-2]
                            else:
                                layer_info["textItem"]["contents"] = text_content

                        # 匹配表头中修改可显性图层属性
                        case ["可显性", *layer_list]:
                            if layer_list[0] == "":
                                layer_info["图层路径"] = []
                            # 这里如果两个图层组需要操作两次的话, 就会在表格中重复, excel 会自动多一个复制处理
                            elif layer_list[-1] in [str(i) for i in range(1, 11)]:
                                layer_info["图层路径"] = layer_list[:-1]
                            elif layer_list[-1] == "":
                                layer_info["图层路径"] = layer_list[0:1]
                            else:
                                layer_info["图层路径"] = layer_list
                            # 匹配单元格内容
                            cell_value_parts = row_dict[header].split("|")
                            match cell_value_parts:
                                # 如果是T或F, 则直接设置visible属性
                                case [str(layer_name), "T"]:
                                    layer_info["图层路径"].append(layer_name)
                                    layer_info["visible"] = True
                                case [str(layer_name), "F"]:
                                    layer_info["图层路径"].append(layer_name)
                                    layer_info["visible"] = False
                                # 如果没有, 默认为True
                                case _:
                                    layer_info["图层路径"].append(row_dict[header])
                                    layer_info["visible"] = True

                        # 匹配其他信息
                        case _:
                            layer_dict["其他信息"][header] = row_dict[header]
                            pass

                            # layer_info["其他信息"] = []
                            # layer_info["其他信息"].append(row_dict[header])

                    if layer_info:
                        full_path = "/".join(layer_info["图层路径"])
                        del layer_info["图层路径"]
                        layer_dict["修改信息"][full_path] = layer_info
            # assert row_dict.get("导出文件名") is not None, "表格中缺少'导出文件名'"
            result_dict[row_dict["导出文件名"]] = layer_dict
        return result_dict

    def selected_skus(self) -> List[Dict[str, Any]]:
        """返回选中的SKUs"""
        result: List[Dict[str, Any]] = []
        # 如果没有选择SKU, 则返回空列表
        if self.selected_ranges:
            if isinstance(self.selected_ranges, tuple):
                sku_list = [i[0] for i in self.selected_ranges if i is not None]
            else:
                sku_list = [self.selected_ranges]

            processed_data = self.filter_data(self.read_range())
            for filename, content in processed_data.items():
                if filename in sku_list:
                    result.append(
                        {
                            "任务名": str(filename).replace(".0", ""),
                            "其他信息": content["其他信息"],
                            "修改信息": content["修改信息"],
                        }
                    )
        return result


def validate_cell_value_parts(input_str: list):
    """
    验证分割后的header_parts参数
    - 第一个参数：随意（不验证）
    - 第二个参数：必须可转换为数字类型
    - 第三个参数：必须是颜色值且只能是1、2、3中的一个
    """
    validated_params = []

    cell_value_parts = str(input_str).split("|")

    # 第一个参数：随意，无需验证
    if len(cell_value_parts) > 0:
        validated_params.append(cell_value_parts[0])

    # 第二个参数：如果存在，必须可转换为数字类型
    if len(cell_value_parts) > 1:
        try:
            second_param = int(cell_value_parts[1])
            validated_params.append(second_param)
        except (ValueError, TypeError):
            raise ValueError(
                f"{input_str}中字体大小参数 '{cell_value_parts[1]}' 无法转换为数字类型"
            )
    else:
        validated_params.append(None)  # 或者不添加，取决于您的需求

    # 第三个参数：如果存在，必须是颜色值且只能是1、2、3中的一个
    if len(cell_value_parts) > 2:
        color_value = str(cell_value_parts[2])
        if not is_valid_hex_color(color_value):
            raise ValueError(
                f"{input_str}中颜色参数 '{color_value}' 不是有效的十六进制颜色值"
            )
        validated_params.append(color_value)  # 统一转为大写
    else:
        validated_params.append(None)

    # 第四个参数：如果存在，必须是1、2、3这三个中的一种
    if len(cell_value_parts) > 3:
        try:
            fourth_param = int(cell_value_parts[3])
            if fourth_param not in [0, 1, 2, 3]:
                raise ValueError(
                    f"{input_str}中删除线参数 '{fourth_param}' 不是0123中的任意一个"
                )
            validated_params.append(fourth_param)
        except (ValueError, TypeError):
            raise ValueError(
                f"{input_str}中第四个参数 '{cell_value_parts[3]}' 无法转换为数字类型或不在允许范围内"
            )
    else:
        validated_params.append(None)

    return validated_params


def is_valid_hex_color(color_string: str) -> bool:
    """
    验证是否为有效的十六进制颜色值
    支持格式：#RGB, #RRGGBB, RGB, RRGGBB
    """
    import re

    # 移除可能的空白字符
    color_string = color_string.strip()

    # 添加 # 前缀如果不存在
    if not color_string.startswith("#"):
        color_string = "#" + color_string

    # 验证十六进制颜色格式
    hex_color_pattern = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    return bool(re.match(hex_color_pattern, color_string))


if __name__ == "__main__":
    ld = LoadData()
    ans = ld.selected_skus()
    print(ans)
