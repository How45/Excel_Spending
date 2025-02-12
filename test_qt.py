import os
import unittest
import sys
from qt_windows.qt_main import MainWindow
from PyQt6.QtWidgets import QApplication


class TestQT(unittest.TestCase):

    def test_receive_data(self):
        """
        Test -> if qt_main properly transforms data into files and folders
        """
        app = QApplication(sys.argv)
        window = MainWindow()
        window.receive_data(["STATEMENTS"],"JSON", "NAME")


if __name__ == '__main__':
    unittest.main()
