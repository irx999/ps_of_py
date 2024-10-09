""" 主启动函数 """

from src.ps_core import Photoshop
from src.loda_data import LoadData


def main():
    """ 主启动函数 """

    lodadata  = LoadData()
    ps = Photoshop(*lodadata.settings)
    text_data = lodadata.selected_skus()
    # 遍历整个字典
    for k, v in text_data.items():
        ps.core(export_name=k,
            text_dict = v[0],
            layer_dict = v[1],
        )

def test():
    """ 测试专用函数 """
    ld = LoadData(sheet_name="Sheet1",table_name="表1")
    print(ld)


if __name__ == '__main__':
    test()
