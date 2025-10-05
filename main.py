"""主启动函数"""

import os
import sys

from load_data import LoadData
from src.ps_core import Photoshop

if getattr(sys, "frozen", False):
    sys.path.append(os.path.dirname(sys.executable))
    # 原来的方案
    main_working_dir = getattr(sys, "_MEIPASS", os.path.abspath(__file__))
    # 现在的方案
    main_working_dir = os.path.dirname(sys.executable)
    sys.path.append(main_working_dir)
    os.chdir(main_working_dir)


def main():
    """主启动函数"""
    try:
        load_data = LoadData()

        ps_settings = load_data.settings

        ps = Photoshop(*ps_settings)

        # 遍历整个字典
        with ps:
            for task in load_data.selected_skus():
                print(task["内容"])
                ps.core(task["任务名"], task["内容"])

    except Exception as e:
        print(f"程序执行出错: {e}")


if __name__ == "__main__":
    main()
