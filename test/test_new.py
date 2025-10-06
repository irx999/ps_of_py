import unittest

from photoshop.api.enumerations import AnchorPosition

from src.ps import Photoshop


class TestNewModule(unittest.TestCase):
    def setUp(self):
        pass
        self.ps = Photoshop(
            psd_name="测试",
            export_folder="./test_export",
            colse_ps=False,
        )

    def test_new_change(self):
        """测试移动和旋转"""
        矩形 = "矩形/矩形1"

        dict_for_test = {
            "No2": {
                矩形: {
                    "move": (350, 350),
                    "rotate": 180,
                },
            },
            "No3": {
                矩形: {
                    "move": (0, 0),
                    "rotate": -180,
                },
            },
        }
        with self.ps:
            for export_name, input_data in dict_for_test.items():
                self.ps.core(export_name, input_data)

    def test_resizeImage(self):
        """测试图片大小调整"""
        # self.ps.doc.crop([0, 0, 800, 600])
        self.ps.doc = self.ps.doc.duplicate("123")
        self.ps.doc.resizeImage(1600, 1600)
        self.ps.ps_saveas("test")
        # self.ps.doc.suspendHistory()

    def test_resize_layer(self):
        """测试图层变换"""

        with self.ps:
            layer = self.ps.layer_factory.get_layer_by_layername("测试图层")[0]
            # 这里是百分比
            layer.resize(100 * (100 / 120), 100, AnchorPosition(5))

    def test_move_layer(self):
        """测试图层变换"""

        with self.ps:
            layer = self.ps.layer_factory.get_layer_by_layername("测试图层")[0]

            new_x = 100
            new_y = 200

            x = layer.bounds[0]  # type: ignore
            y = layer.bounds[1]  # type: ignore
            layer.translate(new_x - x, new_y - y)

    def test_rotate_layer(self):
        """测试旋转图层"""

        矩形 = "矩形/矩形1"

        dict_for_test = {
            "旋转1": {
                矩形: {
                    "rotate": 90,
                },
            },
            "旋转2": {
                矩形: {
                    "rotate": -90,
                },
            },
        }
        for export_name, input_data in dict_for_test.items():
            self.ps.core(export_name, input_data)
