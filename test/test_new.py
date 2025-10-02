import unittest

from src.ps_core import Photoshop


class TestNewModule(unittest.TestCase):
    def setUp(self):
        pass
        self.ps = Photoshop(psd_name="测试", export_folder="./test_export")

    def test_new_change(self):
        """测试字体修改"""
        矩形 = "矩形/矩形1"

        dict_for_test = {
            "No1": {
                矩形: {
                    "visible": False,
                },
            },
            "No2": {
                矩形: {
                    "visible": True,
                    "bounds": {
                        "W": 123,
                        "H": 123,
                    },
                },
            },
            "No3": {
                矩形: {
                    "visible": True,
                    "bounds": {
                        "W": 456,
                        "H": 456,
                    },
                },
            },
        }

        for export_name, input_data in dict_for_test.items():
            self.ps.core(export_name, input_data)
        # self.ps.restore_all_layers_to_initial()
        # self.ps.doc.close()

    def test_resizeImage(self):
        """测试图片大小调整"""
        # self.ps.doc.crop([0, 0, 800, 600])
        self.ps.doc = self.ps.doc.duplicate("123")
        self.ps.doc.resizeImage(1600, 1600)
        self.ps.ps_saveas("test")
        # self.ps.doc.suspendHistory()
