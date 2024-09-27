""" This is a python script for photosop"""


import os
from photoshop import Session



class Photoshop:
    """Photoshop 类"""
    def __init__(self,psd_name,export_folder,file_format="png"):
        """
        :param psd_name: psd文件名
        :param export_folder: 导出文件夹名  
        :param file_format: 导出文件格式，默认为png
        """
        self.psd_name = psd_name
        self.export_folder = f"{os.path.split(os.path.realpath(__file__ ))[0]}/{export_folder}"
        self.file_format = file_format
        #检测传入的文件夹是否存在
        if not os.path.exists(self.export_folder):
            os.makedirs(self.export_folder)
            print(f"创建文件夹{self.export_folder}成功")


        #创建psd会话
        with Session(action=self.psd_name) as ps_session:
            doc = ps_session.active_document
        self.doc = doc

        match self.file_format:
            case "png":
                self.options = ps_session.PNGSaveOptions()
            case "jpg" | "jpeg":
                self.options = ps_session.JPEGSaveOptions()

    def core(self, export_name: str,
                        layer_dict: dict[str, bool],
                        text_dict: dict[str, str|list]) -> None:
        """
        修改psd文件，并保存为指定格式
        :param export_name: 导出文件名
        :param layer_lst: 图层字典，格式为{图层名:是否可见}
        :param text_lst: 文本字典，格式为{图层名:文本内容|[文本内容,字号]}
        """
    
        # 遍历导入的图层名，设置图层可见性
        for layer_name, visible in layer_dict.items():
            print(f"设置{layer_name}的可见性为{visible}")
            self.doc.artLayers.getByName(layer_name).visible = visible
        # 遍历导入的文本名，设置文本内容和大小
        for layer_name, text_content in text_dict.items():
            match text_content:
                case list():
                    self.doc.artLayers.getByName(layer_name).textItem.contents = text_content[0]
                    self.doc.artLayers.getByName(layer_name).textItem.size  = text_content[1]
                case str():
                    self.doc.artLayers.getByName(layer_name).textItem.contents = text_content
        # 保存为指定格式
        self.doc.saveAs(f'{self.export_folder}/{export_name}.{self.file_format}',
                    self.options,
                    asCopy=True)


        #保存后  将图层可见性恢复修改前的状态
        for layer_name, visible in layer_dict.items():
            self.doc.artLayers.getByName(layer_name).visible = not visible





if __name__ == '__main__':
    ps = Photoshop(psd_name='test.psd', export_folder='123')
    ps.core(export_name='test', layer_dict={"test1":True},text_dict={"test2":["修改的文本", 38]})
