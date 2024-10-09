""" 这是专门用来修改图层可显性的脚本 """




def change_layer_visible(ps_doc,layer_all_set_name,layer_dict:dict):
    """
    修改图层可见性
    :param ps_doc: Photoshop Document 对象
    :param layer_all_set_name: 所有图层集的名称列表
    :param layer_dict: 图层名称和可见性的字典
    :return: 无
    """
    for layer_name, value in layer_dict.items():
        try:
            match value:
                case bool():
                    # 如果是单个图层，直接设置可见性
                    if  layer_name in layer_all_set_name:
                        ps_doc.layerSets.getByName(layer_name).visible = True
                    else:
                        ps_doc.artLayers.getByName(value).visible = True
                case dict():
                    # 如果shape组中有子组，则需要遍历子组
                    layer_set = ps_doc.layerSets.getByName(layer_name)
                    layer_set_name = [name.name for name in layer_set.layerSets]
                    for key, visible in value.items():
                        if key in layer_set_name:
                            layer_set.layerSets.getByName(key).visible = visible
                        else:
                            layer_set.artLayers.getByName(key).visible = visible
                case _:
                    # 没有成功匹配到任何情况，报错
                    print(f"设置{layer_name}错误\n")
        except ValueError as e:
            print(f"设置{layer_name}错误\n{e}")

def restore_layer_visible(ps_doc,layer_all_set_name,layer_dict:dict):
    """
    恢复图层可见性
    :param ps_doc: Photoshop Document 对象
    :param layer_all_set_name: 所有图层集的名称列表
    :param layer_dict: 图层名称和可见性的字典
    :return: 无
    """
    for layer_name, value in layer_dict.items():
        try:
            match value:
                case bool():
                    # 如果是单个图层，直接设置可见性
                    if  layer_name in layer_all_set_name:
                        ps_doc.layerSets.getByName(layer_name).visible = False
                    else:
                        ps_doc.artLayers.getByName(value).visible = False
                case dict():
                    # 如果shape组中有子组，则需要遍历子组
                    layer_set = ps_doc.layerSets.getByName(layer_name)
                    layer_set_name = [name.name for name in layer_set.layerSets]
                    for key, visible in value.items():
                        if key in layer_set_name:
                            layer_set.layerSets.getByName(key).visible = not visible
                        else:
                            layer_set.artLayers.getByName(key).visible = not visible
                case _:
                    # 没有成功匹配到任何情况，报错
                    print(f"设置{layer_name}错误\n")
        except ValueError as e:
            print(f"设置{layer_name}错误\n{e}")
