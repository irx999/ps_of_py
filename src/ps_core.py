""" This is a python script for photosop"""


import os
from photoshop import Session

from src.ps_layer_text_changer import change_text_layer,restore_text_layer_font_size
from src.ps_layer_visible_changer import change_layer_visible,restore_layer_visible

class Photoshop:
    """Photoshop 类"""
    def __init__(self,psd_name,export_folder ="测试导出文件夹",file_format="png",suffix = ""):
        """
        初始化Photoshop类

        :param psd_name: psd文件名
        :param export_folder: 导出文件夹名  
        :param file_format: 导出文件格式，默认为png
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
        #创建psd会话
        with Session(file_path=f"{file_path}/psd/{psd_name}.psd", action="open") as ps_session:
            doc = ps_session.active_document
            print(ps_session.echo(ps_session.active_document.name))
        #self.ps_session = ps_session
        self.doc = doc
        # 最外层图层集
        self.layer_outermost_set_name = [_layerSets.name for _layerSets in self.doc.layerSets]

        match self.file_format:
            case "jpg" | "jpeg":
                self.options = ps_session.JPEGSaveOptions()
            case _:
                self.options = ps_session.PNGSaveOptions()

    def core(self, export_name: str,
                    text_dict: dict,
                    layer_dict: dict,
                        ) -> None:
        """
        修改psd文件，并保存为指定格式

        :param export_name: 导出文件名
        :param text_dict: {"test1": "修改test1","组2":{"test3":"修改test3","test4":["修改test4", 38]}}
        :param layer_dict: {"图片1":True,"组1":{"图片1":True,"图片2": False}}
        """


        # 修改文字层 并返回一个
        text_size_cache = change_text_layer(self.doc, text_dict)
        # 遍历导入的图层名，设置图层可见性
        change_layer_visible(self.doc, self.layer_outermost_set_name,layer_dict)


        # 如果文件名是数字，则去掉小数点和后面的数字
        if  isinstance(export_name, float):
            export_name = str(export_name).split(".",maxsplit=1)[0]
        # 保存为指定格式
        self.doc.saveAs(f'{self.export_folder}/{export_name}{self.suffix}.{self.file_format}',
                    self.options,
                    asCopy=True)
        print(f"导出{export_name}.{self.file_format}到{self.export_folder}成功")


        # 保存后 将字体大小恢复修改前的状态
        restore_text_layer_font_size(self.doc, text_size_cache)
        #保存后  将图层可见性恢复修改前的状态
        restore_layer_visible(self.doc, self.layer_outermost_set_name,layer_dict)



if __name__ == '__main__':
    ps = Photoshop(psd_name='test.psd', export_folder='测试导出')


    textdict = {"test1": "修改test1", "test2":["修改test2", 123],\
                 "组2":{"test3":"修改test3","test4":["修改test4", 38]}}
    textdict = {"test1": "修改test1", "test2":["修改test2", 123],}


    layerdict = {"图片1":True,"组1":{"图片1":True,"图片2": False}}



    ps.core(export_name='test',
            text_dict = textdict,
            layer_dict = layerdict,
    )

    # ps.test()
