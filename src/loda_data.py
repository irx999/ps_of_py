""" This module contains functions to load and preprocess data """
from itertools import zip_longest
import xlwings as xw


class LoadData:
    """ This class loads and preprocesses data """
    def __init__(self,sheet_name:str=None,table_name:str|int= 0):
        if sheet_name :
            self.sheet = xw.books.active.sheets[sheet_name]
        else:
            self.sheet =  xw.sheets.active
        self.table = self.sheet.tables[table_name]
        # 读取表格的表头
        self.table_header = self.table.header_row_range.value
        # 读取表格中的数据
        self.table_values = self.table.data_body_range.value
        # 读取当前选择的单元格
        self.selectedranges = self.sheet.api.Application.Selection.Value
        # 读取表格中写入的导出配置信息
        self.settings = self.read_settings()
        """ 
        :param sheet_name: str, sheet name
        :param table_name: str or int, table name or index
        """
    def read_settings(self):
        """ This function reads the export settings """
        try:
            settings = [self.sheet.range("psd_name").value,\
                        self.sheet.range("export_folder").value,\
                        self.sheet.range("file_format").value,\
                        self.sheet.range("suffix").value,]
        except:
            settings = [None,"导出图片","png",""]
        return settings

    def read_range(self):
        """ This function reads the file and returns the data """
        ans  = []


        for i in  self.table_values:
            dct = {k:v for k,v in zip_longest(self.table_header,i,fillvalue=None)}
            ans.append(dct)
        return ans

    def fiter_data(self,input_data):
        """ This function filters the data """
        ans_dct = {}
        for i in input_data:
            text_dict = {}
            layer_dict = {}
            for header in i.keys():
                if i[header]is not None:
                    match i[header]:
                        case None:
                            setting = None
                        case str(setting):
                            _ =i[header].split("丨")
                            if len(_) == 1:
                                setting = _[0]
                            else:
                                setting = [_[0],int(_[1])]
                        case _:
                            setting = i[header]
                    match header.split("丨"):
                        case "文本","",str(name):
                            text_dict[name] = setting
                        case "文本",str(layer_set),str(name):
                            if layer_set not in text_dict:
                                text_dict[layer_set] = {name:setting}
                            else:
                                text_dict[layer_set][name] = setting

                        case "可显性","",_:
                            layer_dict[i[header]] = i[header] is not None
                        case "可显性",str(layer_set),_:
                            if layer_set not in layer_dict:
                                layer_dict[layer_set] = {i[header]:i[header] is not None}
                            else:
                                layer_dict[layer_set][i[header]] = i[header] is not None


            ans_dct[i['导出文件名']]= [text_dict,layer_dict]
        return ans_dct




    def selected_skus(self):
        """ This function returns the selected SKUs """

        load_data = self.fiter_data(self.read_range())

        if self.selectedranges is not None:
            if isinstance(self.selectedranges,str) or isinstance(self.selectedranges,float):
                sku_list = [self.selectedranges]
                print(sku_list)
            else:
                sku_list = [i[0] for i in self.selectedranges if i is not None]
                print(sku_list)
        else:
            sku_list = load_data
        return [] if sku_list == [] else {k:v for k,v in load_data.items() if k in sku_list}




if __name__ == '__main__':
    ld = LoadData()
    print(ld.selected_skus())
