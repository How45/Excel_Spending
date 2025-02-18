import os
import sys
import unittest

from PyQt6.QtWidgets import QApplication

import script as run
from qt_windows.qt_main import MainWindow


class TestQT(unittest.TestCase):

    def test_receive_data(self):
        """
        Test -> if qt_main properly transforms data into files and folders
        """
        app = QApplication(sys.argv)
        window = MainWindow()
        window.receive_data(["STATEMENTS"],"JSON", "NAME")

    def test_received_data_to_script(self):
        """
        Test -> see if extraction in script.create_file() understands data
        """
        dir_file = f"{os.getcwd()}\\test_finance"
        run.create_file(dir_file)



if __name__ == '__main__':
    unittest.main()
