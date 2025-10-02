import unittest
from pprint import pprint

from src.ps_core import Photoshop


class TestBaseModule(unittest.TestCase):
    def setUp(self):
        pass
        self.ps = Photoshop(psd_name="测试", export_folder="./test_export")

    def tearDown(self):
        # time.sleep(2)
        # self.ps.doc.close()
        pass

    def test_info(self) -> None:
        pprint(self.ps)

    def test_fontchange(self):
        """测试字体修改"""
        文本 = "标题/标题1"
        图片1 = "图片/图片1"
        图片2 = "图片/图片2"
        dict_for_test = {
            "No1": {
                文本: {
                    "visible": True,
                    "textItem": {
                        "contents": "标题第一次修改->调整大小",
                        "size": 50,
                        # "color": "#086D7A",
                    },
                },
                图片1: {
                    "visible": True,
                },
                图片2: {
                    "visible": False,
                },
            },
            "No2": {
                文本: {
                    "visible": True,
                    "textItem": {
                        "contents": "标题第二次修改->调整颜色",
                        # "size": 35,
                        "color": "#A00000",
                    },
                },
                图片1: {
                    "visible": False,
                },
                图片2: {
                    "visible": True,
                },
            },
            "No3": {
                文本: {
                    "visible": True,
                    "textItem": {
                        "contents": "标题第三次修改->复原",
                    },
                },
                图片2: {
                    "visible": True,
                },
            },
            "No4": {
                文本: {
                    "visible": True,
                    "textItem": {
                        "contents": "标题第四次修改->复原",
                    },
                },
            },
        }

        for export_name, input_data in dict_for_test.items():
            self.ps.core(export_name, input_data)
        self.ps.restore_all_layers_to_initial()
        self.ps.doc.close()
