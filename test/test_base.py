import unittest
from pprint import pprint

from src.ps_core import Photoshop


class TestBaseModule(unittest.TestCase):
    def setUp(self):
        pass
        self.ps = Photoshop(psd_name="测试", export_folder="./test_export")
        print("\n")

    def tearDown(self):
        # time.sleep(2)
        # self.ps.doc.close()
        pass

    def test_info(self) -> None:
        pprint(self.ps.get_psd_info())

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
                        "contents": "第一次修改->调整字体大小,第一张可见,第二张不可见",
                        "size": 35,
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
                        "contents": "第二次修改->调整颜色,第一张不可见,第二张可见",
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
                        "contents": "第三次修改->复原,第一张可见,第二张可见",
                    },
                },
                图片1: {
                    "visible": True,
                },
                图片2: {
                    "visible": True,
                },
            },
            "No4": {
                文本: {
                    "visible": True,
                    "textItem": {
                        "contents": "第四次修改->复原",
                    },
                },
            },
        }

        for export_name, input_data in dict_for_test.items():
            self.ps.core(export_name, input_data)
        self.ps.restore_all_layers_to_initial()
        print(self.ps.run_time_record)
        self.ps.doc.close()
