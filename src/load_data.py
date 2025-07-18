"""This module contains functions to load and preprocess data"""

from itertools import zip_longest
from typing import Any

import xlwings as xw


class LoadData:
    """This class loads and preprocesses data"""

    def __init__(self, sheet_name: str = None, table_name: str | int = 0):
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
            self.selectedranges = self.sheet.api.Application.Selection.Value
            # 读取表格中写入的导出配置信息
            self.settings = self.read_settings()
        except OSError as e:
            print(f"无法读取您的表格,请检查您的excel文件\n{e}")

        """ 
        :param sheet_name: str, sheet name
        :param table_name: str or int, table name or index
        """

    def read_settings(self):
        """This function reads the export settings"""
        try:
            settings: Any = [
                self.sheet.range("psd_name").value,
                self.sheet.range("psd_file_path").value,
                self.sheet.range("export_folder").value,
                self.sheet.range("file_format").value,
                self.sheet.range("suffix").value,
            ]
        except ValueError as e:
            print(f"无法读取到表格中的配置信息,将使用默认配置\n{e}")
            settings = [None, "导出图片", "png", ""]
        return settings

    def read_range(self) -> list:
        """This function reads the file and returns the data"""
        ans_list = []

        for i in self.table_values:
            dct = {k: v for k, v in zip_longest(self.table_header, i, fillvalue=None)}
            ans_list.append(dct)
        return ans_list

    def filter_data(self, input_data) -> dict:
        """This function filters the data"""
        # 创建一个 {导出文件名： [需要修改的图层的字典列表]}
        ans_dct = {}
        for dct in input_data:
            # 创建一个所有图层的列表
            layer_lst = {}
            for header in dct.keys():
                if dct[header] is not None:
                    # 创建一个每个图层的字典
                    layer_dict = {}
                    # 匹配标题属性
                    match header.split("丨"):
                        # 匹配修改文本图层属性
                        case "文本", str(layer_set), str(layer_name):
                            layer_dict["图层路径"] = (
                                [layer_name]
                                if layer_set == ""
                                else [layer_set, layer_name]
                            )

                            layer_dict["textItem"] = {}
                            match str(dct[header]).split("丨"):
                                case str(text), str(font_size), str(font_color):
                                    layer_dict["textItem"]["contents"] = text
                                    layer_dict["textItem"]["size"] = int(font_size)
                                    layer_dict["textItem"]["color"] = font_color
                                case str(text), str(font_size):
                                    layer_dict["textItem"]["contents"] = text
                                    layer_dict["textItem"]["size"] = int(font_size)
                                case _:
                                    layer_dict["textItem"]["contents"] = dct[header]

                        # 匹配表头中修改可显性图层属性
                        case "可显性", str(layer_set_1), str(layer_set_2):
                            if layer_set_1 == "" and layer_set_2 == "":
                                layer_dict["图层路径"] = []
                            # 这里如果两个图层组需要操作两次的话, 就会在表格中重复, excel 会自动多一个复制处理
                            elif layer_set_2 == "" or layer_set_2 in [
                                str(i) for i in range(1, 11)
                            ]:
                                layer_dict["图层路径"] = [layer_set_1]
                            else:
                                layer_dict["图层路径"] = [layer_set_1, layer_set_2]
                            # 匹配单元格内容
                            match dct[header].split("丨"):
                                # 如果是T或F, 则直接设置visible属性
                                case str(layer_name), "T":
                                    layer_dict["图层路径"].append(layer_name)
                                    layer_dict["visible"] = True
                                case str(layer_name), "F":
                                    layer_dict["图层路径"].append(layer_name)
                                    layer_dict["visible"] = False
                                # 如果没有, 默认为True
                                case _:
                                    layer_dict["图层路径"].append(dct[header])
                                    layer_dict["visible"] = True

                    if layer_dict:
                        # layer_dict["图层路径"] = "|".join(layer_dict["图层路径"])

                        图层路径 = "/".join(layer_dict["图层路径"])
                        del layer_dict["图层路径"]
                        layer_lst[图层路径] = layer_dict
            ans_dct[dct["导出文件名"]] = layer_lst
        return ans_dct

    def selected_skus(self) -> list:
        """This function returns the selected SKUs"""

        load_data = self.filter_data(self.read_range())
        ans = []
        # 如果没有选择SKU, 则返回None
        if self.selectedranges:
            if isinstance(self.selectedranges, tuple):
                sku_list = [i[0] for i in self.selectedranges if i is not None]
            else:
                sku_list = [self.selectedranges]
            for k, v in load_data.items():
                if k in sku_list:
                    ans.append({"任务名": str(k).replace(".0", ""), "内容": v})

            return ans
        else:
            return []


if __name__ == "__main__":
    ld = LoadData()
    ans = ld.selected_skus()
    print(ans)
