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
        self.ps_session = ps_session
        self.doc = doc

        match self.file_format:
            case "png":
                self.options = ps_session.PNGSaveOptions()
            case "jpg" | "jpeg":
                self.options = ps_session.JPEGSaveOptions()


    def test(self):
        """ 测试 """
        for layer in self.doc.layerSets.getByName("123").artLayers:
            print(layer.name)
        self.doc.layerSets.getByName("123").artLayers.getByName("test3").visible = False

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




         # 遍历导入的文本名，设置文本内容和大小
        text_size_cache ={}
        for layer_name, text_content in text_dict.items():

            try:
                match text_content:
                    case str():
                        self.doc.artLayers.getByName(layer_name).textItem.contents = text_content

                    case list():
                        #添加一个修改前字体大小的缓存
                        text_size_cache[layer_name] = self.doc.artLayers.getByName(layer_name).textItem.size
                        #修改字体 内容和大小
                        self.doc.artLayers.getByName(layer_name).textItem.contents = text_content[0]
                        self.doc.artLayers.getByName(layer_name).textItem.size  = text_content[1]

                    case dict():
                        layer_set = self.doc.layerSets.getByName(layer_name)
                        for key, value in text_content.items():
                            match value:
                                case str():
                                    layer_set.artLayers.getByName(key).textItem.contents = value
                                case list():
                                    #添加一个修改前字体大小的缓存
                                    if layer_name  not in  text_size_cache:
                                        text_size_cache[layer_name] = {key:layer_set.artLayers.getByName(key).textItem.size}
                                    else:
                                        text_size_cache[layer_name][key] = layer_set.artLayers.getByName(key).textItem.size


                                    layer_set.artLayers.getByName(key).textItem.contents = value[0]
                                    layer_set.artLayers.getByName(key).textItem.size  = value[1]

            except ValueError as e:
                print(f"设置{layer_name}错误\n{e}")

        # 遍历导入的图层名，设置图层可见性
        for layer_name, value in layer_dict.items():
            try:
                match value:
                    case dict():
                        # 如果shape组中有子组，则需要遍历子组
                        layer_set = self.doc.layerSets.getByName(layer_name)
                        for key, visible in value.items():
                            layer_set.artLayers.getByName(key).visible =  visible
                    case _:
                        # 如果是单个图层，直接设置可见性
                        self.doc.artLayers.getByName(layer_name).visible =  value
            except ValueError as e:
                print(f"设置{layer_name}错误\n{e}")


        # 保存为指定格式
        self.doc.saveAs(f'{self.export_folder}/{export_name}.{self.file_format}',
                    self.options,
                    asCopy=True)
        print(f"导出{export_name}.{self.file_format}到{self.export_folder}成功")


        # 保存后 将字体大小恢复修改前的状态
        print(text_size_cache)
        for text_name, size in text_size_cache.items():
            match size:
                case dict():
                    layer_set = self.doc.layerSets.getByName(text_name)
                    for key, value in size.items():
                        layer_set.artLayers.getByName(key).textItem.size = value
                case _:
                    self.doc.artLayers.getByName(text_name).textItem.size = size

        #保存后  将图层可见性恢复修改前的状态
        for layer_name, value in layer_dict.items():
            try:
                match value:
                    case dict():
                        # 如果shape组中有子组，则需要遍历子组
                        layer_set = self.doc.layerSets.getByName(layer_name)
                        for key, visible in value.items():
                            layer_set.artLayers.getByName(key).visible = not visible
                    case _:
                        # 如果是单个图层，直接设置可见性
                        self.doc.artLayers.getByName(layer_name).visible = not value
            except ValueError as e:
                print(f"设置{layer_name}错误\n{e}")



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
