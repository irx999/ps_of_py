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

    ps_settings, suffix = lodadata.settings[:-1], lodadata.settings[-1]
    ps = Photoshop(*ps_settings)
    # 遍历整个字典
    for task in lodadata.selected_skus():
        print(task["内容"])
        ps.core(task["任务名"] + suffix, task["内容"])
    ps.restore_all_layers_to_initial()


if __name__ == "__main__":
    main()
    pass
