import unittest

from src.ps_of_py import Photoshop


class TestExportFormats(unittest.TestCase):
    """
    测试不同文件格式导出功能
    """

    def test_export_as_jpg(self):
        """测试导出JPG格式"""
        ps = Photoshop(
            psd_name="测试.psd",
            psd_dir_path="test/test_file/",
            export_folder="test/test_export/formats",
            file_format="jpg",
            colse_ps=True,
        )

        with ps:
            # 简单测试导出功能
            test_data = {
                "标题/标题1": {
                    "textItem": {
                        "contents": "JPG格式导出测试",
                        "size": 24,
                        "color": "#FF0000",
                    }
                }
            }

            ps.core("test_jpg_export", test_data)

    def test_export_as_png(self):
        """测试导出PNG格式"""
        ps = Photoshop(
            psd_name="测试.psd",
            psd_dir_path="test/test_file/",
            export_folder="test/test_export/formats",
            file_format="png",
            colse_ps=True,
        )

        with ps:
            # 简单测试导出功能
            test_data = {
                "标题/标题1": {
                    "textItem": {
                        "contents": "PNG格式导出测试",
                        "size": 24,
                        "color": "#00FF00",
                    }
                }
            }

            ps.core("test_png_export", test_data)

    def test_export_as_pdf(self):
        """测试导出PDF格式"""
        ps = Photoshop(
            psd_name="测试.psd",
            psd_dir_path="test/test_file/",
            export_folder="test/test_export/formats",
            file_format="pdf",
            colse_ps=True,
        )

        with ps:
            # 简单测试导出功能
            test_data = {
                "标题/标题1": {
                    "textItem": {
                        "contents": "PDF格式导出测试",
                        "size": 24,
                        "color": "#0000FF",
                    }
                }
            }

            ps.core("test_pdf_export", test_data)

    def test_export_multiple_formats_sequentially(self):
        """依次导出多种格式"""
        formats = ["jpg", "png", "pdf", "gif"]

        for fmt in formats:
            ps = Photoshop(
                psd_name="测试.psd",
                psd_dir_path="test/test_file/",
                export_folder="test/test_export/formats",
                file_format=fmt,
                colse_ps=False,  # 为了性能，只在最后关闭PS
            )

            with ps:
                test_data = {
                    "标题/标题1": {
                        "visible": True,
                        "textItem": {
                            "contents": f"测试{fmt.upper()}格式",
                            "size": 30,
                            "color": "#FF00FF"
                            if fmt == "jpg"
                            else ("#00FFFF" if fmt == "png" else "#FFFF00"),
                        },
                    },
                    "图片/图片1": {"visible": True},
                }

                ps.core(f"test_multi_format_{fmt}", test_data)

        # 最后单独创建一个实例来关闭PS
        close_ps = Photoshop(
            psd_name="测试.psd",
            psd_dir_path="test/test_file/",
            export_folder="test/test_export/formats",
            file_format="png",
            colse_ps=True,
        )
        with close_ps:
            pass  # 只是为了关闭PS


if __name__ == "__main__":
    unittest.main()
