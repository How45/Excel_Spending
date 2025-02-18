import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QGroupBox, QPushButton

class QTload(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading")
        self.resize(300, 200)

        self.layout = QFormLayout(self)
        self.setLayout(self.layout)

        # Outer box (main)
        self.title_groupbox = QGroupBox("SpreadSheet's")
        self.inner_layout = QVBoxLayout()
        self.title_groupbox.setLayout(self.inner_layout)
        self.layout.addWidget(self.title_groupbox)

        self.inner_layout.setContentsMargins(10, 10, 10, 10)
        self.inner_layout.setSpacing(5)

        self.list_file_names = self.list_dir()
        self.files_name = [QPushButton(file, self.title_groupbox) for file in self.list_file_names]

        for file in self.files_name:
            self.inner_layout.addWidget(file)

    def list_dir(self) -> list[str]:
        current_path: str = os.getcwd()
        return os.listdir(f"{current_path}\\spreadsheets")
