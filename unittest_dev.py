import time
import unittest
from pprint import pprint

from src.load_data import LoadData
from src.ps_core import Photoshop


class TestDevModule(unittest.TestCase):
    def setUp(self):
        # os.removedirs("./test_export")
        self.start_time = time.time()
        self.ps = Photoshop(
            psd_name="测试用例",
            export_folder="./test_export",
        )
        self.error_list = []

    def tearDown(self):
        self.ps.restore_all_layers_to_initial()
        end_time = time.time()
        pprint(f"{self._testMethodName} 耗时: {end_time - self.start_time:.4f} 秒")

    def test_info(self) -> None:
        pprint(self.ps)

    def dict_for_test(self):
        dict_for_test = {
            "No1": {
                "标题/标题2": {
                    "visible": True,
                    "textItem": {
                        "文本内容": "标题第一次修改",
                        "字体大小": 35,
                        "字体颜色": "#086D7A",
                    },
                },
                "显卡|GV-N5060OC-8GL": {
                    "visible": True,
                },
            },
            "No2": {
                "标题/标题2": {
                    "visible": True,
                    "textItem": {
                        "文本内容": "标题第一次修改",
                        "字体大小": 35,
                        "字体颜色": "#086D7A",
                    },
                },
                "显卡|GV-N5060OC-8GL": {
                    "visible": False,
                },
            },
            "No3": {
                "标题/标题2": {
                    "visible": True,
                    "textItem": {
                        "文本内容": "标题第二次修改",
                        "字体大小": 35,
                        "字体颜色": "#C218C2",
                    },
                },
                "显卡|GV-N5060GAMING OC-8GD": {
                    "visible": True,
                },
            },
        }

        return dict_for_test

    def test_change(self):
        for export_name, input_data in self.dict_for_test().items():
            start_time = time.time()
            self.ps.core(export_name, input_data)
            pprint(f"导出{export_name} 耗时: {time.time() - start_time:.4f} 秒")

        self.ps.restore_all_layers_to_initial()
        pprint(self.error_list)

    def test_save_initial_layer_state(self):
        self.ps.psd_name = "测试用例 - 副本"
        print(self.ps.psd_name)
        self.ps.init()
        print(self.ps)
        lodadata = LoadData()
        for task in lodadata.selected_skus():
            print(task["内容"])
            start_time = time.time()
            self.ps.core(task["任务名"], task["内容"])
            pprint(f"导出{task['任务名']} 耗时: {time.time() - start_time:.4f} 秒")


if __name__ == "__main__":
    # Run the tests
    unittest.main()
