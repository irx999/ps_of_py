"""主启动函数"""

import os
import sys

from src.load_data import LoadData
from src.ps_core import Photoshop

main_working_dir = os.path.dirname(__file__)
sys.path.append(main_working_dir)
os.chdir(main_working_dir)


def main():
    """主启动函数"""
    try:
        load_data = LoadData()

        ps_settings, suffix = load_data.settings[:-1], load_data.settings[-1]
        ps = Photoshop(*ps_settings)
        # 遍历整个字典
        for task in load_data.selected_skus():
            print(task["内容"])
            ps.core(task["任务名"] + suffix, task["内容"])
        ps.restore_all_layers_to_initial()
    except Exception as e:
        print(f"程序执行出错: {e}")


if __name__ == "__main__":
    main()