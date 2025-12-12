"""主启动函数"""

import os
import sys

from load_data import LoadData
from src.ps.ps_core import Photoshop

if getattr(sys, "frozen", False):
    sys.path.append(os.path.dirname(sys.executable))
    # 原来的方案
    main_working_dir = getattr(sys, "_MEIPASS", os.path.abspath(__file__))
    # 现在的方案
    main_working_dir = os.path.dirname(sys.executable)
    sys.path.append(main_working_dir)
    os.chdir(main_working_dir)


else:
    main__working_dir = os.path.dirname(__file__)
    sys.path.append(main__working_dir)
    os.chdir(main__working_dir)


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

            ps.app.doJavaScript(f'alert("save to jpg: {ps.export_folder}")')

    except Exception as e:
        print(f"程序执行出错: {e}")


def main_for_merge_images():
    """主启动函数"""
    try:
        load_data = LoadData()

        ps_settings = load_data.settings

        ps = Photoshop(*ps_settings)

        # 遍历整个字典
        with ps:
            # for merge_name in load_data.merge_names:
            for task in load_data.selected_skus():
                print(task["任务名"])
                ps.core(task["任务名"], task["修改信息"])

            # ps.app.doJavaScript(f'alert("save to jpg: {ps.export_folder}")')

    except Exception as e:
        print(f"程序执行出错: {e}")


if __name__ == "__main__":
    main_for_merge_images()
