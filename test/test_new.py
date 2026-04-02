import unittest

from src.ps_of_py import Photoshop


class TestNewModule(unittest.TestCase):
    def setUp(self):
        pass
        self.ps = Photoshop(
            psd_name="测试 copy.psd",
            psd_dir_path="test/test_file",
            export_folder="test_export",
            colse_ps=False,
        )

    def test_new_change(self):
        print(self.ps.get_all_layers())
