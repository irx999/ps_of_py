import unittest
from pprint import pprint

from src.ps_core import Photoshop


class TestBaseModule(unittest.TestCase):
    def setUp(self):
        pass
        self.ps = Photoshop(
            psd_name="测试",
            export_folder="./test_export",
            colse_ps=True,
        )
        print("\n")

    def tearDown(self):
        # time.sleep(2)
        # self.ps.doc.close()
        pass

    def test_info(self) -> None:
        pprint(self.ps.get_psd_info())

    def dict_for_test(self):
        文本 = "标题/标题1"
        图片1 = "图片/图片1"
        图片2 = "图片/图片2"
        矩形 = "矩形/矩形1"
        dict_for_test = {
            "No1": {
                文本: {
                    "visible": True,
                    "textItem": {
                        "contents": "第一次修改->调整字体大小,第一张可见,第二张不可见",
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
                矩形: {
                    "visible": True,
                    "move": (350, 350),
                    "rotate": 180,
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
                矩形: {
                    "visible": True,
                    # "move": (0, 0),
                    "rotate": -180,
                },
            },
            "No3": {
                文本: {
                    "visible": True,
                    "textItem": {
                        "contents": "第三次修改->复原,第一张可见,第二张可见",
                        "font": "DingTalk-JinBuTi",
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

        return dict_for_test

    def test_fontchange(self):
        """测试字体修改"""

        with self.ps:
            for export_name, input_data in self.dict_for_test().items():
                self.ps.core(export_name, input_data)
            pprint(self.ps.run_time_record)
            pprint(self.ps.layer_factory.run_time_record)
        pprint("测试结束")


if __name__ == "__main__":
    unittest.main()
