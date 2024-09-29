""" 主启动函数 """

from ps import Photoshop
from loda_data import LoadData

if __name__ == '__main__':
    ps = Photoshop(psd_name='test.psd', export_folder='测试导出')

    ld = LoadData()
    text_data = ld.selected_skus()


    for k, v in text_data.items():
        ps.core(export_name=k,
            text_dict = v[0],
            layer_dict = v[1],
        )
