""" This is a python script for photosop"""


import os
import time
from photoshop import Session

from src.ps_layer_changer import layer_changer

class Photoshop:
    """Photoshop 类"""
    def __init__(self,psd_file_path:str =None,psd_name:str="test",\
                 export_folder ="测试导出文件夹",file_format="png",suffix = ""):
        """
        初始化Photoshop类
        :param psd_file_path: psd文件路径,默认工作目录
        :param psd_name: psd文件名,默认test
        :param export_folder: 导出文件夹名, 是在默认工作目录下面创建,
        :param file_format: 导出文件格式，默认为png
        :param suffix: 导出文件名后缀
        """

        file_path = f"{os.path.split(os.path.abspath(__file__ ))[0]}".replace("src","")
        self.psd_name = psd_name
        self.export_folder = f"{file_path}/{export_folder}"
        self.file_format = file_format
        self.suffix = suffix
        #检测传入的文件夹是否存在
        if not os.path.exists(self.export_folder):
            os.makedirs(self.export_folder)
            print(f"创建文件夹{self.export_folder}成功")
        if psd_file_path is None:
            psd_file_path = file_path
            print(f"未传入psd文件路径，使用默认路径{psd_file_path}")
        #创建psd会话
        with Session(file_path=f"{psd_file_path}/{psd_name}.psd", action="open") as ps_session:
            doc = ps_session.active_document
            print("打开psd文件成功",ps_session.echo(ps_session.active_document.name))
        self.ps_session = ps_session
        self.doc = doc
        # 最外层图层集
        self.layer_outermost_set_name = [_layerSets.name for _layerSets in self.doc.layerSets]

        match self.file_format:
            case "jpg" | "jpeg":
                self.options = ps_session.JPEGSaveOptions()
            case _:
                self.options = ps_session.PNGSaveOptions()

    def core(self, export_name: str,
                    input_data: dict,
                    # keep_modification_parameters: list
                        ) -> None:
        """ 
        :param export_name: 导出文件名
        :param input_data: 图层属性数据
        :return: None
        """


        #修改图层属性
        data_cache = layer_changer(self.ps_session, input_data)
        #保存图片
        self.doc.saveAs(f'{self.export_folder}/{export_name}{self.suffix}.{self.file_format}',
                    self.options,
                    asCopy=True)
        print(f"导出{export_name}.{self.file_format}到{self.export_folder}成功")

        #恢复图层属性


        filtered_list = []
        for item in data_cache:
            if '字体大小' in item or 'visible' in item:
                filtered_list.append(item)
        layer_changer(self.ps_session, filtered_list)



if __name__ == '__main__':
    start_time = time.time()
    ps = Photoshop(psd_name='test', export_folder='测试导出')



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
