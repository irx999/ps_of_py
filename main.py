"""主启动函数"""

import os
import sys

from load_data import LoadData
from src.ps_core import Photoshop


class PSFactory:
    """Photoshop 工厂类，用于创建指定类型的图像处理引擎实例（支持扩展）"""

    @staticmethod
    def create_engine(engine_type: str, *args, **kwargs):
        if engine_type.lower() == "photoshop":
            return Photoshop(*args, **kwargs)
        else:
            raise ValueError(f"不支持的图像处理引擎: {engine_type}")


main_working_dir = os.path.dirname(__file__)
sys.path.append(main_working_dir)
os.chdir(main_working_dir)


def main():
    """主启动函数"""
    try:
        load_data = LoadData()

        ps_settings, suffix = load_data.settings[:-1], load_data.settings[-1]

        # 使用工厂模式创建 Photoshop 实例
        ps = PSFactory.create_engine("photoshop", *ps_settings)

        # 遍历整个字典
        with ps:
            for task in load_data.selected_skus():
                print(task["内容"])
                ps.core(task["任务名"] + suffix, task["内容"])

    except Exception as e:
        print(f"程序执行出错: {e}")


if __name__ == "__main__":
    main()
