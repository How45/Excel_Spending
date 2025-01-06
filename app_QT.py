from PyQt6.QtWidgets import QApplication
from QWindows.qmain import MainWindow

import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
