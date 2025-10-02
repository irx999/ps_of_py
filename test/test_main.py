import unittest
from pprint import pprint

from src.ps_core import Photoshop


class TestDevModule(unittest.TestCase):
    def setUp(self):
        pass
        self.ps = Photoshop(psd_name="测试用例", export_folder="./test_export")

    def tearDown(self):
        # time.sleep(2)
        # self.ps.doc.close()
        pass

    def test_info(self) -> None:
        pprint(self.ps)

    def test_fontchange(self):
        """测试字体修改"""
        title = "标题/标题1"
        dict_for_test = {
            "No1": {
                title: {
                    "visible": True,
                    "textItem": {
                        "contents": "标题第一次修改->调整大小",
                        "size": 50,
                        # "color": "#086D7A",
                    },
                },
            },
            "No2": {
                title: {
                    "visible": True,
                    "textItem": {
                        "contents": "标题第二次修改->调整颜色",
                        # "size": 35,
                        "color": "#A00000",
                    },
                },
            },
            "No3": {
                title: {
                    "visible": True,
                    "textItem": {
                        "contents": "标题第三次修改->复原",
                        # "size": 50,
                        # "color": "#C218C2",
                    },
                },
            },
        }

        for export_name, input_data in dict_for_test.items():
            self.ps.core(export_name, input_data)
        self.ps.restore_all_layers_to_initial()

    def test_resizeImage(self):
        """测试图片大小调整"""
        # self.ps.doc.crop([0, 0, 800, 600])
        self.ps.doc = self.ps.doc.duplicate("123")
        self.ps.doc.resizeImage(1600, 1600)
        self.ps.ps_saveas("test")
        # self.ps.doc.suspendHistory()
