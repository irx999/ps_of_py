"""主启动函数"""

import os
import sys

from src.load_data import LoadData
from src.ps_core import Photoshop

main__working_dir = os.path.dirname(__file__)
sys.path.append(main__working_dir)
os.chdir(main__working_dir)


def main():
    """主启动函数"""
    # try:
    lodadata = LoadData()
    ps = Photoshop(*lodadata.settings)
    # 遍历整个字典
    for task in lodadata.selected_skus():
        print(task["内容"])
        ps.core(task["任务名"], task["内容"])
    # except Exception as e:
    # print(e)
    # win32api.MessageBox(0, str(e), "错误")


def test():
    """测试专用函数"""
    # ld = LoadData(sheet_name="Sheet1",table_name="表1")
    # print(ld)
    ps = Photoshop(psd_name="测试专用")
    print("当前PSD具有以下图层\n", ps.layer_outermost_set_name)


def test2():
    lodadata = LoadData()
    ps = Photoshop(*lodadata.settings)
    # # 遍历整个字典
    # print(lodadata.selected_skus())
    # error_list = {}
    task_list = lodadata.selected_skus()

    ps.run_task2(task_list)

    # enerror_list = "\n".join([f"{key}:{value}" for key, value in error_list.items()])
    # enerror_sum = f" {len(error_list)} / {len(lodadata.selected_skus())}\n"
    # if enerror_list:
    #     win32api.MessageBox(0, enerror_sum + enerror_list, "错误")


if __name__ == "__main__":
    main()
    pass
