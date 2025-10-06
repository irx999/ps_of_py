import unittest

from src.ps import Photoshop


class TestBUGFIXModule(unittest.TestCase):
    def setUp(self):
        pass
        self.ps = Photoshop(
            psd_name="测试",
            export_folder="./test_export",
            colse_ps=True,
        )
        print("\n")

    def test_bugfix(self):
        """测试字体修改"""
        图片1 = "图片/图片1"
        文本 = "标题/标题1"
        dict_for_test = {
            "No1": {
                图片1: {
                    "visible": False,
                },
                文本: {
                    "visible": True,
                    "textItem": {
                        "contents": 3.14,
                        "font": "悠哉字体",
                    },
                },
            },
        }
        with self.ps:
            for export_name, input_data in dict_for_test.items():
                self.ps.core(export_name, input_data)
            print(self.ps.run_time_record)
        print("测试结束")


if __name__ == "__main__":
    # 运行测试
    unittest.main()
