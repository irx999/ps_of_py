"""主启动函数"""

import os
import sys

from src.ps_of_py import Image_utils, Photoshop
from src.ps_of_py.load_data import LoadData

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

        print(**ps_settings)
        print("------------------------------------------------------------------")

        ps = Photoshop(**ps_settings)

        # 遍历整个字典
        with ps:
            for task in load_data.selected_skus():
                print(task["任务名"])
                ps.core(task["任务名"], task["内容"])

            ps.app.doJavaScript(f'alert("save to jpg: {ps.export_folder}")')

    except Exception as e:
        print(f"程序执行出错: {e}")


def main_for_merge_images():
    """主启动函数"""
    load_data = LoadData()

    ps_settings = load_data.settings

    ps = Photoshop(**ps_settings)

    # 遍历整个字典
    with ps:
        # for merge_name in load_data.merge_names:

        merge_dict = {}
        for task in load_data.selected_skus():
            merge_list = task["任务名"].split("|")
            if len(merge_list) > 1:
                if merge_list[0] not in merge_dict:
                    merge_dict[merge_list[0]] = []
                merge_dict[merge_list[0]].append(
                    merge_list[1] + ps.suffix + "." + ps.file_format
                )

            ps.core(task["任务名"], task["修改信息"])

        # ps.app.doJavaScript(f'alert("save to jpg: {ps.export_folder}")')
    print(merge_dict)

    for merge_name, merge_list in merge_dict.items():
        Image_utils.merge_images(
            ps.export_folder + "/" + merge_name,
            merge_list,
            merge_name + "(1)." + ps_settings["file_format"],
        )

    pass


if __name__ == "__main__":
    main_for_merge_images()
