import os
import unittest
from pprint import pprint

from src.ps import Photoshop


class TestBaseModule(unittest.TestCase):
    def setUp(self):
        print(os.getcwd())
        self.ps = Photoshop(
            psd_name="测试",
            psd_dir_path="test/test_psd",
            export_folder="test/test_export",
            colse_ps=True,
        )

    def tearDown(self):
        pprint(self.ps.run_time_record)
        pprint(self.ps.layer_factory.run_time_record)
        del self.ps
        print("测试结束\n")

    def test_init_ps_session(self):
        self.ps.colse_ps = True
        with self.ps:
            pass

    def test_ps_saveas(self):
        with self.ps:
            self.ps.ps_saveas("未修改图片")

    def test_get_psd_info(self):
        pprint(self.ps.get_psd_info())

    def test_visible(self):
        """测试可显"""
        图片1 = "图片/图片1"
        dict_for_test = {
            "test_visible_1": {
                图片1: {
                    "visible": True,
                }
            },
            "test_visible_2": {
                图片1: {
                    "visible": False,
                }
            },
        }
        with self.ps:
            for export_name, input_data in dict_for_test.items():
                self.ps.core(export_name, input_data)

    def test_move(self):
        """测试移动"""
        图片1 = "图片/图片1"
        dict_for_test = {
            "test_move_1": {
                图片1: {
                    "move": (350, 350),
                }
            },
            "test_move_2": {
                图片1: {
                    "move": (0, 0),
                }
            },
        }
        with self.ps:
            for export_name, input_data in dict_for_test.items():
                self.ps.core(export_name, input_data)

    def test_testItem(self):
        """测试文本"""
        文本 = "标题/标题1"
        文本2 = "标题/标题2"
        dict_for_test = {
            "test_test_1": {
                文本: {
                    "textItem": {
                        "contents": "第一次修改",
                        "size": 35,
                        "color": "#A00000",
                        "font": "DingTalk-JinBuTi",
                    },
                },
            },
            "test_test_2": {
                文本2: {
                    "textItem": {
                        "contents": "第二次修改",
                        "size": 20,
                        "color": "#00FF37",
                        "font": "DingTalk-JinBuTi",
                    },
                },
            },
        }
        with self.ps:
            for export_name, input_data in dict_for_test.items():
                self.ps.core(export_name, input_data)

    def test_all_change(self):
        """测试批量修改"""

        with self.ps:
            for export_name, input_data in self.dict_for_test().items():
                self.ps.core(export_name, input_data)

    def dict_for_test(self):
        文本 = "标题/标题1"
        图片1 = "图片/图片1"
        图片2 = "图片/图片2"
        矩形 = "矩形/矩形1"
        dict_for_test = {
            "test_all1": {
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
            "test_all2": {
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
            "test_all3": {
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
            "test_all4": {
                文本: {
                    "visible": True,
                    "textItem": {
                        "contents": "第四次修改->复原",
                    },
                },
            },
        }

        return dict_for_test
