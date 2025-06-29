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


if __name__ == "__main__":
    main()
    pass
