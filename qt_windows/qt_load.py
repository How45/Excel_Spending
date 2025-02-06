from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class QTload(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading")
        self.resize(300, 200)