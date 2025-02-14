""" 主启动函数 """

from src.ps_core import Photoshop
from src.load_data import LoadData


def main():
    """ 主启动函数 """

    lodadata  = LoadData()
    ps = Photoshop(*lodadata.settings)
    text_data = lodadata.selected_skus()
    print(text_data)
    # 遍历整个字典
    if text_data:
        for export_name, v in text_data.items():
            ps.core(export_name=str(export_name).replace(".0",""),
                input_data = v
            )

def test():
    """ 测试专用函数 """
    # ld = LoadData(sheet_name="Sheet1",table_name="表1")
    # print(ld)
    ps = Photoshop(psd_name="MB")
    print(ps.layer_outermost_set_name)

if __name__ == '__main__':
    main()
