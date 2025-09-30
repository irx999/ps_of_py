import unittest

from src.ps_core import Photoshop


class TestBUGFIXModule(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fontchange(self):
        """测试字体修改"""
        text_layer = "标题/标题2"
        dict_for_test = {
            # "No1": {
            #     text_layer: {
            #         "visible": True,
            #         "textItem": {
            #             "contents": "标题第一次修改",
            #             # "size": 50,
            #         },
            #     },
            # },
            "No2": {
                text_layer: {
                    "visible": True,
                    "textItem": {
                        "contents": "标题第二次修改",
                        "size": 100,
                        "color": "#D60909",
                    },
                },
            },
            "No3": {
                text_layer: {
                    "visible": True,
                    "textItem": {
                        "contents": "标题第三次修改",
                        # "size": 50,
                    },
                },
            },
        }
        self.ps = Photoshop(psd_name="测试用例", export_folder="./test_export")
        for export_name, input_data in dict_for_test.items():
            self.ps.core(export_name, input_data)
        # self.ps.restore_all_layers_to_initial()


if __name__ == "__main__":
    # Run the tests
    unittest.main()
