""" This is a python script for photosop"""


import os
import time
from photoshop import Session

from src.ps_layer_changer import layer_changer

class Photoshop:
    """Photoshop 类"""
    def __init__(self,
                 psd_name:str,
                 psd_file_path:str=None,
                 export_folder:str=None,
                 file_format:str= "png",
                 suffix:str = ""
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
        self.suffix = suffix if suffix is not None else ""
        #检测传入的文件夹是否存在

        with Session(file_path=self.psd_file_path, action="open") as ps_session:
            doc = ps_session.active_document
            print("打开psd文件成功",ps_session.echo(ps_session.active_document.name))
        self.ps_session = ps_session
        self.doc = doc
        # 最外层图层集
        self.layer_outermost_set_name = [_layerSets.name for _layerSets in self.doc.layerSets]




        #设置导出选项
        self.saveoptions = self.ps_saveoptions()


    def psd_file_path_set(self,psd_file_path:str =None):
        """ 返回psd文件路径 """ 
        if  psd_file_path is None:
            return f"{os.path.split(os.path.abspath(__file__ ))[0]}/psd/{self.psd_name}.psd"
        else:
            return f"{psd_file_path}/{self.psd_name}.psd"

    def export_folder_set(self,export_folder):
        """ 返回导出文件夹路径 """ 
        if export_folder is None:
            export_folder = "默认导出文件夹"
        home_path = f"{os.path.split(os.path.abspath(__file__ ))[0]}".replace("src","")
        export_folder  = f"{home_path}/{export_folder}"
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)
            print(f"创建文件夹{export_folder}成功")
        return export_folder


    def ps_saveoptions(self):
        """ 设置psd导出选项 """
        match self.file_format:
            case "jpg" | "jpeg":
                saveoptions = self.ps_session.JPEGSaveOptions()
            case _:
                saveoptions = self.ps_session.PNGSaveOptions()
        return saveoptions

    def core(self, export_name: str,
                    input_data: dict) -> None:
        """ 
        :param export_name: 导出文件名
        :param input_data: 图层属性数据
        :return: None
        """
        #修改图层属性
        data_cache = layer_changer(self.ps_session, input_data)
        #保存图片
        self.doc.saveAs(f'{self.export_folder}/{export_name}{self.suffix}.{self.file_format}',
                    self.saveoptions,
                    asCopy=True)
        print(f"导出{export_name}.{self.file_format}到{self.export_folder}成功")
        #恢复图层属性
        filtered_list = [item for item in data_cache if '字体大小' in item or 'visible' in item]

        layer_changer(self.ps_session, filtered_list)



if __name__ == '__main__':
    start_time = time.time()
    ps = Photoshop(psd_file_path ="",
                 psd_name ="test",
                 export_folder = "",
                 file_format= "png",
                 suffix= ""
                )



    test_dict = {
            "test":[
                {
                    "图层路径":["第一层","第二层","文本2"],
                    "visible":True,
                    "文本内容":"修改为:ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                    "字体大小":35,
                    "字体颜色":"#00A9FF",
                }
            ],
            "test2":[
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
                ]
    }

    for key, value in test_dict.items():
        ps.core(key, value)
    print(f"总共耗时{time.time()-start_time}秒")
