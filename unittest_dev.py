import unittest
from pprint import pprint

from src.load_data import LoadData
from src.ps_core import Photoshop


class TestDevModule(unittest.TestCase):
    def setUp(self):
        self.ps = Photoshop(psd_name="测试用例", export_folder="./test_export")

    def tearDown(self):
        pass

    def test_info(self) -> None:
        pprint(self.ps)

    def dict_for_test(self):
        dict_for_test = {
            "No1": {
                "标题/标题2": {
                    "visible": True,
                    "textItem": {
                        "contents": "标题第一次修改",
                        "size": 35,
                        "color": "#086D7A",
                    },
                },
                "显卡/GV-N5060OC-8GL": {
                    "visible": True,
                },
            },
            "No2": {
                "标题/标题2": {
                    "visible": True,
                    "textItem": {
                        "contents": "标题第一次修改",
                        "size": 35,
                        "color": "#086D7A",
                    },
                },
                "显卡/GV-N5060OC-8GL": {
                    "visible": False,
                },
            },
            "No3": {
                "标题/标题2": {
                    "visible": True,
                    "textItem": {
                        "contents": "标题第二次修改",
                        "size": 35,
                        "color": "#C218C2",
                    },
                },
                "显卡/GV-N5060GAMING OC-8GD": {
                    "visible": True,
                },
            },
        }

        return dict_for_test

    @unittest.skip("")
    def test_change(self):
        for export_name, input_data in self.dict_for_test().items():
            self.ps.core(export_name, input_data)
        self.ps.restore_all_layers_to_initial()
        self.ps.doc.close()

    # @unittest.skip("")
    def test_save_initial_layer_state(self):
        self.ps.psd_name = "显卡参数新"
        self.ps.psd__dir_path = r"E:\WORK\工作相关\psd"
        self.ps.reconnect()
        lodadata = LoadData()
        for task in lodadata.selected_skus():
            self.ps.core(task["任务名"], task["内容"])

        self.ps.restore_all_layers_to_initial()
        self.ps.doc.close()


if __name__ == "__main__":
    # Run the tests
    unittest.main()
