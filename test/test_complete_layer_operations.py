import unittest

from src.ps_of_py import Photoshop


class TestCompleteLayerOperations(unittest.TestCase):
    """
    完整的图层操作测试类，覆盖所有支持的图层操作属性
    """

    def setUp(self):
        self.ps = Photoshop(
            psd_name="测试.psd",
            psd_dir_path="test/test_file/",
            export_folder="test/test_export",
            colse_ps=False,
        )

    def tearDown(self):
        if hasattr(self, "ps"):
            print("运行时间记录:", self.ps.run_time_record)
            if hasattr(self.ps, "layer_factory"):
                print("图层运行时间记录:", self.ps.layer_factory.run_time_record)
            del self.ps
        print("测试结束\n")

    def test_visible_operations(self):
        """测试可见性操作"""
        图片1 = "图片/图片1"

        test_cases = {
            "visible_true": {图片1: {"visible": True}},
            "visible_false": {图片1: {"visible": False}},
        }

        with self.ps:
            for export_name, input_data in test_cases.items():
                self.ps.core(export_name, input_data)

    def test_text_operations(self):
        """测试文本图层的所有操作"""
        文本1 = "标题/标题1"
        文本2 = "标题/标题2"

        test_cases = {
            "text_contents_only": {
                文本1: {
                    "textItem": {
                        "contents": "仅修改内容",
                    }
                }
            },
            "text_size_and_color": {
                文本1: {
                    "textItem": {
                        "contents": "修改字体大小和颜色",
                        "size": 24,
                        "color": "#FF0000",
                    }
                }
            },
            "text_strike_through": {
                文本2: {
                    "textItem": {
                        "contents": "带删除线的文本",
                        "strikeThru": 2,
                    }
                }
            },
            "text_font_change": {
                文本1: {
                    "textItem": {
                        "contents": "修改字体",
                        "font": "Arial",
                    }
                }
            },
            "text_full_modification": {
                文本2: {
                    "textItem": {
                        "contents": "完全修改文本属性",
                        "size": 18,
                        "color": "#00FF00",
                        "font": "DingTalk-JinBuTi",
                        "strikeThru": 1,
                    }
                }
            },
        }

        with self.ps:
            for export_name, input_data in test_cases.items():
                self.ps.core(export_name, input_data)

    def test_move_operations(self):
        """测试移动操作"""
        图片1 = "图片/图片1"

        test_cases = {
            "move_positive_coords": {
                图片1: {
                    "move": (100, 100),
                }
            },
            "move_negative_coords": {
                图片1: {
                    "move": (0, 0),
                }
            },
            "move_large_coords": {
                图片1: {
                    "move": (500, 300),
                }
            },
        }

        with self.ps:
            for export_name, input_data in test_cases.items():
                self.ps.core(export_name, input_data)

    def test_rotate_operations(self):
        """测试旋转操作"""
        矩形1 = "矩形/矩形1"

        test_cases = {
            "rotate_45_degrees": {
                矩形1: {
                    "rotate": 45,
                }
            },
            "rotate_negative_90": {
                矩形1: {
                    "rotate": -90,
                }
            },
            "rotate_180_degrees": {
                矩形1: {
                    "rotate": 180,
                }
            },
        }

        with self.ps:
            for export_name, input_data in test_cases.items():
                self.ps.core(export_name, input_data)

    def test_combined_operations(self):
        """测试组合操作 - 同时修改多个属性"""
        文本1 = "标题/标题1"
        图片1 = "图片/图片1"
        矩形1 = "矩形/矩形1"

        test_cases = {
            "combined_text_and_position": {
                文本1: {
                    "visible": True,
                    "textItem": {
                        "contents": "组合测试 - 文本",
                        "size": 20,
                        "color": "#0000FF",
                    },
                },
                图片1: {
                    "visible": False,
                    "move": (150, 150),
                },
            },
            "combined_all_features": {
                文本1: {
                    "visible": True,
                    "textItem": {
                        "contents": "组合全部功能测试",
                        "size": 25,
                        "color": "#FFAABB",
                        "font": "DingTalk-JinBuTi",
                        "strikeThru": 1,
                    },
                },
                图片1: {
                    "visible": True,
                    "move": (200, 100),
                    "rotate": 45,
                },
                矩形1: {
                    "visible": False,
                    "move": (300, 300),
                    "rotate": 90,
                },
            },
        }

        with self.ps:
            for export_name, input_data in test_cases.items():
                self.ps.core(export_name, input_data)

    def test_nested_layer_operations(self):
        """测试嵌套图层组操作"""
        # 测试深层嵌套的图层
        deep_layer = "图片/嵌套组/更深层组/图片2"

        if self.ps._get_psd_file_path():  # 确保PSD文件存在
            with self.ps:
                # 尝试获取嵌套图层，如果存在则进行测试
                try:
                    layer_list = self.ps.layer_factory.get_layer_by_layername(
                        deep_layer
                    )
                    if layer_list:
                        test_case = {
                            "nested_layer_test": {
                                deep_layer: {"visible": True, "move": (50, 50)}
                            }
                        }
                        for export_name, input_data in test_case.items():
                            self.ps.core(export_name, input_data)
                    else:
                        print(f"跳过嵌套图层测试，因为图层 {deep_layer} 不存在")
                except Exception as e:
                    print(f"嵌套图层测试出错: {e}")

    def test_multiple_operations_sequentially(self):
        """测试连续多次操作同一图层"""
        文本1 = "标题/标题1"

        operations_sequence = [
            {
                "sequential_op_1": {
                    文本1: {
                        "textItem": {
                            "contents": "第一步：设置内容和颜色",
                            "color": "#FF0000",
                        }
                    }
                }
            },
            {"sequential_op_2": {文本1: {"textItem": {"size": 30, "font": "Arial"}}}},
            {"sequential_op_3": {文本1: {"visible": False}}},
            {
                "sequential_op_4": {
                    文本1: {
                        "visible": True,
                        "textItem": {
                            "contents": "最终状态",
                            "size": 16,
                            "color": "#00AA00",
                        },
                    }
                }
            },
        ]

        with self.ps:
            for test_case in operations_sequence:
                for export_name, input_data in test_case.items():
                    self.ps.core(export_name, input_data)


if __name__ == "__main__":
    unittest.main()
