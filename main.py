""" 主启动函数 """

from ps import Photoshop
from loda_data import LoadData


def main():
    """ 主启动函数 """

    ld = LoadData()
    ps = Photoshop(*ld.settings)
    text_data = ld.selected_skus()
    for k, v in text_data.items():
        ps.core(export_name=k,
            text_dict = v[0],
            layer_dict = v[1],
        )




if __name__ == '__main__':
    main()
