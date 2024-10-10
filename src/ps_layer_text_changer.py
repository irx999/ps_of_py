""" 这是专门用来修改文本图层的脚本 """

def change_text_layer(ps_doc,text_dict:dict) -> dict:
    """ 修改文本图层的文字内容 """
    text_size_cache ={}
    for layer_name, text_content in text_dict.items():
        try:
            # 文本图层修改
            match text_content:
                case str():
                    ps_doc.artLayers.getByName(layer_name).textItem.contents = text_content
                    if  layer_name+" 拷贝" in [name.name for name in ps_doc.artLayers]:
                        ps_doc.artLayers.getByName(layer_name+" 拷贝").textItem.contents = text_content

                case list():
                    #添加一个修改前字体大小的缓存
                    text_size_cache[layer_name] = ps_doc.artLayers.getByName(layer_name).textItem.size
                    #修改字体 内容和大小
                    ps_doc.artLayers.getByName(layer_name).textItem.contents = text_content[0]
                    ps_doc.artLayers.getByName(layer_name).textItem.size  = text_content[1]
                    if  layer_name+" 拷贝" in [name.name for name in ps_doc.artLayers]:
                        text_size_cache[layer_name+ " 拷贝"] = ps_doc.artLayers.getByName(layer_name+" 拷贝").textItem.size
                        ps_doc.artLayers.getByName(layer_name+" 拷贝").textItem.size = text_content[0]
                        ps_doc.artLayers.getByName(layer_name+" 拷贝").textItem.contents = text_content[1]


                case dict():
                    layer_set = ps_doc.layerSets.getByName(layer_name)
                    layer_set_name = [name.name for name in layer_set.artLayers]
                    print(layer_set_name)
                    for key, value in text_content.items():
                        match value:
                            case str():
                                layer_set.artLayers.getByName(key).textItem.contents = value
                                if  key+" 拷贝" in layer_set_name:
                                    layer_set.artLayers.getByName(key+" 拷贝").textItem.contents = value
                            case list():
                                #添加一个修改前字体大小的缓存
                                if layer_name  not in  text_size_cache:
                                    text_size_cache[layer_name] = {key:layer_set.artLayers.getByName(key).textItem.size}
                                else:
                                    text_size_cache[layer_name][key] = layer_set.artLayers.getByName(key).textItem.size
                                if  key +" 拷贝" in layer_set_name:
                                    text_size_cache[layer_name][key+ " 拷贝"] = layer_set.artLayers.getByName(key+" 拷贝").textItem.size



                                layer_set.artLayers.getByName(key).textItem.contents = value[0]
                                layer_set.artLayers.getByName(key).textItem.size  = value[1]
                                
                                if  key +" 拷贝" in layer_set_name:
                                    layer_set.artLayers.getByName(key+" 拷贝").textItem.contents = value[0]
                                    layer_set.artLayers.getByName(key+" 拷贝").textItem.size = value[1]
        except ValueError as e:
            print(f"设置文本{layer_name}错误\n{e}")

    return text_size_cache


def restore_text_layer_font_size(ps_doc,text_size_cache:dict) -> dict:
    """ 恢复文本图层的字体大小 """
    try:
        for text_name, size in text_size_cache.items():
            match size:
                case dict():
                    layer_set = ps_doc.layerSets.getByName(text_name)
                    for key, value in size.items():
                        layer_set.artLayers.getByName(key).textItem.size = value
                case _:
                    ps_doc.artLayers.getByName(text_name).textItem.size = size
    except ValueError as e:
        print(f"恢复文本{text_name}字体大小错误\n{e}")
