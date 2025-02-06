import os
from qt_windows.qt_create import QTcreate
from qt_windows.qt_load import QTload
from qt_windows.qt_update import QTupdate

from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGroupBox


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Spreadsheet App")
        self.resize(250,200)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        title_groupbox = QGroupBox('SpreadSheet')
        inner_layout = QVBoxLayout()
        title_groupbox.setLayout(inner_layout)

        title_button = ['Create a new', 'Load', 'Update']
        buttons = [QPushButton(t, title_groupbox) for t in title_button]

        inner_layout.addStretch()
        for b in buttons:
            inner_layout.addWidget(b)

        inner_layout.addStretch()
        layout.addWidget(title_groupbox)

        buttons[0].clicked.connect(self.open_create)
        buttons[1].clicked.connect(self.open_load)
        buttons[2].clicked.connect(self.open_update)

    def open_create(self):
        create_window = QTcreate()
        create_window.data_sent.connect(self.receive_data)
        create_window.show()

    def receive_data(self, statement_files, json_files, file_name) -> None:
        print(os.getcwd())
        print("Received Data:")
        print("Statement Files:", statement_files)
        print("JSON Files:", json_files)
        print("File Name:", file_name)
        
        # File path root

    def open_load(self):
        create_window = QTload()
        create_window.show()

    def open_update(self):
        create_window = QTupdate()
        create_window.show()
