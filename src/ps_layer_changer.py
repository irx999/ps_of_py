""" This is a python script for photosop"""




def hex_to_rgb(ps_session,hex_color:str):
    """
    :param ps_session: 实例化后的photoshop对象
    :param hex_color: 16进制颜色值
    :return: photoshop的SolidColor对象
    """
    def a(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = a(hex_color)
    print(r,g,b)
    text_color = ps_session.SolidColor()
    text_color.rgb.red = r
    text_color.rgb.green = g
    text_color.rgb.blue = b
    return text_color
def rgb_to_hex(r,g,b):
    """
    :param r: 红色值
    :param g: 绿色值
    :param b: 蓝色值
    :return: 16进制颜色值
    """
    return f'#{r:02x}{g:02x}{b:02x}'

def layer_changer(ps_session, input_data:dict):
    """ 
    :param ps_doc: 实例化后的ps对象
    :param input_data: 传输的数据
    {图层路径:list,可显性:bool,修改内容:str,字体大小:float,字体颜色:"hex mode"}

    """


    data_cache = {"图层路径":input_data["图层路径"]}
    # 先拿到需要修改的图层对象
    layer_name  = ps_session.active_document
    for layer_item  in input_data["图层路径"]:
        # 如果是图层路径的最后一个
        if layer_item  == input_data["图层路径"][-1]:
            #如果该名字是在组合中 他就是一个组合
            if layer_item  in layer_name.layerSets:
                layer_name = layer_name.layerSets.getByName(layer_item)
            #反之就是一个图层了
            else:
                layer_name = layer_name.artLayers.getByName(layer_item)
        else:
            layer_name = layer_name.layerSets.getByName(layer_item)
    #这样就拿到了需要修改的图层对象
    #开始修改图层属性
    if "visible" in input_data:
        data_cache["visible"] = not input_data["visible"]
        layer_name.visible = input_data["visible"]
    if "文本内容" in input_data:
        data_cache["文本内容"] = layer_name.textItem.contents
        layer_name.textItem.contents = input_data["文本内容"]
    if "字体大小" in input_data:
        data_cache["字体大小"] = layer_name.textItem.size
        layer_name.textItem.size = input_data["字体大小"]
    if "字体颜色" in input_data:
        font_color = layer_name.textItem.color.rgb
        data_cache["字体颜色"] = rgb_to_hex(font_color.red,font_color.green,font_color.blue)
        layer_name.textItem.color = hex_to_rgb(ps_session,input_data["字体颜色"])

    print(data_cache)
