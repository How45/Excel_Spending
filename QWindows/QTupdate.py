from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class QTupdate(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update")
        self.resize(300, 200)